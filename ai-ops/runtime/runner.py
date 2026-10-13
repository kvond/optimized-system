"""Offline deterministic controller. Atomic private SQLite results and receipts; no AI dispatch."""
from __future__ import annotations
import argparse, copy, datetime as dt, hashlib, json, os, re
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol
from foundation import CacheContract, Store, Route, canonical, micros, select_route, timestamp, utcnow, UTC

def digest(value): return hashlib.sha256(canonical(value).encode()).hexdigest()
def text(value):
    if not isinstance(value,str) or not value.strip(): raise ValueError('nonempty string required')
    return value

def validate_routes(config):
    if not isinstance(config,dict) or set(config)!={'version','routes'}: raise ValueError('route config fields invalid')
    text(config['version'])
    if not isinstance(config['routes'],list): raise ValueError('routes array required')
    routes=[]; names=set()
    keys={'name','provider','capability','estimated_cost','privacy_partitions','deterministic','enabled'}
    for r in config['routes']:
        if not isinstance(r,dict) or set(r)!=keys: raise ValueError('route fields invalid')
        name=text(r['name']);text(r['provider'])
        if name in names: raise ValueError('duplicate route name')
        names.add(name)
        if type(r['enabled']) is not bool or type(r['deterministic']) is not bool: raise ValueError('real bool required')
        if type(r['capability']) is not int or r['capability']<0: raise ValueError('nonnegative integer capability required')
        if not isinstance(r['estimated_cost'],str) or not re.fullmatch(r'(0|[1-9][0-9]*)(\.[0-9]{1,6})?',r['estimated_cost']): raise ValueError('nonnegative fixed-point price string required')
        micros(r['estimated_cost'])
        partitions=r['privacy_partitions']
        if not isinstance(partitions,list) or not partitions: raise ValueError('privacy strings required')
        for p in partitions:text(p)
        if len(set(partitions))!=len(partitions): raise ValueError('distinct privacy strings required')
        routes.append(Route(name,r['provider'],r['capability'],r['estimated_cost'],frozenset(partitions),r['deterministic'],r['enabled']))
    return routes

@dataclass(frozen=True)
class SourceSnapshot:
    source_id: str
    revision: str
    privacy_partition: str
    authorized: bool
    readable: bool
    complete: bool
    observed_at: dt.datetime
    content: dict | None
    content_sha256: str | None

class SourceAdapter(Protocol):
    """Read-only bounded adapter. Must not mutate sources or invoke models."""
    def snapshot(self, source_id: str, privacy_partition: str, max_bytes: int) -> SourceSnapshot: ...

class Controller:
    def __init__(self, store: Store, *, adapter: SourceAdapter, routes: dict, handlers: dict,
                 max_source_bytes=1024*1024, max_components=100, freshness_seconds=300):
        self.store=store;self.adapter=adapter;self.routes=validate_routes(routes);self.route_version=routes['version'];self.handlers=handlers
        if type(max_source_bytes) is not int or max_source_bytes<=0 or type(max_components) is not int or max_components<=0: raise ValueError('positive bounds required')
        if type(freshness_seconds) is not int or freshness_seconds<=0: raise ValueError('positive freshness required')
        self.max_source_bytes=max_source_bytes;self.max_components=max_components;self.freshness_seconds=freshness_seconds
        if os.stat(store.path).st_mode & 0o077: raise PermissionError('private state permissions required')
        with store.connection() as db:
            db.executescript('''CREATE TABLE IF NOT EXISTS runner_requests(
            request_key TEXT PRIMARY KEY,fingerprint TEXT NOT NULL,result TEXT NOT NULL,
            sha256 TEXT NOT NULL,receipt TEXT NOT NULL);''')
    def validate_request(self, request):
        keys={'request_id','privacy_partition','contract_version','inputs','components'}
        if not isinstance(request,dict) or set(request)!=keys: raise ValueError('request fields invalid')
        for k in ('request_id','privacy_partition','contract_version'):text(request[k])
        if not isinstance(request['inputs'],dict): raise ValueError('input object required')
        canonical(request['inputs'])
        components=request['components'];names=set()
        if not isinstance(components,list) or not 0<len(components)<=self.max_components: raise ValueError('bounded nonempty components required')
        for c in components:
            if not isinstance(c,dict) or set(c)!={'component_id','source_id','source_revision','task_type','required_capability'}: raise ValueError('component fields invalid')
            for k in ('component_id','source_id','source_revision','task_type'):text(c[k])
            if c['component_id'] in names: raise ValueError('duplicate component')
            names.add(c['component_id'])
            if type(c['required_capability']) is not int or c['required_capability']<0: raise ValueError('invalid capability')
    def snapshot_issue(self, s, c, partition, checked):
        if not isinstance(s,SourceSnapshot): return 'invalid_snapshot'
        if s.source_id!=c['source_id'] or s.privacy_partition!=partition:return 'source_or_partition_mismatch'
        if any(type(x) is not bool for x in (s.authorized,s.readable,s.complete)):return 'invalid_source_flags'
        if not s.authorized:return 'access_denied'
        if not s.readable:return 'source_unreadable'
        if not s.complete:return 'coverage_incomplete'
        if not isinstance(s.revision,str) or not s.revision.strip():return 'revision_missing'
        if s.revision!=c['source_revision']:return 'source_revision_changed'
        try:age=timestamp(checked)-timestamp(s.observed_at)
        except (ValueError,AttributeError,TypeError):return 'invalid_observation_time'
        if age<0 or age>self.freshness_seconds:return 'source_observation_stale'
        if not isinstance(s.content,dict):return 'source_content_missing'
        try:encoded=canonical(s.content).encode()
        except (TypeError,ValueError):return 'invalid_source_content'
        if len(encoded)>self.max_source_bytes:return 'source_size_limit'
        if s.content_sha256!=hashlib.sha256(encoded).hexdigest():return 'source_hash_mismatch'
        return None
    def execute(self, request):
        """Trusted offline callbacks run outside DB writes; supervise externally.

        Concurrent callers may compute the same pure function. They commit coherent
        identical receipts; this controller never authorizes side effects or paid work.
        """
        self.validate_request(request);partition=request['privacy_partition'];key=digest([partition,request['request_id']]);fp=digest({'request':request,'route_version':self.route_version})
        with self.store.connection() as db:
            prior=db.execute('SELECT fingerprint,result,sha256,receipt FROM runner_requests WHERE request_key=?',(key,)).fetchone()
        if prior:
            if prior[0]!=fp:raise ValueError('request ID conflicts with different input')
            self._verify_row(prior[1],prior[2],json.loads(prior[3]))
        checked=self.store.now();timestamp(checked);components={};pending_cache=[];snapshots={};component_expiry={}
        for c in request['components']:
            try:s=self.adapter.snapshot(c['source_id'],partition,self.max_source_bytes)
            except Exception:
                components[c['component_id']]={'status':'blocked','reason':'source_read_failed'};continue
            checked=self.store.now();timestamp(checked)
            issue=self.snapshot_issue(s,c,partition,checked)
            if issue:
                components[c['component_id']]={'status':'blocked','reason':issue};continue
            s=copy.deepcopy(s);snapshots[c['component_id']]=s
            try:
                eligible=[r for r in self.routes if r.deterministic and micros(r.estimated_cost)==0 and r.name in self.handlers]
                route=select_route(eligible,required_capability=c['required_capability'],partition=partition)
            except PermissionError:
                components[c['component_id']]={'status':'blocked','reason':'no_implemented_free_deterministic_route'};continue
            contract=CacheContract(partition,s.source_id,s.revision,c['task_type'],request['contract_version'],
                {'request_inputs':request['inputs'],'content_sha256':s.content_sha256,'component_id':c['component_id'],'route':route.name},self.route_version)
            cache_key=contract.key()
            with self.store.connection() as db:
                cached=db.execute('SELECT payload,expires FROM cache WHERE key=? AND partition=? AND succeeded=1 AND expires>?',(cache_key,partition,timestamp(checked))).fetchone()
            if cached:
                payload=json.loads(cached[0]);component_expiry[c['component_id']]=cached[1]
            else:
                try:
                    payload=self.handlers[route.name](c['task_type'],copy.deepcopy(s.content),copy.deepcopy(request['inputs']));canonical(payload)
                except Exception:
                    components[c['component_id']]={'status':'failed','reason':'deterministic_handler_failed'};continue
                expiry=timestamp(s.observed_at)+self.freshness_seconds
                component_expiry[c['component_id']]=expiry
                pending_cache.append((cache_key,partition,s.source_id,s.revision,expiry,1,canonical(payload)))
            components[c['component_id']]={'status':'complete','source_id':s.source_id,'source_revision':s.revision,'source_sha256':s.content_sha256,'route':route.name,'output':payload}
        checked=self.store.now();timestamp(checked)
        def validate_freshness(at):
            for c in request['components']:
                item=components[c['component_id']]
                if item['status']=='complete':
                    issue=self.snapshot_issue(snapshots[c['component_id']],c,partition,at)
                    if not issue and component_expiry[c['component_id']]<=timestamp(at):issue='cache_expired_during_run'
                    if issue:components[c['component_id']]={'status':'blocked','reason':issue}
        validate_freshness(checked)
        status='complete' if all(c['status']=='complete' for c in components.values()) else 'partial'
        result={'status':status,'components':components};body=canonical(result);sha=hashlib.sha256(body.encode()).hexdigest()
        location={'storage':'sqlite','database':str(Path(self.store.path).resolve()),'table':'runner_requests','request_key':key}
        receipt={'request_id':request['request_id'],'privacy_partition':partition,'status':status,'request_fingerprint':fp,
            'result_location':location,'result_sha256':sha,'checked_at_utc':checked.astimezone(UTC).isoformat(),
            'execution_kind':'deterministic','provider':None,'model':None,'paid_dispatches':0,
            'component_status':{k:v['status'] for k,v in components.items()}}
        with self.store.transaction() as db:
            checked=self.store.now();validate_freshness(checked)
            status='complete' if all(v['status']=='complete' for v in components.values()) else 'partial'
            result={'status':status,'components':components};body=canonical(result);sha=hashlib.sha256(body.encode()).hexdigest()
            receipt.update(status=status,result_sha256=sha,checked_at_utc=checked.astimezone(UTC).isoformat(),component_status={k:v['status'] for k,v in components.items()})
            # Recheck identity/integrity against concurrent commits before writing.
            latest=db.execute('SELECT fingerprint,result,sha256,receipt FROM runner_requests WHERE request_key=?',(key,)).fetchone()
            if latest:
                if latest[0]!=fp:raise ValueError('request ID conflicts with different input')
                existing=json.loads(latest[3]);self._verify_row(latest[1],latest[2],existing)
                if latest[1]==body:receipt=existing
            for item in pending_cache:
                if item[4]>timestamp(checked):db.execute('INSERT OR REPLACE INTO cache VALUES (?,?,?,?,?,?,?)',item)
            db.execute('INSERT OR REPLACE INTO runner_requests VALUES (?,?,?,?,?)',(key,fp,body,sha,canonical(receipt)))
        self.readback(receipt)
        return receipt
    def _verify_row(self, body, sha, receipt):
        if hashlib.sha256(body.encode()).hexdigest()!=sha or receipt['result_sha256']!=sha:raise ValueError('result receipt hash mismatch')
        result=json.loads(body)
        if result['status']!=receipt['status'] or {k:v['status'] for k,v in result['components'].items()}!=receipt['component_status']:raise ValueError('receipt status mismatch')
        return result
    def readback(self,receipt):
        location=receipt['result_location']
        if location['storage']!='sqlite' or location['database']!=str(Path(self.store.path).resolve()) or location['table']!='runner_requests':raise ValueError('result location mismatch')
        with self.store.connection() as db:
            row=db.execute('SELECT result,sha256,receipt FROM runner_requests WHERE request_key=?',(location['request_key'],)).fetchone()
        if row is None:raise KeyError('result missing')
        saved=json.loads(row[2])
        if saved!=receipt:raise ValueError('receipt does not match committed receipt')
        return self._verify_row(row[0],row[1],saved)

class SyntheticAdapter:
    def __init__(self,now):self.now=now
    def snapshot(self,source_id,privacy_partition,max_bytes):
        if privacy_partition!='synthetic' or source_id!='demo-source':raise PermissionError('synthetic source only')
        content={'values':[2,3,5]}
        return SourceSnapshot(source_id,'synthetic-v1',privacy_partition,True,True,True,self.now(),content,digest(content))

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--demo',action='store_true',required=True);parser.add_argument('--state',type=Path,required=True);args=parser.parse_args()
    config={'version':'synthetic-demo-v1','routes':[{'name':'sum','provider':'local','capability':0,'estimated_cost':'0','privacy_partitions':['synthetic'],'deterministic':True,'enabled':True}]}
    store=Store(args.state);controller=Controller(store,adapter=SyntheticAdapter(store.now),routes=config,handlers={'sum':lambda task,content,inputs:{'sum':sum(content['values'])}})
    request={'request_id':'reproducible-demo-v1','privacy_partition':'synthetic','contract_version':'1','inputs':{},'components':[{'component_id':'sum','source_id':'demo-source','source_revision':'synthetic-v1','task_type':'sum','required_capability':0}]}
    receipt=controller.execute(request);print(json.dumps({'receipt':receipt,'readback':controller.readback(receipt)},indent=2))
if __name__=='__main__':main()

"""Offline public-vacancy change gate. No profiles, matching, network or schedules.
Caller approvals and source evidence must come from an independently authorized adapter.
"""
from __future__ import annotations
from dataclasses import dataclass
import datetime as dt
import hashlib
import json
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit, parse_qsl, urlencode
from foundation import Store, canonical, timestamp, utcnow
from storage import RuntimePaths, StorageError, resolve_storage


def hashed(value):return hashlib.sha256(canonical(value).encode()).hexdigest()
def identifier(value):
    if not isinstance(value,str) or not value.strip() or len(value)>500:raise ValueError('bounded explicit identifier required')
    return value

def official_url(value,origin):
    identifier(value);u=urlsplit(value);o=urlsplit(origin)
    if not u.hostname or not o.hostname or any(c.isspace() for c in u.netloc+o.netloc) or '\\' in u.netloc+o.netloc:raise ValueError('valid official hostname required')
    if u.scheme!='https' or u.username or u.password or u.netloc.lower()!=o.netloc.lower() or o.scheme!='https' or o.username or o.password or o.path not in ('','/') or o.query or o.fragment:raise ValueError('official HTTPS origin required')
    return urlunsplit(('https',u.netloc.lower(),u.path or '/',urlencode(sorted(parse_qsl(u.query,keep_blank_values=True))),'') )

@dataclass(frozen=True)
class Grant:
    privacy_partition: str
    employer_id: str
    source_id: str
    coverage_id: str
    official_origin: str
    requires_authentication: bool = True
    def key(self):
        if type(self.requires_authentication) is not bool:raise ValueError('explicit authentication requirement boolean required')
        for k,v in self.__dict__.items():
            if k!='requires_authentication':identifier(v)
        official_url(self.official_origin,self.official_origin)
        return hashed(self.__dict__)

@dataclass(frozen=True)
class SourceRead:
    grant: Grant
    revision: str
    observed_at: dt.datetime
    authorized: bool
    authenticated: bool
    available: bool
    complete: bool
    records: list

class VacancyGate:
    def __init__(self,paths: RuntimePaths,*,approvals: dict,now=utcnow,max_age_seconds=300,max_records=2000):
        if not isinstance(paths,RuntimePaths):raise ValueError('verified storage resolver paths required')
        if type(max_age_seconds) is not int or max_age_seconds<=0 or type(max_records) is not int or max_records<=0:raise ValueError('positive bounds required')
        self.paths=paths;self.now=now;self.max_age=max_age_seconds;self.max_records=max_records;self.approvals={}
        for namespace,grants in approvals.items():
            identifier(namespace)
            if not isinstance(grants,(list,tuple)) or not grants:raise ValueError('explicit namespace grants required')
            self.approvals[namespace]={g.key() for g in grants if isinstance(g,Grant)}
            if len(self.approvals[namespace])!=len(grants):raise ValueError('invalid/duplicate grants')
        self._storage()
        path=paths.root/'vacancies.sqlite'
        if path.is_symlink() or (path.exists() and (not path.is_file() or path.stat().st_mode&0o077)):raise StorageError('unsafe existing vacancy state; preserved')
        self.store=Store(path,now=now)
        with self.store.connection() as db:
            db.executescript('''
            CREATE TABLE IF NOT EXISTS vacancy_sources(scope TEXT PRIMARY KEY,revision TEXT,observed REAL,digest TEXT);
            CREATE TABLE IF NOT EXISTS vacancy_current(scope TEXT,id TEXT,body TEXT,digest TEXT,active INTEGER,PRIMARY KEY(scope,id));
            CREATE TABLE IF NOT EXISTS vacancy_history(scope TEXT,revision TEXT,digest TEXT,observed REAL,body TEXT,PRIMARY KEY(scope,revision));
            CREATE TABLE IF NOT EXISTS vacancy_requests(namespace TEXT,id TEXT,fingerprint TEXT,receipt TEXT,result TEXT,PRIMARY KEY(namespace,id));
            ''')
    def _storage(self):
        mount=Path(self.paths.proof['mount'])
        if mount not in self.paths.root.parents:raise StorageError('state must remain inside verified mount')
        proof=self.paths.probe(mount,Path(self.paths.proof['backing_image']))
        if proof.get('mount_verified') is not True or proof.get('encryption_verified') is not True or proof.get('filesystem')!='apfs':raise StorageError('storage verification failed; no writes')
        for p in (self.paths.root,*self.paths.root.parents):
            if p.is_symlink():raise StorageError('symlink storage rejected')
        if not self.paths.root.is_dir() or self.paths.root.stat().st_mode&0o077:raise StorageError('private state directory required')
    def apply(self,namespace,request_id,read: SourceRead):
        identifier(namespace);identifier(request_id)
        if not isinstance(read,SourceRead) or not isinstance(read.grant,Grant):raise ValueError('explicit source read required')
        scope=read.grant.key()
        if scope not in self.approvals.get(namespace,set()):raise PermissionError('namespace/source/privacy/coverage not approved')
        identifier(read.revision);observed=timestamp(read.observed_at);checked=timestamp(self.now())
        if any(type(f) is not bool for f in (read.authorized,read.authenticated,read.available,read.complete)):raise ValueError('explicit boolean evidence required')
        if not isinstance(read.records,list) or len(read.records)>self.max_records:raise ValueError('bounded record list required')
        if len(canonical(read.records).encode())>2_000_000:raise ValueError('snapshot byte limit')
        fp=hashed({'scope':scope,'revision':read.revision,'observed':observed,'flags':[read.authorized,read.authenticated,read.available,read.complete],'records':read.records})
        issue=next((label for flag,label in [(read.authorized,'unauthorized'),(read.authenticated or not read.grant.requires_authentication,'unauthenticated'),(read.available,'unavailable'),(read.complete,'partial')] if not flag),None)
        if not issue and (observed>checked or checked-observed>self.max_age):issue='stale_or_future_observation'
        normalized={}
        if not issue:
            for record in read.records:
                if not isinstance(record,dict) or set(record)!={'vacancy_id','official_url','fields'}:raise ValueError('record schema requires public listing only')
                ident=identifier(record['vacancy_id'])
                if ident in normalized:raise ValueError('duplicate vacancy ID')
                fields=record['fields']
                allowed={'title','location','department','employment_type','deadline','description'}
                if not isinstance(fields,dict) or not fields or set(fields)-allowed or any(not isinstance(v,str) or len(v)>20000 for v in fields.values()):raise ValueError('bounded public fields required; no profiles')
                normalized[ident]={'vacancy_id':ident,'official_url':official_url(record['official_url'],read.grant.official_origin),'fields':fields}
        self._storage()
        with self.store.transaction() as db:
            prior=db.execute('SELECT fingerprint,receipt FROM vacancy_requests WHERE namespace=? AND id=?',(namespace,request_id)).fetchone()
            if prior:
                if prior[0]!=fp:raise ValueError('conflicting request identity')
                receipt=json.loads(prior[1])
            else:
                checked=timestamp(self.now())
                if not issue and (observed>checked or checked-observed>self.max_age):issue='stale_or_future_observation'
                changes={'new':[],'materially_changed':[],'unchanged':[],'closed':[]};content_hash=hashed(normalized)
                if not issue:
                    existing_revision=db.execute('SELECT digest FROM vacancy_history WHERE scope=? AND revision=?',(scope,read.revision)).fetchone()
                    if existing_revision and existing_revision[0]!=content_hash:raise ValueError('revision conflicts with different listing content')
                    latest=db.execute('SELECT revision,observed,digest FROM vacancy_sources WHERE scope=?',(scope,)).fetchone()
                    if latest and (observed<latest[1] or (observed==latest[1] and content_hash!=latest[2])):issue='observation_regression_or_conflict'
                if not issue:
                    old={r[0]:(r[1],r[2],r[3]) for r in db.execute('SELECT id,body,digest,active FROM vacancy_current WHERE scope=?',(scope,))}
                    for ident,record in normalized.items():
                        h=hashed(record);before=old.get(ident)
                        category='new' if not before or not before[2] else 'unchanged' if before[1]==h else 'materially_changed'
                        changes[category].append(ident)
                        db.execute('INSERT OR REPLACE INTO vacancy_current VALUES (?,?,?,?,1)',(scope,ident,canonical(record),h))
                    for ident,before in old.items():
                        if before[2] and ident not in normalized:
                            changes['closed'].append(ident);db.execute('UPDATE vacancy_current SET active=0 WHERE scope=? AND id=?',(scope,ident))
                    db.execute('INSERT OR IGNORE INTO vacancy_history VALUES (?,?,?,?,?)',(scope,read.revision,content_hash,observed,canonical(normalized)))
                    db.execute('INSERT OR REPLACE INTO vacancy_sources VALUES (?,?,?,?)',(scope,read.revision,observed,content_hash))
                result={'classification':{k:None if issue else sorted(v) for k,v in changes.items()},'prior_source_state_preserved':bool(issue),'complete_exact_scope_read':not bool(issue)}
                receipt={'namespace':namespace,'request_id':request_id,'source_scope':scope,'coverage_id':read.grant.coverage_id,'source_revision':read.revision,'source_observed_utc':read.observed_at.astimezone(dt.timezone.utc).isoformat(),'checked_at_utc':dt.datetime.fromtimestamp(checked,dt.timezone.utc).isoformat(),'status':'blocked' if issue else 'complete','reason':issue,'result_sha256':hashed(result),'counts':{k:None if issue else len(v) for k,v in changes.items()},'ai_calls':0,'closure_evidence':not bool(issue)}
                db.execute('INSERT INTO vacancy_requests VALUES (?,?,?,?,?)',(namespace,request_id,fp,canonical(receipt),canonical(result)))
        self.readback(receipt)
        return receipt
    def readback(self,receipt):
        scope=receipt['source_scope'];namespace=receipt['namespace']
        if scope not in self.approvals.get(namespace,set()):raise PermissionError('readback scope not approved')
        self._storage()
        with self.store.connection() as db:row=db.execute('SELECT receipt,result FROM vacancy_requests WHERE namespace=? AND id=?',(namespace,receipt['request_id'])).fetchone()
        if row is None or json.loads(row[0])!=receipt or hashed(json.loads(row[1]))!=receipt['result_sha256']:raise ValueError('atomic receipt/readback mismatch')
        return json.loads(row[1])

# CLI deliberately absent until an actual source adapter/approval file is verified.
# This API accepts normalized public source evidence only; no source fetch is implied.

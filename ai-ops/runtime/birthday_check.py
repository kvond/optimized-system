"""Read verified private birthday inputs; no connectors, writes to source or AI."""
import argparse,datetime as dt,hashlib,json,os
from pathlib import Path
from birthdays import reconcile,public_summary
from storage import resolve_storage
from worker_context import build_context
from vacancies import identifier

TASK_ID='6aa9962611648191b900495a9ea89cd8'
CALENDAR_BINDING_SHA256='3d7e21189baee1b1b566f0d557ea7d5151d8e53ffcf29d9b573a2200f3c4f0c9'
PROJECT_BINDING_SHA256='c1e71e93ad7b14568b09e8a8adf150a5a55baab1d7d1b18f6251ea6c47da6b0a'
INPUT_NAME='birthday-current-inputs.json'

def read_private(path,max_bytes=2_000_000):
    if path.is_symlink() or not path.is_file() or path.stat().st_mode&0o077:
        raise ValueError('Private regular input required')
    before=path.stat()
    with path.open('rb') as stream:raw=stream.read(max_bytes+1)
    after=path.stat()
    if len(raw)>max_bytes or (before.st_ino,before.st_size,before.st_mtime_ns)!=(after.st_ino,after.st_size,after.st_mtime_ns):
        raise ValueError('Input changed or exceeded bound')
    return raw

def run(request_id,*,paths=None,now=None):
    identifier(request_id);now=now or dt.datetime.now(dt.timezone.utc)
    paths=paths or resolve_storage(initialize=False)
    def recheck():
        resolve_storage(paths.root,mount=paths.proof['mount'],image=paths.proof['backing_image'],probe=paths.probe,environ={})
    recheck();raw=read_private(paths.root/INPUT_NAME);data=json.loads(raw)
    if data['task_id']!=TASK_ID or hashlib.sha256(data['calendar_id'].encode()).hexdigest()!=CALENDAR_BINDING_SHA256 or hashlib.sha256(data['project_id'].encode()).hexdigest()!=PROJECT_BINDING_SHA256 or data['scope']!='home-birthday-gifts':
        raise ValueError('Exact original source scope required')
    context=build_context('birthday',max_words=400)
    # Unknown family identity is a hold, never eligibility or a zero finding.
    complete=data['normalization_complete'] is True
    bindings=data['family_bindings'];allowed={b['event_id'] for b in bindings if b.get('verified') is True and b.get('history_task_id') and b.get('source_receipt_id')}
    if len(allowed)!=len(bindings) or any(e['event_id'] not in allowed for e in data['events']):complete=False
    history_source={**data['history_source'],'complete':data['history_source']['complete'] and complete}
    result=reconcile(scope=data['scope'],now=now,timezone='America/New_York',lookahead_days=30,
                     calendar_source=data['calendar_source'],history_source=history_source,
                     events=data['events'],history=data['history'])
    holds=data.get('scoped_holds',[])
    if not isinstance(holds,list) or len(holds)>1000:raise ValueError('Bounded scoped holds required')
    current_holds=sum(h.get('current_window') is not False for h in holds)
    result['family_crosswalk_complete']=complete and not holds
    result['scoped_hold_count']=len(holds)
    result['current_window_hold_count']=current_holds
    result['current_window_coverage_complete']=complete and current_holds==0
    result['reconciliation_status']='partial' if holds else 'complete'
    result['scoped_holds']=holds
    if current_holds and result['status']=='complete':
        result['status']='partial';result['no_work_conclusion_permitted']=False
    result['context_sha256']=context['context_sha256'];result['context_words']=context['context_words']
    result['input_sha256']=hashlib.sha256(raw).hexdigest()
    key=hashlib.sha256(request_id.encode()).hexdigest();dest=paths.receipts/('birthday-check-'+key+'.json')
    packet={'request_id':request_id,'task_id':TASK_ID,'source_receipt_path':data['source_receipt_path'],'result':result}
    recheck()
    if dest.exists():
        if json.loads(read_private(dest))!=packet:raise ValueError('Request identity conflict; no overwrite')
    else:
        fd=os.open(dest,os.O_WRONLY|os.O_CREAT|os.O_EXCL|getattr(os,'O_NOFOLLOW',0),0o600)
        with os.fdopen(fd,'w') as stream:
            json.dump(packet,stream,sort_keys=True,indent=2);stream.flush();os.fsync(stream.fileno())
    recheck()
    if json.loads(read_private(dest))!=packet:raise ValueError('Receipt readback mismatch')
    return {**public_summary(result),'receipt_path':str(dest),'receipt_readback_verified':True,
            'compact_context':context['context'],
            'context_sha256':result['context_sha256'],'context_words':result['context_words'],
            'family_crosswalk_complete':result['family_crosswalk_complete'],
            'scoped_hold_count':result['scoped_hold_count'],'current_window_hold_count':result['current_window_hold_count'],
            'current_window_coverage_complete':result['current_window_coverage_complete'],
            'reconciliation_status':result['reconciliation_status'],'source_refresh_required_each_business_day':True}

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--request-id',required=True);args=parser.parse_args()
    if args.request_id.strip() in {'ACTUAL_UTC_RUN_TIME','doe-watch-YYYYMMDDTHHMMSSZ','YYYYMMDDTHHMMSSZ'}:
        print(json.dumps({'status':'blocked','counts':None,'reason':'literal_request_timestamp_placeholder','ai_calls':0}));return 2
    try:result=run(args.request_id)
    except Exception:
        print(json.dumps({'status':'blocked','counts':None,'reason':'private_input_storage_scope_or_readback_unverified','ai_calls':0}));return 2
    print(json.dumps(result,sort_keys=True));return 0 if result['status']=='complete' else 1
if __name__=='__main__':raise SystemExit(main())

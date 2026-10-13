"""Reuse today's verified birthday evidence for News; no fetch, AI or ordering."""
import datetime as dt
import hashlib
import json
from pathlib import Path
from zoneinfo import ZoneInfo
from birthday_check import run,read_private,INPUT_NAME
from storage import resolve_storage
from vacancies import identifier


def reuse_for_news(request_id,*,paths=None,now=None):
    """Returns aggregate evidence and private packet path, preserving21/7-day policy.

    Does not interpret the News thresholds as purchase/cart authorization. Reuses
    source reads only when original scope and current-date coverage pass the same
    birthday CLI gates. Out-of-window reconciliation holds remain separate.
    """
    identifier(request_id);now=now or dt.datetime.now(dt.timezone.utc)
    paths=paths or resolve_storage(initialize=False)
    summary=run('news-birthday-'+request_id,paths=paths,now=now)
    if summary['status']!='complete' or summary['current_window_coverage_complete'] is not True:
        return {'status':'hold','counts':None,'duplicate_source_read_skipped':False,
                'reason':'fresh_complete_scoped_birthday_evidence_unavailable','ai_calls':0}
    packet_path=Path(summary['receipt_path'])
    if packet_path.parent!=paths.receipts:raise ValueError('Private receipt path mismatch')
    packet=json.loads(read_private(packet_path));result=packet['result']
    raw=read_private(paths.root/INPUT_NAME)
    if hashlib.sha256(raw).hexdigest()!=result['input_sha256']:
        raise ValueError('Birthday inputs changed after verification')
    today=now.astimezone(ZoneInfo('America/New_York')).date()
    if result['business_date']!=today.isoformat() or result['fingerprint']!=summary['fingerprint']:
        raise ValueError('Receipt date or fingerprint conflict')
    private_items=result['items']['eligible']
    near21=0;near7=0
    for item in private_items:
        days=(dt.date.fromisoformat(item['occurrence_date'])-today).days
        if not 0<=days<=30:raise ValueError('Eligible date outside verified window')
        near21+=days<=21;near7+=days<=7
    # Revalidate mounted storage after all reads, before returning a reuse claim.
    resolve_storage(paths.root,mount=paths.proof['mount'],image=paths.proof['backing_image'],probe=paths.probe,environ={})
    return {'status':'verified_reuse','counts':summary['counts'],
            'eligible_within21_days':near21,'eligible_within7_days':near7,
            'business_date':today.isoformat(),'input_sha256':result['input_sha256'],
            'fingerprint':result['fingerprint'],'private_eligible_packet_path':str(packet_path),
            'current_window_coverage_complete':True,'reconciliation_status':result['reconciliation_status'],
            'out_of_window_hold_count':result['scoped_hold_count'],
            'duplicate_source_read_skipped':True,'api_reads':0,'ai_calls':0,
            'news_thresholds_preserved':[21,7],'cart_purchase_message_actions':0}

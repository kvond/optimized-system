"""Pure private birthday date/history eligibility. No network, AI or mutations.
Inputs must be normalized by an independently authorized Calendar/Todoist adapter.
Never infer an event/identity/date, purchase, contact or delivery from a filename.
"""
import datetime as dt
import hashlib
import json
from zoneinfo import ZoneInfo

MAX_EVENTS = 1000
MAX_HISTORY = 5000


def _id(value):
    if not isinstance(value,str) or not value.strip() or len(value)>500:
        raise ValueError('Explicit bounded identity required')
    return value


def _date(value):
    if not isinstance(value,str): raise ValueError('ISO date required')
    parsed=dt.date.fromisoformat(value)
    if parsed.isoformat()!=value: raise ValueError('Canonical ISO date required')
    return parsed


def reconcile(*,scope,now,timezone,lookahead_days,calendar_source,history_source,
              events,history):
    """Actual expanded occurrence dates only; window includes today and end day.

    History records close only the exact event+occurrence after a verified saved
    handled receipt. Pending/planned/unverified work never implies completion.
    Complete fresh source evidence is mandatory even on unchanged runs.
    """
    _id(scope)
    if not isinstance(now,dt.datetime) or now.tzinfo is None:
        raise ValueError('Aware current time required')
    zone=ZoneInfo(timezone)
    if type(lookahead_days) is not int or not 0<=lookahead_days<=366:
        raise ValueError('Explicit bounded window required; no default')
    today=now.astimezone(zone).date()
    keys={'source_id','revision','complete','available','observed_at'}
    evidence=[];issues=[]
    for label,source in [('calendar',calendar_source),('history',history_source)]:
        if not isinstance(source,dict) or set(source)!=keys: raise ValueError('Exact source evidence required')
        _id(source['source_id']);_id(source['revision'])
        if type(source['complete']) is not bool or type(source['available']) is not bool:
            raise ValueError('Explicit source flags required')
        observed=dt.datetime.fromisoformat(source['observed_at'].replace('Z','+00:00'))
        if observed.tzinfo is None: raise ValueError('Aware observation required')
        # Same business-day freshness; future evidence is invalid.
        if observed>now or observed.astimezone(zone).date()!=today:issues.append(label+'_stale_or_future')
        if not source['available'] or not source['complete']:issues.append(label+'_incomplete_or_unavailable')
        evidence.append(source)
    if not isinstance(events,list) or len(events)>MAX_EVENTS or not isinstance(history,list) or len(history)>MAX_HISTORY:
        raise ValueError('Bounded event/history lists required')
    normalized=[];seen=set()
    for event in events:
        if not isinstance(event,dict) or set(event)!={'event_id','occurrence_date'}:
            raise ValueError('Event ID/date only; no personal bodies')
        ident=_id(event['event_id']);date=_date(event['occurrence_date']);key=(ident,date.isoformat())
        if key in seen: raise ValueError('Duplicate event occurrence')
        seen.add(key);normalized.append(key)
    handled=set();receipts=set()
    for row in history:
        if not isinstance(row,dict) or set(row)!={'event_id','occurrence_date','status','receipt_id','verified','saved_at'}:
            raise ValueError('Exact history evidence required')
        ident=_id(row['event_id']);date=_date(row['occurrence_date'])
        for field in ('receipt_id','saved_at'):
            if row[field] is not None and (not isinstance(row[field],str) or len(row[field])>500):
                raise ValueError('Bounded optional history metadata required')
        if row['status'] not in ('handled','planned','pending'):raise ValueError('Unsupported history status')
        if type(row['verified']) is not bool:raise ValueError('Explicit receipt verification required')
        if row['status']=='handled' and row['verified']:
            receipt=_id(row['receipt_id']);saved=dt.datetime.fromisoformat(row['saved_at'].replace('Z','+00:00'))
            if saved.tzinfo is None or saved>now:raise ValueError('Invalid saved receipt time')
            identity=(ident,date.isoformat())
            if receipt in receipts:raise ValueError('Duplicate handled receipt')
            receipts.add(receipt);handled.add(identity)
    counts=None;items=None
    if not issues:
        items={'eligible':[],'handled':[],'outside_window':[]}
        for ident,date_string in sorted(normalized):
            days=(_date(date_string)-today).days;key=(ident,date_string)
            category='outside_window' if days<0 or days>lookahead_days else 'handled' if key in handled else 'eligible'
            items[category].append({'event_id':ident,'occurrence_date':date_string})
        counts={k:len(v) for k,v in items.items()}
    identity={'scope':scope,'business_date':today.isoformat(),'timezone':timezone,
              'lookahead_days':lookahead_days,'sources':evidence,'events':sorted(normalized),
              'history':sorted(history,key=lambda r:json.dumps(r,sort_keys=True))}
    encoded=json.dumps(identity,sort_keys=True,separators=(',',':')).encode()
    if len(encoded)>2_000_000: raise ValueError('Input byte bound exceeded')
    fingerprint=hashlib.sha256(encoded).hexdigest()
    return {'scope':scope,'status':'blocked' if issues else 'complete','issues':sorted(set(issues)),
            'business_date':today.isoformat(),'timezone':timezone,'lookahead_days':lookahead_days,
            'counts':counts,'items':items,'fingerprint':fingerprint,'ai_calls':0,
            'contact_cart_purchase_message_actions':0,'no_work_conclusion_permitted':not issues}


def public_summary(result):
    """Safe console summary; event IDs/dates stay in protected private state."""
    return {k:result[k] for k in ['status','issues','business_date','timezone','lookahead_days','counts','fingerprint','ai_calls','contact_cart_purchase_message_actions']}

"""Fixed DOE source packet for the existing statewide job watch, with compact context.

Source changes are never evidence that a candidate has already been reviewed or
reported. The receiving task must reconcile its own verified report history.
"""
import argparse
import json
from pathlib import Path
import doe_check
import doe_source
from storage import resolve_storage
from vacancies import VacancyGate, hashed, official_url
from worker_context import build_context


def packet(request_id, vacancy_id=None):
    context = build_context('doe-watch')
    paths = resolve_storage(initialize=True)
    report = doe_check.check(request_id, paths=paths)
    result = dict(report, coverage='Delaware Department of Education only',
                  statewide_coverage=False, context=context['context'],
                  context_sha256=context['context_sha256'],
                  candidate_review_history_verified=False)
    if report['status'] != 'complete':
        result['listings'] = None
        return result
    artifact = Path(report['receipt_path'])
    saved = json.loads(artifact.read_text())
    gate = VacancyGate(paths, approvals={doe_check.NAMESPACE:[doe_source.GRANT]})
    classification = gate.readback(saved['receipt'])['classification']
    with gate.store.connection() as db:
        row = db.execute('SELECT body,digest FROM vacancy_history WHERE scope=? AND revision=?',
                         (saved['receipt']['source_scope'],saved['receipt']['source_revision'])).fetchone()
    if row is None:
        raise ValueError('Immutable source snapshot unavailable')
    snapshot = json.loads(row[0])
    normalized = {item['vacancy_id']:dict(item,official_url=official_url(item['official_url'],doe_source.GRANT.official_origin))
                  for item in saved['public_listings']}
    if len(normalized) != len(saved['public_listings']) or hashed(snapshot)!=row[1] or normalized!=snapshot:
        raise ValueError('Public listing snapshot readback mismatch')
    result['source_classification'] = classification
    # Include all active public records: an unchanged source may still contain a
    # vacancy never evaluated by this particular candidate workflow.
    if vacancy_id is not None:
        if vacancy_id not in snapshot: raise ValueError('Vacancy absent from verified snapshot')
        result['listings'] = [snapshot[vacancy_id]]
        result['full_description_included'] = True
    else:
        result['listings'] = [dict(snapshot[key],fields={k:v for k,v in snapshot[key]['fields'].items() if k!='description'},
                                  public_listing_sha256=hashed(snapshot[key])) for key in sorted(snapshot)]
        result['full_description_included'] = False
        result['detail_command'] = ('Use the same command and request ID with --vacancy-id EXACT_ID only for an '
                                    'unreviewed/materially changed relevant candidate. It reads the verified '
                                    'saved source; no source refetch. Full descriptions are omitted from routine packets.')
    result['candidate_history_rule'] = ('Compare every active ID with verified '
        'task-specific reviewed/reported history and current criteria. Source '
        'unchanged alone does not authorize skipping candidate review. Do not '
        'mark anything reported without a verified destination receipt.')
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--request-id', required=True)
    parser.add_argument('--vacancy-id', help='One exact public ID from the verified saved snapshot')
    args = parser.parse_args()
    if args.request_id.strip() in {'ACTUAL_UTC_RUN_TIME','doe-watch-YYYYMMDDTHHMMSSZ','YYYYMMDDTHHMMSSZ'}:
        print(json.dumps({'status':'failed_closed','listings':None,
                          'reason':'literal_request_timestamp_placeholder','ai_calls':0}))
        return 2
    try:
        result = packet(args.request_id, args.vacancy_id)
    except Exception:
        print(json.dumps({'status':'failed_closed', 'listings':None,
                          'reason':'source_context_storage_or_readback_failure',
                          'ai_calls':0}))
        return 2
    print(json.dumps(result, sort_keys=True))
    return 0 if result['status']=='complete' else 1


if __name__=='__main__': raise SystemExit(main())

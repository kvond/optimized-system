"""On-demand fixed DOE public-source check. No AI, matching or scheduling."""
import argparse
import datetime as dt
import hashlib
import json
import multiprocessing as mp
import os
import signal
from pathlib import Path
import sqlite3
import time
import threading
import queue
import doe_source
from storage import resolve_storage
from vacancies import VacancyGate, identifier

NAMESPACE = 'doe-operator-watch'
DEADLINE_SECONDS = 45


def _worker(send):
    # Trusted fixed reader creates no descendants; this is not a general sandbox.
    try:
        os.setsid()
        send.send(doe_source.read_source())
    except BaseException:
        try: send.send({'worker_exception_class': type(__import__('sys').exc_info()[1]).__name__})
        except (BrokenPipeError, OSError): pass
    finally:
        send.close()


def acquire(deadline=DEADLINE_SECONDS, *, _context=None, _worker_target=None):
    """45s acquisition maximum, followed by at most4s cleanup joins.

    Receive runs in a boundedly supervised thread so partial pipe frames cannot
    extend acquisition. Failed cleanup raises before any gate-state write.
    """
    if not 0 < deadline <= DEADLINE_SECONDS: raise ValueError('Invalid acquisition deadline')
    context = _context or mp.get_context('spawn')
    receive, send = context.Pipe(duplex=False)
    process = None; reader = None; started = False; result = None
    mailbox = queue.Queue(maxsize=1)
    failure = None; clean = True
    def read_pipe():
        try: mailbox.put(receive.recv())
        except (EOFError, OSError): mailbox.put(None)
    try:
        process = context.Process(target=_worker_target or _worker, args=(send,))
        expires = time.monotonic() + deadline
        process.start(); started = True; send.close()
        reader = threading.Thread(target=read_pipe, daemon=True)
        reader.start()
        try: result = mailbox.get(timeout=max(0, expires-time.monotonic()))
        except queue.Empty: pass
    except BaseException as exc:
        failure = exc
    finally:
        # Close parent write end even when start/setsid fails, allowing EOF.
        send.close()
        if process is not None and process.pid is not None: started = True
        if started:
            try:
                if process.is_alive():
                    try:
                        if os.getpgid(process.pid) == process.pid:
                            os.killpg(process.pid, signal.SIGKILL)
                        else: process.kill()
                    except ProcessLookupError: pass
                    except OSError:
                        # Group signal may fail; try only the owned process PID.
                        try: process.kill()
                        except OSError: clean = False
            finally:
                try: process.join(timeout=2)
                except (AssertionError, OSError): clean = False
        try:
            if reader is not None:
                reader.join(timeout=2)
                clean = clean and not reader.is_alive()
        finally:
            receive.close()
        if started: clean = clean and not process.is_alive()
        if not clean: raise RuntimeError('Owned child cleanup unconfirmed; no state write')
    if failure is not None: raise RuntimeError('Owned child start/receive failed; no state write') from failure
    exception_class = result.get('worker_exception_class') if isinstance(result, dict) else None
    if result is None or exception_class is not None:
        observed = dt.datetime.now(dt.timezone.utc)
        read = doe_source.SourceRead(doe_source.GRANT, hashlib.sha256(b'acquisition-deadline-or-worker-failure').hexdigest(), observed, True, False, False, False, [])
        return doe_source.AdapterResult(read, 'owned_child_timeout_or_failure', {'posting_count':None,'complete_exact_scope_read':False,'model_calls':0,'child_cleanup_confirmed':True,'acquisition_deadline_seconds':deadline,'cleanup_join_budget_seconds':4,'worker_start_method':context.get_start_method(),'worker_exitcode':process.exitcode,'worker_exception_class':exception_class})
    result.evidence.update(worker_start_method=context.get_start_method(),worker_exitcode=process.exitcode,worker_result_received=True)
    return result


def _resolve_again(paths):
    return resolve_storage(paths.root, mount=paths.proof['mount'], image=paths.proof['backing_image'], probe=paths.probe, environ={})


def check(request_id, *, paths=None):
    identifier(request_id)
    # Resolve encrypted storage before network, then again before every write.
    paths = paths or resolve_storage(initialize=True)
    _resolve_again(paths)
    key = hashlib.sha256(request_id.encode()).hexdigest()
    artifact = paths.receipts / ('doe-operator-watch-' + key + '.json')
    if artifact.exists():
        if artifact.is_symlink() or artifact.stat().st_mode & 0o077: raise ValueError('Unsafe existing receipt')
        saved = json.loads(artifact.read_text())
        if saved['receipt']['request_id'] != request_id: raise ValueError('Receipt identity conflict')
        gate = VacancyGate(paths, approvals={NAMESPACE:[doe_source.GRANT]})
        gate.readback(saved['receipt'])
        return summary(saved['receipt'], artifact, reused=True)
    # A prior atomic gate receipt without its artifact is uncertain: do not refetch.
    database = paths.root / 'vacancies.sqlite'
    if database.exists():
        with sqlite3.connect('file:'+str(database)+'?mode=ro',uri=True) as db:
            prior = db.execute('SELECT 1 FROM vacancy_requests WHERE namespace=? AND id=?',(NAMESPACE,request_id)).fetchone()
        if prior: raise ValueError('Prior atomic request lacks artifact; requires readback recovery')
    result = acquire()
    _resolve_again(paths)
    gate = VacancyGate(paths, approvals={NAMESPACE:[doe_source.GRANT]})
    receipt = gate.apply(NAMESPACE, request_id, result.read)
    gate.readback(receipt)
    saved = {'receipt':receipt,'evidence':result.evidence,'source_reason':result.reason,'public_listings':result.read.records}
    _resolve_again(paths)
    payload = json.dumps(saved,sort_keys=True,indent=2)+'\n'
    fd = os.open(artifact,os.O_WRONLY|os.O_CREAT|os.O_EXCL|getattr(os,'O_NOFOLLOW',0),0o600)
    with os.fdopen(fd,'w') as stream:
        stream.write(payload); stream.flush(); os.fsync(stream.fileno())
    _resolve_again(paths)
    if json.loads(artifact.read_text()) != saved: raise ValueError('Receipt artifact readback mismatch')
    return summary(receipt,artifact,reused=False)


def summary(receipt,artifact,*,reused):
    return {'namespace':NAMESPACE,'request_id':receipt['request_id'],'status':receipt['status'],
            'source_observed_utc':receipt['source_observed_utc'],
            'checked_at_utc':receipt['checked_at_utc'],
            'reused_snapshot_requires_freshness_check':reused,
            'counts':receipt['counts'],'source_revision':receipt['source_revision'],
            'result_sha256':receipt['result_sha256'],'receipt_path':str(artifact),
            'receipt_readback_verified':True,'reused_request':reused,'ai_calls':0,
            'scheduled':False,'candidate_matching':False}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--request-id',required=True)
    args=parser.parse_args()
    try:
        report=check(args.request_id)
    except Exception:
        print(json.dumps({'status':'failed_closed','reason':'storage_or_request_or_readback_failure','ai_calls':0}))
        return 2
    print(json.dumps(report,sort_keys=True)); return 0 if report['status']=='complete' else 1

if __name__=='__main__': raise SystemExit(main())

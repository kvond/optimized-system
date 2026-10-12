"""Private, provider-neutral usage receipts. No payloads, network or adapters."""
from __future__ import annotations
import contextlib
import datetime as dt
from decimal import Decimal
import json
import os
from pathlib import Path
import sqlite3
from zoneinfo import ZoneInfo


def money(value):
    if value is None: raise ValueError('unknown price: no dispatch')
    n=Decimal(str(value))*1_000_000
    if not n.is_finite() or n<0 or n!=n.to_integral_value(): raise ValueError('invalid dollar amount')
    return int(n)


def instant(value):
    if value.tzinfo is None or value.utcoffset() is None: raise ValueError('aware clock required')
    return value


class UsageLedger:
    def __init__(self,path,*,business_timezone,now=lambda:dt.datetime.now(dt.timezone.utc)):
        self.zone=ZoneInfo(business_timezone);self.now=now;self.path=str(path)
        if self.path==':memory:':raise ValueError('private durable database required')
        Path(path).parent.mkdir(parents=True,exist_ok=True)
        try:
            fd=os.open(path,os.O_CREAT|os.O_EXCL|os.O_WRONLY,0o600);os.close(fd)
        except FileExistsError:pass
        if os.stat(path).st_mode&0o077:raise PermissionError('database permissions must be private')
        with self.db() as db:
            db.executescript('''
            CREATE TABLE IF NOT EXISTS settings(key TEXT PRIMARY KEY,value TEXT NOT NULL);
            CREATE TABLE IF NOT EXISTS caps(scope TEXT,period TEXT,cap INTEGER NOT NULL,PRIMARY KEY(scope,period));
            CREATE TABLE IF NOT EXISTS counters(scope TEXT,period TEXT,window TEXT,spent INTEGER DEFAULT 0,pending INTEGER DEFAULT 0,PRIMARY KEY(scope,period,window));
            CREATE TABLE IF NOT EXISTS requests(id TEXT PRIMARY KEY,workflow TEXT NOT NULL,provider TEXT NOT NULL,model TEXT NOT NULL,estimate INTEGER NOT NULL,created TEXT NOT NULL,day TEXT NOT NULL,month TEXT NOT NULL,state TEXT NOT NULL,receipt TEXT,actual INTEGER,settled_at TEXT);
            CREATE TABLE IF NOT EXISTS alerts(scope TEXT,period TEXT,window TEXT,threshold INTEGER,created TEXT,PRIMARY KEY(scope,period,window,threshold));
            ''')
        with self.tx() as db:
            old=db.execute("SELECT value FROM settings WHERE key='timezone'").fetchone()
            if old and old[0]!=business_timezone:raise ValueError('timezone change requires separate ledger')
            db.execute("INSERT OR IGNORE INTO settings VALUES ('timezone',?)",(business_timezone,))

    @contextlib.contextmanager
    def db(self):
        db=sqlite3.connect(self.path,timeout=10,isolation_level=None)
        try:yield db
        finally:db.close()

    @contextlib.contextmanager
    def tx(self):
        with self.db() as db:
            db.execute('BEGIN IMMEDIATE')
            try:yield db;db.execute('COMMIT')
            except BaseException:db.execute('ROLLBACK');raise

    def configure(self,scope,*,daily,monthly):
        if scope!='combined' and not(scope.startswith('workflow:') or scope.startswith('provider:')):raise ValueError('explicit scope required')
        caps={'day':money(daily),'month':money(monthly)}
        with self.tx() as db:
            for period,cap in caps.items():
                # Never reduce below liabilities, including pending requests in old windows.
                liability=db.execute('SELECT COALESCE(MAX(spent+pending),0) FROM counters WHERE scope=? AND period=?',(scope,period)).fetchone()[0]
                if cap<liability:raise ValueError('cap below recorded liability')
                db.execute('INSERT INTO caps VALUES (?,?,?) ON CONFLICT(scope,period) DO UPDATE SET cap=excluded.cap',(scope,period,cap))

    @staticmethod
    def scopes(workflow,provider):return ['combined','workflow:'+workflow,'provider:'+provider]

    def reserve(self,*,request_id,workflow,provider,model,estimated_cost):
        if not all(isinstance(v,str) and v.strip() for v in [request_id,workflow,provider,model]):raise ValueError('explicit identifiers required')
        estimate=money(estimated_cost)
        if estimate<=0:raise ValueError('positive priced bound required')
        clock=instant(self.now());local=clock.astimezone(self.zone);day=local.date().isoformat();month=day[:7]
        identity=(workflow,provider,model,estimate)
        with self.tx() as db:
            old=db.execute('SELECT workflow,provider,model,estimate,state FROM requests WHERE id=?',(request_id,)).fetchone()
            if old:
                if old[:4]!=identity:raise ValueError('conflicting request')
                # Return state, never a fresh dispatch authority.
                return {'request_id':request_id,'new':False,'state':old[4]}
            for scope in self.scopes(workflow,provider):
                for period,window in [('day',day),('month',month)]:
                    cap=db.execute('SELECT cap FROM caps WHERE scope=? AND period=?',(scope,period)).fetchone()
                    if cap is None:raise PermissionError('missing budget')
                    spent=db.execute('SELECT COALESCE(SUM(spent),0) FROM counters WHERE scope=? AND period=? AND window=?',(scope,period,window)).fetchone()[0]
                    # Pending liabilities remain charged after midnight/month rollover.
                    pending=db.execute('SELECT COALESCE(SUM(pending),0) FROM counters WHERE scope=? AND period=?',(scope,period)).fetchone()[0]
                    if spent+pending+estimate>cap[0]:raise PermissionError('budget exhausted')
            db.execute('INSERT INTO requests(id,workflow,provider,model,estimate,created,day,month,state,receipt,actual) VALUES (?,?,?,?,?,?,?,?,?,NULL,NULL)',(request_id,*identity,clock.astimezone(dt.timezone.utc).isoformat(),day,month,'pending'))
            for scope in self.scopes(workflow,provider):
                for period,window in [('day',day),('month',month)]:
                    db.execute('INSERT INTO counters(scope,period,window,pending) VALUES (?,?,?,?) ON CONFLICT(scope,period,window) DO UPDATE SET pending=pending+excluded.pending',(scope,period,window,estimate))
                    self._alerts(db,scope,period,window,clock)
        return {'request_id':request_id,'new':True,'state':'pending'}

    def _alerts(self,db,scope,period,window,clock):
        cap=db.execute('SELECT cap FROM caps WHERE scope=? AND period=?',(scope,period)).fetchone()[0]
        spent=db.execute('SELECT spent FROM counters WHERE scope=? AND period=? AND window=?',(scope,period,window)).fetchone()[0]
        pending=db.execute('SELECT COALESCE(SUM(pending),0) FROM counters WHERE scope=? AND period=?',(scope,period)).fetchone()[0]
        for threshold in [50,80,100]:
            if (spent+pending)*100>=cap*threshold:
                db.execute('INSERT OR IGNORE INTO alerts VALUES (?,?,?,?,?)',(scope,period,window,threshold,clock.isoformat()))

    def settle(self,request_id,*,receipt_id,actual_cost,input_tokens=None,cached_tokens=None,output_tokens=None,duration_seconds=None,status='succeeded',retry_state='none',error_code=None):
        # Metadata only: never accept free-form errors, response bodies or prompts.
        if not isinstance(receipt_id,str) or not receipt_id.strip():raise ValueError('receipt identity required')
        if status not in {'succeeded','failed','cancelled'} or retry_state not in {'none','eligible','blocked','exhausted'}:raise ValueError('invalid status')
        if error_code is not None and (not isinstance(error_code,str) or len(error_code)>80 or not all(c.isalnum() or c in '_.-' for c in error_code)):raise ValueError('bounded symbolic error code required')
        for n in [input_tokens,cached_tokens,output_tokens]:
            if n is not None and (isinstance(n,bool) or not isinstance(n,int) or n<0):raise ValueError('unknown tokens must be null')
        if duration_seconds is not None:
            duration=Decimal(str(duration_seconds))
            if not duration.is_finite() or duration<0:raise ValueError('invalid duration')
        if cached_tokens is not None and input_tokens is not None and cached_tokens>input_tokens:raise ValueError('cached tokens exceed input tokens')
        actual=money(actual_cost);clock=instant(self.now());day=clock.astimezone(self.zone).date().isoformat();month=day[:7]
        receipt=json.dumps(dict(receipt_id=receipt_id,actual_micros=actual,input_tokens=input_tokens,cached_tokens=cached_tokens,output_tokens=output_tokens,duration_seconds=duration_seconds,status=status,retry_state=retry_state,error_code=error_code),sort_keys=True,allow_nan=False)
        with self.tx() as db:
            row=db.execute('SELECT workflow,provider,estimate,day,month,state,receipt FROM requests WHERE id=?',(request_id,)).fetchone()
            if row is None:raise KeyError('unknown request')
            if row[5]=='settled':
                if row[6]!=receipt:raise ValueError('conflicting receipt')
                return
            duplicate=db.execute('SELECT id FROM requests WHERE receipt IS NOT NULL AND json_extract(receipt,\'$.receipt_id\')=?',(receipt_id,)).fetchone()
            if duplicate:raise ValueError('receipt already assigned')
            for scope in self.scopes(row[0],row[1]):
                for period,old_window,new_window in [('day',row[3],day),('month',row[4],month)]:
                    db.execute('UPDATE counters SET pending=pending-? WHERE scope=? AND period=? AND window=?',(row[2],scope,period,old_window))
                    db.execute('INSERT INTO counters(scope,period,window,spent) VALUES (?,?,?,?) ON CONFLICT(scope,period,window) DO UPDATE SET spent=spent+excluded.spent',(scope,period,new_window,actual))
                    self._alerts(db,scope,period,new_window,clock)
            db.execute("UPDATE requests SET state='settled',receipt=?,actual=?,settled_at=? WHERE id=?",(receipt,actual,clock.astimezone(dt.timezone.utc).isoformat(),request_id))

    def receipts(self):
        with self.db() as db:
            return [dict(request_id=r[0],workflow=r[1],provider=r[2],model=r[3],estimated_micros=r[4],created_at=r[5],state=r[6],receipt=json.loads(r[7]) if r[7] else None,settled_at=r[8]) for r in db.execute('SELECT id,workflow,provider,model,estimate,created,state,receipt,settled_at FROM requests')]

    def alerts(self):
        with self.db() as db:return [dict(scope=r[0],period=r[1],window=r[2],threshold=r[3],created_at=r[4]) for r in db.execute('SELECT * FROM alerts ORDER BY scope,period,window,threshold')]

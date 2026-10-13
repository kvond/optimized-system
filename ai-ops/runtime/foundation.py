"""Provider-neutral local execution primitives. No network or provider adapters."""
from __future__ import annotations
import contextlib, datetime as dt, hashlib, json, os, signal, sqlite3, subprocess, time, uuid
from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path
UTC = dt.timezone.utc

def timestamp(value: dt.datetime) -> float:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError('timezone-aware datetime required')
    return value.timestamp()

def utcnow() -> dt.datetime:
    return dt.datetime.now(UTC)

def canonical(value) -> str:
    return json.dumps(value, sort_keys=True, separators=(',', ':'), allow_nan=False)

def micros(amount) -> int:
    value = Decimal(str(amount)) * 1_000_000
    if not value.is_finite() or value < 0 or value != value.to_integral_value():
        raise ValueError('cost must be finite nonnegative dollars with <=6 decimals')
    return int(value)

@dataclass(frozen=True)
class CacheContract:
    privacy_partition: str
    source_id: str
    source_revision: str
    task_type: str
    contract_version: str
    inputs: dict
    route_version: str
    def key(self) -> str:
        fields = self.__dict__
        if any(not isinstance(fields[k], str) or not fields[k].strip() for k in fields if k != 'inputs'):
            raise ValueError('nonempty explicit cache contract fields required')
        if not isinstance(self.inputs, dict):
            raise ValueError('inputs must be an object')
        return hashlib.sha256(canonical(fields).encode()).hexdigest()

class Store:
    def __init__(self, path, now=utcnow):
        self.path = str(path)
        self.now = now
        if self.path == ':memory:':
            raise ValueError('durable SQLite path required')
        Path(self.path).parent.mkdir(parents=True, exist_ok=True)
        # New private database only; never relax permissions on existing directories.
        fd = os.open(self.path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600) if not Path(self.path).exists() else None
        if fd is not None: os.close(fd)
        with self.connection() as db:
            db.executescript('''
            CREATE TABLE IF NOT EXISTS cache(key TEXT PRIMARY KEY, partition TEXT NOT NULL,
              source_id TEXT NOT NULL, revision TEXT NOT NULL, expires REAL NOT NULL,
              succeeded INTEGER NOT NULL CHECK(succeeded IN (0,1)), payload TEXT NOT NULL);
            CREATE TABLE IF NOT EXISTS budgets(partition TEXT PRIMARY KEY, cap INTEGER NOT NULL CHECK(cap>=0),
              spent INTEGER NOT NULL DEFAULT 0 CHECK(spent>=0));
            CREATE TABLE IF NOT EXISTS reservations(id TEXT PRIMARY KEY, partition TEXT NOT NULL,
              amount INTEGER NOT NULL CHECK(amount>=0), state TEXT NOT NULL CHECK(state IN ('reserved','settled','cancelled')),
              actual INTEGER, created REAL NOT NULL, FOREIGN KEY(partition) REFERENCES budgets(partition));
            ''')
    @contextlib.contextmanager
    def connection(self):
        db = sqlite3.connect(self.path, timeout=10, isolation_level=None)
        db.execute('PRAGMA foreign_keys=ON')
        db.execute('PRAGMA busy_timeout=10000')
        try: yield db
        finally: db.close()
    @contextlib.contextmanager
    def transaction(self):
        with self.connection() as db:
            db.execute('BEGIN IMMEDIATE')
            try:
                yield db
                db.execute('COMMIT')
            except BaseException:
                db.execute('ROLLBACK')
                raise
    def put(self, contract: CacheContract, payload, expires_at: dt.datetime, *, succeeded: bool):
        key = contract.key(); expiry = timestamp(expires_at)
        if not isinstance(succeeded, bool): raise ValueError('explicit boolean success required')
        if expiry <= timestamp(self.now()): raise ValueError('expiry must be in future')
        with self.transaction() as db:
            db.execute('INSERT OR REPLACE INTO cache VALUES (?,?,?,?,?,?,?)',
                       (key, contract.privacy_partition, contract.source_id, contract.source_revision, expiry, int(succeeded), canonical(payload)))
    def get(self, contract: CacheContract):
        with self.connection() as db:
            row = db.execute('SELECT payload FROM cache WHERE key=? AND partition=? AND source_id=? AND revision=? AND expires>? AND succeeded=1',
                (contract.key(),contract.privacy_partition,contract.source_id,contract.source_revision,timestamp(self.now()))).fetchone()
            return None if row is None else json.loads(row[0])
    def invalidate_source(self, partition: str, source_id: str):
        if not partition or not source_id: raise ValueError('explicit scope required')
        with self.transaction() as db:
            return db.execute('DELETE FROM cache WHERE partition=? AND source_id=?',(partition,source_id)).rowcount
    def configure_budget(self, partition: str, dollars):
        if not partition: raise ValueError('explicit partition required')
        cap = micros(dollars)
        with self.transaction() as db:
            used=db.execute("SELECT COALESCE((SELECT spent FROM budgets WHERE partition=?),0)+COALESCE((SELECT SUM(amount) FROM reservations WHERE partition=? AND state='reserved'),0)",(partition,partition)).fetchone()[0]
            if cap < used: raise ValueError('cap cannot fall below spent plus reserved')
            db.execute('INSERT INTO budgets(partition,cap) VALUES (?,?) ON CONFLICT(partition) DO UPDATE SET cap=excluded.cap',(partition,cap))
    def reserve(self, partition: str, estimated_dollars) -> str:
        amount = micros(estimated_dollars)
        if amount <= 0: raise ValueError('positive bounded estimate required')
        with self.transaction() as db:
            budget=db.execute('SELECT cap,spent FROM budgets WHERE partition=?',(partition,)).fetchone()
            if budget is None: raise PermissionError('missing budget: fail closed')
            reserved=db.execute("SELECT COALESCE(SUM(amount),0) FROM reservations WHERE partition=? AND state='reserved'",(partition,)).fetchone()[0]
            if budget[1]+reserved+amount > budget[0]: raise PermissionError('budget exhausted')
            ident = str(uuid.uuid4())
            db.execute('INSERT INTO reservations VALUES (?,?,?,\'reserved\',NULL,?)',(ident,partition,amount,timestamp(self.now())))
            return ident
    def settle(self, reservation_id: str, actual_dollars):
        """Record actual cost even if estimate was exceeded; then future reservations fail closed."""
        actual=micros(actual_dollars)
        with self.transaction() as db:
            row=db.execute('SELECT partition,state,actual FROM reservations WHERE id=?',(reservation_id,)).fetchone()
            if row is None: raise KeyError('unknown reservation')
            if row[1]=='settled':
                if row[2]!=actual: raise ValueError('conflicting settlement')
                return
            if row[1]!='reserved': raise ValueError('reservation not active')
            db.execute('UPDATE budgets SET spent=spent+? WHERE partition=?',(actual,row[0]))
            db.execute("UPDATE reservations SET state='settled',actual=? WHERE id=?",(actual,reservation_id))
    def cancel_unstarted(self, reservation_id: str, *, execution_started: bool):
        if execution_started is not False: raise PermissionError('uncertain/started executions retain reservation until reconciliation')
        with self.transaction() as db:
            row=db.execute('SELECT state FROM reservations WHERE id=?',(reservation_id,)).fetchone()
            if row is None: raise KeyError('unknown reservation')
            if row[0]=='settled': raise ValueError('settled reservation cannot cancel')
            db.execute("UPDATE reservations SET state='cancelled' WHERE id=?",(reservation_id,))

@dataclass(frozen=True)
class Route:
    name: str
    provider: str
    capability: int
    estimated_cost: str
    privacy_partitions: frozenset[str]
    deterministic: bool = False
    enabled: bool = False

def select_route(routes: list[Route], *, required_capability: int, partition: str) -> Route:
    if isinstance(required_capability,bool) or not isinstance(required_capability,int) or required_capability<0 or not partition:
        raise ValueError('explicit nonnegative capability and partition required')
    eligible=[]
    for route in routes:
        if not isinstance(route.capability,int) or isinstance(route.capability,bool) or route.capability<0: raise ValueError('invalid route capability')
        cost=micros(route.estimated_cost)
        if route.enabled and route.capability >= required_capability and partition in route.privacy_partitions:
            eligible.append((0 if route.deterministic else 1,cost,route.capability,route.name,route))
    if not eligible: raise PermissionError('no authorized sufficient route')
    return min(eligible,key=lambda v:v[:4])[-1]

def run_bounded(command: list[str], *, deadline: dt.datetime, now=utcnow, grace_seconds=0.2) -> dict:
    """POSIX owned process group; stop descendants on timeout and after leader exit.
    No shell, no background survivors. Children escaping process groups require OS isolation.
    """
    if os.name!='posix': raise RuntimeError('POSIX process groups required')
    remaining=timestamp(deadline)-timestamp(now())
    if remaining <= 0: raise TimeoutError('deadline passed; no launch')
    if not command or not all(isinstance(x,str) for x in command): raise ValueError('explicit argv required')
    if not 0 <= grace_seconds <= 1: raise ValueError('grace outside bound')
    # Reserve cleanup time inside deadline. Do not start with too little time to stop safely.
    if remaining <= grace_seconds+0.05: raise TimeoutError('insufficient deadline margin')
    started=time.monotonic(); group=None; proc=None; timed_out=False; signal_errors=[]
    def send(sig):
        try: os.killpg(group,sig)
        except ProcessLookupError: pass
        except PermissionError as exc:
            signal_errors.append({'signal':int(sig),'error':str(exc)})
            # Never report group cleanup confirmed after an OS denial.
            if proc is not None and proc.poll() is None:
                proc.kill()
    def budget_left():
        return max(0,min(remaining-(time.monotonic()-started),timestamp(deadline)-timestamp(now())))
    reap_confirmed=False
    try:
        proc=subprocess.Popen(command,start_new_session=True,stdin=subprocess.DEVNULL,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        group=proc.pid
        while proc.poll() is None:
            budget=budget_left()
            if budget <= grace_seconds+0.05:
                timed_out=True; break
            time.sleep(min(0.02,budget-grace_seconds-0.05))
        send(signal.SIGTERM)
        # Preserve a 50ms reap margin inside the original deadline.
        cleanup=max(0,min(grace_seconds,budget_left()-0.05))
        if cleanup: time.sleep(cleanup)
    finally:
        if group is not None:
            send(signal.SIGKILL)
            if proc is not None:
                reap_confirmed=proc.poll() is not None
                reap_budget=budget_left()
                if not reap_confirmed and reap_budget>0:
                    try:
                        proc.wait(timeout=reap_budget)
                        reap_confirmed=True
                    except subprocess.TimeoutExpired: pass
    # Build receipt after every cleanup attempt; later denials cannot mutate it.
    return {'returncode':proc.returncode,'timed_out':timed_out,'process_group':group,
            'cleanup_attempted':True,'cleanup_confirmed':reap_confirmed and not signal_errors,
            'reap_confirmed':reap_confirmed,'signal_errors':list(signal_errors)}

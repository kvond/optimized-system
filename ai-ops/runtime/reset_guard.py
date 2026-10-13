"""Reset-only entrypoint; never schedule this after the fixed cutoff."""
import datetime as dt, sys, json
from foundation import run_bounded, UTC
DEADLINE=dt.datetime(2026,10,12,10,0,tzinfo=UTC)
if __name__=="__main__":
 if dt.datetime.now(UTC)>=DEADLINE: raise SystemExit("Reset deadline reached")
 if len(sys.argv)<2: print(int((DEADLINE-dt.datetime.now(UTC)).total_seconds()))
 else:
  result=run_bounded(sys.argv[1:],deadline=DEADLINE,grace_seconds=0.5)
  print(json.dumps(result))
  raise SystemExit(0 if result.get("returncode")==0 and result.get("cleanup_confirmed") else 1)

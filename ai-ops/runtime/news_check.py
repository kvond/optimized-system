"""Fixed public-feed packet; civic policy/trend synthesis remains explicit fallback.
No paid calls, private profiles, birthday/finance actions or schedule changes.
Socket timeout is not an absolute process deadline: external supervisor required.
"""
import argparse,datetime as dt,hashlib,json,os,sqlite3,multiprocessing as mp,threading,queue,time,signal
from pathlib import Path
from urllib.request import Request,build_opener,HTTPRedirectHandler
from urllib.parse import urlsplit
from zoneinfo import ZoneInfo
from news import Feed,Read,NewsGate,parse_feed,digest,stamp
from storage import resolve_storage
from worker_context import build_context
from shared_birthday import reuse_for_news

FEEDS=(
 ('major_world',Feed('bbc-world','https://feeds.bbci.co.uk/news/world/rss.xml',('www.bbc.com','www.bbc.co.uk')),2),
 ('major_us',Feed('bbc-us','https://feeds.bbci.co.uk/news/world/us_and_canada/rss.xml',('www.bbc.com','www.bbc.co.uk')),2),
 ('economy_markets',Feed('bbc-business','https://feeds.bbci.co.uk/news/business/rss.xml',('www.bbc.com','www.bbc.co.uk')),2),
 ('ai_research',Feed('mit-ai','https://news.mit.edu/topic/mitartificial-intelligence2-rss.xml',('news.mit.edu',)),1),
 ('education_research',Feed('mit-education','https://news.mit.edu/rss/topic/education',('news.mit.edu',)),1),
)
CIVIC=('https://news.delaware.gov/','https://legis.delaware.gov/')
ALLOWED={f.url for _,f,_ in FEEDS}|set(CIVIC)

class Redirect(HTTPRedirectHandler):
 def redirect_request(self,req,fp,code,msg,headers,newurl):
  if newurl not in ALLOWED or urlsplit(newurl).netloc!=urlsplit(req.full_url).netloc:raise ValueError('unapproved redirect')
  return super().redirect_request(req,fp,code,msg,headers,newurl)

def fetch(url):
 if url not in ALLOWED:raise ValueError('fixed approved source only')
 with build_opener(Redirect()).open(Request(url,headers={'User-Agent':'AI-ops public news metadata/1.0'}),timeout=8) as response:
  if response.geturl()!=url:raise ValueError('source URL changed')
  data=response.read(1_000_001)
  if len(data)>1_000_000:raise ValueError('source too large')
  return data

def collect(*,fetcher=fetch,now=None):
 now=stamp(now or dt.datetime.now(dt.timezone.utc));reads=[];evidence=[]
 for category,feed,limit in FEEDS:
  try:
   data=fetcher(feed.url);read=parse_feed(feed,data,now)
   reason=None
  except Exception:
   read=Read(feed,now,'failed-source',False,False,[]);reason='source_fetch_or_parse_failed'
  reads.append(read);evidence.append({'category':category,'source_url':feed.url,'feed_read_complete':read.complete,'reason':reason,'revision':read.revision,'observed_at':now.isoformat()})
 civic=[]
 for address in CIVIC:
  try:
   body=fetcher(address)
   civic.append({'source_url':address,'page_read':True,'sha256':hashlib.sha256(body).hexdigest(),'bytes':len(body),'policy_research_complete':False})
  except Exception:civic.append({'source_url':address,'page_read':False,'policy_research_complete':False})
 return reads,evidence,civic

def _collect_worker(send):
 try:
  os.setsid();send.send(collect())
 except BaseException:
  try:send.send(None)
  except OSError:pass
 finally:send.close()

def acquire(*,deadline=45,worker=_collect_worker,_context=None):
 if not 0<deadline<=45:raise ValueError('bounded acquisition deadline required')
 context=_context or mp.get_context('spawn');receive,send=context.Pipe(duplex=False)
 process=None;reader=None;started=False;result=None;clean=True;failure=None;mailbox=queue.Queue(maxsize=1)
 def read_pipe():
  try:mailbox.put(receive.recv())
  except (EOFError,OSError):mailbox.put(None)
 try:
  process=context.Process(target=worker,args=(send,));expires=time.monotonic()+deadline
  process.start();started=True;send.close();reader=threading.Thread(target=read_pipe,daemon=True);reader.start()
  try:result=mailbox.get(timeout=max(0,expires-time.monotonic()))
  except queue.Empty:pass
 except BaseException as exc:failure=exc
 finally:
  send.close()
  if process is not None and process.pid is not None:started=True
  if started:
   try:
    if process.is_alive():
     try:
      if os.getpgid(process.pid)==process.pid:os.killpg(process.pid,signal.SIGKILL)
      else:process.kill()
     except ProcessLookupError:pass
     except OSError:
      try:process.kill()
      except OSError:clean=False
   finally:
    try:process.join(timeout=2)
    except (AssertionError,OSError):clean=False
  try:
   if reader is not None:reader.join(timeout=2);clean=clean and not reader.is_alive()
  finally:receive.close()
  if started:clean=clean and not process.is_alive()
  if not clean:raise RuntimeError('owned news cleanup unconfirmed; no state write')
 if failure is not None:raise RuntimeError('news acquisition failed; no state write') from failure
 if result is None:raise RuntimeError('news acquisition timeout; no state write')
 return result

def check(request_id,*,paths=None,fetcher=fetch,now=None):
 if not isinstance(request_id,str) or not request_id.strip() or len(request_id)>300:raise ValueError('bounded request id required')
 paths=paths or resolve_storage(initialize=True)
 def verify():return resolve_storage(paths.root,mount=paths.proof['mount'],image=paths.proof['backing_image'],probe=paths.probe,environ={})
 verify();artifact=paths.receipts/('news-'+hashlib.sha256(request_id.encode()).hexdigest()+'.json')
 if artifact.exists():
  if artifact.is_symlink() or artifact.stat().st_mode&0o077:raise ValueError('unsafe existing packet')
  packet=json.loads(artifact.read_text());claimed=packet.pop('packet_sha256')
  if packet.get('request_id')!=request_id or digest(packet)!=claimed:raise ValueError('packet identity/hash mismatch')
  packet['packet_sha256']=claimed;return packet
 database=paths.root/'news.sqlite'
 if database.exists():
  if database.is_symlink() or database.stat().st_mode&0o077:raise ValueError('unsafe existing news state')
  with sqlite3.connect('file:'+str(database)+'?mode=ro',uri=True) as db:
   if db.execute('SELECT 1 FROM news_requests WHERE id=? LIMIT 1',(request_id,)).fetchone():raise ValueError('atomic component receipt lacks packet; explicit recovery required')
 now=stamp(now or dt.datetime.now(dt.timezone.utc));local=now.astimezone(ZoneInfo('America/New_York'))
 start=local.replace(hour=0,minute=0,second=0,microsecond=0);end=start+dt.timedelta(days=1)
 reads,evidence,civic=acquire() if fetcher is fetch else collect(fetcher=fetcher,now=now)
 if fetcher is fetch:now=dt.datetime.now(dt.timezone.utc)
 receipts=[];included=[];seen=set()
 for (category,feed,limit),read in zip(FEEDS,reads):
  gate=NewsGate(paths,sources=[feed],partition='daily-news-public-'+category,now=lambda:now,max_words=60,max_items=limit)
  result=gate.apply(request_id,[read],start=start,end=end);receipts.append({'category':category,'receipt':result})
  for article in result['included']:
   if article['url'] not in seen:included.append(article);seen.add(article['url'])
 packet={'request_id':request_id,'status':'partial','observed_at':now.isoformat(),'window':[start.isoformat(),end.isoformat()],
 'headlines':included,'headline_count':len(included),'max_headlines':8,'max_words':500,
 'digest':'\n'.join(a['title']+' '+a['url'] for a in included),'source_evidence':evidence,'civic_evidence':civic,'component_receipts':receipts,
 'coverage':{'feed_metadata':'complete' if all(r.complete for r in reads) else 'partial','major_news_completeness':'not_established','civic_policy_actions':'incomplete_requires_original_check','answerable_teaching_ai_book_trends':'requires_original_judgment'},
 'fallback_required':['original civic decisions/lawful action check','today importance and book-trend judgment','additional sources for incomplete feed categories'],
 'paid_calls':0,'finance_or_birthday_actions':False,'scheduled':False}
 packet['digest_words']=len(packet['digest'].split());packet['packet_sha256']=digest(packet)
 verify();fd=os.open(artifact,os.O_CREAT|os.O_EXCL|os.O_WRONLY|getattr(os,'O_NOFOLLOW',0),0o600)
 with os.fdopen(fd,'w') as f:f.write(json.dumps(packet,sort_keys=True,indent=2)+'\n');f.flush();os.fsync(f.fileno())
 verify()
 if json.loads(artifact.read_text())!=packet:raise ValueError('packet readback mismatch')
 return packet

def delivery(packet):
 out={k:packet[k] for k in ('request_id','status','headline_count','digest_words','packet_sha256','coverage','paid_calls','headlines','digest','fallback_required','source_evidence','civic_evidence')}
 try:
  context=build_context('news')
  if context['context_words']>400 or context['context_words']!=len(context['context'].split()) or hashlib.sha256(context['context'].encode()).hexdigest()!=context['context_sha256']:raise ValueError('context verification mismatch')
  out['compact_context']={k:context[k] for k in ('context','context_words','context_sha256','manifest_sha256','provenance_fingerprint')}
  out['compact_context_status']='verified'
 except (ValueError,PermissionError,OSError,KeyError,UnicodeError):
  out['compact_context_status']='held_original_task_context_required'
 out['delivery_sha256']=digest(out)
 return out

def acknowledge(request_id,output_path,*,paths=None):
 """Output JSON: request_id, packet_sha256, digest, final_brief (actual final text).
 This acknowledges local private persistence only, never cloud/user display.
 """
 paths=paths or resolve_storage()
 artifact=paths.receipts/('news-'+hashlib.sha256(request_id.encode()).hexdigest()+'.json')
 if artifact.is_symlink() or not artifact.is_file() or artifact.stat().st_mode&0o077:raise ValueError('prepared packet unavailable')
 packet=json.loads(artifact.read_text());metadata=dict(packet);claimed=metadata.pop('packet_sha256')
 if packet.get('request_id')!=request_id or digest(metadata)!=claimed:raise ValueError('prepared packet hash mismatch')
 start,end=[dt.datetime.fromisoformat(x) for x in packet['window']];proofs=[]
 for category,feed,limit in FEEDS:
  component=next(c['receipt'] for c in packet['component_receipts'] if c['category']==category)
  if component['status']=='complete' and component['included']:
   gate=NewsGate(paths,sources=[feed],partition='daily-news-public-'+category,max_words=60,max_items=limit)
   proofs.append(gate.acknowledge_local_output(request_id,start=start,end=end,output_path=output_path,packet=packet))
 if not proofs:raise ValueError('no delivered headlines to acknowledge')
 return {'request_id':request_id,'local_output_readback_verified':True,'output_sha256':proofs[0]['local_output_sha256'],'acknowledged_components':len(proofs),'cloud_delivery_verified':False,'paid_calls':0}

def main():
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--request-id',required=True);parser.add_argument('--acknowledge-output',type=Path,help='separate private JSON: request_id, packet_sha256, digest, final_brief');args=parser.parse_args()
 try:
  if args.acknowledge_output:
   print(json.dumps(acknowledge(args.request_id,args.acknowledge_output),sort_keys=True));return 0
  packet=check(args.request_id)
  output=delivery(packet)
  try: output['birthday_source_reuse']=reuse_for_news(args.request_id)
  except Exception:
   output['birthday_source_reuse']={'status':'hold','counts':None,'duplicate_source_read_skipped':False,
                                  'reason':'fresh_complete_scoped_birthday_evidence_unavailable','ai_calls':0}
  output['execution_notes']={'fresh_run_id':'Use actual UTC run time as request ID; retain it for completion/readback.',
     'birthday_refresh':'Reuse only verified current-business-date evidence; otherwise refresh original Calendar/Todoist sources once using /Volumes/T7/AI-Archive/ops/birthday-refresh.md. Preserve original family,21-day,7-day and cart rules.',
     'delivery_deduplication':'Prepared is not delivered. Read back the actual prior briefing before capturing its exact final text privately and acknowledging its matching packet using --acknowledge-output. Unacknowledged headlines remain eligible.',
     'scope':'Original civic decisions/actions, importance and AI/book judgment remain required; feed metadata alone is partial. Keep original destinations and schedules.'}
  output['delivery_sha256']=digest({k:v for k,v in output.items() if k!='delivery_sha256'})
  print(json.dumps(output,sort_keys=True));return 0
 except Exception:print(json.dumps({'status':'failed_closed','paid_calls':0}));return 2
if __name__=='__main__':raise SystemExit(main())

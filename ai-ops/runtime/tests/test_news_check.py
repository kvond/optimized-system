import sys,unittest,tempfile,datetime as dt,hashlib,json
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).parents[1]))
import news_check as cli
from storage import resolve_storage
class NewsCheckTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);b=Path(self.tmp.name).resolve();m=b/'mount';m.mkdir();i=b/'image';i.mkdir()
  def probe(m,i):return {'mount':str(m),'backing_image':str(i),'filesystem':'apfs','mount_verified':True,'encryption_verified':True}
  self.paths=resolve_storage(m/'state',mount=m,image=i,initialize=True,probe=probe,environ={});self.now=dt.datetime(2026,10,12,23,tzinfo=dt.timezone.utc)
 def fetch(self,url):
  if url in cli.CIVIC:return b'<html>Current official page</html>'
  f=next(f for _,f,_ in cli.FEEDS if f.url==url);origin=f.article_origins[0]
  return ('<rss><channel><title>Official feed</title>'+''.join(f'<item><title>Headline {j} {f.source_id}</title><link>https://{origin}/{f.source_id}/{j}</link><pubDate>Mon, 12 Oct 2026 12:00:00 GMT</pubDate></item>' for j in range(5))+'</channel></rss>').encode()
 def test_bounded_packet_repeat_no_network_civic_incomplete(self):
  r=cli.check('first',paths=self.paths,fetcher=self.fetch,now=self.now)
  self.assertLessEqual(r['headline_count'],8);self.assertLessEqual(r['digest_words'],500)
  self.assertEqual(r['coverage']['civic_policy_actions'],'incomplete_requires_original_check');self.assertTrue(all(x['page_read'] for x in r['civic_evidence']))
  def forbidden(u):raise AssertionError('no refetch')
  self.assertEqual(r,cli.check('first',paths=self.paths,fetcher=forbidden,now=self.now))
  repeat=cli.check('second',paths=self.paths,fetcher=self.fetch,now=self.now)
  self.assertTrue(all(x['receipt']['counts']['unchanged']==0 for x in repeat['component_receipts']));self.assertEqual(r['headlines'],repeat['headlines'])
 def test_owned_worker_timeout_cleans_and_no_write(self):
  import time,os
  def hung(send):os.setsid();time.sleep(10)
  started=time.monotonic()
  with self.assertRaises(RuntimeError):cli.acquire(deadline=.1,worker=hung,_context=__import__('multiprocessing').get_context('fork'))
  self.assertLess(time.monotonic()-started,5);self.assertFalse((self.paths.root/'news.sqlite').exists())
 def test_partial_pipe_frame_is_bounded(self):
  import time,os,struct,multiprocessing as mp
  def partial(send):os.setsid();os.write(send.fileno(),struct.pack('!i',100000)+b'x');time.sleep(10)
  started=time.monotonic()
  with self.assertRaises(RuntimeError):cli.acquire(deadline=.1,worker=partial,_context=mp.get_context('fork'))
  self.assertLess(time.monotonic()-started,5)
 def test_ack_real_local_output_then_revision_dedupe(self):
  packet=cli.check('deliver',paths=self.paths,fetcher=self.fetch,now=self.now)
  out=self.paths.receipts/'actual-final-brief.json';out.write_text(json.dumps({'request_id':'deliver','packet_sha256':packet['packet_sha256'],'digest':packet['digest'],'final_brief':packet['digest']}));out.chmod(0o600)
  ack=cli.acknowledge('deliver',out,paths=self.paths);self.assertTrue(ack['local_output_readback_verified']);self.assertFalse(ack['cloud_delivery_verified'])
  repeat=cli.check('after',paths=self.paths,fetcher=self.fetch,now=self.now)
  self.assertTrue(all(c['receipt']['counts']['unchanged']>=1 for c in repeat['component_receipts']))
 def test_ack_rejects_prepared_packet_and_missing_final_urls(self):
  packet=cli.check('bad-ack',paths=self.paths,fetcher=self.fetch,now=self.now)
  original=next(self.paths.receipts.glob('news-*'))
  with self.assertRaises(ValueError):cli.acknowledge('bad-ack',original,paths=self.paths)
  out=self.paths.receipts/'unverified-output.json';out.write_text(json.dumps({'request_id':'bad-ack','packet_sha256':packet['packet_sha256'],'digest':packet['digest'],'final_brief':'not rendered'}));out.chmod(0o600)
  with self.assertRaises(ValueError):cli.acknowledge('bad-ack',out,paths=self.paths)
 def test_long_titles_cannot_overflow_packet_bound(self):
  def long(u):return self.fetch(u).replace(b'Headline',(' '.join(['long']*120)).encode())
  packet=cli.check('long',paths=self.paths,fetcher=long,now=self.now)
  self.assertLessEqual(packet['digest_words'],500);self.assertLessEqual(packet['headline_count'],8)
 def test_partial_feed_no_zero_claim(self):
  failed=cli.FEEDS[0][1].url
  def fetch(u):
   if u==failed:raise TimeoutError()
   return self.fetch(u)
  r=cli.check('partial',paths=self.paths,fetcher=fetch,now=self.now)
  self.assertEqual(r['coverage']['feed_metadata'],'partial');self.assertIsNone(r['component_receipts'][0]['receipt']['counts']);self.assertTrue(r['headline_count']>0)
 def test_redirect_and_unknown_url_rejected_before_network(self):
  with self.assertRaises(ValueError):cli.fetch('https://evil.example/feed')
  from urllib.request import Request
  with self.assertRaises(ValueError):cli.Redirect().redirect_request(Request(cli.FEEDS[0][1].url),None,302,'redirect',{},'https://evil.example/feed')
 def test_context_hash_checked_and_no_fake_context(self):
  p=cli.check('context',paths=self.paths,fetcher=self.fetch,now=self.now)
  c={'context':'reviewed context','context_words':2,'context_sha256':hashlib.sha256(b'reviewed context').hexdigest(),'manifest_sha256':'a'*64,'provenance_fingerprint':'b'*64}
  with patch.object(cli,'build_context',return_value=c):self.assertEqual(cli.delivery(p)['compact_context_status'],'verified')
  c['context_sha256']='c'*64
  with patch.object(cli,'build_context',return_value=c):self.assertNotIn('compact_context',cli.delivery(p))
 def test_missing_packet_does_not_refetch_uncertain_components(self):
  cli.check('gap',paths=self.paths,fetcher=self.fetch,now=self.now)
  next(self.paths.receipts.glob('news-*')).unlink()
  with patch.object(cli,'collect',side_effect=AssertionError('no refetch')):
   with self.assertRaises(ValueError):cli.check('gap',paths=self.paths,fetcher=self.fetch,now=self.now)
 def test_tampered_packet_readback_rejected(self):
  cli.check('tamper',paths=self.paths,fetcher=self.fetch,now=self.now)
  p=next(self.paths.receipts.glob('news-*'));p.write_text(p.read_text().replace('Headline','Altered'))
  with self.assertRaises(ValueError):cli.check('tamper',paths=self.paths,fetcher=self.fetch,now=self.now)
if __name__=='__main__':unittest.main()

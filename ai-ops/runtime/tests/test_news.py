import sys,tempfile,unittest,datetime as dt
from pathlib import Path
import json
sys.path.insert(0,str(Path(__file__).parents[1]))
from news import Feed,Read,NewsGate,parse_feed
from storage import resolve_storage

class NewsTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
  b=Path(self.tmp.name).resolve();m=b/'mount';m.mkdir();i=b/'image';i.mkdir()
  self.proof=lambda m,i:{'mount':str(m),'backing_image':str(i),'filesystem':'apfs','mount_verified':True,'encryption_verified':True}
  self.paths=resolve_storage(m/'state',mount=m,image=i,initialize=True,probe=self.proof,environ={})
  self.now=dt.datetime(2026,10,12,18,tzinfo=dt.timezone.utc);self.start=self.now-dt.timedelta(hours=12)
  self.feed=Feed('approved','https://example.org/feed',('example.org',))
  self.gate=NewsGate(self.paths,sources=[self.feed],partition='personal-news',now=lambda:self.now,max_words=20)
 def read(self,title='Public headline',link='https://example.org/article?utm_source=x',observed=None):
  body=f'<rss><channel><title>Example</title><item><title>{title}</title><link>{link.replace("&","&amp;")}</link><pubDate>Mon, 12 Oct 2026 12:00:00 +0000</pubDate><description>Public description</description></item></channel></rss>'.encode()
  return parse_feed(self.feed,body,observed or self.now)
 def apply(self,id,reads,gate=None):return (gate or self.gate).apply(id,reads,start=self.start,end=self.now)
 def ack(self,id,receipt,gate=None):
  g=gate or self.gate;p=self.paths.receipts/('delivered-'+id+'.json');p.write_text(json.dumps({'request_id':id,'result_sha256':receipt['result_sha256'],'digest':receipt['digest']}));p.chmod(0o600)
  return g.acknowledge_local_output(id,start=self.start,end=self.now,output_path=p)
 def test_canonical_dedupe_and_changed_revision(self):
  a=self.apply('a',[self.read()]);self.assertEqual(a['counts']['changed_or_new'],1);self.ack('a',a)
  b=self.apply('b',[self.read(link='https://example.org/article?fbclid=foo')]);self.assertEqual(b['counts']['unchanged'],1);self.assertEqual(b['digest'],'')
  c=self.apply('c',[self.read(title='Updated title')]);self.assertEqual(c['counts']['changed_or_new'],1)
 def test_missing_stale_failed_never_zero_and_preserve(self):
  seed=self.apply('seed',[self.read()]);self.ack('seed',seed)
  missing=self.apply('missing',[]);self.assertEqual(missing['status'],'blocked');self.assertIsNone(missing['counts'])
  stale=self.apply('stale',[self.read(observed=self.now-dt.timedelta(minutes=6))]);self.assertEqual(stale['status'],'blocked')
  bad=Read(self.feed,self.now,'failure',False,False,[]);self.assertIsNone(self.apply('failed',[bad])['counts'])
  self.assertEqual(self.apply('fresh',[self.read()])['counts']['unchanged'],1)
 def test_idempotent_receipt_conflict(self):
  r=self.read();a=self.apply('same',[r]);self.assertEqual(a,self.apply('same',[r]))
  with self.assertRaises(ValueError):self.apply('same',[self.read(title='Changed')])
 def test_expired_source_cannot_reuse_success(self):
  r=self.read();self.apply('same',[r]);self.now+=dt.timedelta(minutes=6)
  # Preserve identical day window to test actual prior receipt freshness check.
  with self.assertRaises(ValueError):self.gate.apply('same',[r],start=self.start,end=self.now-dt.timedelta(minutes=6))
 def test_prepared_is_not_delivered(self):
  self.apply('prepared',[self.read()]);again=self.apply('next',[self.read()])
  self.assertEqual(again['counts']['unchanged'],0);self.assertEqual(len(again['included']),1)
 def test_ack_requires_actual_separate_readback(self):
  r=self.apply('a',[self.read()]);p=self.paths.receipts/'bad.json';p.write_text('{}');p.chmod(0o600)
  with self.assertRaises(ValueError):self.gate.acknowledge_local_output('a',start=self.start,end=self.now,output_path=p)
  proof=self.ack('a',r);self.assertTrue(proof['local_output_readback_verified']);self.assertFalse(proof['cloud_delivery_verified'])
 def test_partition_isolation(self):
  self.apply('seed',[self.read()]);g=NewsGate(self.paths,sources=[self.feed],partition='other',now=lambda:self.now,max_words=20)
  self.assertEqual(self.apply('seed',[self.read()],g)['counts']['changed_or_new'],1)
 def test_window_excludes_old_and_future(self):
  r=self.read();r.articles[0]['published_at']=(self.start-dt.timedelta(days=1)).isoformat()
  self.assertEqual(self.apply('old',[r])['counts']['eligible'],0)
 def test_bound_omission_not_silently_consumed(self):
  r=self.read(title='one two three four five six seven eight nine ten eleven twelve')
  other=dict(r.articles[0],url='https://example.org/z',title='another headline',revision='second');r.articles.append(other)
  a=self.apply('a',[r]);self.assertLessEqual(a['digest_words'],20)
  # Tight total forces one omission, then next fresh request delivers it.
  r.articles[1]['title']='a b c d e f g h i j k l m n o'
  g=NewsGate(self.paths,sources=[self.feed],partition='bounds',now=lambda:self.now,max_words=20)
  a=self.apply('one',[r],g);self.assertEqual(a['omitted_from_digest'],1);self.ack('one',a,g)
  b=self.apply('two',[r],g);self.assertEqual(len(b['included']),1)
 def test_parser_rejects_untrusted_origin_dates_entities(self):
  with self.assertRaises(ValueError):self.read(link='https://evil.org/article')
  with self.assertRaises(ValueError):parse_feed(self.feed,b'<!DOCTYPE rss><rss/>',self.now)
  with self.assertRaises(ValueError):parse_feed(self.feed,b'<rss><channel><title>A</title><item><title>A</title><link>https://example.org/a</link></item></channel></rss>',self.now)
 def test_ejection_prevents_write(self):
  from unittest.mock import patch
  with patch.object(self.gate,'verify',side_effect=RuntimeError('ejected')):
   with self.assertRaises(RuntimeError):self.apply('eject',[self.read()])
 def test_fresh_complete_empty_explicit(self):
  r=parse_feed(self.feed,b'<rss><channel><title>Approved feed</title></channel></rss>',self.now)
  self.assertEqual(self.apply('empty',[r])['counts']['eligible'],0)
if __name__=='__main__':unittest.main()

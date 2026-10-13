"""Deterministic approved-feed article gate. No AI, schedules or network calls.
Callers provide bounded public feed bytes and explicit source/window evidence.
"""
from dataclasses import dataclass
import datetime as dt
import hashlib,json,re,sqlite3,os
from urllib.parse import urlsplit,urlunsplit,parse_qsl,urlencode
from xml.etree import ElementTree as ET
from email.utils import parsedate_to_datetime
from foundation import Store,canonical,utcnow
from storage import RuntimePaths,resolve_storage,StorageError

@dataclass(frozen=True)
class Feed:
    source_id: str
    url: str
    article_origins: tuple

@dataclass(frozen=True)
class Read:
    source: Feed
    observed_at: dt.datetime
    revision: str
    available: bool
    complete: bool
    articles: list

def stamp(value):
    if not isinstance(value,dt.datetime) or value.tzinfo is None or value.utcoffset() is None:raise ValueError('aware timestamp required')
    return value.astimezone(dt.timezone.utc)

def url(value):
    u=urlsplit(value)
    if u.scheme!='https' or not u.hostname or u.username or u.password or '\\' in u.netloc or any(c.isspace() for c in value):raise ValueError('public HTTPS URL required')
    pairs=[(k,v) for k,v in parse_qsl(u.query,keep_blank_values=True) if not k.lower().startswith('utm_') and k.lower() not in ('fbclid','gclid')]
    return urlunsplit(('https',u.netloc.lower(),u.path or '/',urlencode(sorted(pairs)),''))

def digest(x):return hashlib.sha256(canonical(x).encode()).hexdigest()
def text(x):return ' '.join(re.sub('<[^>]*>',' ',x or '').split())

def parse_feed(feed,body,observed_at):
    """Parse bounded RSS/Atom; malformed/date-less items hold entire source."""
    stamp(observed_at)
    if not isinstance(body,bytes) or len(body)>1_000_000 or b'<!DOCTYPE' in body.upper() or b'<!ENTITY' in body.upper():raise ValueError('bounded XML without declarations required')
    root=ET.fromstring(body)
    def local(tag):return tag.rsplit('}',1)[-1]
    if local(root.tag) not in ('rss','feed'):raise ValueError('RSS/Atom required')
    if local(root.tag)=='rss' and not any(local(e.tag)=='channel' for e in root):raise ValueError('RSS channel required')
    if not any(local(e.tag)=='title' and text(e.text) for e in root.iter()):raise ValueError('feed identity required')
    items=[e for e in root.iter() if local(e.tag) in ('item','entry')]
    if len(items)>500:raise ValueError('article limit exceeded')
    records=[]
    for item in items:
        fields={};links=[]
        for child in item:
            key=local(child.tag)
            if key=='link':links.append(child.attrib.get('href') or child.text or '')
            else:fields[key]=child.text or ''
        title=text(fields.get('title'))
        date=fields.get('pubDate') or fields.get('published') or fields.get('updated')
        try:
            published=dt.datetime.fromisoformat(date.replace('Z','+00:00')) if re.match(r'^\d{4}-\d{2}-\d{2}T',date) else parsedate_to_datetime(date)
            published=stamp(published)
        except (ValueError,TypeError,AttributeError):raise ValueError('genuine publication timestamp required')
        article=url(next((v for v in links if v.startswith('https://')), ''))
        if urlsplit(article).netloc not in feed.article_origins or not title or len(title)>1000:raise ValueError('approved article/title required')
        summary=text(fields.get('description') or fields.get('summary'))[:3000]
        records.append({'url':article,'title':title,'published_at':published.isoformat(),'summary':summary,'revision':digest([title,summary,published.isoformat()])})
    return Read(feed,observed_at,hashlib.sha256(body).hexdigest(),True,True,records)

class NewsGate:
    def __init__(self,paths,*,sources,partition,now=utcnow,max_age=300,max_words=500,max_items=8):
        if not isinstance(paths,RuntimePaths) or not sources or not isinstance(partition,str) or not partition.strip():raise ValueError('verified paths/explicit sources/partition required')
        if type(max_age)is not int or max_age<=0 or type(max_words)is not int or max_words<20:raise ValueError('positive freshness/word bounds required')
        self.paths=paths;self.sources={s.source_id:s for s in sources};self.partition=partition;self.now=now;self.max_age=max_age;self.max_words=max_words;self.max_items=max_items
        if len(self.sources)!=len(sources):raise ValueError('duplicate source identity')
        for s in sources:
            if not s.source_id or url(s.url)!=s.url or not s.article_origins:raise ValueError('explicit canonical feed required')
        if type(max_items)is not int or not 0<max_items<=8:raise ValueError('bounded headline count required')
        self.verify();p=paths.root/'news.sqlite'
        if p.is_symlink() or p.exists() and (not p.is_file() or p.stat().st_mode&0o077):raise StorageError('unsafe existing news database')
        self.store=Store(p,now=now)
        with self.store.connection() as db:db.executescript('''CREATE TABLE IF NOT EXISTS news_requests(scope TEXT,id TEXT,input TEXT,receipt TEXT,PRIMARY KEY(scope,id));CREATE TABLE IF NOT EXISTS news_seen(scope TEXT,url TEXT,revision TEXT,published TEXT,PRIMARY KEY(scope,url));CREATE TABLE IF NOT EXISTS news_delivery(scope TEXT,url TEXT,revision TEXT,output_sha TEXT,PRIMARY KEY(scope,url,revision));''')
    def verify(self):
        resolve_storage(self.paths.root,mount=self.paths.proof['mount'],image=self.paths.proof['backing_image'],probe=self.paths.probe,environ={})
    def apply(self,request_id,reads,*,start,end):
        if not isinstance(request_id,str) or not request_id.strip() or len(request_id)>300:raise ValueError('request identity required')
        start=stamp(start);end=stamp(end);now=stamp(self.now())
        if start>=end or start>now or (end-start).total_seconds()>172800:raise ValueError('explicit bounded day window required')
        scope=digest([self.partition,[self.sources[k].__dict__ for k in sorted(self.sources)],start.isoformat(),end.isoformat(),self.max_words,self.max_items])
        material=[];issue=None;seen_sources=set();articles={}
        for r in reads:
            if not isinstance(r,Read) or self.sources.get(r.source.source_id)!=r.source or r.source.source_id in seen_sources:raise ValueError('exact unique approved sources required')
            seen_sources.add(r.source.source_id)
            if not isinstance(r.revision,str) or not r.revision or not isinstance(r.articles,list) or len(r.articles)>500:raise ValueError('bounded source revision/records required')
            age=(now-stamp(r.observed_at)).total_seconds()
            if any(type(v)is not bool for v in (r.available,r.complete)):raise ValueError('real coverage booleans required')
            material.append([r.source.source_id,r.revision,r.observed_at.isoformat(),r.available,r.complete,r.articles])
            if not r.available or not r.complete or age<0 or age>self.max_age:issue='source_unavailable_incomplete_or_stale'
            for a in r.articles:
                if not isinstance(a,dict) or not isinstance(a.get('title'),str) or len(a['title'])>1000 or not isinstance(a.get('revision'),str):raise ValueError('bounded public article metadata required')
                link=url(a['url']);pub=stamp(dt.datetime.fromisoformat(a['published_at']))
                if urlsplit(link).netloc not in r.source.article_origins or not a['title'] or not a['revision']:raise ValueError('invalid article metadata')
                if start<=pub<end and pub<=now:
                    if link in articles and articles[link]['revision']!=a['revision']:issue='conflicting_article_revisions'
                    articles[link]=dict(a,url=link)
        if seen_sources!=set(self.sources):issue='required_source_missing'
        identity=digest(material);self.verify()
        with self.store.connection() as db:
            db.execute('BEGIN IMMEDIATE')
            prior=db.execute('SELECT input,receipt FROM news_requests WHERE scope=? AND id=?',(scope,request_id)).fetchone()
            if prior:
                if issue:raise ValueError('prior receipt cannot mask stale/incomplete source evidence')
                if prior[0]!=identity:raise ValueError('conflicting request identity')
                return json.loads(prior[1])
            rows=[];unchanged=0
            if not issue:
                for link,a in sorted(articles.items()):
                    old=db.execute('SELECT revision FROM news_delivery WHERE scope=? AND url=? AND revision=?',(scope,link,a['revision'])).fetchone()
                    if old and old[0]==a['revision']:unchanged+=1;continue
                    rows.append(a)

            words=[];included=[]
            rows.sort(key=lambda a:(a['published_at'],a['url']),reverse=True)
            for a in rows:
                if len(included)>=self.max_items:break
                # Deterministic headline metadata digest; no invented commentary.
                line=(a['title']+' '+a['url']).split()
                if len(line)>self.max_words:line=a['title'].split()[:self.max_words-2]+['[truncated]',a['url']]
                if len(words)+len(line)>self.max_words:continue
                words.extend(line);included.append({'title':' '.join(line[:-1]),'url':a['url'],'revision':a['revision']})
                db.execute('INSERT OR REPLACE INTO news_seen VALUES(?,?,?,?)',(scope,a['url'],a['revision'],a['published_at']))
            receipt={'request_id':request_id,'status':'blocked' if issue else 'complete','reason':issue,'coverage':'all_approved_sources' if not issue else 'partial_or_unverified','counts':None if issue else {'eligible':len(articles),'unchanged':unchanged,'pending_or_changed':len(rows),'changed_or_new':len(rows)},'digest':' '.join(words),'digest_words':len(words),'included':included,'omitted_from_digest':None if issue else len(rows)-len(included),'window':[start.isoformat(),end.isoformat()],'paid_calls':0,'candidate_or_finance_or_birthday_actions':False,'delivery_acknowledged':False,'dedupe_basis':'verified_local_output_readback_only'}
            receipt['result_sha256']=digest(receipt)
            self.verify();db.execute('INSERT INTO news_requests VALUES(?,?,?,?)',(scope,request_id,identity,canonical(receipt)))
            db.commit()
            return receipt

    def acknowledge_local_output(self,request_id,*,start,end,output_path,packet=None):
        """Acknowledge only actual private output bytes, never a caller success flag.
        This establishes local output persistence, not cloud/chat delivery.
        """
        self.verify();p=__import__('pathlib').Path(output_path)
        if not p.is_absolute() or self.paths.receipts not in p.parents or any(x.is_symlink() for x in [p,*p.parents]) or not p.is_file() or p.stat().st_mode&0o077 or p.name.startswith('news-'):raise ValueError('separate private destination output required')
        if p.stat().st_size>100000:raise ValueError('bounded output required')
        raw=p.read_bytes();out=json.loads(raw)
        scope=digest([self.partition,[self.sources[k].__dict__ for k in sorted(self.sources)],stamp(start).isoformat(),stamp(end).isoformat(),self.max_words,self.max_items])
        with self.store.connection() as db:
            db.execute('BEGIN IMMEDIATE')
            prior=db.execute('SELECT receipt FROM news_requests WHERE scope=? AND id=?',(scope,request_id)).fetchone()
            if not prior:raise ValueError('prepared request missing')
            receipt=json.loads(prior[0])
            if packet is None:
                matched=out.get('result_sha256')==receipt['result_sha256'] and out.get('digest')==receipt['digest']
            else:
                metadata=dict(packet);packet_sha=metadata.pop('packet_sha256',None)
                matched=digest(metadata)==packet_sha and out.get('packet_sha256')==packet_sha and out.get('digest')==packet.get('digest') and isinstance(out.get('final_brief'),str) and all(a['url'] in out['final_brief'] for a in packet['headlines']) and any(c['receipt']==receipt for c in packet['component_receipts'])
            if receipt['status']!='complete' or out.get('request_id')!=request_id or not matched or not receipt['included']:raise ValueError('actual output must match prepared digest')
            for a in receipt['included']:
                record=db.execute('SELECT revision FROM news_seen WHERE scope=? AND url=?',(scope,a['url'])).fetchone()
                # Bind to revision saved in this request, not a later updated article.
                if record is None:raise ValueError('prepared article missing')
                db.execute('INSERT OR IGNORE INTO news_delivery VALUES(?,?,?,?)',(scope,a['url'],a['revision'],hashlib.sha256(raw).hexdigest()))
            self.verify()
            if p.read_bytes()!=raw:raise ValueError('output changed during readback')
            db.commit()
        return {'request_id':request_id,'local_output_sha256':hashlib.sha256(raw).hexdigest(),'local_output_readback_verified':True,'cloud_delivery_verified':False}

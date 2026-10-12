"""Bounded ordinary HTTP reader for the explicitly approved DOE Frontline filter.
No candidate matching, schedules, model calls, JavaScript execution or guessed endpoints.
"""
from __future__ import annotations
from dataclasses import dataclass
import datetime as dt
import hashlib
from html.parser import HTMLParser
import re
from urllib.parse import urljoin, urlsplit
from urllib.request import Request
from vacancies import Grant, SourceRead

SOURCE_URL = 'https://www.applitrack.com/joindelawareschools/onlineapp/default.aspx?AppliTrackPostingSearch=location%3A%22Delaware+Department+of+Education%22'
ORIGIN = 'https://www.applitrack.com'
LOCATION = 'Delaware Department of Education'
GRANT = Grant('public-doe-listings', 'delaware-doe', SOURCE_URL,
              'DOE-exact-location-filter-v1', ORIGIN, requires_authentication=False)
MAX_BYTES = 1_000_000
TIMEOUT = 20

class IncompleteSource(ValueError):
    pass

class PostingParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.text=[];self.titles=[];self.descriptions={};self.title=None
        self.description=None;self.span_depth=0;self.target_depth=0
    def handle_starttag(self, tag, attrs):
        attrs=dict(attrs)
        if tag=='td' and attrs.get('id')=='wrapword':
            if self.title is not None:raise IncompleteSource('nested title')
            self.title=[]
        if tag=='span':
            self.span_depth+=1
            match=re.fullmatch(r'DescriptionText(\d+)_\d+',attrs.get('id',''))
            if match:
                if self.description is not None or match[1] in self.descriptions:raise IncompleteSource('duplicate/nested description')
                self.description=(match[1],[]);self.target_depth=self.span_depth
        if tag in ('p','br','li','div','tr'):
            self.handle_data(' ')
    def handle_endtag(self,tag):
        if tag=='td' and self.title is not None:
            self.titles.append(' '.join(''.join(self.title).split()));self.title=None
        if tag=='span':
            if self.description is not None and self.span_depth==self.target_depth:
                key,parts=self.description;self.descriptions[key]=' '.join(''.join(parts).split());self.description=None
            self.span_depth-=1
        if tag in ('p','li','div','tr'):self.handle_data(' ')
    def handle_data(self,data):
        self.text.append(data)
        if self.title is not None:self.title.append(data)
        if self.description is not None:self.description[1].append(data)

def decode_literal(value):
    # Only HTML literals are decoded; never execute downloaded JavaScript.
    def sub(m):
        c=m[1]
        if c not in "'\\\"/nrt":raise IncompleteSource('unsupported literal escape')
        return {'n':'\n','r':'\r','t':'\t'}.get(c,c)
    return re.sub(r'\\(.)',sub,value)

def parse_output(body):
    if not isinstance(body,bytes) or len(body)>MAX_BYTES:raise IncompleteSource('bounded bytes required')
    try:script=body.decode('utf-8')
    except UnicodeDecodeError:raise IncompleteSource('invalid UTF-8') from None
    calls=re.findall(r"document\.write\('((?:\\.|[^'\\])*)'\);",script)
    if not calls:raise IncompleteSource('posting literals absent; metadata-only response')
    html=''.join(decode_literal(s) for s in calls)
    if not html.startswith("<div id='AppliTrackOutput'>") or not html.endswith('</form></div>'):
        raise IncompleteSource('truncated posting document')
    parser=PostingParser();parser.feed(html);parser.close()
    text=' '.join(''.join(parser.text).split())
    count=re.search(r'Having location:"([^"]+)"\s*\((\d+) openings\)',text)
    if not count or count[1]!=LOCATION:raise IncompleteSource('exact filter/count missing')
    ids=re.findall(r'JobID:\s*(\d+)',text);expected=int(count[2])
    if expected>100 or len(ids)!=expected or len(set(ids))!=expected or len(parser.titles)!=expected or set(parser.descriptions)!=set(ids) or parser.description is not None:
        raise IncompleteSource('posting count/ID/title/description mismatch')
    records=[]
    for key,title in zip(ids,parser.titles):
        description=parser.descriptions[key]
        if not title or len(title)>20000 or len(description)<100 or len(description)>20000:
            raise IncompleteSource('missing or unbounded posting description')
        records.append({'vacancy_id':key,'official_url':urljoin(SOURCE_URL,'default.aspx?AppliTrackJobID='+key),
                        'fields':{'title':title,'location':LOCATION,'description':description}})
    return records

def fetch_public(url):
    if urlsplit(url).netloc!='www.applitrack.com' or urlsplit(url).scheme!='https':raise IncompleteSource('source origin rejected')
    # Reject cross-origin redirects before sending a follow-up request.
    from urllib.request import HTTPRedirectHandler, build_opener
    class SameOrigin(HTTPRedirectHandler):
        def redirect_request(self,req,fp,code,msg,headers,newurl):
            target=urlsplit(newurl)
            if target.scheme!='https' or target.netloc!='www.applitrack.com':raise IncompleteSource('cross-origin redirect')
            return super().redirect_request(req,fp,code,msg,headers,newurl)
    with build_opener(SameOrigin()).open(Request(url,headers={'User-Agent':'AI-Ops-Public-Source-Reader/1.0'}),timeout=TIMEOUT) as response:
        if response.status!=200:raise IncompleteSource('source HTTP unavailable')
        body=response.read(MAX_BYTES+1)
        if len(body)>MAX_BYTES:raise IncompleteSource('response size limit')
        return body

@dataclass(frozen=True)
class AdapterResult:
    read: SourceRead
    reason: str | None
    evidence: dict

def read_source(*,fetch=fetch_public,now=lambda:dt.datetime.now(dt.timezone.utc)):
    observed=now();evidence={'source_url':SOURCE_URL,'coverage_id':GRANT.coverage_id,'anonymous_public_read':True,'model_calls':0}
    shell=None;output=None
    try:
        shell=fetch(SOURCE_URL)
        if len(shell)>MAX_BYTES:raise IncompleteSource('shell size limit')
        text=shell.decode('utf-8')
        # This exact public script source and query propagation must be visible.
        if not re.search(r'var targetURL\s*=\s*"jobpostings/Output\.asp"',text) or not re.search(r'var Search\s*=\s*location\.search',text) or 'ScriptLoc = targetURL + Search' not in text:
            raise IncompleteSource('observed public posting source absent')
        endpoint=urljoin(SOURCE_URL,'jobpostings/Output.asp')+'?'+urlsplit(SOURCE_URL).query+'&'
        output=fetch(endpoint);records=parse_output(output)
        revision=hashlib.sha256(output).hexdigest()
        evidence.update(shell_sha256=hashlib.sha256(shell).hexdigest(),output_sha256=revision,posting_count=len(records),posting_source_url=endpoint,complete_exact_scope_read=True)
        return AdapterResult(SourceRead(GRANT,revision,observed,True,False,True,True,records),None,evidence)
    except Exception as exc:
        # Never label an incomplete response as an empty complete snapshot.
        reason=str(exc) if isinstance(exc,IncompleteSource) else type(exc).__name__
        evidence.update(complete_exact_scope_read=False,posting_count=None,hold_reason=reason)
        revision=hashlib.sha256((shell or b'')+(output or b'')).hexdigest()
        return AdapterResult(SourceRead(GRANT,revision,observed,True,False,False,False,[]),reason,evidence)

"""Offline compact context retrieval; word cap applies to emitted context, not JSON envelope."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import re

HASH=re.compile(r'^[a-f0-9]{64}$')
SECRET=re.compile(r'(?:sk-[A-Za-z0-9_-]{20,}|gh[opusr]_[A-Za-z0-9]{20,}|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY)')
STOP={'the','and','for','with','from','this','that','what','how','are','use','into','our','your','to','a','of','in','is','it','on','do'}
ALIASES={'cost':{'cheap','cheapest','budget','model','deterministic','operating','preferences'},'cutting':{'cheap','cheapest','deterministic'},'jobs':{'workflow','scheduled','recurring'},'job':{'workflow','scheduled','recurring'},'monitoring':{'workflow','scheduled','source'},'voice':{'writing','substack','prose'},'style':{'voice','prose'}}


def terms(text):return set(re.findall(r'[a-z0-9]+',text.lower()))-STOP


def read_bounded(path,limit=5_000_000):
    if path.is_symlink() or any(p.is_symlink() for p in path.parents):raise ValueError('symlink source rejected')
    with path.open('rb') as stream:raw=stream.read(limit+1)
    if len(raw)>limit:raise ValueError('source byte bound exceeded')
    return raw


def checked(path,expected):
    if not isinstance(expected,str) or not HASH.fullmatch(expected):raise ValueError('missing/invalid source hash')
    raw=read_bounded(path)
    if hashlib.sha256(raw).hexdigest()!=expected:raise ValueError('source hash mismatch: '+path.name)
    return raw


def retrieve(directory,query,*,max_words=500,max_bundles=3,source_root=None):
    """Hash source bytes only; never emit source documents or private audit content.
    Manifest is operator-trusted metadata, not authentication or a signature.
    """
    if type(max_words) is not int or not 1<=max_words<=10000 or type(max_bundles) is not int or not 1<=max_bundles<=11:raise ValueError('invalid context bounds')
    if not isinstance(query,str) or not query.strip() or len(query)>2000:raise ValueError('bounded query required')
    directory=Path(directory).absolute();repo=directory.parent.parent
    manifest_raw=read_bounded(directory/'manifest.json',1_000_000);manifest=json.loads(manifest_raw)
    if not isinstance(manifest,list) or not 0<len(manifest)<=100:raise ValueError('invalid manifest')
    q=terms(query)
    for word in list(q):q.update(ALIASES.get(word,set()))
    candidates=[];seen=set();baseline=0
    for item in manifest:
        name=item.get('bundle','')
        if not isinstance(name,str) or Path(name).name!=name or not name.endswith('.md') or name in seen:raise ValueError('invalid/duplicate bundle path')
        seen.add(name)
        if item.get('privacy_class')!='private_operational':raise PermissionError('privacy-ineligible bundle')
        body=checked(directory/name,item.get('bundle_sha256')).decode('utf-8')
        if SECRET.search(body):raise PermissionError('credential-shaped bundle content rejected')
        sources=[]
        for source in item.get('sources',[]):
            p=Path(source['path'])
            if p.is_absolute():
                if not source.get('scope','').startswith(('local_only_private_audit','local_only_source')):raise PermissionError('unapproved external source')
            else:
                p=repo/p
                if not p.resolve().is_relative_to(repo.resolve()):raise ValueError('source escapes repository')
            try:checked(p,source.get('sha256'))
            except (FileNotFoundError,ValueError):
                if source_root is None or Path(source['path']).is_absolute():raise ValueError('verification source unavailable or changed: '+p.name)
                historic_root=Path(source_root).absolute();historic=historic_root/source['path']
                if not historic.resolve().is_relative_to(historic_root.resolve()):raise ValueError('historic source escapes root')
                checked(historic,source.get('sha256'));p=historic
            sources.append({'path':source['path'],'verified_path':str(p),'sha256':source['sha256'],'verification':'sha256_matched'})
        receipt=item.get('live_source_receipts')
        receipt_hash=None
        if receipt:
            if Path(receipt).name!=receipt:raise ValueError('invalid receipt path')
            receipt_bytes=read_bounded(directory/receipt,1_000_000);json.loads(receipt_bytes)
            receipt_hash=hashlib.sha256(receipt_bytes).hexdigest()
        baseline+=len(body.split())
        score=6*len(q&terms(name))+2*len(q&terms(body.split('\n',1)[0]))+len(q&terms(body))
        if score:candidates.append((score,name,body,item,sources,receipt,receipt_hash))
    candidates.sort(key=lambda v:(-v[0],v[1]))
    context=[];records=[]
    for score,name,body,item,sources,receipt,receipt_hash in candidates:
        if len(records)>=max_bundles:break
        # Whole paragraphs only; no truncated negation, scoring rule or dangling sentence.
        paragraphs=[p.strip() for p in re.split(r'\n\s*\n',body) if p.strip() and not p.startswith('#')]
        paragraphs.sort(key=lambda p:-len(q&terms(p)))
        header=f'SOURCE {name} SHA256 {item["bundle_sha256"]} Excerpts only; verify full contract before action.\nPROVENANCE {item.get("provenance","unspecified")}\nORIGINAL-SOURCES '+', '.join(source["verified_path"] for source in sources)
        if receipt:header+=f'\nLIVE-RECEIPT {receipt} SHA256 {receipt_hash}; remote source not revalidated.'
        selected=[];current=sum(len(p.split()) for p in context)
        if current+len(header.split())>=max_words:continue
        for paragraph in paragraphs:
            count=current+len(header.split())+sum(len(p.split()) for p in selected)+len(paragraph.split())
            if count<=max_words:selected.append(paragraph)
        if not selected:continue
        block=header+'\n\n'+'\n\n'.join(selected);context.append(block)
        records.append({'bundle':name,'bundle_sha256':item['bundle_sha256'],'privacy_class':item['privacy_class'],'provenance':item.get('provenance','unspecified'),'sources':sources,'live_receipt_path':receipt,'live_receipt_sha256':receipt_hash,'live_receipt_verification':'readable metadata; current remote source not revalidated' if receipt else None,'score':score,'excerpt_not_full_contract':True})
    rendered='\n\n'.join(context);count=len(rendered.split())
    if not records:raise ValueError('no relevant complete paragraph fits context budget')
    if count>max_words:raise AssertionError('context cap violated')
    return {'context':rendered,'context_words':count,'max_words':max_words,'baseline_all_bundle_words':baseline,'word_reduction_percent':round(100*(1-count/baseline),2),'sources':records,'manifest_sha256':hashlib.sha256(manifest_raw).hexdigest(),'execution':'offline deterministic; no API calls; no dollar savings measured','token_count':None,'token_count_reason':'words are exact whitespace units, not model tokenizer tokens'}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('query');parser.add_argument('--source-root',type=Path,help='explicit original source checkout for unchanged historical source hashes; never substitutes different bytes');parser.add_argument('--directory',type=Path,default=Path(__file__).resolve().parents[1]/'knowledge');parser.add_argument('--max-words',type=int,default=500);parser.add_argument('--max-bundles',type=int,default=3);parser.add_argument('--format',choices=['json','text'],default='text');args=parser.parse_args()
    try:result=retrieve(args.directory,args.query,max_words=args.max_words,max_bundles=args.max_bundles,source_root=args.source_root)
    except (ValueError,PermissionError,OSError,KeyError,UnicodeError) as exc:parser.exit(2,'Context rejected: '+str(exc)+'\n')
    print(result['context'] if args.format=='text' else json.dumps(result,indent=2))

if __name__=='__main__':main()

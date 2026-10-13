"""Verified compact appendices for existing routine workers; never replacement prompts.
No model calls, live task edits, private prompt/profile extraction or schedules.
"""
from __future__ import annotations
import argparse,hashlib,json
from pathlib import Path
import re
from knowledge import retrieve,checked,read_bounded,HASH

PROFILES={
 'doe-watch':{'task_id':'6ac29fe996ac81918b03a7d59354ef9f','boundary':'Use the original task criteria, approved official sources, prior-listing history and destination. This context does not provide a cloud-accessible local cache or establish statewide source completeness. Reassess changed criteria independently.',
              'paragraphs':{'workflow-preferences.md':['Prefer compact retrieval bundles','Prefer a filesystem path']}},
 'news':{'task_id':'6aa2783463288191aa4b53146177bf6c','boundary':'Use the original news scope, approved sources, freshness checks and destination. Keep separate finance work within its original restricted workflow. Original birthday/cart instructions remain authoritative; this appendix does not resolve cross-task policy conflicts.',
         'paragraphs':{'workflow-preferences.md':['Prefer compact retrieval bundles','Prefer a filesystem path'],'teaching-principles.md':['AI may reduce production labor']}},
 'birthday':{'task_id':'6aa9962611648191b900495a9ea89cd8','boundary':'Use only the original approved calendar and gift-history sources, dates, family boundaries and destination. Keep private gift/recipient data in the existing task. Follow its original cart/purchase restrictions; this appendix does not merge the news workflow.',
             'paragraphs':{'workflow-preferences.md':['Prefer compact retrieval bundles','Prefer a filesystem path']}},
 'writing-on-demand':{'task_id':None,'boundary':'Apply only during an authorized on-demand writing session. Original draft, current chapter, destination and editorial scope control. This appendix authorizes no manuscript write, grading, scheduling or publication.',
             'paragraphs':{'writing-voice.md':["Preserve Katherine's wording",'The source revision ledger retires'],'substack-voice.md':['Canonical source:','The original stored voice script remains unavailable','The preferred voice session executes']}}
}

def digest(data):return hashlib.sha256(data).hexdigest()
def build_context(worker,*,directory=None,source_root=None,binding=None,max_words=400):
    if worker not in PROFILES:raise ValueError('explicit existing worker required')
    if type(max_words) is not int or not 1<=max_words<=400:raise ValueError('worker limit must be 1..400 words')
    directory=Path(directory or Path(__file__).resolve().parents[1]/'knowledge');profile=PROFILES[worker]
    if len(profile['paragraphs'])>2:raise ValueError('worker bundle cap exceeded')
    # Reuse the existing verifier, including exact private-source hashes. No cached
    # appendix or historic digest can substitute for unavailable source bytes.
    verified=retrieve(directory,' '.join(profile['paragraphs']),max_words=10000,max_bundles=11,source_root=source_root)
    rows={x['bundle']:x for x in verified['sources']};blocks=[];sources=[]
    for name,prefixes in profile['paragraphs'].items():
        row=rows.get(name)
        if row is None:raise ValueError('selected bundle verification missing')
        body=checked(directory/name,row['bundle_sha256']).decode('utf-8')
        paragraphs=[p.strip() for p in re.split(r'\n\s*\n',body) if p.strip()]
        selected=[]
        for prefix in prefixes:
            found=[p for p in paragraphs if p.startswith(prefix)]
            if len(found)!=1:raise ValueError('reviewed paragraph unavailable or ambiguous')
            selected.append(found[0])
        blocks.append('BUNDLE '+name+' SHA256 '+row['bundle_sha256']+'\n'+'\n\n'.join(selected))
        sources.append({'bundle':name,'bundle_sha256':row['bundle_sha256'],'paragraph_sha256':[digest(x.encode()) for x in selected],'provenance':row['provenance'],'source_fingerprints':[{'path':x['path'],'sha256':x['sha256']} for x in row['sources']],'live_receipt_path':row['live_receipt_path'],'live_receipt_sha256':row['live_receipt_sha256'],'remote_source_revalidated':False})
    if binding is not None:
        allowed={'task_id','original_prompt_sha256','source_prompt_preserved','destination_unchanged'}
        if set(binding)!=allowed or binding['task_id']!=profile['task_id'] or not isinstance(binding['original_prompt_sha256'],str) or not HASH.fullmatch(binding['original_prompt_sha256']) or binding['source_prompt_preserved'] is not True or binding['destination_unchanged'] is not True:raise ValueError('exact preserved original-task binding required')
        if profile['task_id'] is None:raise ValueError('on-demand writing has no scheduled-task binding')
    text='COMPACT CONTEXT — '+worker+'\nSupplement only: retain the full original task. Current user instructions control; historical source policy is not execution proof.\n'+profile['boundary']+'\n\n'+'\n\n'.join(blocks)
    count=len(text.split())
    if count>max_words:raise ValueError('reviewed whole-paragraph context exceeds worker cap; do not truncate')
    fingerprints={'worker':worker,'task_id':profile['task_id'],'manifest_sha256':verified['manifest_sha256'],'context_sha256':digest(text.encode()),'sources':sources,'binding':binding}
    fingerprint=digest(json.dumps(fingerprints,sort_keys=True,separators=(',',':')).encode())
    return {'worker':worker,'task_id':profile['task_id'],'context':text,'context_words':count,'bundle_count':len(sources),'max_words':max_words,'context_sha256':fingerprints['context_sha256'],'manifest_sha256':verified['manifest_sha256'],'provenance_fingerprint':fingerprint,'sources':sources,'original_task_binding':binding,'ready_for_live_append':binding is not None,'on_demand_policy_only':profile['task_id'] is None,'all_bundle_words':verified['baseline_all_bundle_words'],'word_reduction_vs_all_bundles_percent':round(100*(1-count/verified['baseline_all_bundle_words']),2),'paid_calls':0,'live_task_edited':False,'dollar_savings_measured':False}

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('worker',choices=list(PROFILES));parser.add_argument('--directory',type=Path);parser.add_argument('--source-root',type=Path);parser.add_argument('--binding',type=Path,help='private metadata-only preserved task binding; never raw prompt');parser.add_argument('--format',choices=['json','text'],default='text');args=parser.parse_args()
    try:
        binding=json.loads(read_bounded(args.binding,10000)) if args.binding else None
        result=build_context(args.worker,directory=args.directory,source_root=args.source_root,binding=binding)
    except (ValueError,PermissionError,OSError,KeyError,UnicodeError) as exc:parser.exit(2,'Worker context held: '+type(exc).__name__+'\n')
    print(json.dumps(result,indent=2) if args.format=='json' else result['context'])
if __name__=='__main__':main()

import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {pathToFileURL} from 'node:url';

export const MANUAL_ID = '1kUWjxAnxK1qrTNlmI72ugYYOj85EGRA2gc5M0bwhYZA';
const volatile = new Set(['contentUrl', 'thumbnailUrl']);
export function stable(value) {
  if (Array.isArray(value)) return value.map(stable);
  if (value && typeof value === 'object') return Object.fromEntries(Object.keys(value).sort()
    .filter(k => !volatile.has(k)).map(k => [k, stable(value[k])]));
  return value;
}
export const hash = value => crypto.createHash('sha256').update(JSON.stringify(stable(value))).digest('hex');
export function unwrap(raw) {
  if (raw?.isError || raw?.structuredContent?.isError) throw Error('Source read failed; retain previous baseline');
  const d = raw?.structuredContent?.result ?? raw?.structuredContent ?? raw?.result ?? raw;
  if (!d || d.isError) throw Error('Invalid source response');
  return d;
}
const tidy = s => String(s).replace(/\r\n/g, '\n').trim() + '\n';

export function manualBundle(raw, checkedAt = new Date().toISOString()) {
  const d = unwrap(raw);
  if (d.documentId !== MANUAL_ID || !Array.isArray(d.paragraphs) || !d.revisionId)
    throw Error('A complete current native read of the designated manual is required');
  const p = d.paragraphs;
  const section = (start, end) => {
    const a = p.map((v,i) => ({v,i})).filter(({v}) => v.text.trim() === start && /^HEADING/.test(v.namedStyleType || ''));
    const b = p.map((v,i) => ({v,i})).filter(({v}) => v.text.trim() === end && /^HEADING/.test(v.namedStyleType || ''));
    if (a.length !== 1 || b.length !== 1 || b[0].i <= a[0].i || a[0].v.tabId !== b[0].v.tabId)
      throw Error(`Manual heading boundaries need inspection: ${start}`);
    const part = p.slice(a[0].i,b[0].i);
    if (part.some(v => v.tabId !== a[0].v.tabId)) throw Error('Cross-tab section requires inspection');
    while (part.length && /^[\s_]*$/.test(part.at(-1).text)) part.pop();
    return tidy(part.map(v => v.text).join('\n'));
  };
  const sections = {
    'skill-3.txt': section('Skill 3 — Embed the codes the feedback tools read', 'Skill 4 — Read a set of student decks'),
    'appendix-b.txt': section('Appendix B: The skills, ready to copy', 'Appendix C: Attribution and lineage'),
    'section-13.txt': section('13. The AI skills you can copy into your own assistant', '14. Enhancing a deck, and handling an upgrade'),
    'section-14.txt': section('14. Enhancing a deck, and handling an upgrade', 'Appendix A: The year on one sheet')
  };
  if (!/google slides/i.test(sections['skill-3.txt']) || !/DO NOT create a pp[xpt]/i.test(sections['skill-3.txt']))
    throw Error('Native Slides amendment changed or is absent; inspect before proceeding');
  return {manifest: {schema:1, manualId:d.documentId, revisionId:d.revisionId, checkedAt,
    sourceUrl:`https://docs.google.com/document/d/${d.documentId}/edit`,
    fullTextHash:hash(p.map(v => ({tabId:v.tabId,text:v.text}))),
    ruleBundleHash:hash(sections), sectionHashes:Object.fromEntries(Object.entries(sections).map(([k,v])=>[k,hash(v)])),
    publisherVersion:'not established by this extractor; inspect the manual',
    scope:'All paragraphs returned by current native text read; verify full tab coverage separately'}, sections};
}

function readJson(file) { return JSON.parse(fs.readFileSync(file,'utf8')); }
function assertSafeDir(dir) {
  const absolute=path.resolve(dir);
  let cursor=path.parse(absolute).root;
  for (const part of absolute.slice(cursor.length).split(path.sep).filter(Boolean)) {
    cursor=path.join(cursor,part);
    if (fs.existsSync(cursor) && fs.lstatSync(cursor).isSymbolicLink()) throw Error('Refusing symlink output');
  }
  if ([path.parse(absolute).root,process.env.HOME,process.env.CODEX_HOME].includes(absolute)) throw Error('Output directory is too broad');
  return absolute;
}
function atomicWrite(file, data) {
  if(fs.existsSync(file) && fs.lstatSync(file).isSymbolicLink()) throw Error('Refusing symlink file');
  const tmp=file+'.tmp-'+crypto.randomUUID();
  fs.writeFileSync(tmp,data,{flag:'wx',mode:0o600});
  fs.renameSync(tmp,file);
}
export function refreshManual(bundle, directory, commit=false) {
  const dir=assertSafeDir(directory), current=path.join(dir,'manual-current');
  const priorPath=path.join(current,'manifest.json');
  const prior=fs.existsSync(priorPath)?readJson(priorPath):null;
  const changed=!prior || prior.ruleBundleHash!==bundle.manifest.ruleBundleHash;
  const result={changed,fullTextChanged:!prior||prior.fullTextHash!==bundle.manifest.fullTextHash,
    committed:false,manifest:bundle.manifest,previousRuleBundleHash:prior?.ruleBundleHash??null};
  if(!commit) return result;
  fs.mkdirSync(dir,{recursive:true});
  // Archive the complete previous cache, including legacy files, before updating anything.
  const previous={};
  for(const name of ['manual-skill-3.txt','manual-enhancement-rules.txt']) {
    const file=path.join(dir,name);
    if(fs.existsSync(file)) previous[name]=fs.readFileSync(file,'utf8');
  }
  if(fs.existsSync(current)) for(const name of fs.readdirSync(current)) {
    if(!/^[a-z0-9.-]+$/.test(name)) throw Error('Unexpected current-cache filename');
    const file=path.join(current,name);
    if(!fs.lstatSync(file).isFile()) throw Error('Unexpected current-cache entry');
    previous['current-'+name]=fs.readFileSync(file,'utf8');
  }
  if(Object.keys(previous).length && (changed || !prior)) {
    const history=path.join(dir,'manual-history',hash(previous));
    assertSafeDir(history); fs.mkdirSync(history,{recursive:true});
    for(const [name,content] of Object.entries(previous)) {
      const file=path.join(history,name);
      if(!fs.existsSync(file)) fs.writeFileSync(file,content,{flag:'wx',mode:0o600});
      else if(fs.readFileSync(file,'utf8')!==content) throw Error('History collision; no cache refresh');
    }
    result.archivedTo=history;
  }
  assertSafeDir(current); fs.mkdirSync(current,{recursive:true});
  for(const [name,content] of Object.entries(bundle.sections)) atomicWrite(path.join(current,name),content);
  atomicWrite(path.join(dir,'manual-skill-3.txt'),bundle.sections['skill-3.txt']);
  atomicWrite(path.join(dir,'manual-enhancement-rules.txt'),bundle.sections['section-14.txt']);
  // Publish the manifest last. It contains expected hashes for recovery after interrupted writes.
  atomicWrite(priorPath,JSON.stringify(bundle.manifest,null,2)+'\n');
  return {...result,committed:true};
}

export function deckSnapshot(raw, checkedAt=new Date().toISOString()) {
  const p=unwrap(raw);
  if(raw.course==='Biology' && Number(raw.week)===2) throw Error('Biology 02 is excluded');
  if(!p.presentationId || !Array.isArray(p.slides) || !p.revisionId) throw Error('Complete native deck required');
  const ids=p.slides.map(s=>s.objectId);
  if(ids.some(x=>!x)||new Set(ids).size!==ids.length) throw Error('Missing/duplicate slide IDs');
  return {schema:1,id:p.presentationId,title:p.title,revisionId:p.revisionId,checkedAt,
    deckHash:hash({slides:p.slides,layouts:p.layouts,masters:p.masters,pageSize:p.pageSize,notesMaster:p.notesMaster}),
    themeHash:hash({layouts:p.layouts,masters:p.masters,pageSize:p.pageSize,notesMaster:p.notesMaster}),
    slides:p.slides.map((s,i)=>({id:s.objectId,number:i+1,hash:hash(s)})),
    status:'observed, not code-verified',visualQA:'not established by fingerprint'};
}
export function compareDecks(before, after) {
  if(before.id!==after.id) throw Error('Cannot compare different Drive IDs as one deck');
  const a=new Map(before.slides.map(s=>[s.id,s])),b=new Map(after.slides.map(s=>[s.id,s]));
  return {id:after.id,revisionChanged:before.revisionId!==after.revisionId,
    contentChanged:before.deckHash!==after.deckHash,themeChanged:before.themeHash!==after.themeHash,
    added:after.slides.filter(s=>!a.has(s.id)).map(s=>s.id),
    removed:before.slides.filter(s=>!b.has(s.id)).map(s=>s.id),
    changed:after.slides.filter(s=>a.has(s.id)&&a.get(s.id).hash!==s.hash).map(s=>s.id),
    reordered:before.slides.filter(s=>b.has(s.id)).map(s=>s.id).join('\n')!==after.slides.filter(s=>a.has(s.id)).map(s=>s.id).join('\n'),
    interpretation:'Change detection only; removed means absent in this complete native deck read, not deleted by the sweep'};
}
if(process.argv[1] && import.meta.url===pathToFileURL(path.resolve(process.argv[1])).href) {
  try {
    const [mode,first,second,...flags]=process.argv.slice(2);
    let result;
    if(mode==='manual' && first && second && flags.every(f=>f==='--commit')) result=refreshManual(manualBundle(readJson(first)),second,flags.includes('--commit'));
    else if(mode==='deck' && first && !second) result=deckSnapshot(readJson(first));
    else if(mode==='compare' && first && second && !flags.length) result=compareDecks(readJson(first),readJson(second));
    else throw Error('Usage: manual INPUT.json OUTPUT-DIR [--commit] | deck RAW.json | compare OLD.json NEW.json');
    console.log(JSON.stringify(result,null,2));
  } catch(error) { console.error(error.message); process.exitCode=1; }
}

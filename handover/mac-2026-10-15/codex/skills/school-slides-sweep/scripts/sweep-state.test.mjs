import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {MANUAL_ID,hash,manualBundle,refreshManual,deckSnapshot,compareDecks} from './sweep-state.mjs';
const h=text=>({text,tabId:'t.0',namedStyleType:'HEADING_2'});
const n=text=>({text,tabId:'t.0',namedStyleType:'NORMAL_TEXT'});
const manual=()=>({documentId:MANUAL_ID,revisionId:'r1',paragraphs:[
  h('13. The AI skills you can copy into your own assistant'),n('markers'),
  h('14. Enhancing a deck, and handling an upgrade'),n('keep active cycles'),h('Appendix A: The year on one sheet'),
  h('Appendix B: The skills, ready to copy'),n('Skill 1 full rules'),
  h('Skill 3 — Embed the codes the feedback tools read'),n('Google Slides: DO NOT create a ppx.'),
  h('Skill 4 — Read a set of student decks'),n('grading rules'),h('Appendix C: Attribution and lineage')]});
const deck=()=>({presentationId:'same',revisionId:'r1',title:'test',slides:[
  {objectId:'a',pageElements:[{objectId:'label',shape:{text:'original'},image:{contentUrl:'volatile1',sourceUrl:'stable'}}]},
  {objectId:'b',slideProperties:{notesPage:{text:'revision prompt'}}}],masters:[{objectId:'m',color:'red'}]});
test('stable keys and ephemeral image URLs do not invent changes',()=>{
  assert.equal(hash({b:2,a:1}),hash({a:1,b:2}));const a=deck(),b=deck();b.slides[0].pageElements[0].image.contentUrl='volatile2';
  assert.equal(deckSnapshot(a).deckHash,deckSnapshot(b).deckHash);
});
test('native text and notes changes are detected',()=>{
  const a=deck(),b=deck();b.slides[0].pageElements[0].shape.text='edited';b.slides[1].slideProperties.notesPage.text='changed';
  assert.deepEqual(compareDecks(deckSnapshot(a),deckSnapshot(b)).changed,['a','b']);
});
test('reorder differs from insertion and removal',()=>{
  const a=deck(),b=deck();b.slides.reverse();assert.equal(compareDecks(deckSnapshot(a),deckSnapshot(b)).reordered,true);
  const c=deck();c.slides.push({objectId:'c'});const diff=compareDecks(deckSnapshot(a),deckSnapshot(c));
  assert.deepEqual(diff.added,['c']);assert.equal(diff.reordered,false);
  c.slides=c.slides.slice(1);assert.deepEqual(compareDecks(deckSnapshot(a),deckSnapshot(c)).removed,['a']);
});
test('theme changes require review even with unchanged slides',()=>{
  const a=deck(),b=deck();b.masters[0].color='blue';assert.equal(compareDecks(deckSnapshot(a),deckSnapshot(b)).themeChanged,true);
});
test('unknown sources, errors, duplicate slides and wrong deck IDs fail closed',()=>{
  assert.throws(()=>deckSnapshot({isError:true}));const a=deck();a.slides.push(a.slides[0]);assert.throws(()=>deckSnapshot(a));
  assert.throws(()=>compareDecks({id:'a'},{id:'b'}));assert.throws(()=>manualBundle({...manual(),documentId:'wrong'}));
  assert.throws(()=>deckSnapshot({...deck(),course:'Biology',week:2}));
});
test('manual separates full text change from rule change',()=>{
  const a=manual(),b=manual();b.paragraphs.unshift(n('unrelated preface change'));
  assert.notEqual(manualBundle(a).manifest.fullTextHash,manualBundle(b).manifest.fullTextHash);
  assert.equal(manualBundle(a).manifest.ruleBundleHash,manualBundle(b).manifest.ruleBundleHash);
  b.paragraphs.splice(-1,0,n('new grading rule'));assert.notEqual(manualBundle(a).manifest.ruleBundleHash,manualBundle(b).manifest.ruleBundleHash);
});
test('missing, duplicated, or cross-tab headings cannot refresh cached rules',()=>{
  const a=manual();a.paragraphs.pop();assert.throws(()=>manualBundle(a));
  const b=manual();b.paragraphs.push(h('Appendix C: Attribution and lineage'));assert.throws(()=>manualBundle(b));
  const c=manual();c.paragraphs[8].tabId='other';assert.throws(()=>manualBundle(c));
});
test('preview does not write; commit archives old content; repeated commit is idempotent',()=>{
  const dir=fs.realpathSync(fs.mkdtempSync(path.join(os.tmpdir(),'school-slides-sweep-test-')));
  const out=path.join(dir,'derived');const a=manualBundle(manual(),'2026-09-10T12:00:00Z');
  assert.equal(refreshManual(a,out).committed,false);assert.equal(fs.existsSync(out),false);
  fs.mkdirSync(out);fs.writeFileSync(path.join(out,'manual-skill-3.txt'),'old exact rules');
  const first=refreshManual(a,out,true);assert.equal(fs.readFileSync(path.join(first.archivedTo,'manual-skill-3.txt'),'utf8'),'old exact rules');
  const again=refreshManual(a,out,true);assert.equal(again.changed,false);assert.equal(again.archivedTo,undefined);
  const b=manual();b.paragraphs.splice(-1,0,n('new grader rule'));const changed=refreshManual(manualBundle(b),out,true);
  assert.equal(changed.changed,true);assert.equal(fs.existsSync(path.join(changed.archivedTo,'current-appendix-b.txt')),true);
  const persisted=JSON.parse(fs.readFileSync(path.join(out,'manual-current','manifest.json')));
  for(const [file,fingerprint] of Object.entries(persisted.sectionHashes)) assert.equal(hash(fs.readFileSync(path.join(out,'manual-current',file),'utf8')),fingerprint);
});

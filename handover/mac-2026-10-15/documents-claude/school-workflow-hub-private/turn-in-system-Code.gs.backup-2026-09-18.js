// PRE-CHANGE BACKUP — 📤 Turn-in system (Apps Script project 133uC3RCEDVNBQsJEYM_N5smRp3jr2PykYsm6eNbWHAZgUWN3H0QSpgD-)
// Captured 2026-09-18 from the script editor before adding the recovery functions.
// Trigger identity: onDeckSubmit ON_FORM_SUBMIT bound to FORM_ID below.
// PRIVATE — do not commit to GitHub. No secret values are present (IDs only).

/**********************************************************************
 * 📤 TURN-IN SYSTEM v2 — one form, every assignment, auto-filed uploads
 *
 * Lives INSIDE the "Agenda 26-27 CLEAN" Google Sheet
 * (Extensions → Apps Script → paste → run SETUP once).
 *
 * SETUP (safe to re-run any time — it repairs, never duplicates):
 *   1. Checks it's running in the right spreadsheet — fails loudly if not.
 *   2. Forces the form to collect verified student emails (identity!).
 *   3. Adds an "Assignment" field to the form (if missing).
 *   4. Builds a private, teacher-only tree:  📥 Submissions 26-27 /
 *      <course> / <Wk NN — Topic> /   — students never see inside it.
 *   5. Writes a 📤 Turn it in link on every course-tab week row.
 *   6. Installs the router: every submission's files are MOVED into the
 *      right assignment folder, renamed "student — date — file", logged.
 **********************************************************************/

const FORM_ID      = '1Lg6mSoPRZT2zKnuBttVp5t35i2YRtZtEpl3SxcqDJNY';
const AGENDA_ID    = '1m4qhXb5M7y0nMNJHeuxu2J4eFXokIKYxiGVyOfpg-uY';   // Agenda 26-27 CLEAN
const COURSE_TABS  = ['🌿 Biology', '🫀 A&P', '🔬 Forensics'];
const ASSIGN_TITLE = 'Assignment (auto-filled — please do not change)';
const MAP_SHEET    = '🗂 TurnIn Map';
const LOG_SHEET    = '📥 Log';
const SUB_ROOT      = '00 ALL TURN IN (school account only)';   // consolidated 2026-09-18
const UNSORTED     = '📥 UNSORTED submissions';
const ROW_FIRST = 4;
const COL = { wk:1, topic:3, link:20, raw:21 };   // A, C, T, U

const FOLDER_NAMES = {
  "🔬 Forensics · Wk 01 — Work a case": "Wk 01 — Work a case — 2026-09-02",
  "🔬 Forensics · Wk 02 — Lab Safety, Equipment & the Microscope": "Wk 02 — Lab Safety, Equipment & the Microscope — 2026-09-09",
  "🔬 Forensics · Wk 03 — Observation Skills & Deductive Reasoning": "Wk 03 — Observation Skills & Deductive Reasoning — 2026-09-14",
  "🔬 Forensics · Wk 04 — Eyewitness Testimony & The Innocence Project": "Wk 04 — Eyewitness Testimony & The Innocence Project — 2026-09-23",
  "🔬 Forensics · Wk 05 — Investigative Processes & Types of Evidence": "Wk 05 — Investigative Processes & Types of Evidence — 2026-09-28",
  "🔬 Forensics · Wk 06 — Searching & Photographing the Scene": "Wk 06 — Searching & Photographing the Scene — 2026-10-05",
  "🔬 Forensics · Wk 07 — Sketching the Scene & Evidence Collection": "Wk 07 — Sketching the Scene & Evidence Collection — 2026-10-12",
  "🔬 Forensics · Wk 08 — History of Forensics  +  Crime Scene to Courtroom (Mock Tria": "Wk 08 — History of Forensics + Crime Scene to Courtroom — 2026-10-19",
  "🔬 Forensics · Wk 09 — Unit 1 Review — completion + Growth Reports (no exam)": "Wk 09 — Unit 1 Review (Growth Reports, no exam) — 2026-10-26",
  "🔬 Forensics · Wk 10 — Mock Crime Scene": "Wk 10 — Mock Crime Scene — 2026-11-02",
  "🔬 Forensics · Wk 11 — Arson": "Wk 11 — Arson — 2026-11-09",
  "🔬 Forensics · Wk 12 — Ballistics": "Wk 12 — Ballistics — 2026-11-16",
  "🔬 Forensics · Wk 14 — Blood Evidence (Part 2)": "Wk 14 — Blood Evidence (Part 2) — 2026-11-30",
  "🔬 Forensics · Wk 15 — DNA Profiling (Part 1)": "Wk 15 — DNA Profiling (Part 1) — 2026-12-07",
  "🔬 Forensics · Wk 16 — DNA Profiling (Part 2)  +  [EMPTY — no topic assigned. Match": "Wk 16 — DNA Profiling (Part 2) — 2026-12-14",
  "🔬 Forensics · Wk 17 — DNA Profiling (Part 3) & Fibers": "Wk 17 — DNA Profiling (Part 3) & Fibers — 2027-01-04",
  "🔬 Forensics · Wk 18 — Fibers  +  Fingerprints": "Wk 18 — Fibers + Fingerprints — 2027-01-11",
  "🔬 Forensics · Wk 19 — Hair": "Wk 19 — Hair — 2027-01-22",
  "🔬 Forensics · Wk 22 — Cold Case Synthesis (activity doc)": "Wk 22 — Cold Case Synthesis — 2027-02-08",
  "🔬 Forensics · Wk 23 — Forensic Pathology & Expert in Court (activity doc)": "Wk 23 — Forensic Pathology & Expert in Court — 2027-02-17",
  "🔬 Forensics · Wk 24 — Intro to Toxicology & Drug Schedules": "Wk 24 — Intro to Toxicology & Drug Schedules — 2027-02-22",
  "🔬 Forensics · Wk 25 — Toxicology & Forensics": "Wk 25 — Toxicology & Forensics — 2027-03-01",
  "🔬 Forensics · Wk 26 — Toxicology Review — completion + Growth Reports (no exam)": "Wk 26 — Toxicology Review (Growth Reports, no exam) — 2027-03-08",
  "🔬 Forensics · Wk 27 — Intro to Death & What Is Death": "Wk 27 — Intro to Death & What Is Death — 2027-03-15",
  "🔬 Forensics · Wk 28 — Stages of Decomposition & The Body Farm": "Wk 28 — Stages of Decomposition & The Body Farm — 2027-03-22",
  "🔬 Forensics · Wk 30 — Autopsy Week (+ Pig Autopsy / Necrobiome materials in Unit 3": "Wk 30 — Autopsy Week — 2027-04-05",
  "🔬 Forensics · Wk 31 — Livor / Rigor / Algor Mortis (Time of Death)": "Wk 31 — Livor Rigor Algor Mortis (Time of Death) — 2027-04-12",
  "🔬 Forensics · Wk 33 — Intro to Entomology & Time of Death": "Wk 33 — Intro to Entomology & Time of Death — 2027-04-26",
  "🔬 Forensics · Wk 34 — Entomology Review, Forensic Anthropology & Human Skull": "Wk 34 — Entomology Review & Forensic Anthropology — 2027-05-03",
  "🔬 Forensics · Wk 35 — Forensic Anthropology — Pelvic & Long Bones": "Wk 35 — Forensic Anthropology (Pelvic & Long Bones) — 2027-05-10",
  "🔬 Forensics · Wk 36 — Forensic Anthropology Lab + Culminating Capstone — Convictio": "Wk 36 — Forensic Anthropology Lab + Capstone — 2027-05-17"
};

/* ---------- private-folder helpers (id remembered, trash-proof) ---- */
function ownedFolder_(name, parent) {
  const props = PropertiesService.getScriptProperties();
  const pkey  = 'FID_' + name + (parent ? '_' + parent.getId() : '');
  const saved = props.getProperty(pkey);
  if (saved) {
    try {
      const f = DriveApp.getFolderById(saved);
      if (!f.isTrashed()) return f;
    } catch (e) { /* fall through */ }
  }
  const it = (parent || DriveApp)
    .searchFolders('title = "' + name + '" and trashed = false and "me" in owners');
  const f = it.hasNext() ? it.next()
                         : (parent ? parent.createFolder(name)
                                   : DriveApp.createFolder(name));
  props.setProperty(pkey, f.getId());
  return f;
}

/* ============================== SETUP ============================== */
function SETUP() {
  const ss = SpreadsheetApp.getActive() || SpreadsheetApp.openById(AGENDA_ID);
  PropertiesService.getScriptProperties().setProperty('AGENDA_ID', ss.getId());

  // -- 1. right spreadsheet? fail loudly BEFORE touching anything ----
  const missing = COURSE_TABS.filter(t => !ss.getSheetByName(t));
  if (missing.length) {
    throw new Error('SETUP aborted — tab(s) not found: ' + missing.join(', ') +
      '. Is this the "Agenda 26-27 CLEAN" sheet, with tab names (incl. emoji) unchanged?');
  }

  // -- 2. the form must know WHO submitted -------------------------
  const form = FormApp.openById(FORM_ID);
  form.setCollectEmail(true);
  if (!form.collectsEmail()) {
    throw new Error('Could not enable email collection — open the form: ' +
      'Settings → Responses → Collect email addresses → "Verified", then re-run SETUP.');
  }
  // Apps Script cannot set the Verified flavor — that is a one-time UI step:
  const VERIFY_NOTE = '⚠ ONE MANUAL STEP: open the form → Settings → Responses → ' +
    'Collect email addresses → set to "VERIFIED" (script cannot set this). ' +
    'Without it, student names on files are typed, not verified.';
  console.log(VERIFY_NOTE);
  try { ss.toast(VERIFY_NOTE, 'Turn-in setup', 10); } catch (e) {}

  // -- 3. Assignment field, at the top -----------------------------
  let assignItem = form.getItems(FormApp.ItemType.TEXT)
    .find(it => it.getTitle() === ASSIGN_TITLE);
  if (!assignItem) {
    const t = form.addTextItem().setTitle(ASSIGN_TITLE).setRequired(true);
    form.moveItem(t.getIndex(), 0);
    assignItem = form.getItems(FormApp.ItemType.TEXT)
      .find(it => it.getTitle() === ASSIGN_TITLE);
  }
  const textItem = assignItem.asTextItem();

  // -- 4. private teacher-only tree --------------------------------
  const root     = ownedFolder_(SUB_ROOT, null);
  const unsorted = ownedFolder_(UNSORTED, root);
  const courseFolder = {};
  COURSE_TABS.forEach(t => courseFolder[t] = ownedFolder_(t, root));

  // -- 5. per-course links (batched I/O, progress toasts) ----------
  const map = [];
  let made = 0, skipped = 0;
  COURSE_TABS.forEach(tab => {
    const sh = ss.getSheetByName(tab);
    if (sh.getMaxColumns() < COL.raw)
      sh.insertColumnsAfter(sh.getMaxColumns(), COL.raw - sh.getMaxColumns());
    const lastOld = sh.getLastRow();
    const nRows = Math.max(1, lastOld - ROW_FIRST + 1);
    const data  = sh.getRange(ROW_FIRST, 1, nRows, COL.topic).getValues();
    let last = data.length - 1;                       // trim to real week rows
    while (last >= 0 && String(data[last][COL.wk - 1]).trim() === '') last--;
    const links = [], raws = [];
    for (let i = 0; i <= last; i++) {
      const wk    = String(data[i][COL.wk - 1]).trim();
      const topic = String(data[i][COL.topic - 1]).trim();
      if (!wk) { skipped++; links.push(['']); raws.push(['']); continue; }
      const key = tab + ' · ' + wk + (topic ? ' — ' + topic.slice(0, 60) : '');
      const url = form.createResponse()
        .withItemResponse(textItem.createResponse(key))
        .toPrefilledUrl();
      links.push(['=HYPERLINK("' + url + '","📤 Submit ↗")']);
      raws.push([url]);
      map.push([key, courseFolder[tab].getId(), tab, wk]);
      made++;
    }
    sh.getRange(3, COL.link, 1, 2)
      .setValues([['📤 Turn it in', '_turnInURL']]).setFontWeight('bold');
    if (links.length) {
      sh.getRange(ROW_FIRST, COL.link, links.length, 1).setValues(links);
      sh.getRange(ROW_FIRST, COL.raw,  raws.length, 1).setValues(raws)
        .setFontColor('#999999').setFontSize(9);
    }
    const from = ROW_FIRST + links.length;
    if (lastOld >= from) sh.getRange(from, COL.link, lastOld - from + 1, 2).clearContent();
    sh.hideColumns(COL.raw);
    try { ss.toast(tab + ': ' + made + ' links so far', 'Turn-in setup', 5); } catch (e) {}
    console.log(tab + ' done — running total ' + made);
  });
  if (!made) throw new Error(
    'SETUP aborted — no week rows found (col A, rows 4+). Router NOT installed.');
  map.push(['__UNSORTED__', unsorted.getId(), '', '']);

  // Atomic map rebuild: ONE setValues padded over the old extent, so a
  // submission can never read a half-written or empty map. The lock is
  // belt-and-suspenders against a concurrent SETUP.
  const lock = LockService.getScriptLock();
  lock.waitLock(30000);
  try {
    const ms = ss.getSheetByName(MAP_SHEET) || ss.insertSheet(MAP_SHEET);
    const oldRows = ms.getLastRow();
    const block = [['assignment key', 'target folder id', 'course', 'week']]
      .concat(map);
    while (block.length < oldRows) block.push(['', '', '', '']);
    if (ms.getMaxColumns() > 4)
      ms.getRange(1, 5, Math.max(1, oldRows), ms.getMaxColumns() - 4).clearContent();
    ms.getRange(1, 1, block.length, 4).setValues(block);
    ms.getRange(1, 1, 1, 4).setFontWeight('bold');
    ms.hideSheet();
  } finally {
    lock.releaseLock();
  }

  if (!ss.getSheetByName(LOG_SHEET)) {
    ss.insertSheet(LOG_SHEET).getRange(1, 1, 1, 5).setValues(
      [['when', 'student', 'assignment', 'file', 'filed into']])
      .setFontWeight('bold');
  }

  // -- 6. router trigger: create only if missing (no unguarded gap) --
  const mine = ScriptApp.getProjectTriggers()
    .filter(t => t.getHandlerFunction() === 'onDeckSubmit');
  mine.filter(t => t.getTriggerSourceId() !== FORM_ID)
    .forEach(t => ScriptApp.deleteTrigger(t));
  const have = mine.some(t =>
    t.getEventType() === ScriptApp.EventType.ON_FORM_SUBMIT &&
    t.getTriggerSourceId() === FORM_ID);
  if (!have) {
    ScriptApp.newTrigger('onDeckSubmit').forForm(form).onFormSubmit().create();
  }

  try { BUILD_FOLDERS(); } catch(e){ console.log('folder build: '+e); } // auto
  const msg = '📤 Turn-in ready: ' + made + ' submit links across ' +
    COURSE_TABS.length + ' tabs (' + skipped + ' blank rows skipped). ' +
    'Uploads will file into "' + SUB_ROOT + '" (private to you).';
  console.log(msg);
  try { ss.toast(msg, 'Turn-in system', 10); } catch (e) {}
}

/* ============================== ROUTER ============================= */
function onDeckSubmit(e) {
  if (!e || !e.response) return;
  const props = PropertiesService.getScriptProperties();
  const ss    = SpreadsheetApp.openById(props.getProperty('AGENDA_ID') || AGENDA_ID);
  const log   = ss.getSheetByName(LOG_SHEET);
  const msh   = ss.getSheetByName(MAP_SHEET);
  if (!msh) {
    if (log) log.appendRow([new Date(), '', '',
      'ERROR: 🗂 TurnIn Map tab missing — re-run SETUP', '']);
    return;
  }
  const rows = msh.getDataRange().getValues().slice(1);
  const map  = Object.create(null);
  rows.forEach(r => { if (r[0]) map[String(r[0]).trim()] = String(r[1]); });

  // what was submitted
  let key = '', fileIds = [];
  e.response.getItemResponses().forEach(ir => {
    const t = ir.getItem().getType();
    if (t === FormApp.ItemType.TEXT && ir.getItem().getTitle() === ASSIGN_TITLE) {
      key = String(ir.getResponse()).trim();
    } else if (t === FormApp.ItemType.FILE_UPLOAD) {
      fileIds = fileIds.concat(ir.getResponse());
    }
  });
  if (!fileIds.length) return;

  // who submitted (form enforces verified email; belt-and-suspenders here)
  const email   = e.response.getRespondentEmail() || '';
  const student = email ? email.split('@')[0]
                        : 'unknown-' + e.response.getId().slice(-6);

  // where it goes: exact key → stable "course · week" prefix → UNSORTED
  let homeId = map[key] || null, mrow = null;
  if (homeId) {
    mrow = rows.find(r => String(r[0]).trim() === key);
  } else {
    mrow = rows.find(r => {
      if (!r[2]) return false;
      const stable = r[2] + ' · ' + r[3];
      return key === stable || key.indexOf(stable + ' — ') === 0;
    });
    if (mrow) homeId = String(mrow[1]);
  }
  homeId = homeId || map['__UNSORTED__'];
  let home;
  try {
    home = DriveApp.getFolderById(homeId);
    if (home.isTrashed()) throw new Error('trashed');
  } catch (err) {
    home = ownedFolder_(UNSORTED, ownedFolder_(SUB_ROOT, null));
    if (log) log.appendRow([new Date(), email, key,
      'WARNING: target folder unavailable — used UNSORTED. Re-run SETUP.', '']);
  }

  // per-assignment subfolder, named from the CURRENT map row (stable
  // across topic renames); find-or-create under a lock (submit bursts)
  const subName = '📥 ' + (FOLDER_NAMES[key] || (mrow ? String(mrow[0]).replace(/^[^·]+·\s*/, '') : (key || 'unmatched')));
  const lock = LockService.getScriptLock();
  let target;
  try {
    lock.waitLock(30000);
    const subs = home.getFoldersByName(subName);
    target = subs.hasNext() ? subs.next() : home.createFolder(subName);
  } catch (lockErr) {
    const subs = home.getFoldersByName(subName);
    target = subs.hasNext() ? subs.next() : home.createFolder(subName);
  } finally {
    try { lock.releaseLock(); } catch (ignore) {}
  }

  // move + rename (guard against double-prefix on duplicate firings)
  const prefix = student + ' — ';
  fileIds.forEach(id => {
    try {
      const f = DriveApp.getFileById(id);
      if (f.getName().indexOf(prefix) !== 0) {
        const stamp = Utilities.formatDate(new Date(),
          Session.getScriptTimeZone(), 'MM-dd HH.mm');
        f.setName(prefix + stamp + ' — ' + f.getName());
      }
      f.moveTo(target);
      if (log) log.appendRow([new Date(), email || '(no email collected)',
        key || '(none)', f.getName(), subName]);
    } catch (err) {
      if (log) log.appendRow([new Date(), email, key || '(none)',
        'ERROR moving file ' + id + ': ' + err, '']);
    }
  });
}


/* temp: dump Forensics submit links for the ParentSquare build */
function DUMP_FORENSICS(){
  const ss=SpreadsheetApp.openById(AGENDA_ID);
  const sh=ss.getSheetByName('🔬 Forensics');
  const v=sh.getRange(4,1,40,21).getValues();
  const out=v.filter(r=>String(r[0]).trim()).map(r=>({wk:String(r[0]).trim(),topic:String(r[2]).trim().slice(0,60),url:String(r[20]).trim()}));
  console.log(JSON.stringify(out));
}


/* ===== Pre-create dated Forensics submission folders (lesson name + date) ===== */
function BUILD_FOLDERS() {
  const root = ownedFolder_(SUB_ROOT, null);
  const fcourse = ownedFolder_('🔬 Forensics', root);
  let made = 0, kept = 0;
  for (const key in FOLDER_NAMES) {
    const name = '📥 ' + FOLDER_NAMES[key];
    const it = fcourse.getFoldersByName(name);
    if (it.hasNext()) { kept++; } else { fcourse.createFolder(name); made++; }
  }
  const msg = '📁 Forensics submission folders ready: ' + made + ' created, ' + kept + ' already existed. They live in ' + SUB_ROOT + ' / 🔬 Forensics.';
  console.log(msg);
  try { SpreadsheetApp.openById(AGENDA_ID).toast(msg, 'Folders', 10); } catch (e) {}
}



/* =====================================================================
 * 🛟 RECOVERY 2026-09-18 — bounded, reversible restore of student
 * originals endangered by the turn-in reorganization.
 *
 * Run order (never skip ahead):
 *   1. RECOVERY_INVENTORY_20260918 — READ-ONLY dry run. Walks the
 *      deprecated root tree (even in trash), scans the account trash for
 *      router-renamed / Log-listed student files, and lists live
 *      UNSORTED files. Writes one row per file with a proposed action to
 *      the '🛟 Recovery 2026-09-18' sheet in the Agenda. Moves NOTHING.
 *   2. RECOVER_ONE_20260918 — restores exactly ONE planned file
 *      (untrash + move + readback) so postconditions can be inspected.
 *   3. RECOVER_UNMATCHED_20260918 — restores the remaining planned
 *      files, one at a time, each with its own readback receipt.
 *
 * Guarantees: never empties trash, never deletes, never restores the
 * whole deprecated root folder, never runs SETUP, preserves file IDs
 * and contents. Assignment placement only when the file's own recorded
 * path or Log row proves it; otherwise the file goes to a visible
 * '🛟 RECOVERED — needs match' folder under the active turn-in root.
 * =================================================================== */
const RECOVERY_SHEET = '🛟 Recovery 2026-09-18';
const OLD_ROOT_ID    = '1oEpTa873f1cKWxGH_NbPXx-PQ3yOK0AN'; // deprecated turn-in root
const RECOVERY_HOLD  = '🛟 RECOVERED — needs match';
const RECOVERY_MAX   = 300;   // hard cap on rows handled per run
const TRASH_SCAN_MAX = 2000;  // hard cap on trash entries examined
const RECOVERY_HEADERS = ['file id','file name','recorded path','trashed at inventory',
  'proposed destination','status','last update','detail'];

function recoverySheet_() {
  const ss = SpreadsheetApp.openById(AGENDA_ID);
  let sh = ss.getSheetByName(RECOVERY_SHEET);
  if (!sh) {
    sh = ss.insertSheet(RECOVERY_SHEET);
    sh.getRange(1,1,1,RECOVERY_HEADERS.length).setValues([RECOVERY_HEADERS]).setFontWeight('bold');
  }
  return sh;
}

function recoveryRows_(sh) {
  const n = sh.getLastRow();
  return n > 1 ? sh.getRange(2,1,n-1,RECOVERY_HEADERS.length).getValues() : [];
}

function walkTree_(folder, path, out, depth) {
  if (depth > 8 || out.length >= RECOVERY_MAX) return;
  const files = folder.getFiles();
  while (files.hasNext() && out.length < RECOVERY_MAX) {
    const f = files.next();
    out.push({ id: f.getId(), name: f.getName(), path: path, trashed: f.isTrashed() });
  }
  const subs = folder.getFolders();
  while (subs.hasNext() && out.length < RECOVERY_MAX) {
    const s = subs.next();
    walkTree_(s, path + ' / ' + s.getName(), out, depth + 1);
  }
}

// Assignment is "certain" only when the recorded path itself shows a
// course tab plus a week-named assignment folder. Anything else is held.
function proposeDestination_(recordedPath) {
  const parts = String(recordedPath).split(' / ').map(function(p){ return p.trim(); });
  let course = null, week = null;
  parts.forEach(function(p) {
    if (COURSE_TABS.indexOf(p) !== -1) course = p;
    const cleaned = p.replace(/^📥\s*/, '');
    if (/^Wk \d\d\s*—/.test(cleaned)) week = cleaned;
  });
  if (course && week) return course + ' / 📥 ' + week;
  return RECOVERY_HOLD;
}

function RECOVERY_INVENTORY_20260918() {
  const sh = recoverySheet_();
  const known = {};
  recoveryRows_(sh).forEach(function(r){ if (r[0]) known[String(r[0])] = true; });
  const out = [];

  // 1. deprecated tree — reachable by ID even while in trash
  try {
    const oldRoot = DriveApp.getFolderById(OLD_ROOT_ID);
    walkTree_(oldRoot, oldRoot.getName(), out, 0);
  } catch (e) {
    sh.appendRow(['', '', 'deprecated root unreachable: ' + e, '', '', 'note', new Date(), '']);
  }

  // 2. trash scan for router-renamed or Log-listed student files that
  //    were trashed individually (not under the deprecated root)
  const seen = {};
  out.forEach(function(f){ seen[f.id] = true; });
  const logNames = {};
  try {
    const ls = SpreadsheetApp.openById(AGENDA_ID).getSheetByName(LOG_SHEET);
    if (ls && ls.getLastRow() > 1) {
      ls.getRange(2, 4, ls.getLastRow() - 1, 1).getValues().forEach(function(r){
        if (r[0]) logNames[String(r[0])] = true;
      });
    }
  } catch (e) {}
  const renamePattern = /^[^—]{1,40} — \d\d-\d\d \d\d\.\d\d — /;
  try {
    const it = DriveApp.searchFiles('trashed = true and "me" in owners');
    let scanned = 0;
    while (it.hasNext() && scanned < TRASH_SCAN_MAX && out.length < RECOVERY_MAX) {
      const f = it.next(); scanned++;
      if (seen[f.getId()]) continue;
      const name = f.getName();
      if (!logNames[name] && !renamePattern.test(name)) continue;
      seen[f.getId()] = true;
      out.push({ id: f.getId(), name: name, path: '(found in trash, outside deprecated root)',
                 trashed: true, fromTrashScan: true });
    }
  } catch (e) {
    sh.appendRow(['', '', 'trash scan failed: ' + e, '', '', 'note', new Date(), '']);
  }

  // 3. live UNSORTED files — report-only; they are safe where they are
  try {
    const unsorted = ownedFolder_(UNSORTED, ownedFolder_(SUB_ROOT, null));
    const live = [];
    walkTree_(unsorted, SUB_ROOT + ' / ' + UNSORTED, live, 0);
    live.forEach(function(f){ f.liveUnmatched = true; out.push(f); });
  } catch (e) {
    sh.appendRow(['', '', 'UNSORTED unreachable: ' + e, '', '', 'note', new Date(), '']);
  }

  let added = 0;
  const rows = [];
  out.forEach(function(f) {
    if (known[f.id]) return;
    known[f.id] = true; added++;
    if (f.liveUnmatched) {
      rows.push([f.id, f.name, f.path, String(f.trashed), '(stays in UNSORTED)',
        'live-unmatched', new Date(), 'safe where it is — match through the dashboard']);
    } else {
      rows.push([f.id, f.name, f.path, String(f.trashed), proposeDestination_(f.path),
        f.trashed ? 'planned' : 'planned-move-only', new Date(),
        f.fromTrashScan ? 'individually trashed router file' : '']);
    }
  });
  if (rows.length) sh.getRange(sh.getLastRow()+1, 1, rows.length, RECOVERY_HEADERS.length).setValues(rows);
  const msg = 'Recovery inventory (read-only): ' + out.length + ' files seen, '
    + added + ' new rows on "' + RECOVERY_SHEET + '". Nothing was moved or untrashed.';
  console.log(msg);
  return msg;
}

function resolveDestination_(destLabel) {
  const root = ownedFolder_(SUB_ROOT, null);
  if (!destLabel || destLabel === RECOVERY_HOLD) return ownedFolder_(RECOVERY_HOLD, root);
  const cut = String(destLabel).indexOf(' / ');
  if (cut === -1) return ownedFolder_(RECOVERY_HOLD, root);
  const course = String(destLabel).slice(0, cut), sub = String(destLabel).slice(cut + 3);
  if (COURSE_TABS.indexOf(course) === -1) return ownedFolder_(RECOVERY_HOLD, root);
  const cf = ownedFolder_(course, root);
  const found = cf.getFoldersByName(sub);
  return found.hasNext() ? found.next() : cf.createFolder(sub);
}

function restoreRows_(maxCount) {
  const sh = recoverySheet_();
  const rows = recoveryRows_(sh);
  let done = 0, failed = 0, already = 0;
  for (let i = 0; i < rows.length && (done + failed) < maxCount; i++) {
    const status = String(rows[i][5]);
    if (status !== 'planned' && status !== 'planned-move-only') continue;
    const id = String(rows[i][0]);
    const receipt = sh.getRange(i + 2, 6, 1, 3); // status / last update / detail
    try {
      const f = DriveApp.getFileById(id);
      const dest = resolveDestination_(String(rows[i][4]));
      if (!f.isTrashed()) { // resume safety: skip anything already live in place
        const ps = f.getParents();
        if (ps.hasNext() && ps.next().getId() === dest.getId()) {
          receipt.setValues([['already-recovered', new Date(), 'live in destination; skipped']]);
          already++; continue;
        }
      }
      try { f.setTrashed(false); } catch (u) { /* inherited trash: the move below lifts it */ }
      f.moveTo(dest);
      // readback: the file itself must be live and sitting in the destination
      if (f.isTrashed()) { try { f.setTrashed(false); } catch (u2) {} }
      const p = f.getParents();
      const parentId = p.hasNext() ? p.next().getId() : '';
      if (f.isTrashed()) throw new Error('still trashed after untrash + move');
      if (parentId !== dest.getId()) throw new Error('parent readback mismatch');
      receipt.setValues([['restored', new Date(), 'now in: ' + dest.getName()]]);
      done++;
    } catch (e) {
      receipt.setValues([['failed: ' + String(e).slice(0, 160), new Date(), '']]);
      failed++;
    }
  }
  const msg = 'Recovery run: ' + done + ' restored, ' + failed + ' failed, '
    + already + ' already recovered. Receipts on "' + RECOVERY_SHEET + '".';
  console.log(msg);
  return msg;
}

function RECOVER_ONE_20260918()       { return restoreRows_(1); }
function RECOVER_UNMATCHED_20260918() { return restoreRows_(RECOVERY_MAX); }

/**
 * 03 BIOLOGY (Public) — convert Office files to native Google format.
 *
 * Walks "03 BIOLOGY (Public)" and EVERY subfolder, and makes a native
 * Google copy of each Office file:
 *
 *     .docx / .doc  ->  Google Doc
 *     .pptx / .ppt  ->  Google Slides
 *     .xlsx / .xls  ->  Google Sheets
 *
 * The converted copy is created in the SAME folder as the original, with the
 * file extension dropped from the name.
 *
 * NOTHING IS DELETED. Originals stay exactly where they are. Run
 * listLeftoverOriginals() afterwards to see what you may want to clean up.
 *
 * Safe to re-run: anything already converted is skipped, so you can run this
 * again later when you add new files.
 *
 * RUN THIS AS katherine.vonduyke@redclay.k12.de.us (the account that owns
 * these files), so the new Docs are owned by the same account.
 */

const ROOT_FOLDER_ID = '1GvlqU7JGJaYOOQlus38Fa7JgiSu-C6Hq';  // 03 BIOLOGY (Public)

const CONVERT_MAP = {
  'application/vnd.openxmlformats-officedocument.wordprocessingml.document':  'application/vnd.google-apps.document',
  'application/msword':                                                       'application/vnd.google-apps.document',
  'application/vnd.openxmlformats-officedocument.presentationml.presentation':'application/vnd.google-apps.presentation',
  'application/vnd.ms-powerpoint':                                            'application/vnd.google-apps.presentation',
  'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':        'application/vnd.google-apps.spreadsheet',
  'application/vnd.ms-excel':                                                 'application/vnd.google-apps.spreadsheet',
};

const KIND = {
  'application/vnd.google-apps.document':     'Doc',
  'application/vnd.google-apps.presentation': 'Slides',
  'application/vnd.google-apps.spreadsheet':  'Sheet',
};


/** ============ MAIN — run this one ============ */
function convertBiologyFolder() {
  const stats = { converted: 0, skipped: 0, failed: 0, folders: 0 };
  const lines = [];

  const root = DriveApp.getFolderById(ROOT_FOLDER_ID);
  walkFolder_(root, root.getName(), stats, lines);

  lines.push('');
  lines.push('==================================================');
  lines.push('Folders scanned : ' + stats.folders);
  lines.push('Converted       : ' + stats.converted);
  lines.push('Already done    : ' + stats.skipped);
  lines.push('Failed          : ' + stats.failed);
  lines.push('==================================================');
  lines.push('Originals were NOT deleted.');

  const report = lines.join('\n');
  Logger.log(report);
  return report;
}


/** Recurse through a folder and everything under it. */
function walkFolder_(folder, path, stats, lines) {
  stats.folders++;

  const files = folder.getFiles();
  while (files.hasNext()) {
    const file = files.next();
    const target = CONVERT_MAP[file.getMimeType()];
    if (!target) continue;                      // not an Office file — leave alone

    const newName = stripExtension_(file.getName());

    if (alreadyConverted_(folder, newName, target)) {
      stats.skipped++;
      lines.push('SKIP  [' + KIND[target] + '] ' + path + '/' + newName + '  (already exists)');
      continue;
    }

    try {
      copyAsGoogleType_(file.getId(), newName, target, folder.getId());
      stats.converted++;
      lines.push('OK    [' + KIND[target] + '] ' + path + '/' + newName);
    } catch (err) {
      stats.failed++;
      lines.push('FAIL  [' + KIND[target] + '] ' + path + '/' + file.getName() + '  -> ' + err);
    }

    Utilities.sleep(300);                       // stay well inside Drive quota
  }

  const subs = folder.getFolders();
  while (subs.hasNext()) {
    const sub = subs.next();
    walkFolder_(sub, path + '/' + sub.getName(), stats, lines);
  }
}


/**
 * Copy a file and convert it in the same step.
 * Uses the Drive REST API directly, so you do NOT have to enable the
 * Advanced Drive Service. Passing a Google mimeType to /copy is what
 * triggers Google's own server-side conversion.
 */
function copyAsGoogleType_(fileId, name, targetMimeType, parentId) {
  const url = 'https://www.googleapis.com/drive/v3/files/' + fileId +
              '/copy?supportsAllDrives=true&fields=id,name,mimeType';

  const res = UrlFetchApp.fetch(url, {
    method: 'post',
    contentType: 'application/json',
    headers: { Authorization: 'Bearer ' + ScriptApp.getOAuthToken() },
    payload: JSON.stringify({
      name: name,
      mimeType: targetMimeType,
      parents: [parentId],
    }),
    muteHttpExceptions: true,
  });

  const code = res.getResponseCode();
  if (code < 200 || code >= 300) {
    throw new Error('HTTP ' + code + ' ' + res.getContentText());
  }
  return JSON.parse(res.getContentText());
}


/** True if this folder already holds a converted file of the right name and type. */
function alreadyConverted_(folder, name, targetMimeType) {
  const hits = folder.getFilesByName(name);
  while (hits.hasNext()) {
    if (hits.next().getMimeType() === targetMimeType) return true;
  }
  return false;
}


/** "Interview forms.docx" -> "Interview forms" */
function stripExtension_(name) {
  return name.replace(/\.(docx|doc|pptx|ppt|xlsx|xls)$/i, '');
}


/** ============ OPTIONAL — run after the conversion ============
 * Lists every Office original that now has a Google twin sitting beside it.
 * It only PRINTS them. It deletes nothing. Use the list to decide what to
 * clear out by hand.
 */
function listLeftoverOriginals() {
  const lines = [];
  const root = DriveApp.getFolderById(ROOT_FOLDER_ID);
  findLeftovers_(root, root.getName(), lines);

  const report = lines.length
    ? lines.join('\n') + '\n\n' + lines.length + ' original(s) now have a Google version alongside them.'
    : 'No leftover Office originals with a Google twin.';
  Logger.log(report);
  return report;
}

function findLeftovers_(folder, path, lines) {
  const files = folder.getFiles();
  while (files.hasNext()) {
    const file = files.next();
    const target = CONVERT_MAP[file.getMimeType()];
    if (!target) continue;
    if (alreadyConverted_(folder, stripExtension_(file.getName()), target)) {
      lines.push(path + '/' + file.getName() + '   ' + file.getUrl());
    }
  }
  const subs = folder.getFolders();
  while (subs.hasNext()) {
    const sub = subs.next();
    findLeftovers_(sub, path + '/' + sub.getName(), lines);
  }
}

/** TILLER FIX v3 — auto-check Bill Payment Tracker from Transactions.
 *  Replaces the manual Jul–Jun checkboxes (H24:S30) with formulas that mark a
 *  bill paid when a negative transaction matching its Description lands in
 *  that month. No more manual checking, ever.
 *  Run: Extensions > Apps Script > paste over old code > select fixBillTracker > Run
 *  (then check the SPREADSHEET tab for the done popup!)
 */
function fixBillTracker() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const t = ss.getSheetByName('Bill Payment Tracker');
  let wired = 0;
  for (let r = 24; r <= 30; r++) {
    const desc = String(t.getRange(r, 3).getValue() || '').trim();
    if (!desc) continue;                       // skip empty bill rows
    for (let c = 8; c <= 19; c++) {            // H..S = the 12 month columns
      const col = t.getRange(1, c).getA1Notation().replace(/\d+/, '');
      t.getRange(r, c).setFormula(
        '=COUNTIFS(Transactions!$C$2:$C$5011,"*"&$C' + r + '&"*",' +
        'Transactions!$B$2:$B$5011,">="&' + col + '$23,' +
        'Transactions!$B$2:$B$5011,"<"&EDATE(' + col + '$23,1),' +
        'Transactions!$E$2:$E$5011,"<0")>0');
    }
    wired++;
  }
  SpreadsheetApp.getUi().alert('Bill tracker wired to Transactions for ' +
    wired + ' bills.\nBoxes now check themselves when a matching payment ' +
    'appears.\nSafe to delete the Synchrony Bank row if that bill is dead.');
}

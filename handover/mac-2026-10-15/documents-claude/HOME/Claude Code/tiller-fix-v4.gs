/** TILLER FIX v4 — run fixV4 (then check the SHEET tab for the popup)
 * 1. Renames MARGINSv2 -> MARGIN (all formulas auto-update)
 * 2. Red fill on MARGIN column D when over budget (< 0)
 * 3. Bill Payment Tracker: C24-down = every Bills + Rental Bills category
 *    (pulled live from Categories), paid-boxes match by CATEGORY in
 *    Transactions, green = paid, red = not paid. Est Amount = July budget.
 */
function fixV4() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();

  // 1. rename
  const m = ss.getSheetByName('MARGINSv2') || ss.getSheetByName('MARGIN');
  m.setName('MARGIN');

  // 2. red over-budget on column D
  const dRange = m.getRange('D5:D45');
  const rules = m.getConditionalFormatRules().filter(r =>
    !r.getRanges().some(g => g.getA1Notation().startsWith('D')));
  rules.push(SpreadsheetApp.newConditionalFormatRule()
    .whenNumberLessThan(0).setBackground('#f4c7c3').setFontColor('#990000')
    .setRanges([dRange]).build());
  m.setConditionalFormatRules(rules);

  // 3. bill tracker from Categories groups
  const cats = ss.getSheetByName('Categories');
  const data = cats.getRange(2, 1, cats.getLastRow() - 1, 2).getValues();
  const bills = data.filter(r => r[1] === 'Bills' || r[1] === 'Rental Bills')
                    .map(r => String(r[0]));
  const t = ss.getSheetByName('Bill Payment Tracker');
  t.getRange(24, 1, 25, 19).clearContent();          // clear old Bill Setup rows
  for (let i = 0; i < bills.length; i++) {
    const r = 24 + i;
    t.getRange(r, 3).setValue(bills[i]);             // C: category name
    t.getRange(r, 4).setFormula(                     // D: July budget
      '=SUMIF(Categories!$A:$A,$C' + r + ',Categories!$K:$K)');
    const fs = [[]];
    for (let c = 8; c <= 19; c++) {
      const col = String.fromCharCode(64 + c);       // H..S
      fs[0].push('=COUNTIFS(Transactions!$D$2:$D$5011,$C' + r +
        ',Transactions!$B$2:$B$5011,">="&' + col + '$23' +
        ',Transactions!$B$2:$B$5011,"<"&EDATE(' + col + '$23,1)' +
        ',Transactions!$E$2:$E$5011,"<0")>0');
    }
    t.getRange(r, 8, 1, 12).setFormulas(fs);
  }
  // green/red on the paid grid
  const grid = t.getRange(24, 8, bills.length, 12);
  const tr = t.getConditionalFormatRules();
  tr.push(SpreadsheetApp.newConditionalFormatRule().whenTextEqualTo('TRUE')
    .setBackground('#b7e1cd').setRanges([grid]).build());
  tr.push(SpreadsheetApp.newConditionalFormatRule().whenTextEqualTo('FALSE')
    .setBackground('#f4c7c3').setRanges([grid]).build());
  t.setConditionalFormatRules(tr);

  SpreadsheetApp.getUi().alert('v4 done: MARGIN renamed, red over-budget on, ' +
    bills.length + ' bills wired green/red from Categories + Transactions.');
}

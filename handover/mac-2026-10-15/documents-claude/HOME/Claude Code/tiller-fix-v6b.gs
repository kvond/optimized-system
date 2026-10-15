/** TILLER v6b — total Bill Payment Tracker rebuild. Run fixV6Tracker, then
 *  check the SHEET tab for the popup. WIPES the whole tracker tab and rebuilds:
 *  A=Bill  B=Monthly budget  C=Last paid date  D=Last amount  F:Q=Jul-Jun grid
 *  Bills = every Bills/Rental Bills category with a July budget > 0.
 *  Boxes + colors: green=paid that month, red=not, straight from Transactions.
 */
function fixV6Tracker() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const t = ss.getSheetByName('Bill Payment Tracker');
  const cats = ss.getSheetByName('Categories');
  const data = cats.getRange(2, 1, cats.getLastRow() - 1, 11).getValues();
  const bills = data.filter(r =>
    (r[1] === 'Bills' || r[1] === 'Rental Bills') && Number(r[10]) > 0)
    .map(r => String(r[0]));                    // col K = index 10 (July)

  t.clear(); t.clearConditionalFormatRules();
  t.getRange(1, 1, t.getMaxRows(), t.getMaxColumns()).clearDataValidations();
  t.getRange('A1').setValue('BILL TRACKER — auto-paid from Transactions')
    .setFontWeight('bold');
  t.getRange('A2:D2').setValues([['Bill', 'Budget/mo', 'Last paid', 'Last amt']])
    .setFontWeight('bold');
  t.getRange('F2').setFormula('=DATE(2026,7,1)');
  for (let c = 7; c <= 17; c++)
    t.getRange(2, c).setFormula('=EDATE(' + t.getRange(2, c - 1).getA1Notation() + ',1)');
  t.getRange('F2:Q2').setNumberFormat('mmm yy').setFontWeight('bold');

  for (let i = 0; i < bills.length; i++) {
    const r = 3 + i;
    t.getRange(r, 1).setValue(bills[i]);
    t.getRange(r, 2).setFormula('=SUMIF(Categories!$A:$A,$A' + r + ',Categories!$K:$K)');
    t.getRange(r, 3).setFormula(
      '=IFERROR(TEXT(MAXIFS(Transactions!$B$2:$B$5011,Transactions!$D$2:$D$5011,$A' + r +
      ',Transactions!$E$2:$E$5011,"<0"),"m/d/yy"),"—")');
    t.getRange(r, 4).setFormula(
      '=IFERROR(INDEX(SORT(FILTER({Transactions!$B$2:$B$5011,Transactions!$E$2:$E$5011},' +
      'Transactions!$D$2:$D$5011=$A' + r + ',Transactions!$E$2:$E$5011<0),1,FALSE),1,2),"—")');
    const fs = [[]];
    for (let c = 6; c <= 17; c++) {
      const col = t.getRange(2, c).getA1Notation().replace(/\d+/, '');
      fs[0].push('=COUNTIFS(Transactions!$D$2:$D$5011,$A' + r +
        ',Transactions!$B$2:$B$5011,">="&' + col + '$2' +
        ',Transactions!$B$2:$B$5011,"<"&EDATE(' + col + '$2,1)' +
        ',Transactions!$E$2:$E$5011,"<0")>0');
    }
    t.getRange(r, 6, 1, 12).setFormulas(fs);
  }
  const grid = t.getRange(3, 6, bills.length, 12);
  const rules = [];
  rules.push(SpreadsheetApp.newConditionalFormatRule().whenTextEqualTo('TRUE')
    .setBackground('#b7e1cd').setFontColor('#b7e1cd').setRanges([grid]).build());
  rules.push(SpreadsheetApp.newConditionalFormatRule().whenTextEqualTo('FALSE')
    .setBackground('#f4c7c3').setFontColor('#f4c7c3').setRanges([grid]).build());
  t.setConditionalFormatRules(rules);
  t.setFrozenRows(2); t.autoResizeColumns(1, 4);
  SpreadsheetApp.getUi().alert('Tracker rebuilt: ' + bills.length +
    ' bills, last-paid dates + amounts, 12-month green/red grid.');
}

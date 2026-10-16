/** TILLER FIX v5 — run fixV5, then check the SHEET tab for the popup.
 * 1. Deletes the empty/rental row 13 on MARGIN (the one that bugs you)
 * 2. Repairs the two formulas that break when it goes (Plan-left F3 + Chase subtotal)
 * 3. Rebuilds the one rental row in the Capital One section: planned from
 *    Categories, MTD from Transactions (ALL accounts), Remaining = B+C
 */
function fixV5() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const m = ss.getSheetByName('MARGIN') || ss.getSheetByName('MARGINSv2');
  const A = v => m.getRange(v).getValue();

  // 1. delete row 13 only if it is the rental row or blank
  const a13 = String(A('A13'));
  if (a13 === '' || a13.indexOf('Rental') !== -1) {
    m.deleteRow(13);
  }

  // locate key rows by label (layout-proof)
  const col = m.getRange('A1:A45').getValues().map(r => String(r[0]));
  const find = txt => col.findIndex(v => v.indexOf(txt) !== -1) + 1;
  const rUncat = find('Uncategorized');        // Chase uncategorized row
  const rSub   = rUncat + 1;                    // Chase subtotal row under it
  const rCap   = find('CAPITAL ONE');
  let   rRent  = col.findIndex((v,i) => i+1 > rCap && v.indexOf('Rental Bills') !== -1) + 1;
  const rSavor = find('Savor');                 // Personal — Savor row
  const rPrime = find('Prime');
  const r360   = find('360 Checking') === 0 ? 0 : col.findIndex((v,i)=> i+1>rCap && v.indexOf('360 Checking')!==-1)+1;
  const rPer   = find('Periodic');

  // 2. rebuild the rental row (Capital One section)
  if (rRent > 0) {
    m.getRange(rRent, 1).setValue('Rental Bills (out)');
    m.getRange(rRent, 2).setFormula('=SUMIF(Categories!$B:$B,"Rental Bills",Categories!$K:$K)');
    m.getRange(rRent, 3).setFormula(
      '=SUMPRODUCT(COUNTIF(FILTER(Categories!$A$2:$A$100,Categories!$B$2:$B$100="Rental Bills"),Transactions!$D$2:$D$5011)' +
      '*(Transactions!$B$2:$B$5011>=DATE(2026,7,1))*(Transactions!$B$2:$B$5011<DATE(2026,8,1))*Transactions!$E$2:$E$5011)');
    m.getRange(rRent, 4).setFormula('=B' + rRent + '+C' + rRent);
  }

  // 3. repair Plan-left (F3) + Chase subtotal
  const parts = ['D12', 'D' + rUncat, 'D' + rRent, 'D' + rSavor, 'D' + rPrime];
  if (r360 > 0) parts.push('D' + r360);
  if (rPer > 0) parts.push('D' + rPer);
  m.getRange('F3').setFormula('=ROUND(' + parts.map(p => 'MAX(0,' + p + ')').join('+') + ',2)');
  m.getRange('B' + rSub).setFormula('=B10+B11-B12');

  SpreadsheetApp.getUi().alert('v5 done. Row 13 removed, rental row rebuilt at row ' +
    rRent + ', Plan-left = MAX of rows ' + parts.join(', '));
}

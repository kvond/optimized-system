/** TILLER FIX v2 — rebuilds the deleted Rental Bills row, repairs Plan-left,
 *  and re-runs the transaction recategorization (safe to run repeatedly).
 *  Run: Extensions > Apps Script > paste over old code > Run (▶)
 */
function fixTillerV2() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const m = ss.getSheetByName('MARGINSv2');
  const log = [];

  // 1. Rebuild "Rental Bills (out)" as row 13 if missing
  if (String(m.getRange('A13').getValue()) !== 'Rental Bills (out)') {
    m.insertRowBefore(13);
    m.getRange('A13').setValue('Rental Bills (out)');
    log.push('Reinserted Rental Bills row 13');
  }
  m.getRange('B13').setFormula('=SUMIF(Categories!$B:$B,"Rental Bills",Categories!$K:$K)');
  m.getRange('C13').setFormula(
    '=SUMPRODUCT(COUNTIF(FILTER(Categories!$A$2:$A$100,Categories!$B$2:$B$100="Rental Bills"),Transactions!$D$2:$D$5011)' +
    '*(Transactions!$B$2:$B$5011>=DATE(2026,7,1))*(Transactions!$B$2:$B$5011<DATE(2026,8,1))' +
    '*Transactions!$E$2:$E$5011)');
  m.getRange('D13').setFormula('=B13+C13');
  m.getRange('E13').setValue('7/17');

  // 2. Repair Plan-left (F3)
  m.getRange('F3').setFormula(
    '=ROUND(MAX(0,D12)+MAX(0,D13)+MAX(0,D16)+MAX(0,D27)+MAX(0,D28)+MAX(0,D29)+MAX(0,D30)+MAX(0,D36),2)');
  log.push('F3 Plan-left repaired');

  // 3. Transactions cleanup (same rules as v1; only touches invalid rows)
  const exact = {'AI':'Subscriptions','Amaz-Lunch, shop, gifts':'Amazon - unsorted',
    'Saltwrap - supplements':'Amazon - Supplements','Teaching Materials':'Teacher expenses'};
  const byDesc = [['jpmorgan chase','Mortgage'],['citadel fcu','Citadel Car Payments'],
    ['crunch fit','Balance Fitness'],['balance strength','Balance Fitness'],
    ['the edge fit','Balance Fitness'],['greensky','Green Sky 11%'],
    ['state farm','State Farm'],['irs usataxpymt','Taxes'],['freetaxusacom','Taxes'],
    ['advs ed','Aidvantage2024Loan'],['vanguard','Vanguard'],['verizon','Internet'],
    ['qualitycutlawnserv','Lawn Care'],['miller environmental','Lawn Care'],
    ['boulden',"Boulden's VPI"],['green pest','Pest Control'],
    ['home depot','Rental - repair supplies'],['cooper roofing','Rental Maintenance'],
    ['delaware drain','Rental Maintenance'],['first state garage','Rental Maintenance'],
    ['u-haul','Rental Maintenance'],['places 4 students','Rental Maintenance'],
    ['zillow','Rental Maintenance']];
  const cats = ss.getSheetByName('Categories');
  const canonical = new Set(cats.getRange(2,1,cats.getLastRow()-1,1).getValues()
    .map(r=>String(r[0])).filter(v=>v&&v!=='null'));
  const tx = ss.getSheetByName('Transactions');
  const n = tx.getLastRow()-1;
  const descs = tx.getRange(2,3,n,1).getValues();
  const cr = tx.getRange(2,4,n,1); const cur = cr.getValues();
  let changed=0; const un=[];
  for (let i=0;i<n;i++){
    const cat=String(cur[i][0]||'');
    if(!cat||canonical.has(cat))continue;
    if(exact[cat]){cur[i][0]=exact[cat];changed++;continue;}
    if(cat==='Bills'||cat==='Rental Bills'){
      const d=String(descs[i][0]||'').toLowerCase();
      const hit=byDesc.find(([s])=>d.indexOf(s)!==-1);
      if(hit){cur[i][0]=hit[1];changed++;continue;}
    }
    un.push('row '+(i+2)+': "'+cat+'" '+String(descs[i][0]).slice(0,35));
  }
  cr.setValues(cur);
  log.push('Transactions: '+changed+' rows recategorized'+(un.length?'; left alone: '+un.length:''));
  un.forEach(u=>log.push('  '+u));
  SpreadsheetApp.getUi().alert('Fix v2 done\n\n'+log.join('\n'));
}

/**
 * TILLER CONSISTENCY FIX — one-time cleanup, July 2026
 * What it does:
 *  1. MARGINSv2: repairs B13 (Rental Bills target) + C13 (Rental Bills MTD, group-aware)
 *  2. AutoCat: fixes 5 rules that assign group names / stale names as categories
 *  3. Transactions: recategorizes every row whose category is not a real
 *     Categories-page category (241 rows found in audit), using description rules.
 * It changes NOTHING else. Unmatched rows are left alone and listed at the end.
 *
 * HOW TO RUN: Extensions > Apps Script > paste this whole file over the empty
 * script > click Run (▶). Approve the permission prompt (it runs as you, only
 * on this spreadsheet). Read the summary popup when it finishes.
 */
function fixTillerConsistency() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const log = [];

  // ---- 1. MARGINSv2 formulas ----------------------------------------------
  const m = ss.getSheetByName('MARGINSv2');
  m.getRange('B13').setFormula(
    '=SUMIF(Categories!$B:$B,"Rental Bills",Categories!$K:$K)');
  m.getRange('C13').setFormula(
    '=SUMPRODUCT(COUNTIF(Categories!$A$32:$A$38,Transactions!$D$2:$D$5011)' +
    '*(Transactions!$B$2:$B$5011>=DATE(2026,7,1))' +
    '*(Transactions!$B$2:$B$5011<DATE(2026,8,1))' +
    '*Transactions!$E$2:$E$5011)');
  log.push('MARGINSv2: B13 + C13 formulas repaired');

  // ---- 2. AutoCat rule fixes ----------------------------------------------
  const ac = ss.getSheetByName('AutoCat');
  const acFixes = {5:'Vanguard', 15:'Teacher expenses', 16:'Teacher expenses',
                   29:'Pest Control', 60:"Boulden's VPI"};
  for (const [row, cat] of Object.entries(acFixes)) {
    const cur = ac.getRange(+row, 1).getValue();
    ac.getRange(+row, 1).setValue(cat);
    log.push('AutoCat row ' + row + ': "' + cur + '" -> "' + cat + '"');
  }
  // NOTE: AutoCat row 14 ("Spending" <- Venmo) is redundant with rows 3/23/27/28.
  // Deleting rows is left to you — just delete that row when convenient.

  // ---- 3. Transactions recategorization -----------------------------------
  // exact-rename rules (category -> new category, regardless of description)
  const exact = {
    'AI': 'Subscriptions',
    'Amaz-Lunch, shop, gifts': 'Amazon - unsorted',
    'Saltwrap - supplements': 'Amazon - Supplements',
    'Teaching Materials': 'Teacher expenses'
  };
  // description-contains rules, applied only when category is 'Bills' or 'Rental Bills'
  const byDesc = [   // [substring (lowercase), new category]
    ['jpmorgan chase',        'Mortgage'],
    ['citadel fcu',           'Citadel Car Payments'],
    ['crunch fit',            'Balance Fitness'],
    ['balance strength',      'Balance Fitness'],
    ['the edge fit',          'Balance Fitness'],
    ['greensky',              'Green Sky 11%'],
    ['state farm',            'State Farm'],
    ['irs usataxpymt',        'Taxes'],
    ['freetaxusacom',         'Taxes'],
    ['advs ed',               'Aidvantage2024Loan'],
    ['vanguard',              'Vanguard'],
    ['verizon',               'Internet'],
    ['qualitycutlawnserv',    'Lawn Care'],
    ['miller environmental',  'Lawn Care'],
    ['boulden',               "Boulden's VPI"],
    ['green pest',            'Pest Control'],
    ['home depot',            'Rental - repair supplies'],
    ['cooper roofing',        'Rental Maintenance'],
    ['delaware drain',        'Rental Maintenance'],
    ['first state garage',    'Rental Maintenance'],
    ['u-haul',                'Rental Maintenance'],
    ['places 4 students',     'Rental Maintenance'],
    ['zillow',                'Rental Maintenance']
  ];

  // canonical category list from Categories!A
  const cats = ss.getSheetByName('Categories');
  const canonical = new Set(
    cats.getRange(2, 1, cats.getLastRow() - 1, 1).getValues()
        .map(r => String(r[0])).filter(v => v && v !== 'null'));

  const tx = ss.getSheetByName('Transactions');
  const n = tx.getLastRow() - 1;
  const descs = tx.getRange(2, 3, n, 1).getValues();   // col C
  const catRange = tx.getRange(2, 4, n, 1);            // col D
  const cur = catRange.getValues();
  let changed = 0; const unmatched = [];

  for (let i = 0; i < n; i++) {
    const cat = String(cur[i][0] || '');
    if (!cat || canonical.has(cat)) continue;          // valid or blank: skip
    if (exact[cat]) { cur[i][0] = exact[cat]; changed++; continue; }
    if (cat === 'Bills' || cat === 'Rental Bills') {
      const d = String(descs[i][0] || '').toLowerCase();
      const hit = byDesc.find(([sub]) => d.indexOf(sub) !== -1);
      if (hit) { cur[i][0] = hit[1]; changed++; continue; }
    }
    unmatched.push('row ' + (i + 2) + ': "' + cat + '" — ' +
                   String(descs[i][0]).slice(0, 40));
  }
  catRange.setValues(cur);
  log.push('Transactions: ' + changed + ' rows recategorized');
  if (unmatched.length) {
    log.push('LEFT ALONE (no rule matched — fix by hand):');
    unmatched.forEach(u => log.push('   ' + u));
  }
  SpreadsheetApp.getUi().alert('Tiller consistency fix — done\n\n' + log.join('\n'));
}

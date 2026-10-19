---
name: panama-grocery-order
description: Default Panama grocery/delivery order for Katherine when staying near P.H. DOVLE Cincuentenario, Panama City. Use whenever she asks to reorder groceries in Panama, says "usual Panama order," or asks for a grocery delivery run there without specifying items. Produces the cheapest single-store delivery that covers as many items as possible, applying the dietary constraints below. Triggers - "usual Panama order", "reorder groceries in Panama", "Panama grocery delivery".
---

# Panama Grocery Order (default)

## Location
Near P.H. DOVLE Cincuentenario, Panama City, Panama. Delivery zone: "Vía Cincuentenario, Panamá, Panama."

## Standing item list
- Naproxen — generic preferred over brand, want a meaningful supply, not a single dose
- Sugar-free electrolyte packets or drinks
- Bone broth or chicken broth
- Rotisserie chicken or other prepared chicken
- Boiled eggs
- Tuna or salmon
- Unsweetened almond milk
- Sparkling water
- Avocados
- Cucumbers
- Mixed salad greens or bag of salad
- Macadamia nuts or almonds
- Low-carb dairy-free protein drinks if available

## Constraints (in priority order)
1. Fewest separate stores — strongly prefer ONE store, one delivery, even if it means some items are compromises.
2. Lowest total cost.
3. Eliminate added sugar where possible; keep carbohydrates relatively low.

## Panama market realities learned (July 2026 pass)
- **Naproxen is a pharmacy item.** Pure grocery chains (Riba Smith) do not stock any OTC medication at all — this is a category-wide gap, not a store defect. Only stores with an integrated pharmacy (e.g., Super Xtra / Xtra Farma) can include it in a grocery order.
- **Panama OTC meds are sold in small boxes (commonly 10 tablets), not large US-style bottles.** To approximate "a full bottle," buy multiple boxes (we used 4 boxes of La Sante Naproxeno 500mg = 40 tablets for ~$2.28 at Super Xtra).
- **Riba Smith** (ribasmith.com) is the premium/imported-goods chain — best selection for the specialty low-carb items (Electrolit Zero, real bone broth boxes, Orgain dairy-free protein drink, macadamia nuts, San Pellegrino/Perrier/Waterloo, real rotisserie chicken via "Comidas Preparadas Rimith"). It has ~92% item coverage but zero pharmacy items. Flat delivery fee ~$3.50.
- **Super Xtra** (superxtra.com, has "Xtra Farma" built in) is the value/local chain — carries the pharmacy item but is noticeably weaker on specialty/low-carb goods: only regular-sugar Electrolit (no Zero line), no real bone broth (only bouillon powder/cubes), no rotisserie or other prepared chicken (raw whole chicken only), no boiled/prepared eggs (raw only), and **no dairy-free protein drink at all** (no Orgain/Vega — closest is a dairy whey powder, which doesn't meet "dairy-free" and was left out rather than force a bad match). Delivery fee starts at $3.75, reduced/free above a spend threshold (~$11.44 more from a ~$30 cart triggered "free shipping" progress in one test).
- Given the standing priority "fewest stores" outranks ingredient quality, **default to whichever single store can include Naproxen (i.e., Super Xtra/Xtra Farma or an equivalent grocery+pharmacy hybrid) rather than the store with the best specialty selection**, unless Katherine says she's fine leaving Naproxen for a separate pharmacy trip that day.
- Always flag substitutions plainly: raw vs. prepared items, bouillon vs. real broth, regular vs. zero-sugar, and any item that couldn't be found at all (don't force a fake match).

## Output format each time
1. Best single store for that day (re-verify stock/price live — don't assume last visit's inventory holds).
2. Estimated subtotal, delivery fee, and total.
3. Line-item list with prices.
4. Substitutions/gaps called out explicitly, each with a one-line reason.
5. Note that the cart is a guest cart built in her connected Chrome session — she needs to log in/enter address & payment herself to complete checkout (per standing policy: don't enter payment or personal data into forms).

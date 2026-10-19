---
name: wegmans-grocery-order
description: Katherine's home grocery run at Wegmans Wilmington (371 Buckley Mill Rd), built as a pickup order in her connected Chrome session. Use whenever she asks to build, rebuild, restock, or repair a Wegmans order, says "the usual Wegmans run," or asks for groceries at home without naming items. Carries the verified product catalog and the write protocol that keeps the Wegmans cart from silently dropping items. Triggers - "the usual Wegmans run", "Wegmans order", "rebuild the Wegmans cart".
---

# Wegmans Grocery Order (Wilmington)

## Store and fulfillment

- Wegmans Wilmington, 371 Buckley Mill Rd, Wilmington, DE 19807.
- **Pickup**, not delivery. Katherine's account defaults to this store; confirm the store name in the header before adding anything, because Wegmans silently reprices and re-stocks against whatever store is selected.
- Pickup slots appear in the header next to the store name. Do not reserve a slot; she picks it at checkout.
- She is logged in. Never enter payment information or complete checkout. Build the cart, verify it, hand it back.

## The Wegmans cart is unreliable. Read this before adding anything.

This is the operationally important part of the skill. The Wegmans web cart has two failure modes that were observed directly on 2026-08-06, and both are silent: the interface reports success while the server discards the write.

**Failure mode 1: dropped writes.** Rapid successive clicks on the add-to-cart control are accepted by the page and animated as if they landed, but the server records only a fraction of them. In the observed instance, six clicks spaced three seconds apart produced a single unit increase. The header cart count is the only trustworthy signal; the button animation is not.

**Failure mode 2: spontaneous shedding.** A cart that was verified complete at 96 units and $415.62 was found at 69 units and $358.53 on a later reload, with no action taken in between. Twelve product lines vanished entirely or partially. This is server-side loss, not a mis-click.

### Write protocol

1. Add in small batches. Three to four clicks maximum, then stop.
2. After each batch, read the cart count in the page header and compare it against the expected count. The count is authoritative.
3. If a batch of N clicks yields fewer than N units, **stop immediately**. Do not retry, and do not increase the click rate. The service is degraded and further writes will compound the damage. Report the degradation to Katherine and offer to resume later, rather than continuing to hammer.
4. Before declaring the cart finished, reload it twice with at least ten seconds between reloads and confirm the unit count and subtotal are identical both times. A single clean read is not sufficient evidence of stability.
5. Record the final unit count and subtotal in the handback. These two numbers are the checksum that makes the next session's audit cheap.

### Audit protocol

When repairing or verifying an existing cart, the unit count and subtotal together identify the gap faster than a line-by-line walk. Compute the expected count from the catalog below, diff against the header, then locate the specific missing lines.

Use the `find` tool against the cart page to query several product names at once rather than scrolling and screenshotting the whole cart. One caution: `find` returns hits from the "My Items" recommendation rail alongside genuine cart lines, and the two are visually similar in its output. A product appearing only as a My Items tile is **not** in the cart. Confirm anything ambiguous by its quantity control, which exists only on real cart lines.

## Standing catalog

Quantities are the 2026-08-06 baseline, which was a large batch-cooking and freezer stock-up rather than a weekly shop. Treat the product strings as verified and the quantities as a starting point to confirm with Katherine.

Product names below marked **[verified]** were resolved on the live site and add correctly. Names marked **[unverified]** were in the cart but their exact catalog string was not captured; search and confirm before adding.

### Produce

| Product | Size | Qty |
|---|---|---|
| Wegmans Mixed Peppers, 3 Pack **[verified]** | 16 oz | 1 |
| Wegmans Onions, Yellow **[verified]** | 2 lb | 1 |
| Red Onions, bulk **[verified]** | ~0.45 lb | 1 |
| Wegmans Cleaned & Cut Microwaveable Broccoli Florets **[verified]** | 12 oz | 2 |
| Wegmans Sliced Baby Bella Mushrooms, FAMILY PACK **[verified]** | 20 oz | 1 |
| Wegmans Baby Gold Potatoes **[verified]** | 24 oz | 1 |
| Wegmans Trimmed Green Beans, FAMILY PACK **[verified]** | 32 oz | 1 |
| Green Squash (Zucchini), bulk **[verified]** | ~0.55 lb ea | 4 |
| Wegmans Cherry Tomatoes **[verified]** | 1 pint | 1 |
| Wegmans Avocados, Bagged, FAMILY PACK **[verified]** | 4 ct | 1 |
| Wegmans Organic Baby Spinach, FAMILY PACK **[verified]** | 11 oz | 3 |
| Wegmans Lemons, Bagged **[verified]** | 32 oz | 1 |
| Wegmans Limes, Bagged **[verified]** | 32 oz | 1 |
| Bulk Garlic **[verified]** | ~0.2 lb ea | 3 |
| Wegmans Organic Ginger **[verified]** | 3 oz | 1 |
| Wegmans Apples, Bagged **[unverified — confirm variety]** | 3 lb | 1 |

### Fresh herbs

| Product | Size | Qty |
|---|---|---|
| Fresh Cilantro (Corriander) **[verified]** | 1 each | 2 |
| Fresh Dill **[verified]** | 1 each | 1 |
| Italian Parsley **[verified]** | 1 each | 1 |
| Wegmans Basil **[verified]** | 2 oz | 1 |
| Green Onions (Scallions) **[verified]** | 1 each | 1 |

### Protein

| Product | Size | Qty |
|---|---|---|
| Wegmans Organic Chicken Bone Broth **[verified]** | 32 fl oz | 12 |
| Wegmans Frozen Farm Raised Atlantic Salmon, FAMILY PACK **[verified]** | — | 3 |
| Wegmans Solid White Albacore Tuna in Water **[unverified — confirm pouch vs can]** | 3 oz | 4 |
| Rotisserie or whole chicken **[unverified]** | — | 2 |
| Eggs **[unverified — confirm size and count]** | — | 1 |
| Tofu **[unverified — confirm firmness]** | — | 2 |

Bone broth is the single largest line in the order and the one most often lost to shedding. Add it first, in batches of three, and verify after each batch.

### Frozen

| Product | Size | Qty |
|---|---|---|
| Wegmans Organic Frozen Riced Cauliflower **[verified]** | 16 oz | 4 |
| Wegmans Frozen Mixed Berries, FAMILY PACK **[verified]** | — | 2 |
| Mukimame (shelled edamame) **[unverified]** | — | 2 |

### Grains and legumes

| Product | Size | Qty |
|---|---|---|
| Wegmans Jasmine Rice **[unverified — confirm size]** | 5 lb | 1 |
| Wegmans Organic White Quinoa **[unverified — confirm size]** | 32 oz | 1 |
| Wegmans Organic Red Lentils **[unverified — confirm size]** | 16 oz | 1 |
| Wegmans Cannellini Beans **[verified]** | — | 1 |

### Pantry and canned

| Product | Qty |
|---|---|
| Wegmans Original Unsweetened Almondmilk **[verified]** | 3 |
| Wegmans Organic Unsweetened Coconut Milk, Light **[verified]** | 1 |
| Wegmans Crushed Tomatoes **[verified]** | 1 |
| Wegmans Organic Italian Classics Marinara Pasta Sauce **[verified]** | 1 |
| Wegmans Guacamole, Medium Mini, 8 oz **[unverified]** | 2 |
| Bob's Red Mill Starch/Flour, Premium Quality, Arrowroot **[verified]** | 1 |
| JFC Sesame Seed, White, Premium Roasted **[verified]** | 1 |
| Wegmans Organic Ready To Eat Chia Seeds **[verified]** | 1 |
| Wegmans Organic Seasoning, Powder, Curry **[verified]** | 1 |

### Storage and household

| Product | Qty |
|---|---|
| Wegmans Small Slider Top Freezer Bags, Quart Size **[verified]** | 1 |
| Wegmans Large Press & Close Freezer Bags, Gallon, 28 ct **[unverified]** | 1 |
| Glad Take-Aways Meal Prep Containers, 38 oz, 7-pack **[unverified]** | 1 |
| Glad Take-Aways Food Storage Containers, 38 oz, 20 ct **[unverified]** | 1 |
| Expo Dry Erase Markers, Assorted Ink, Low Odor **[verified]** | 1 |
| Ball Labels, Dissolvable **[verified]** | 1 |
| Tide Free & Gentle Liquid Laundry Detergent **[verified]** | 1 |
| Hand or dish soap **[unverified]** | 2 |

### Spices and condiments — pending

Katherine asked for the full spices and condiments set on 2026-08-06, but the cart failure prevented adding them and none of these product strings have been resolved on the site. Ask her to confirm the list before the first run that includes them, then record the verified strings here.

### Excluded by standing decision

- **Collagen peptides.** Removed deliberately. Do not re-add unless she asks.

## Constraints

1. Single store, single pickup. There is no multi-store tradeoff here as there is in Panama.
2. Product-name fidelity matters more than price. Wegmans stocks several near-identical variants (FAMILY PACK versus standard, organic versus conventional, pouch versus can), and substituting silently produces the wrong quantity of food for a batch-cooking week. When the exact catalog string is not available, say so rather than picking the closest match.
3. Flag anything out of stock explicitly with a one-line reason. Do not force a substitute.

## Output format each time

1. Final cart unit count and subtotal, both confirmed stable across two reloads.
2. Any lines that could not be added, each with a reason.
3. Any substitutions made, each with a reason.
4. A note that Katherine completes slot selection, payment, and checkout herself.
5. If the service degraded mid-run: what was completed, the exact remaining list with quantities, and a recommendation on when to resume.

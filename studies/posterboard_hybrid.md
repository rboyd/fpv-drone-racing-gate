# Posterboard inserts with printed framing: comparison study

2026-09-17. This study retains the 2700 × 2700 mm outer face, 1500 × 1500 mm opening, single PVC backing frame, corner braces and both base options. It does not change the committed Blender design. [Interactive comparison](posterboard_hybrid.html) · [CSV](posterboard_hybrid.csv) · [Exact layouts/assumptions](posterboard_hybrid.json)

**Recommendation:** test two constructions: **600 × 450 mm paper pieces with a middle retaining rib** for lowest material/handling cost, and **300 × 250 mm inserts** for smaller, more easily replaced panels. Avoid choosing 300 mm squares by habit: they waste nearly half the purchased paper. Making every insert fit the printer's bed is unnecessary; only the printed rails need to fit.

## Stock and scope

Hobby Lobby lists a single **22 × 28 inch cardstock sheet for $0.99**. Dimensions are **558.8 × 711.2 mm**. Its thickness and outdoor durability are not specified, so those require an actual sample. This is not foamboard. [Hobby Lobby listing](https://www.hobbylobby.com/Art-Supplies/Project-Supplies/Poster-Projects/Poster-Board---22-x-28/p/81118411)

Face area is **5.04 m²**; one stock sheet is about 0.3974 m². The area-only minimum is **13 sheets / $12.87**. Practical repeatable rectangular cuts in this study use 17–28 sheets. These are verified layouts, not a proof of the global optimum over every possible nesting pattern.

## Same rail construction, different panel sizes

The table assumes shared printed rails between adjoining panels, PETG at 1.28 g/cm³, **28 mm² of plastic cross-section per rail**, $20/kg filament, and $0.99 sheets. It includes 20% additional rail mass for joints/nodes, 250 g for new PVC mounting clips and 10% printing waste. These are design allowances, not slicer results. [PETG density](https://eu.store.bambulab.com/en-mt/products/petg-hf?variant=49068714557788)

| Nominal panel size, mm | Paper pieces | Stock sheets | PETG estimate | Consumed paper + filament | Purchase whole spools + paper |
|---|---:|---:|---:|---:|---:|
| 600 × 450, perimeter only | 20 | 19 | 1.64 kg | $52 | $59 / 2 spools |
| **600 × 450 + middle retaining rib** | **20** | **19** | **1.78 kg** | **$54** | **$59 / 2 spools** |
| 300 × 450 | 40 | 19 | 2.04 kg | $60 | $79 / 3 spools |
| 300 × 300 | 56 | 28 | 2.26 kg | $73 | $88 / 3 spools |
| **300 × 250** | **68** | **17** | **2.43 kg** | **$65** | **$77 / 3 spools** |
| 300 × 200 | 84 | 17 | 2.66 kg | $70 | $77 / 3 spools |
| 150 × 150 | 224 | 19 | 3.85 kg | $96 | $99 / 4 spools |

**Costs are for the new face system only:** paper, printed rails, joints and new PVC mounts. Existing PVC, eight brace connectors, feet, anchors/ballast, labor, power, coatings, tax and shipping are excluded. Reusing existing mounting clips may save some filament. Consumed cost allocates partial spools; purchase cost buys whole 1 kg spools. Small estimate changes can cross a spool threshold, especially the 2.04 kg option.

Rail section is the main uncertainty. At **20–36 mm²** instead of 28, the ribbed large-panel version spans **1.39–2.17 kg**, and the 300 × 250 version **1.82–3.05 kg**, with the same other allowances. The interactive page lets you vary rail size and prices. A 28 mm² section is an illustrative material budget for retaining lips plus a rear stiffening web; there is no engineered rail cross-section yet. Solid-equivalent area, not the external bounding rectangle, determines mass.

## Verified cutting layouts

All dimensions below are nominal blanks. Final insert clearance can trim them slightly smaller; the future design must accommodate the web, edge capture and exact gate perimeter/opening without adding oversize paper beyond these blanks.

- **600 × 450:** orient the 600 mm side along the sheet's 711.2 mm side. One full piece per sheet. Eighteen full pieces plus two 600 × 150 end fillers from one additional sheet: 19 sheets total.
- **300 × 450:** two per sheet, occupying 450 × 600 mm. Thirty-six full pieces plus four 300 × 150 fillers from one additional sheet: 19 sheets.
- **300 × 300:** only two per sheet; two across would require 600 mm, exceeding 558.8 mm. Fifty-six pieces use 28 sheets.
- **300 × 250:** four per sheet in a 500 × 600 mm rectangle. Sixty-four full pieces use 16 sheets; four 300 × 200 end fillers use one more. Total: 68 pieces, 17 sheets.
- **300 × 200:** five per sheet using mixed orientation: a 300 mm-wide column with three 200 mm-high pieces, alongside a 200 mm-wide column with two 300 mm-high pieces. Eighty-four pieces require 17 sheets, with one spare position.
- **150 × 150:** twelve per sheet, three across and four along. Two hundred twenty-four pieces require 19 sheets, with four spare positions.

Gate layouts use two 2700 × 600 top/bottom strips and two 1500 × 600 side strips. Rotation and a few end fillers make them cover the exact ring without overlaps. All stock rectangles are checked for fit and pairwise overlap. Colored coating/grain may favor one orientation; verify whether mixed rotation matters before adopting the 300 × 200 pattern.

## Why middle ribs are attractive

An unbraced 600 × 450 panel offers the lowest framing cost but the largest unsupported paper area. A rib halfway across the 600 mm dimension creates roughly **two 300 × 450 support bays** while retaining a single piece of paper. Across the gate this adds **8.4 m of light ribs**; at an assumed 10 mm² rib section, the total estimated filament increase is only about **142 g**, including allowances.

That is cheaper than cutting the paper into two inserts and adding another complete retaining rail. The rib must attach to the frame and lightly capture the paper at several points so it supports both wind directions. Merely touching the rear of loose paper is not equivalent. The existing PVC follows this middle region, which may allow integrated short supports; that attachment arrangement remains to be designed.

Smaller panels should flex and flutter less under comparable support conditions and cost less to replace individually. But extra rail joints can introduce play, so “more frames” does not automatically make the whole gate more stable. Paper grade, humidity, rib depth and joint rigidity can dominate nominal panel size. These are qualitative comparisons, not deflection or wind ratings.

## Printable parts and assembly effort

1. **Shared edge rail:** rear ledges support two adjacent inserts, with a raised spine behind. Removable front keepers retain the paper without requiring it to slide through a completed closed frame. Outer/inner boundaries use one-sided rails.
2. **Straight connectors and corner/T/cross nodes:** keyed alignment plus positive retention; joint release from the rear permits repair. Rail bodies up to 150 mm with compact joints can stay within an approximately 170 mm envelope on the A1 Mini.
3. **PVC saddles:** attach reinforced rail nodes to the existing 33.4 mm OD main pipe. Paper itself should not be the structural link between the printed grid and PVC.
4. **Optional middle ribs with paper retainers:** narrow supports instead of another full framed seam.

Approximate rail/rib body counts at a 150 mm maximum body length: **248** for the ribbed large-panel version, **342** for 300 × 250, and **504** for 150 × 150. Nodes, mounts and front keepers are additional. Several slender rails can print together; these are part counts, not print-job counts. Long rails may need more depth/stiffness than this first estimate allows.

Independent removable picture-frame cassettes are easier to handle separately, but duplicate each shared edge. For 300 × 250 panels, total perimeter rises from **45.6 m shared** to **74.4 m separate**—about **63% more rail length**. The table intentionally uses the more economical shared-grid architecture. One-piece 150 mm frames could reduce loose rail assembly, at the expense of duplicated edges and more material.

## Dry-weather durability and comparison with Coroplast

The $0.99 item is cardstock and has no stated weatherproof rating. Treat it as an indoor/dry-weather, replaceable skin until tested; edge capture does not waterproof it. Wet grass/dew, damp storage and a light shower are relevant to the outdoor setup. Lamination/sealing adds unpriced material and labor. Purpose-made plastic posterboard is a separate option; the manufacturer describes UCreate plastic posterboard as waterproof, but it requires a separate current price and thickness comparison. [Manufacturer catalog](https://dixonticonderogacompany.com/wp-content/uploads/2022/01/2022_Dixon-Tic_Pacon-Prod-Catalog_01.20.22.pdf)

The hybrid retains a nearly closed 5.04 m² face, so it does **not** inherit the wind reduction of the earlier open-lattice idea. Keep the existing bracing and appropriate anchoring/ballast. The printed rail mass estimates also exclude the paper's own weight; weigh a sample to establish total gate mass.

Current Coroplast sheet allocation is about **$60.94 before its attachment prints**. A hybrid at $54–65 consumed face-system material could be competitive, but the potential savings are modest relative to hundreds of printed parts. Local availability, small replacement inserts and color options may be stronger reasons to choose it than first-build cost alone.

**Next decision:** prototype one ribbed 600 × 450 panel and one 300 × 250 panel, using the actual $0.99 stock. Compare two-direction hand loading, flutter, crease resistance, insertion/replacement, humidity response, and slicer mass/time. Then choose the panel size before detailing the complete frame.

Recalculate with `python3 studies/estimate_posterboard_hybrid.py`, then `python3 studies/make_posterboard_study.py`.

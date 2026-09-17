# Printed PVC-mounted FPV gate: first-pass material study

2026-09-17. Existing symmetric Coroplast design is committed at `a584819`; the working tree was clean when this study began. No gate geometry or fabrication files have been changed for this study.

**Finding:** a modular printed face is possible in principle, but one or two 1 kg spools cannot make a convincingly rigid, closed replacement for the current broad face. A very open lattice is the promising low-filament option: approximately **3 spools for a face with its new clips/joiners**, or **3–4 spools as an initial whole-gate printed-parts budget** while retaining the PVC. Strength and visibility remain untested.

## Scope and arithmetic

Keep the existing 2700 × 2700 mm outer dimension, 1500 × 1500 mm opening, single PVC backing square, corner braces, feet and anchoring. “Entirely printed” means the visible face and its connectors replace Coroplast; it does not mean printing the PVC or ballast.

Projected face area = 2.7² − 1.5² = **5.04 m²**. This counts one sheet area, not both exposed surfaces. Bambu PETG HF density is **1.28 g/cm³**. A spool is assumed to contain **1000 g of filament**, excluding the empty spool. PETG is the study material; changing to PLA would not deliver the several-fold weight reduction needed. [Manufacturer density](https://eu.store.bambulab.com/en-mt/products/petg-hf?variant=49068714557788)

**Face mass (kg) = 5.04 × solid-equivalent thickness (mm) × 1.28 = 6.4512 × thickness.**

One spool contains 781.25 cm³, enough for only **0.155 mm** over the whole face. Two spools give **0.310 mm**. These are theoretical sheets without edges, ribs, joins, clips, waste or retained brace connectors. A 0.2 mm face is a single-layer film at a 0.2 mm layer height; a 0.4 mm face is only two layers. Neither is an established durable gate panel.

| Construction | Face plastic | Minimum whole 1 kg spools | Spool purchase at assumed $20/kg |
|---|---:|---:|---:|
| 0.2 mm film | 1.29 kg | 2 | $40 |
| 0.4 mm thin sheet | 2.58 kg | 3 | $60 |
| 0.8 mm sheet | 5.16 kg | 6 | $120 |
| 1.0 mm sheet | 6.45 kg | 7 | $140 |
| 4 mm sandwich: two 0.4 mm skins, 10% of remaining core | 7.23 kg | 8 | $160 |
| 4 mm solid | 25.80 kg | 26 | $520 |

**Table excludes tile sidewalls, connectors, PVC clips, retained brace joints, purge, brims and failed prints.** $20/kg is a planning assumption, not a live offer; multiply costs by 0.75–1.25 for $15–25/kg. Electricity, printer wear and labor are excluded.

“10% infill” does not mean 10% of an entire closed plate. The two skins alone in the sandwich consume 5.16 kg, before its 2.06 kg core and any perimeter walls. This illustrative sandwich is not a slicer prediction or a printable bridge design. Standard 4 mm Coroplast is corrugated, not a solid 4 mm slab; the 25.8 kg example is deliberately the solid-print upper comparison, not an estimate of Coroplast weight.

## Open-lattice alternative

Use 150 × 150 mm module pitch. The gate is an **18 × 18 grid with a 10 × 10 central hole: 224 modules**. A flat module plus compact connectors fits within the A1 Mini's 180 × 180 mm plate; only one such tile fits flat per plate. Integrated tabs would need to remain within about 170 × 170 mm to leave brim space. [A1 Mini specifications](https://cdn1.bambulab.com/documentation/quick-start-f507128172bdf/Quick%20start%20guide%20-%20A1%20mini-EN.pdf)

An arithmetic example uses each tile's own 2 mm-wide perimeter plus two crossing 2 mm-wide ribs, all **3 mm deep**. It has four open windows. Its projected plastic area is 1764 mm² out of 22500 mm²: **7.84% plastic, 92.16% open**. Adjacent tile borders are counted twice, so the calculation does not hide the weight of duplicate seam rails.

- Bare lattice face: **1.517 kg**, about 6.77 g per tile.
- Allow **0.50 kg** for new joining features/keys and PVC mounting clips; this is a design allowance, not modeled hardware.
- Add 10% for brims, purge and waste: **2.219 kg**, requiring **3 spools / $60** at the assumed price.
- If also printing the existing eight brace connectors from scratch, their *solid CAD volume* adds about **0.646 kg PETG** before waste. Total becomes about **2.93 kg** with the same waste allowance: three spools is tight, so **3–4 spools / $60–80** is a more useful first-build budget. Actual infill/perimeters and supports must be sliced later. Current face saddles/washers are replaced by the new clip allowance, not counted again.

At a 3 mm lattice depth, reserving 0.50 kg for new joints/clips and 10% waste limits coverage to about **2.1% for one spool**, **6.8% for two**, or **11.5% for three**, before the retained brace connectors. Thus two spools could be a target only for a lighter, sparser face with very efficient joints; one spool is an extreme skeleton or a narrower-border concept. Neither is a proven equivalent to the current gate.

A 92%-open face will look much less solid through FPV goggles. It would likely reduce wind loading, but the reduction cannot be treated as equal to the open-area fraction without testing. Thin ribs and snap roots also need impact and repeated assembly tests. A narrow, strongly colored outline could be a different low-material direction, but it changes the current 600 mm border requirement.

## What the parts could look like

See `printed_gate_concept.svg`: a schematic, not fabrication geometry.

1. **Standard tile:** flat square perimeter with open windows/cross ribs; alternatively a thin face skin on a shallow rib frame. Recessed edge sockets keep the tile pitch consistent. The four-tile border is 600 mm wide. No special diagonal corner panels are needed on this square grid.
2. **Replaceable click key:** short bowtie/dovetail-shaped bridge with a spring detent. The dovetail carries in-plane load; the detent retains the key against falling out of the vertical gate. Give it a release tab so broken parts can be replaced.
3. **PVC mounting clip:** split C-shaped saddle around the actual **33.4 mm OD** main pipe, with a locking latch and a flat dovetail/tab that mates with a tile's reinforced rear boss. Mounting tiles transfer load directly to PVC. A backup tie slot could retain a clip if the latch wears.
4. **Optional edge insert/cap:** smooths exposed sockets on the inner opening and outer perimeter; included in the connector allowance, not a dimensioned part yet.

The referenced Clickfinity implementation uses flexible latch tongues for bins and separate bowtie keys between plates. Its keys are retained by the supporting bench; a vertical, vibrating gate would need its own positive key retention. We can borrow the modular joining idea, not assume a desktop organizer joint is adequate for this gate. [Clickfinity implementation and joining mechanism](https://github.com/IamMrCupp/clickfinity-openscad/blob/main/README.md)

There are **392 neighboring tile seams**, potentially two locks per seam. Together with **224 flat tile print jobs**, that is a substantial assembly and printing commitment even if the filament price is competitive. Multi-part plate strategies or printing orientations could be examined later; no print-hour estimate is claimed here.

## Decision before detailed design

For a closed face, expect roughly **7–10+ spools** once reasonable thin skins, connections and retained brace joints are counted, depending on thickness and construction. For an open face, **3–4 spools** is a plausible material budget worth testing, not a strength promise. The current Coroplast face stock is about **$60.94 per gate** at batch allocation, so printed lattice material is in the same price region but entails far more printer/assembly time and lower visual coverage.

The next useful step would be two joined lattice tiles and one PVC clip to test snapping, flex, visibility and actual slicer mass. A full 224-tile design should follow those results. This study deliberately stops before that design stage.

Recalculate with `python3 studies/estimate_printed_gate.py`. CSV/JSON retain all assumptions and arithmetic.

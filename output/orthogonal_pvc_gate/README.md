# Three-type PVC gate / friction-fit iteration

The gate now uses **one elbow, one cross and one magnetic sleeve design**. All pipe connections and sleeve positioning use friction. Straight PVC links join the inner and outer perimeters into a rectangular grid. The earlier corded iteration remains in ../pvc_paper_gate for comparison.

[Blender model](Orthogonal_PVC_Gate.blend) · [Visual index](index.html) · [Assembly PDF](Orthogonal_Gate_Assembly.pdf) · [Complete kit](Orthogonal_PVC_Gate_Kit.zip)

## Required parts and actual slicing estimates

| Part | Single gate | Two-level total | Print bounds, mm |
|---|---:|---:|---|
| ELBOW | 4 | 4 | 133.314 x 133.314 x 53.345 |
| CROSS | 12 | 20 | 136.627 x 136.627 x 53.345 |
| MAG_SLEEVE | 48 | 80 | 20.0 x 86.75 x 53.345 |

There are **3 unique required printed types**. Fit gauges are tooling. PAPER_PAD is optional. Quantities above exclude both. The same cross serves four-way and three-way junctions; leave an unused socket empty. Elbows are only at the four overall outside corners. Inner opening corners use crosses because their other two ports connect directly to the outer perimeter.

| Configuration | Printed pieces | PETG kg | Print hours | Plate runs | 10-ft PVC sticks / cost | PVC + PETG subtotal |
|---|---:|---:|---:|---:|---|---:|
| single | 64 | 2.528 | 102.2 | 23 | 8 / $48 | $98.57 |
| split_s | 104 | 4.031 | 163.3 | 36 | 14 / $84 | $164.63 |

Your PVC price is $6 per 10-ft stick. PETG is an assumed $20/kg, not a supplier quote. Subtotals cover the face skeleton only; magnets, paper, adhesive and a ground-support system are additional. Print estimates come from local Bambu Studio slicing: A1 Mini, 0.4 mm nozzle, 0.20 mm layers, Generic PETG, four walls, 20% infill, no supports, no brim. Failed prints and manual work are not included. Three 1-kg spools cover the single with 10% allowance; the double requires five spools (4.434 kg with 10% allowance).

This simplifies assembly and inventory but **does not lower the modeled material or printer time versus the previous corded version**. That single used 5 types, 62 pieces, 1.759 kg, 71.0 hours and six PVC sticks ($71.17 PVC + PETG). This single uses 3 types, 64 pieces, 2.528 kg and 102.2 hours ($98.57). Universal crosses print unused sockets at the perimeter, and straight seam links consume more PVC. In return there is no tying, cord routing, cord tensioning or special seam saddle.

## Geometry and connection details

Single outside dimensions: **2700 x 2700 mm**. Stacked: **2700 x 4790.4 mm**, before a base. Each opening is **1480.8 x 1480.8 mm**. All paper bands, including the shared divider, are **609.6 mm / 24 inches** wide.

The PVC axes sit **75 mm inside the paper boundary** and **24 mm behind its face**. Opposing pipe axes across a band are 459.6 mm apart. Each socket mouth is 65 mm from its fitting center, leaving the unused perimeter socket behind paper with 10 mm to spare. Pad centers offset 57 mm from pipe axes put magnets 18 mm inside the paper edges. The model checks every printed vertex in front projection and every front magnet center against the paper rectangles. PVC follows the same concealed grid. Structure may be visible from an oblique view.

Socket engagement is **30 mm**, against a stop **35 mm from the fitting center**. Nominal pipe OD is 33.4 mm. The provisional friction bore is **33.5 mm**; printed fit must be selected using real pipe. Nominal socket walls are 4 mm, central webs are 32 mm wide and 12 mm thick, and magnetic arms have 20 mm-wide continuous 3 mm flanges with thicker roots. The peaked roof is retained for support-free horizontal printing. Magnet windows alone retain the requested 0.4 mm skin.

MAG_SLEEVE engages 16 mm of pipe. Its friction fit locates the magnet and resists rotation; it has no separate fastener. Leave accepted sleeves on their marked pipes during transport. All three production meshes fit the A1 Mini. The largest is CROSS at 136.627 x 136.627 x 53.345 mm; supplied plates maintain at least 5 mm bed margin.

## First print and fit test

[FIRST_FRICTION_FIT_A1Mini_PETG.3mf](sliced/FIRST_FRICTION_FIT/FIRST_FRICTION_FIT_A1Mini_PETG.3mf): **126.20 g / 4.97 hours**. Five pieces: one 33.5 mm-bore ELBOW, full 30 mm-long FIT_333 / FIT_335 / FIT_337 coupons, and one optional PAPER_PAD. The three samples are 33.3 / 33.5 / 33.7 mm bores, ordered from front to rear on the right side of the plate. Label them before removing them. The coupons have no end stop; test 30 mm engagement. Their shape and print orientation match the sockets.

1. Measure and deburr an actual pipe offcut. Test each coupon by hand; choose the fit that seats the full 30 mm and releases deliberately while resisting pull-out and rotation. Do not hammer a tight sample onto the pipe. If none meets that behavior, revise the bore rather than accepting a loose or forced fit.
2. Test both elbow sockets to their stops, with a 30 mm insertion mark on each pipe. Check that the elbow stays square and its paper face stays flat. Repeat fitting and release at least 20 times; check for cracking, whitening, increasing looseness and movement past witness marks.
3. The supplied elbow and production files use 33.5 mm. If another sample fits better, regenerate with PVC_FIT_BORE set to that diameter and re-slice before production. Do not scale an STL; that also changes centers, magnet pockets and cut lengths.
4. Then print [CROSS_AND_SLEEVE](sliced/CROSS_AND_SLEEVE/CROSS_AND_SLEEVE_A1Mini_PETG.3mf): **146.39 g / 5.70 hours**. It tests all four socket directions and the shorter sleeve. A coupon result alone does not prove sleeve grip.
5. For a two-foot band demonstration, join the elbow to the cross with one **389.6 mm** pipe and place the sleeve at **194.8 mm from its cut end**. Orient both printed faces into the same plane. The elbow's outward pad and the cross's opposite-side pad span the paper band with 18 mm edge margins. Lay a 609.6 mm-wide paper strip over them and mark the 18 mm margins. Use six magnets for three grip sites, adding a short perpendicular pipe offcut to each fitting to test square alignment.
6. Bond rear magnets after checking polarity; let the adhesive cure. Test magnetic grip with the real paper, both a bare front magnet and the optional front pad. Pull/rotate the sleeve, flex the paper gently and repeat assembly. After that passes, build one short square grid cell (four 389.6 mm pipes, one elbow, three crosses) flat and check racking and joint withdrawal before producing the complete gate.

The fit and handling tests above are prototype checks, not a rated wind/load test. The first two test plates are separate from the production queue below; accepted production pieces from them can count toward the final BOM.

## Full production queue

| Recipe | Single runs | Double runs | Pieces/run | g/run | h/run |
|---|---:|---:|---:|---:|---:|
| ONE_ELBOW | 4 | 4 | 1 | 68.47 | 2.69 |
| ONE_CROSS | 12 | 20 | 1 | 132.59 | 5.07 |
| BATCH_MAG_SLEEVE | 6 | 11 | 7 | 96.74 | 4.46 |
| TAIL_MAG_SLEEVE_6 | 1 | 0 | 6 | 82.93 | 3.85 |
| TAIL_MAG_SLEEVE_3 | 0 | 1 | 3 | 41.50 | 2.07 |

Each CSV queue links to the corresponding prepared PETG 3MF. BATCH_MAG_SLEEVE holds seven identical sleeves; it is one part type. The six- and three-piece tails avoid overprinting. All plates passed the bed-clearance, non-overlap and support-off slicing checks. Open prepared 3MFs as projects and confirm your actual filament profile before printing. No job has been sent to a printer.

## PVC cuts and assembly

Only **two finished pipe lengths** are used: **389.6 mm** and **1560.8 mm**. The single needs **16 short + 8 long**; the double needs **24 short + 14 long**. Their respective center spacings are 459.6 and 1630.8 mm, because the two stop offsets add 70 mm. The longest loose pipe is 1.561 m.

The stock ledgers reserve 10 mm total end allowance per stick and 3 mm kerf per cut. Two long pieces cannot fit one 3048 mm stick, so eight long pieces require at least eight sticks; fourteen require fourteen. All short pieces fit alongside those long pieces. Label cuts using PVC_Cuts.csv; node coordinates and Assembly_Map.svg use the front view, measured from the bottom-left paper corner.

1. Print and qualify the selected fit, then cut, deburr and label all PVC. Mark 30 mm engagement at both ends. Mark sleeve stations from Sleeve_Positions.csv before covering the cut starts with fittings.
2. Slide **one sleeve onto each short pipe**, centered at 194.8 mm from its cut start. Put **four sleeves on each long pipe** at **291.16, 617.32, 943.48 and 1269.64 mm** from the cut start. Rotate them to the direction shown in Blender; their flat paper faces must be coplanar with the fitting faces. The sleeve positions are clear of every socket.
3. Work on a flat surface with all paper-facing surfaces down. Build each horizontal row from four nodes and three pipes in **short / long / short** order. The single has four rows at y = 75, 534.6, 2165.4 and 2625 mm. Only the ends of its bottom/top row use elbows; every other node is a cross. A node's unused cross socket simply stays empty.
4. Place four vertical pipes into each row, then press the next complete row onto them together, keeping the mating sockets aligned. Single vertical gaps use **short / long / short** pipes, from bottom to top. Seat all four connections evenly to their marks; avoid levering one partially engaged socket to close another. Check equal diagonals and coplanar paper pads as each row goes on.
5. Populate only the magnet pockets shown by Magnet_Positions.csv. The cross has four available pads for symmetry, but not all are used at every node. A straightedge across the fixed fitting pads helps clock the sliding sleeves; mark accepted positions on the pipe for repeat assembly.
6. Install the paper as described below. For transport, remove the paper and separate rows/long members as needed, pulling at socket bodies. Leave sleeves on their labeled pipes. Fully assembled horizontal rows are about 2.7 m wide, so remove an end stub or separate at an inner cross to remain within the earlier approximately 2.15 m transport size.

## Paper and magnets

Use untrimmed 609.6 mm roll width. Single: **two 2700 mm horizontal bars and two 1552.8 mm side inserts**. Double: **three 2700 mm bars and four 1552.8 mm inserts**. Each side insert overlaps a horizontal bar by **36 mm at each end**. Consumption is 8.5056 m per single or 14.3112 m per double: three singles or two doubles from a 100-ft roll, before cutting waste.

Lay horizontal bars first, then side inserts. Align paper edges 18 mm beyond the corresponding magnet centers. The straight short PVC links carry magnets along the overlap seams, so no suspended seam parts are needed. Use **72 magnet pairs / 144 magnets** for a single, or **116 pairs / 232 magnets** for a double, all 6 mm diameter x 2 mm thick. Long-span sleeve spacing is 326.16 mm; grip at that spacing needs testing with the actual roll.

The stack is **rear magnet -> 0.4 mm frame plastic -> paper -> bare front magnet**. Frame pockets remain 6.3 mm diameter and are rear-loaded. Secure rear magnets with a compatible adhesive; the pocket clearance is not a guaranteed press fit. Check polarity before bonding. Only populate selected pockets. The bare front magnets align directly with the fixed rear magnets. The existing PAPER_PAD is an optional handle/protector around a front magnet; it adds another 0.4 mm skin and is excluded from the BOM, mass and time totals.

## Extend to the two-level gate

Reuse **every existing pipe without cutting**, all 48 sleeves, all 12 crosses and all four elbows. Add **8 CROSS + 32 MAG_SLEEVE**, **8 short + 6 long PVC cuts**, and **44 magnet pairs / 88 magnets**. The additional PVC needs six more 10-ft sticks. Add one 2700 mm paper bar and two 1552.8 mm side inserts.

Lay the single frame flat and remove its paper. Detach its complete top horizontal row (both elbows, both crosses, all three pipes and their sleeves) from the four short verticals below it. Move that complete row upward to the new top height, y = 4715.4 mm. This preserves its populated magnet pads and sleeve directions together; label its new node positions using the double map.

Build a replacement all-cross row at the old top height, y = 2625 mm, using four new crosses and short / long / short pipes. It becomes the upper row of the shared divider. Add four long verticals to a second new all-cross row at y = 4255.8 mm, also using four new crosses and short / long / short horizontal pipes. Add four short verticals above it and seat the retained top row onto them. This accounts for all eight additional crosses, six long pipes and eight short pipes. No special divider fitting is required.

The divider's two pipe rows are y = 2165.4 and 2625 mm: **459.6 mm axis spacing**, supporting the same 609.6 mm band as every other border. Use the double assembly and magnet maps when relocating/populating magnets at the former top edge.

## What is checked and what remains

Digital checks cover connected manifold masters, actual A1 Mini placements, no overlapping plate parts, no generated supports or slicer warnings, exact queue quantities, socket-free sleeve positions, backing-pocket alignment, front concealment, orthogonal PVC, and reuse of all single-height pipe lengths on extension. Nine Blender scenes show both finished faces, both PVC frames, the three part types, connections, magnetic stack, first test plate and shared divider.

This is a **friction-fit face-frame prototype**. Actual pull-out, sleeve rotation, PETG wear, paper grip and frame racking still require physical tests. Feet and ground restraint for soil or hard surfaces have not been sized in this iteration; the 4.79 m frame is not yet a qualified freestanding outdoor obstacle. No cord is included in this design.

## References and regeneration

- [FORMUFIT PVC sizing](https://formufit.com/pages/pvc-101) explains nominal pipe size versus OD; nominal 1-inch PVC is approximately 1.315 inches outside diameter. Measure the actual pipe used for this print.
- [Prusa modeling guidance](https://help.prusa3d.com/article/modeling-with-3d-printing-in-mind_164135) covers print orientation, overhangs and tolerances. The peaked sockets and proposed clearances are this project's prototype geometry.

Regenerate with scripts/build_orthogonal_pvc_gate.py in Blender, then scripts/slice_orthogonal_pvc_gate.py, scripts/validate_orthogonal_pvc_gate.py and scripts/package_orthogonal_pvc_gate.py. Set PVC_FIT_BORE on the Blender build command to change the bore. The package script uses ReportLab. A changed bore requires rebuilding and re-slicing; the supplied files currently use 33.5 mm.

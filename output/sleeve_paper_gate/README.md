# Integral PVC sleeve gate

This revision replaces the bolted face-to-PVC dock with **one printed RUNG_SLEEVE**. The frame segment, tapered root and closed pipe loop are one connected manifold part. There are **no bolts, nuts, split collars, separate dock tongues or extra cord stays at this attachment**. The existing PVC corner fittings complete the square as requested. The cords that brace the face bays remain.

[Blender assembly](Sleeve_Paper_Gate.blend) opens at the new attachment. See the [bare part](renders/10_SLEEVE_PRINT_FACE.png), [PVC threaded through it](renders/06_INTEGRAL_PVC_SLEEVE.png), [full gate](renders/01_ASSEMBLED_FRONT.png), [assembly PDF](Sleeve_Gate_Assembly.pdf), and [printable kit](Sleeve_Paper_Gate_Kit.zip).

## The new part

- Native print bounds: **133.867 x 49.95 x 78.668 mm**, well inside the A1 Mini's 180 mm cube.
- Designed pipe: **33.4 mm outside diameter** (the nominal 1-inch Schedule 40 PVC already used in this project).
- Trial bore: **34.2 mm** across the circular portion, giving nominal 0.8 mm diametral clearance. This is a sliding fit, not a press-fit clamp.
- Continuous loop wall: **6 mm** nominal; sleeve length along the pipe: **24 mm**.
- Broad root: **68 mm** across the rung and **24 mm** along the pipe, tapering upward into the closed loop. No narrow dock neck or flexible latch carries the sleeve-to-rung connection.
- Pipe center: **46 mm behind the paper**, reduced from 98.9 mm. The pipe's front is 29.3 mm behind the face, giving about 5.1 mm clearance to the modeled bracing-cord envelope.
- The upper opening has a 45-degree peaked roof. Its lower 270 degrees follow a circle; the peak adds clearance above the pipe so the part prints flat on its paper face without support inside a round ceiling. The peak does not key into or tightly clamp the round pipe.
- The existing frame click interface and magnetic D lug are retained. The normal RUNG is also simplified by removing its unused M3 mounting holes.

Use four sleeves per border, sixteen per gate. Six crossmembers per border still consist of three segments each; only the middle segments of crossmembers 2, 3, 4 and 5 become RUNG_SLEEVE. The other fourteen segments per border are plain RUNG.

## First print: frame click test

Start with the separate [four-piece A1 Mini frame test](../first_frame_print/index.html): two identical production EDGE_BRANCH rails and two CLICK_KEY connectors. It tests straight and perpendicular connections using the same parts. The fifth PAPER_PAD is optional on an alternate plate. See its illustrated assembly/test PDF before printing a full bay.

## Subsequent PVC sleeve fit test

**One sleeve:** open [Q_RUNG_SLEEVE_TAIL](sliced/Q_RUNG_SLEEVE_TAIL/Q_RUNG_SLEEVE_TAIL_A1Mini_PETG.3mf). It contains exactly one production sleeve rung: **49.41 g / 140 minutes**. Print it flat in the supplied orientation, deburr the bore's entry edges, and slide a clean, measured PVC offcut through it.

**Combined fit plate:** [T00_SLEEVE_FIT](sliced/T00_SLEEVE_FIT/T00_SLEEVE_FIT_A1Mini_PETG.3mf) contains one sleeve, three short bore gauges, two click keys and one magnetic pad: **7 pieces / 77.13 g / 219 minutes**. The gauges are left-to-right 34.0, 34.2, 34.4 mm as seen from the plate front in Bambu Studio. Mark them before removing them. Their horizontal print orientation matches the sleeve's bore; a short gauge does not prove the fit over the full 24 mm sleeve length.

Use PETG, 0.4 mm nozzle, 0.20 mm layers, **4 walls, 20% infill, no supports, no brim**. These are actual local Bambu Studio slices. All supplied recipes are warning-free. The source STL is [RUNG_SLEEVE.stl](printable/RUNG_SLEEVE.stl). No print job has been submitted.

The pipe should slide by hand through the full sleeve without force or splitting, and the keys should seat and release normally. If 34.2 mm does not fit the actual pipe/printer combination, use the gauges to choose a revised bore and regenerate; do not force the pipe or scale the whole part, which would also change the click geometry. Check the molded lettering, burrs and OD variation along the actual pipe, not only one end. Then assemble a bay and check its behavior on the completed square, including movement, handling and warm-weather relaxation. Physical strength and service life are not yet established.

## What this removes

Each old attachment used a plain rung plus two collar halves, a receiver and a tongue. The new attachment uses one sleeve rung. Across the gate it removes **64 printed pieces, 96 M3 bolts, 96 M3 nuts and 160 M3 washers**. The old three attachment part types disappear; one sleeve-rung type is added. With optional front pads fitted, main-gate printed types fall **10 to 8**, pieces **624 to 560**. Omit all 136 optional PAPER_PAD parts for **424 pieces / 7 types**.

| Current part | Quantity | Print bounds mm |
|---|---:|---|
| EDGE_PLAIN | 64 | 136.314 x 49.95 x 12.0 |
| EDGE_BRANCH | 48 | 136.314 x 76.0 x 29.0 |
| RUNG | 56 | 133.867 x 49.95 x 12.0 |
| CLICK_KEY | 200 | 66.0 x 32.0 x 5.0 |
| PAPER_PAD (optional) | 136 | 24.0 x 24.0 x 3.0 |
| RUNG_SLEEVE | 16 | 133.867 x 49.95 x 78.668 |
| V_BLOCK | 32 | 24.0 x 64.0 x 22.0 |
| CROSS_PLATE | 8 | 70.0 x 70.0 x 6.0 |

The renders show optional front pads fitted. PAPER_PAD is optional throughout the BOM and queue. Per border, omitting its 34 pads leaves 96 pieces. Four borders plus the 40 brace pieces total 424 without pads. The three gauge sizes are optional test pieces and are not gate part types or included in 560. Per border: 16 EDGE_PLAIN, 12 EDGE_BRANCH, 14 RUNG, 4 RUNG_SLEEVE, 50 CLICK_KEY and 34 PAPER_PAD = 130 pieces. Four borders total 520. Existing PVC corner braces add 32 V_BLOCK and 8 CROSS_PLATE = 40.

## Revised print and material totals

Full gate **with optional pads**: **6.995 kg PETG, 286.0 printer-hours, 105 plate runs**. A 10% material allowance is 7.69 kg, so plan eight 1 kg spools. At an assumed $20/kg, the deposited plastic is about $140; hardware, PVC, paper and cord are additional. Compared with the previous bolted version this saves 135 g of plastic, 8.9 printer-hours and seven plate runs. The main improvement is less assembly work and fewer small attachment components; this remains a large printing project.

Without front pads: **6.792 kg PETG, 277.2 printer-hours, 101 plate runs**. Skip the Q_PAPER_PAD recipes to save 202.36 g and 8.83 printer-hours. Both configurations use 272 magnets when all 136 face attachment sites are populated; only the front plastic pads are optional.

[Print_Queue.csv](Print_Queue.csv) lists each production plate recipe and repeat count. [Every_Plate_Run.csv](Every_Plate_Run.csv) lists every run individually. Test prints are extra unless you subtract their accepted pieces from production totals. Filament estimates include the selected slicing profile and startup assumptions; manual plate handling, failed prints, glue cure time and physical assembly are not included in printer-hours.

## Reusable full-width test bay

Print T01_BRANCH four times, T02_RUNG once, T03_BAY_SLEEVE once and T05_SINGLE_PLAIN twice. This produces **32 pieces**: four branches, two plain edge rails, five plain rungs, one sleeve rung, twelve keys and eight optional pads. The supplied recipes include those pads; omitting them leaves 24 structural pieces, and requires removing those objects and re-slicing the mixed test plates. The assembled bay is **436.943 x 609.6 mm**. Add one 3.3 m bracing cord, sixteen 6 x 2 mm magnets, a paper rectangle, and a 33.4 mm OD pipe offcut.

This kit is 417.5 g and 18.12 printer-hours over eight runs. The sleeve replaces the middle rung of one of the two crossmembers. Thread the pipe through it; there is no separate dock assembly. All 32 pieces can be used in the full gate. The separate T04_BRACE plate tests the existing corner-brace clamps.

## Workshop assembly of a full border

1. Build two long rails. Each rail uses fourteen 136.314 mm bodies and thirteen CLICK_KEYs with 14 mm exposed middles, totaling 2090.4 mm. Use EDGE_BRANCH at zero-based positions 0, 2, 5, 8, 11, 13; the remaining eight positions are EDGE_PLAIN. Face all branch sockets inward. Rotate the opposite long rail 180 degrees; the symmetric pattern aligns its branches.
2. Make six three-segment crossmembers. Put a RUNG_SLEEVE in the middle of crossmembers 2 through 5. Crossmembers 1 and 6 use only plain RUNG. Every crossmember needs four keys: two internal and one at each end. Use the same paper-facing plane for all pieces and point every loop toward the back.
3. Join both long rails to the crossmembers. Check 2090.4 x 609.6 mm overall dimensions, equal diagonals and full engagement of both key catches. The sleeve centerline passes through the centers of its four loops at 304.8 mm across the border. The sleeve axes run along the long direction.
4. Thread and tension the five X bays as below. Keep these cords installed during transport. There are no extra sleeve-positioning cord stays.
5. Populate 28 long-edge magnet lugs and six middle-rung lugs, leaving twelve outer-rung pockets empty. Use 34 loose front magnets, or optionally bond those magnets into 34 PAPER_PAD parts for easier handling and a larger paper contact area. Check polarity and fit before bonding. Without pads the stack is rear magnet, unchanged 0.4 mm rail skin, paper, bare front magnet. With pads it is rear magnet, unchanged 0.4 mm rail skin, paper, 0.4 mm pad skin, front magnet. The frame-side holder is unchanged in both configurations. Test grip with the actual paper and adhesive cure; magnet dimensions alone do not establish holding force.
6. Cut one 2090.4 mm length from the 609.6 mm-wide roll. Attach paper after the first complete frame fit-up to avoid damaging it during initial handling. Repeat for four identical borders. The four rectangles form a pinwheel with 2700 mm outside and 1480.8 mm opening; no corner paper patches are required.

## PVC threading and corner assembly

Thread each **bare straight square rail** through the four loops of its border before installing PVC tees, end fittings or brace clamps. Fittings cannot pass through the sleeve. The four pipe axes and four PVC corner fittings form the backing square. Mark pipe insertion depths and border positions after the first successful full assembly.

On a padded flat surface, arrange the four borders in the pinwheel. Build a top U assembly with the top pipe and its two corner tees. Insert the left/right pipe ends into those tees. Fit the bottom pipe into its two tees, then bring this bottom U assembly onto the two exposed parallel side-pipe ends together. Fully seat the sockets and square the assembly. Support the printed borders while moving the PVC. Confirm the real fitting sizes allow the intended joints to seat before drilling any retention holes.

The prior M4 retention bolts in the PVC corner/foot fittings and the V clamps on the PVC corner braces are still listed in Hardware_BOM.csv. They belong to the backing structure; **none attaches the printed face to its pipe**. This change removes the pictured bolted dock, not the existing brace and base design. No extra cord stays or attachment fasteners have been added to the sleeves.

The square's centerline spacing remains 2090.4 mm. Its lower/upper horizontal centerlines remain 354.8 / 2445.2 mm above ground, but its plane moves forward to **46 mm behind the paper**. The 3/4-inch corner braces remain 60.475 mm behind the main pipe plane. Paper spans ground heights 50 to 2750 mm. Upper guy masts extend to 3100 mm.

Sleeves are closed, so a border does not snap straight off an assembled square. For teardown, support the border and release the relevant corner fittings and brace clamps; then slide the pipe out, or leave it threaded for transport. With fittings and interfering brace hardware removed, the pipe can slide about 304.8 mm inward from its assembly position to fit inside the border's 2090.4 mm transport length. Its parked extent is about 17.5 to 2072.9 mm from the border end. Mark both positions. Reposition it at setup before joining corners. Do not force installed fittings or clamps through a loop.

The circle is a clearance bore, so this design does not claim that every individual sleeve is a friction clamp or a rotational key. Per your instruction, the trial assembly relies on the completed PVC square and corner fittings without extra stays. Check the assembled result before producing all sixteen sleeves.

## Pipe cuts, braces and base

See PVC_Cuts.csv for quantities and example lengths. The four 1-inch square rails are 2055.48 mm; two lower legs 294.88 mm; two upper masts 637.34 mm; four grass half-feet 582.54 mm; four alternative hard-surface half-feet 1182.54 mm. The four 3/4-inch braces are 645.69 mm. These are example cuts using 17.4625 mm fitting-center-to-seated-pipe-end take-up. Measure actual purchased fittings before cutting. For two fittings, cut = center spacing minus both take-ups. Purchased fitting models are illustrative envelopes.

For both foot sets, six 10-ft sticks of 1-inch PVC can be nested as follows: sticks 1-2 each make a square rail, upper mast and lower leg; sticks 3-4 each make a square rail and grass half-foot; sticks 5-6 each make two hard-surface half-feet and one grass half-foot. One 10-ft stick of 3/4-inch makes all four braces. Use six 1-inch tees (four square corners plus two foot tees), six caps (four foot ends plus two mast ends), and the existing retained-fitting hardware in Hardware_BOM.csv.

Brace crossings lie 400 mm along adjoining sides from each square corner. Each pipe projects 40 mm past its two crossings, giving sqrt(400² + 400²) + 80 = 645.69 mm. Each crossing uses four identical V_BLOCK halves and one CROSS_PLATE. Use the straight plate-hole pair with two M4 x 80 bolts for the main pipe; use the appropriate +/-45-degree pair with two M4 x 70 bolts for the brace. Add washers/nuts and tighten alternately until gripping without crushing pipe or printed parts. Four braces require eight crossings. Test slip and rotation using the actual pipe before relying on them.

For soil, use the 1200 mm fore-aft foot set and four suitable ground stakes. For hard surfaces, use the 2400 mm foot set, rubber pads and four attached 15 kg ballast bags. That 60 kg arrangement is an initial test setup, not a wind rating. Retain all structural PVC fitting ports with the specified M4 bolts after seating and squaring. Attach the four external guys below mast stop bolts at roughly 3075 mm high; the upper extensions route the front guys above the paper. Do not attach front guys to the lower 2445.2 mm square rail, where they would cross the face. Keep guys outside the flight opening and attach ballast securely to the feet.

## Face cord adjustment

Use 2.4 mm 275 paracord. Cut twenty equal 3.3 m face cords and four 4 m external guys: 82 m total, covered by three 100-ft hanks with 9.44 m spare. The face-bracing cleats remain integrated into EDGE_BRANCH; no separate tensioner is needed there.

For each bay, viewed from behind, label its inward-facing eyes lower-left (LL), upper-right (UR), lower-right (LR), upper-left (UL). Tie a stopper larger than the eye; thread LL -> UR -> LR -> UL -> LL. The cord makes two diagonals and two short return legs. Turn outside the posts after threading their transverse holes. Feed slack progressively around all four eyes, pull the return tail, make two figure-eight wraps around the lower-left branch's two posts, and finish with a locking half-hitch. Leave a 100 mm tail. Hand-tension only until slack is removed and the rail stays straight. To adjust, hold the tail, undo the hitch, unwrap, feed slack and rewrap. Keep all five bays threaded in transport.

## Verification and first-use checks

All eleven exported masters (eight production types and three optional gauges) are manifold, positive-volume and inside the A1 Mini envelope. The sleeve is **one connected mesh**, not overlapping independent solids. Every supplied plate has at least 5 mm bed margin, no part overlap and no slicer warnings with supports disabled. Production plate counts match the 560-piece BOM and full-scene instances. Sampled key interfaces show no penetration; the modeled PVC circle has at least 0.39 mm clearance to the bore polygon. These digital checks are not physical strength or fatigue tests.

Start with the separate four-piece frame click test. Then use a measured pipe offcut and the full sleeve. Check insertion, removal, key engagement and visible cracking or whitening while applying modest hand loads in all directions. Next test a full-width bay, then one full border, then the complete square in calm conditions. Check sleeve roots, frame keys, cord slip, pipe-brace grip, magnetic retention and base stability. Recheck after repeated assembly and warm outdoor exposure. The 6 mm wall and broad root are design dimensions, not a tested load rating. No wind rating is claimed.

The prior research on nominal pipe OD, PETG click joinery and cord remains in [the preceding guide](../full_paper_gate/README.md#research-used); this revision's dimensions and estimates come from its local CAD and slicer. No physical prototype has been printed here. No printer job was submitted.

Rebuild with scripts/build_sleeve_paper_gate.py, slice_sleeve_paper_gate.py, render_sleeve_paper_gate.py, validate_sleeve_paper_gate.py and package_sleeve_paper_gate.py. Slicing requires locally installed Bambu Studio; packaging requires ReportLab.

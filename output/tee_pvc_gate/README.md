# Accepted 33.5 mm bore / tees, top guy elbows and measuring tools

The user confirmed that the printed MAG_SLEEVE fits the purchased PVC perfectly on 2026-09-18. **33.5 mm is now the fixed design bore for every PVC interface in this iteration. The MAG_SLEEVE STL is byte-for-byte unchanged.** The deeper fitting sockets and workshop tools still need their first physical checks; no further bore-selection samples are included.

[Blender model](Tee_PVC_Gate.blend) · [Visual index](index.html) · [Assembly and measuring PDF](Tee_Gate_and_Measuring_Guide.pdf) · [Kit](Tee_PVC_Gate_Kit.zip)

## Workshop status / 2026-09-19

The user printed MAG_SLEEVE and confirmed a perfect fit on purchased PVC; retain 33.5 mm throughout. The selected next job is ONE_TEE in PETG, opened in Bambu Studio (98.49 g / 226.45 minutes). No successful tee print or strength test has been reported, and the assistant has not submitted a job to the printer.

For the two fixed PVC lengths, accurately cut and checked PVC master pieces are the preferred simple marking templates. The printed measuring jig is optional and deferred; prioritize production fittings. The current guy elbow has one eye behind the face. The next design request is simultaneous front/rear tie-down access with a diagonal extension and top/side magnet pads; that revision is not part of this baseline.

## Print these new parts

- [Two-head measuring kit](sliced/MEASURING_KIT/MEASURING_KIT_A1Mini_PETG.3mf): **80.89 g / 3.29 hours**. JIG_ZERO + JIG_MARK only. Use these with a straight spare piece of 1-inch PVC and a metric tape measure.
- [One three-way tee](sliced/ONE_TEE/ONE_TEE_A1Mini_PETG.3mf): **98.49 g / 3.77 hours**.
- [One top guy elbow](sliced/ONE_GUY_ELBOW/ONE_GUY_ELBOW_A1Mini_PETG.3mf): **77.39 g / 3.04 hours**.
- [Optional 30 mm insertion-depth gauge](sliced/ONE_DEPTH_30/ONE_DEPTH_30_A1Mini_PETG.3mf): **25.10 g / 1.21 hours**. This marks engagement depth on every pipe end; it is not another bore-selection sample.

[MEASURING_KIT_PLUS_DEPTH](sliced/MEASURING_KIT_PLUS_DEPTH/MEASURING_KIT_PLUS_DEPTH_A1Mini_PETG.3mf) combines the two heads and optional depth gauge. Use supplied orientations. All plates fit the A1 Mini with at least 5 mm bed margin and slice with supports off and no warnings. Estimates use Generic PETG, 0.4 mm nozzle, 0.20 mm layers, four walls and 20% infill. No printer job has been submitted.

## Measuring tools for the Husky ratcheting PVC cutter

The cutter is the user's **Husky 1-1/4-inch ratcheting PVC cutter**. This jig establishes a repeatable pencil line; the pipe is removed before cutting. There is no blade slot or attachment to the cutter.

Two small heads turn a length of existing PVC into a reusable length gauge. It avoids printing a multi-foot telescoping ruler: the PVC carries the spacing, a trusted metric tape establishes the actual length, and the heads transfer that length repeatedly. Printed telescoping segments would introduce extra joints and would still need calibration. This design improves repeatability; it does not promise perfect absolute accuracy from a printed scale.

**JIG_ZERO** has a 32 mm-long friction sleeve on the reference rail, an open cradle for the workpiece and an end-stop wall. The workpiece end contacts the wall's inner face, which is **X = 0**. A single witness groove on the connecting foot identifies the datum. Both pipe axes are 24 mm above the table and 70 mm apart.

**JIG_MARK** has a 32 mm-long reference sleeve and a 12 mm-long, full circular marking collar. The **collar face nearest the zero stop is the marking plane, also local X = 0**. Its three small grooves distinguish it from the stop. Both bores are 33.5 mm; this tool prints standing on its datum end face, giving circular vertical holes without support. The gate fittings keep their existing horizontal peaked bores. Keep the supplied jig orientation when slicing.

### Set up once for each length

1. Use a straight, clean reference pipe at least **1650 mm long**, preferably an uncut 10-ft stick already on hand. Slip the zero head and then the marking head onto it, both with feet flat on the same surface and their workpiece openings on the same side. Do not cut this reference rail while it is carrying the jig.
2. Put the zero head near one end. With the workpiece absent, measure along the workpiece axis from the **inside contact face of the stop** to the **near face of the marking collar**. Set **389.6 mm** for short cuts or **1560.8 mm** for long cuts. The fronts of the printed parts, their centers and their far faces are not interchangeable measurement references.
3. Support the rail and long stock so they stay straight and level. Mark each head's position on the reference pipe with a fine witness line. Hold the marking head while threading stock through its collar toward the zero stop, so the reference sleeve cannot creep during loading. Press the pipe end gently against the stop.
4. Draw a fine line along the near face of the collar. Rotate the workpiece while keeping its end against the stop to continue the line around its circumference. Use a fine mechanical pencil or fine marker; a broad marker line reduces repeatability.
5. Pull the stock free of the marking collar while holding the head in place. **Remove it from the jig**, then support it and use the Husky cutter on the marked line. Keep the blade perpendicular to the pipe; the jig transfers length but cannot correct cutter drift or a slanted cut.
6. Measure the first finished piece and check that its ends are square. If the finished piece differs from the target, move the marking head by the measured error and repeat a trial. This calibrates the complete tape / pencil / cutter process, including the line edge you consistently cut to. Compare repeated pieces side-by-side and recheck the rail witness lines during the batch.
7. Cut all long pieces, reset and verify the short setting, then cut the short pieces. The reference rail can be one of the budgeted sticks: after the other cuts are complete, remove the heads and transfer lengths from an accepted finished piece to cut the rail itself. No permanently dedicated extra stick is necessary.

Friction retains both heads. The reference sleeves are longer than the workpiece collar to help them stay put, but this is not a positive locking mechanism. Calibration and witness marks matter. Keep a consistent light touch, and support rather than bend long stock. If a tool binds, clean/deburr it and check the printing result rather than forcing it; the accepted design bore remains 33.5 mm.

**Optional DEPTH_30:** push a deburred pipe end into the gauge until it contacts the closed stop. Mark around the open face, exactly 30 mm from the end in CAD. These marks show when the elbow, tee and cross sockets are fully seated. It also provides a small first check of the longer 30 mm engagement before printing all fittings. The gauge has the accepted 33.5 mm bore.

## Three-way tee placement and material savings

The new **TEE** has three sockets and two magnet pads on the side without a socket. Rotate the same part at every outside three-way junction: its missing branch points away from the gate. It replaces **8 crosses on the single** and **12 on the stacked gate**. Crosses remain at all true four-way inner junctions.

A tee uses **98.49 g** versus **132.59 g** for the cross: **34.10 g and 77.8 minutes saved per replacement**. The magnetic pad coordinates, paper coverage, pipe stops and cut lengths remain the same. The assembly maps and node CSVs identify every tee and its rotation.

## Top elbow with guy attachment

**GUY_ELBOW** replaces the two overall top outside elbows. The two bottom corners retain ELBOW. The same top part rotates for left and right; no mirrored file is needed.

The attachment is a **10.5 mm nominal passage** with a printable peaked roof, in a **14 mm-thick, 36 mm-wide eye** rising directly from the thick central elbow body. The hole center is 31 mm behind the paper plane; the complete eye remains behind the paper. It is separate from the magnetic flange and neither changes the PVC bore nor consumes a magnet pocket.

Thread the guy through the rear eye and tie it around that eye. Use a smooth compatible cord or a protected loop at the plastic; bare tensioned metal wire should not saw against the printed edge. The Blender view shows a short threading segment, not a finished knot or a prescribed anchor arrangement. Smooth any rough printed edge before threading. Check hand access and the actual line with one printed top elbow before repeating it.

Top guy lines are newly authorized in this iteration; **internal PVC joints remain friction-only**. Bench-test the eye and watch the pipe engagement marks as tension is introduced. The printed eye has no assigned load rating, and adding it does not establish a wind rating or size the ground anchors/ballast. The tall stacked frame still needs a suitable installation design for the actual surface.

## Full gate parts and costs

| Part | Single | Stacked total | A1 Mini print bounds, mm |
|---|---:|---:|---|
| ELBOW | 2 | 2 | 133.314 x 133.314 x 53.345 |
| GUY_ELBOW | 2 | 2 | 133.314 x 133.314 x 53.345 |
| TEE | 8 | 12 | 136.627 x 133.314 x 53.345 |
| CROSS | 4 | 8 | 136.627 x 136.627 x 53.345 |
| MAG_SLEEVE | 48 | 80 | 20.0 x 86.75 x 53.345 |

There are **five required gate part types**, with **64 pieces single / 104 stacked**. Workshop tools and optional front pads are additional and excluded from these counts. Your already-printed sleeve counts toward the required 48 or 80. The supplied full production queues assume printing the whole BOM from zero; subtract accepted pieces already in hand when planning batches.

| Configuration | Pieces | PETG kg | Print h | Plate runs | 10-ft PVC / cost | PVC + PETG subtotal |
|---|---:|---:|---:|---:|---|---:|
| single | 64 | 2.273 | 92.6 | 23 | 8 / $48 | $93.47 |
| split_s | 104 | 3.640 | 148.5 | 36 | 14 / $84 | $156.80 |

PVC uses your $6/stick price; PETG assumes $20/kg. Add paper, magnets, adhesive, workshop tooling and ground support. Compared with the previous all-cross version, the new single saves **254.96 g / 9.67 hours**, including the added top eyes. The stacked gate saves **391.36 g / 14.85 hours**. Three 1-kg spools cover the single with 10% allowance. The stacked gate needs 3.640 kg nominally; a 10% allowance is 4.004 kg, slightly above four full spools, so keep spare filament available if budgeting that allowance.

## Production print queue

| Recipe | Single runs | Stacked runs | Pieces/run | g/run | h/run |
|---|---:|---:|---:|---:|---:|
| ONE_ELBOW | 2 | 2 | 1 | 68.47 | 2.69 |
| ONE_TEE | 8 | 12 | 1 | 98.49 | 3.77 |
| ONE_CROSS | 4 | 8 | 1 | 132.59 | 5.07 |
| ONE_GUY_ELBOW | 2 | 2 | 1 | 77.39 | 3.04 |
| BATCH_MAG_SLEEVE | 6 | 11 | 7 | 96.74 | 4.46 |
| TAIL_MAG_SLEEVE_6 | 1 | 0 | 6 | 82.93 | 3.85 |
| TAIL_MAG_SLEEVE_3 | 0 | 1 | 3 | 41.5 | 2.07 |

Each configuration's Print_Queue.csv links to the prepared A1 Mini PETG 3MFs. The sleeve batch contains seven identical sleeves; tail recipes avoid overprinting. New_Parts_Print_Queue.csv lists only the new fitting/tool test jobs. Inspect one tee and one guy elbow first; your accepted sleeve fit is preserved, but the 30 mm-long sockets have not yet been physically checked.

## Cuts, assembly and paper

The two finished PVC lengths remain **389.6 mm** and **1560.8 mm**. Single: **16 short + 8 long**, from eight 10-ft sticks. Stacked: **24 short + 14 long**, from fourteen sticks. Each pipe enters its sockets 30 mm; the stop is 35 mm from the fitting center. Pipe-center spacing is therefore the cut length plus 70 mm.

The stock ledger reserves 10 mm per stick plus 3 mm per cut for conservative trimming/measurement allowance. **The 3 mm is not a saw-kerf instruction for the Husky cutter, and is not added to a finished cut length.** Mark every finished piece from its actual squared starting end. No need to trim an extra 3 mm off between good cuts.

1. Use the jig to mark and verify cuts, then deburr and label the pipes using PVC_Cuts.csv. Mark 30 mm insertion depth at each end. Slide sleeves on before adding fittings.
2. A short pipe gets one sleeve at **194.8 mm** from its cut end. A long pipe gets four at **291.16, 617.32, 943.48 and 1269.64 mm** from the named cut start. Keep all magnetic faces coplanar; Sleeve_Positions.csv supplies every location and rotation.
3. Assemble each horizontal row with four nodes and short / long / short PVC. Single row heights from the paper bottom are **75, 534.6, 2165.4 and 2625 mm**. Bottom ends use ELBOW, top ends GUY_ELBOW, outside three-way nodes TEE, inner four-way nodes CROSS. Both pads on a tee face the outside paper edge.
4. Work flat with the paper faces down. Join successive rows using four vertical pipes at a time, seating them evenly to their insertion marks. Single vertical intervals use short / long / short pipes. Check coplanarity and equal diagonals while assembling.
5. Populate magnet pockets according to the magnet CSV. Front appearance and paper sizes are unchanged: **2700 mm square single**, or **2700 x 4790.4 mm stacked**, **1480.8 mm openings**, and **609.6 mm bands**. All fittings and pipes stay behind paper in the checked front projection.
6. Single paper: two 2700 mm bars and two 1552.8 mm side inserts, all full 609.6 mm roll width. Stacked: three bars and four inserts. Put bars on first, then side inserts overlapping 36 mm at each end. Use **72 pairs / 144 magnets** single, or **116 pairs / 232 magnets** stacked, all 6 x 2 mm. Rear magnet -> 0.4 mm printed skin -> paper -> bare front magnet. Retain the old optional front pads if desired.
7. Thread guys through the two top eyes with the frame accessible. Keep pipe joints fully seated during installation. Footing and anchor details are separate from the face-frame print queue.

## Upgrade from single to stacked

Move the **complete top row** upward, including both GUY_ELBOWs, its two tees, its three pipes and their sleeves. Add a replacement row at y = 2625 mm, with two tees at the outside and two crosses inside. Four new long verticals connect to another new row at y = 4255.8 mm, again with two tees and two crosses. Four new short verticals connect that row to the retained top row at y = 4715.4 mm.

Add **4 tees + 4 crosses + 32 sleeves**, **8 short + 6 long pipes**, and **44 magnet pairs**. Every original pipe, printed gate fitting, sleeve and populated magnet location is reused. The added PVC fits six more sticks. Add one 2700 mm paper bar and two 1552.8 mm side inserts. The two divider rows stay 459.6 mm apart on center, maintaining the shared 609.6 mm face band.

## Verification and sources

The supplied geometry is connected/manifold. Plate bounds, part separation, exact print quantities, support-off slicing, tee-port orientation, magnet-pocket alignment, top-eye placement, paper concealment and reuse on extension were checked. The accepted MAG_SLEEVE STL is unchanged. New tool fit, marking repeatability, deeper socket fit and eye loads await physical tests.

- [Kreg: repeatable cuts using stops](https://learn.kregtool.com/learn/make-repeatable-cuts-using-stops/) describes the general measure-once/repeat-stop approach. This two-head PVC marking jig is an original project design, not a Kreg accessory.
- [Husky 1-1/4-inch ratcheting PVC cutter](https://www.homedepot.com/p/304217581) is the tool-family reference; the jig does not depend on its external dimensions because cutting occurs off the jig.
- [Prusa: modeling with 3D printing in mind](https://help.prusa3d.com/article/modeling-with-3d-printing-in-mind_164135) discusses orientation and print geometry. Supports being disabled and absent from the supplied toolpaths is a digital check, not a physical strength result.

Rebuild using scripts/build_tee_pvc_gate.py, slice_tee_pvc_gate.py, validate_tee_pvc_gate.py and package_tee_pvc_gate.py. Previous iterations remain in their original folders. The bore is fixed at 33.5 mm in this builder; it does not inherit an environment override from an earlier fit study.

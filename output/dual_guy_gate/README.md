# Dual front/rear guy elbow / diagonal ear

The previous PVC/tee design and workshop status were documented and committed as **6a7fb47** before this revision. That record includes the physically accepted 33.5 mm sleeve fit, the selected ONE_TEE PETG job opened in Bambu Studio, and the preference for checked PVC master pieces instead of printing measuring tools first. Tee completion has not been reported.

This revision replaces only the two top GUY_ELBOWs with **DUAL_GUY_ELBOW**. It adds simultaneous independent front and rear tie-downs, and moves the single corner magnet to one top-edge and one side-edge holder. All other production STLs are byte-for-byte identical to the committed tee iteration. PVC bores remain **33.5 mm**, with **30 mm engagement** and **35 mm center-to-stop**.

[Blender model](Dual_Guy_Gate.blend) · [Visual index](index.html) · [Assembly/test PDF](Dual_Guy_Assembly.pdf) · [Kit](Dual_Guy_Gate_Kit.zip)

## First print

[ONE_DUAL_GUY_ELBOW_A1Mini_PETG.3mf](sliced/ONE_DUAL_GUY_ELBOW/ONE_DUAL_GUY_ELBOW_A1Mini_PETG.3mf): **102.57 g PETG / 3.95 hours**. One required top corner, with both eyes and both magnet holders. Print one and test before making the second. No new job was opened or submitted, so the previously selected tee job is not replaced in Bambu Studio.

Bounds are **168.614 x 168.614 x 53.345 mm**. The supplied A1 Mini layout places it at X=5, Y=5, leaving at least 5 mm bed margin. Use the supplied flat-face-down orientation, 0.4 mm nozzle, 0.20 mm layers, four walls, 20% infill and Generic PETG. All supplied recipes slice without supports or warnings. The PVC sockets retain the accepted peaked roofs; both tie-down holes print vertically through the flat ear.

The old guy elbow used 77.39 g / 3.04 hours. Each replacement adds **25.18 g / 54.16 minutes**. Two replacements add **50.36 g / 1.81 hours** per gate, whether single or stacked.

## What changed

A **32 mm-wide, 14 mm-thick diagonal arm** runs from the central elbow body toward the outside paper corner. A sloped root rib rises to 28 mm behind the paper plane. The arm ends in a rounded ear containing **two 10.5 mm through-holes**, 18 mm apart on center. Each hole has a **0.8 mm, 45-degree chamfer** on both entrances, giving a 12.1 mm mouth. The straight bores have 8 mm outer edge material and 7.5 mm between holes; at the chamfer mouths these reduce to 7.2 mm and 5.9 mm respectively.

One hole takes the **front guy**, the other the **rear guy**. Each cord gets its own eye and attachment loop, so both can remain attached and be adjusted independently. The through-hole axes point front-to-back through the ear. There is no hidden rear-only eye requiring the front line to pass through paper. The same part rotates into both top corners; no mirrored file is needed.

The hole mouths lie completely beyond the paper outline. The ear projects up to **28.614 mm past the adjacent top/side edges**. This is an intentional visible exception to the earlier paper-only front: the paper remains uncut, and the PVC, body and magnet pads remain concealed behind it. Paper dimensions stay **2700 mm square single**, or **2700 x 4790.4 mm stacked**. Including the two ears, the hardware reaches about **2757.2 mm wide** and **2728.6 / 4819.0 mm high**, before feet.

The diagonal ear occupies the old corner-magnet direction. Its replacement pads lie along the **top and side edges**, each **18 mm inside the edge and 90 mm from the paper corner**. Both keep the existing 6.3 mm rear magnet pocket and **0.4 mm frame-side plastic skin**. Use the same 6 x 2 mm magnets. Optional front paper pads remain optional and are available in the earlier kit.

## Fit and thread both lines

1. Print one DUAL_GUY_ELBOW. Inspect the 0.4 mm magnetic skins, two vertical through-holes, diagonal arm and root rib. Clear loose strings and smooth any rough entrance edges without enlarging the PVC bores.
2. Fit two actual PVC offcuts and seat both sockets the full 30 mm, using insertion witness marks. The design bore stays 33.5 mm; the longer socket fit still needs its first physical check despite the successful sleeve print.
3. Thread a separate attachment loop through each eye and around its adjacent outside rim. Lead one guy toward the front of the gate and the other toward the rear. The orange/teal Blender lines show this routing; they are schematic loops, not a knot prescription. Choose appropriate secure knots/loops for the actual line and confirm knot clearance with both fitted simultaneously.
4. Use smooth cord or a protected connection at the plastic. Bare metal wire should not abrade directly against a printed edge. The modeled line diameter is **3 mm**; test the actual chosen cord or protected wire loop rather than treating this as a universal hardware fit.
5. Lay a paper corner over the fitting without a hole or notch. Align its two edges with the 18 mm magnet inset. Fit the two rear/front magnet pairs, and check that both cords can be connected and released with the paper in place. Bond rear magnets only after checking polarity and fit.
6. With the corner supported, try each guy independently, then both together, watching the elbow root and the pipe engagement marks. Check for visible flex that does not recover, whitening, cracks, cord-edge wear and socket withdrawal. Opposing guys do not remove the loads in the printed part. Repeat attachment/release and inspect again before committing to the second corner or an outdoor setup.

The digital routing check sampled **1046 points** on the illustrated loops and local tails against the actual printed mesh, with a minimum centerline distance of **5.049 mm** for 3 mm cord. The sampled paper crossings also clear the paper. Knots, flexible deformation and real line loads are not simulated. **This is a fabrication prototype with no assigned eye or wind load rating.** Ground support and anchor sizing remain separate installation work, particularly for the tall Split-S frame.

## Replace the top corners in the gate

Install two DUAL_GUY_ELBOWs in place of the two old GUY_ELBOWs. The native part has PVC ports +X and +Y; the assembly maps rotate it 270 degrees at upper left and 180 degrees at upper right. The ears point outside the overall corners. All stop positions, PVC lengths and paper cuts remain identical.

Facing the gate, the new top-left magnet centers are **(18, H-90)** and **(90, H-18)** mm from the paper's bottom-left origin. Top-right centers are **(2700-18, H-90)** and **(2700-90, H-18)**. H is 2700 mm for single or 4790.4 mm for stacked. The updated Magnet_Positions.csv files include these changes; remove the old single corner position at each top corner.

Each top elbow now needs two magnet pairs instead of one. Totals become **74 pairs / 148 magnets single**, or **118 pairs / 236 magnets stacked**: **four more individual magnets** than the committed tee design. Paper roll usage, overlap seams and all other magnet positions are unchanged.

| Required part | Single | Stacked total |
|---|---:|---:|
| ELBOW | 2 | 2 |
| DUAL_GUY_ELBOW | 2 | 2 |
| TEE | 8 | 12 |
| CROSS | 4 | 8 |
| MAG_SLEEVE | 48 | 80 |

The gate still has **five required printed types**, **64 pieces single / 104 stacked**. Single production estimate: **2.324 kg / 94.4 hours**, 23 plate runs. Stacked: **3.690 kg / 150.3 hours**, 36 plate runs. Count the sleeve already printed toward the BOM; full queues are from zero.

PVC requirements remain 16 short + 8 long cuts for single, or 24 short + 14 long for stacked, at **389.6 / 1560.8 mm**. Eight or fourteen 10-ft sticks at the supplied $6 price. At an assumed $20/kg PETG, PVC + PETG face-frame subtotals are **$94.47 / $157.81**, excluding magnets, paper, cord, adhesive and ground support.

## Full print queue

| Recipe | Single runs | Stacked runs | g/run | h/run |
|---|---:|---:|---:|---:|
| ONE_ELBOW | 2 | 2 | 68.47 | 2.69 |
| ONE_TEE | 8 | 12 | 98.49 | 3.77 |
| ONE_CROSS | 4 | 8 | 132.59 | 5.07 |
| ONE_DUAL_GUY_ELBOW | 2 | 2 | 102.57 | 3.95 |
| BATCH_MAG_SLEEVE | 6 | 11 | 96.74 | 4.46 |
| TAIL_MAG_SLEEVE_6 | 1 | 0 | 82.93 | 3.85 |
| TAIL_MAG_SLEEVE_3 | 0 | 1 | 41.5 | 2.07 |

Each CSV queue links to prepared A1 Mini PETG projects. Only ONE_DUAL_GUY_ELBOW is a new part/job; the other geometry matches the committed files. No print has been submitted.

## Assembly and extension

The row-by-row assembly from the [committed tee guide](../tee_pvc_gate/README.md) still applies, substituting the two new top elbows and new top magnet locations. Use checked PVC master pieces for repeated marking as recorded in the baseline; the optional jig is not required.

To extend upward, move the complete top row with both dual-guy elbows, its two tees, three pipes and sleeves. Add **4 tees, 4 crosses, 32 sleeves, 8 short PVC cuts and 6 long cuts**. Every existing pipe, fitting and populated magnetic attachment is reused. Two top elbows still provide four guys total: front and rear at each corner. Anchor endpoints and tension settings are not prescribed by the illustrative Blender views.

## Verification and source

Checks cover connected manifold masters; A1 Mini plate bounds, clearances and support-free toolpaths; exact queues and node ports; unchanged non-guy STLs; matching magnetic pockets; full hole-mouth clearance beyond paper; sampled cord/body and cord/paper clearance; and reuse of all single-height parts on extension. The exposed diagonal ear is explicitly allowed in the front-projection check; other protrusions fail it.

[Prusa's modeling guidance](https://help.prusa3d.com/article/modeling-with-3d-printing-in-mind_164135) discusses how geometry and print orientation affect mechanical behavior. The arm dimensions and cord layout here are original prototype choices, not a strength rating derived from that source.

Rebuild with scripts/build_dual_guy_gate.py, slice_dual_guy_gate.py, validate_dual_guy_gate.py and package_dual_guy_gate.py. Baseline commit: **6a7fb47**. The new iteration is separate in output/dual_guy_gate; earlier printable parts and documentation remain intact.

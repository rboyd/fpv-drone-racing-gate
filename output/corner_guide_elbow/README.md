# Three-magnet guy elbow / paper alignment guides

This iteration adds a corner magnet and shallow paper alignment grooves to the preceding [two-magnet dual-guy elbow](../dual_guy_gate/README.md). The earlier committed PVC/tee baseline is 6a7fb47. This is the current production-file revision; the sleeve fit is confirmed and full-gate tests remain outstanding.

[All five parts](renders/11_ALL_PRODUCTION_PARTS.png) · [Blender](Corner_Guide_Elbow.blend) · [Rendered views](index.html) · [Assembly PDF](Corner_Guide_Elbow.pdf) · [One-elbow PETG print](sliced/ONE_DUAL_GUY_ELBOW/ONE_DUAL_GUY_ELBOW_A1Mini_PETG.3mf)

## Three magnet positions

One 6 x 2 mm magnet now sits at the corner, **18 mm inside both paper edges**. The existing top and side magnets remain 18 mm inside their respective edge and 90 mm along it from the corner. Use three rear magnets and three opposing front magnets per elbow. Front paper pads remain optional.

The new seat is cut into the existing 32 mm-wide diagonal arm. Its **6.3 mm bore** retains a **0.4 mm plastic skin** facing the paper. A **10 mm rear access well** opens down to Z=2.6 mm; the 6.3 mm seat runs from Z=0.4 to 2.6 mm. The 2 mm magnet rests on the skin with its rear face at Z=2.4 mm. Insert it from the rear with a small nonmagnetic dowel, then use a small amount of suitable adhesive after checking polarity. There is no hole through the paper-side skin. The rear access well leaves nominally 11 mm of arm width on each side at its center section; the new pocket still requires a physical guy-load test.

Native CAD magnet centers are (-57,15), (15,-57), and (-57,-57) mm. The native paper corner is (-75,-75) mm, with paper extending toward +X and +Y. Installed at upper left, the new corner magnet is (18,H-18) mm from the paper's bottom-left; at upper right it is (2700-18,H-18). H=2700 single / 4790.4 stacked.

## Exact paper alignment

The paper-facing underside has a recessed **L-shaped guide, 0.8 mm wide and 0.4 mm deep**, extending about 22 mm along each edge. Its centerlines are exactly X=-75 and Y=-75 mm. Their intersection is the intended paper corner. Align the paper edges to the **middle of the grooves**, not their inside or outside walls. The outer half of each groove remains visible beside correctly aligned paper. The marks locate the local corner and edge directions; they are not full-length cutting guides.

The orange guide color in the paper-face render illustrates optional marker rubbed into the actual groove floors; the printable file is a single PETG part. The guide is recessed so the paper can sit flat. It does not cut across a magnet skin or either guy hole. With the supplied face-down print orientation, the 0.8 mm grooves require small bridges; the supplied slice generates them without supports. Actual first-layer squish can soften these fine marks, so inspect them on the first print. Optional contrasting marker rubbed into the recess improves visibility without adding a ridge.

## First print and assembly check

1. Print **one** elbow using the supplied A1 Mini PETG 3MF, 0.4 mm nozzle, 0.20 mm layers, four walls and 20% infill. Use the supplied orientation. The guides are on the bed-facing surface; flip the finished part over to see them.
2. Inspect the recessed L and all three 0.4 mm magnet skins. Fit the purchased PVC into both **33.5 mm** sockets, using full 30 mm insertion and witness marks. The successfully printed sleeve bore is preserved; this elbow's socket fit still needs checking.
3. Check all magnet polarities. Lower the new corner magnet through its access well into the smaller seat using a nonmagnetic dowel. Inspect the seat before bonding. Install the other two backing magnets as before.
4. Place the paper corner at the intersection of the guide centerlines. Align both edges with the groove centerlines, and attach the corner front magnet first. Then attach the top and side front magnets. These are three separate magnet pairs.
5. Attach separate front and rear guys through the two 10.5 mm eyes. They remain outside the paper outline, with no paper notch required. Check the actual knots or loops with paper and all magnets fitted.
6. Check both guys separately and together while supporting the corner. Inspect the diagonal arm around the new access well, the groove intersection, and pipe witness marks for cracking, permanent deformation or socket withdrawal. No eye or wind load rating has been established.

## Print estimate and full-gate effect

One revised elbow: **103.06 g PETG / 239.68 minutes** (about 4 hours). Dimensions remain **168.614 x 168.614 x 53.345 mm**, fitting the 180 mm A1 Mini with at least 5 mm layout margin. The slice has no warnings and no generated supports.

Compared with the preceding two-magnet elbow: **+0.49 g / +2.91 minutes per elbow**. Cutting a hole can slightly increase sliced material because the new hole adds perimeters. Two elbows per gate add **four individual magnets** (two additional pairs).

Single gate: **76 pairs / 152 individual magnets**, **2.325 kg PETG / 94.46 print-hours**. Stacked: **120 pairs / 240 individual magnets**, **3.691 kg / 150.37 hours**. All other STLs, PVC cuts, paper cuts, node positions and production counts remain unchanged. The exposed guy ear still reaches about 28.6 mm beyond adjacent paper edges.

| Part | Single | Stacked |
|---|---:|---:|
| ELBOW | 2 | 2 |
| DUAL_GUY_ELBOW | 2 | 2 |
| TEE | 8 | 12 |
| CROSS | 4 | 8 |
| MAG_SLEEVE | 48 | 80 |

| Recipe | Single runs | Stacked runs | g/run | h/run |
|---|---:|---:|---:|---:|
| ONE_ELBOW | 2 | 2 | 68.47 | 2.69 |
| ONE_TEE | 8 | 12 | 98.49 | 3.77 |
| ONE_CROSS | 4 | 8 | 132.59 | 5.07 |
| ONE_DUAL_GUY_ELBOW | 2 | 2 | 103.06 | 3.99 |
| BATCH_MAG_SLEEVE | 6 | 11 | 96.74 | 4.46 |
| TAIL_MAG_SLEEVE_6 | 1 | 0 | 82.93 | 3.85 |
| TAIL_MAG_SLEEVE_3 | 0 | 1 | 41.5 | 2.07 |

Full queues count from zero. Count the sleeve already printed toward the BOM. Prepared files do not submit a job to the printer.

## Current material costs

Using the owner's approximate purchase prices (4 kg black PETG for $39.59, 800 magnets for $19.99, and 10-ft PVC sticks at $5.34), priced materials are **$69.53 single / $117.29 stacked**. This counts sliced PETG consumption, the individual magnets used and all required PVC stock including offcuts. Paper, guy lines, anchors/ballast, adhesive, electricity, failed prints, tax and shipping are excluded. See the [project README](../../README.md) for full costs and pack-purchase totals. Prior iteration guides retain historical prices.

## Verification

Connected manifold geometry, plate bounds and clearances, support-free slicing, unchanged non-elbow STLs, aligned magnetic pockets, exact production counts and Split-S reuse checks pass. Ray probes of the actual mesh verify the groove floors at Z=0.4 mm, adjacent face at Z=0, magnet seat floor at Z=0.4 and access-well shoulder at Z=2.6. The prior 3 mm cord routing still clears the modified mesh and the paper. This checks geometry, not physical strength or printer accuracy.

The full assembly follows the preceding dual-guy guide, substituting this elbow and adding its corner magnets. The complete top row can still be moved upward for Split-S. See the updated CSVs for complete counts and magnet positions. Rebuild with build_corner_guide_elbow.py, slice_corner_guide_elbow.py, validate_corner_guide_elbow.py and package_corner_guide_elbow.py in scripts/.

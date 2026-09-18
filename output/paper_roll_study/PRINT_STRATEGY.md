# Diagonal rails and sacrificial stacks

A1 Mini nominal volume is 180 × 180 × 180 mm. At 45°, a rectangular footprint of length L and maximum width W occupies (L + W)/sqrt(2) on each bed axis. With 5 mm margins, **L + W ≤ 240.416 mm**. All tongues, holders, starter feet and brims count. A 20 mm-wide part permits 220.4 mm total length; a 32 mm-wide connector envelope permits only 208.4 mm. The raw 254.6 mm diagonal is a zero-width line.

## Actual sliced samples

| Sample | Rails | Bed envelope | Height | PETG | Estimated time |
|---|---:|---:|---:|---:|---:|
| DIAGONAL_1x220 | 1 × 220 mm | 169.7 mm square | 13.0 mm | 15.9 g | 43 min |
| DIAGONAL_8x220 | 8 × 220 mm | 169.7 mm square | 99.8 mm | 104.3 g | 4 h 19 min |
| DIAGONAL_13x198 | 13 × 198 mm | 154.1 mm square | 161.8 mm | 150.7 g | 6 h 17 min |
| 06_OVERNIGHT_26_RAILS | 26 × 198 mm, two stacks | 169.7 mm square | 161.8 mm | 301.4 g | 11 h 54 min |

Bambu Studio estimates: A1 Mini 0.4 mm nozzle, Generic PETG, 0.2 mm layers, 3 walls, 15% infill, textured PEI, supports off, no brim; times include startup. Actual printer/filament conditions will differ. Exact source files and sliced projects are supplied. No printer job was sent.

The two-stack plate has 2 mm between its starter feet. Both stacks print together by layer. It produces 5.148 m of plain rail: 1.8× the length of thirteen 220 mm rails, but shorter rails mean more eventual frame connections. These are **manufacturing samples without final rail-end joinery or magnet lugs**, not pieces to assemble into the gate. Integrated lugs may invalidate this footprint or the stacking orientation. Keep spring keys and lugs out of sacrificial seams; refine rail bodies after choosing the joint.

## First test: three short stacks

Print `03_STACK_SEPARATION_TESTS` before a tall run: 33.3 g, about 94 min. It contains:

- `STACK_TEST_06`: three 60 mm rails, continuous 0.6 mm scoring neck.
- `STACK_TEST_08`: same, with 0.8 mm neck.
- `STACK_TEST_TABS`: 0.6 mm-wide, 2 mm-long tabs on 10 mm pitch between upper rails; the intervening 8 mm spans must bridge.

The initial 0.4 mm neck disappeared in the standard slicer profile, causing empty layers; it was removed from the supplied kit. All current continuous necks survive slicing, and extrusion was checked at every neck height. The initial tab pattern also triggered a floating-cantilever warning. Adding a terminal tab at each end removed that warning; all current slices are warning-free with supports off. The intervening 8 mm bridges still require physical testing.

Each diamond section expands at approximately 45° from a narrow neck. The starter foot and necks are sacrificial. PETG is fused to PETG here; easy separation is not established. Let the short print cool, support it flat, score the neck from both sides and separate one interface at a time. If it needs excessive force or splits a rail layer, stop that method and record the failure. Measure remaining scars, straightness and cross-section. The 220 mm continuous neck has 3.67× the joined length of the 60 mm coupon; short-test success is not proof of full-length separation.

Do not scale parts to fit: that changes joint clearances. Preserve the supplied 45° orientation. Any added brim must be rechecked against the bed boundary. A simple open air gap is not a substitute for a supporting connection. Taller prints on a moving bed need a successful progressively taller physical trial before treating this as a reliable overnight process.

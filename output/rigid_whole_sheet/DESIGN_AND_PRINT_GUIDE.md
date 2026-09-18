# Rigid whole-sheet gate / printable assembly prototype

Previous folding comparison committed as `d6d0196`. This iteration uses the user's updated allowance for rigid borders about 2.15 m long.

## Full-size iteration

**Full-size parts audit:** see [FULL_SIZE_PARTS_AUDIT.md](FULL_SIZE_PARTS_AUDIT.md). The two full-length rear rib variants exceed the A1 Mini volume. Connector assemblies and rail/rib joins are not yet a complete production BOM. The miniature and five test-sample checks do not establish full-size kit printability.

Four identical rigid borders, each **2145.6 × 562.8 mm**, form the same pinwheel as whole-sheet option C. Each contains three uncut **711.2 × 558.8 mm (28 × 22 in)** posterboard sheets. Twelve sheets per gate, zero paper cuts. Outside dimension **2708.4 mm**; clear opening **1582.8 mm**. The 4 mm cell allowance still accounts for channel backs and clearance.

**No hinges, hinge pins, offset mounts or fold locks.** Two internal sheet boundaries per border now use permanent straight workshop splices. The loaded borders travel as four long flat sections. Do not bend them to fit a smaller vehicle; allow padding between paper faces. Approximate section thickness is 20–30 mm, subject to final dock design.

Eight removable corner bridge keys (two per seam) join the four borders at the field. Sixteen docks attach the face to the established single PVC backing frame; the four PVC corner braces remain. Internal channel joints stay assembled. Removing folding reduces moving parts, joint play and setup operations, but does not prove sufficient stiffness or wind resistance.

The full-size face still uses slide-in U channels, removable paper end caps, rear cross ribs, workshop nodes, dovetail receivers and accessible release springs. The A1 Mini requires **216 short channel pieces** even without hinges. Removing folding does not remove that workshop assembly labor. The full-size twin-runner corner adapters, rail end-node interfaces and positive PVC keeper still need detailed fit prototypes; they are schematic envelopes in Blender, not a complete production STL kit.

Assembly: set up and anchor/ballast the PVC frame; position the four rigid loaded borders on a flat surface; install eight corner keys; with two people supporting the face, engage sixteen PVC docks. For transport detach the face, release its corner keys, and stack four padded borders. Paper stays installed. Retain the earlier grass-stake and hard-surface ballast/guy arrangements; the small feet in this concept view are not a replacement for those restraints. Use ordinary posterboard as replaceable dry-weather stock.

## Full-size cost estimate

The earlier whole-sheet option estimated 2.370 kg PETG. Removing eight fold assemblies at a 60 g allowance each, including the previous 10% waste factor, saves **0.528 kg**. The new planning figure is **1.842 kg**, or **two 1 kg spools** with about 158 g margin.

At the same $20/kg filament and $0.99/sheet assumptions: approximately **$48.72 consumed face materials**, or **$51.88 cash for two complete spools plus twelve sheets**. This retains the earlier channel, workshop joint, dock and corner-key allowances. It excludes PVC, brace clamps, feet, anchoring, labor, shipping and tax. This is an allowance-based comparison, not a sliced full-size bill of materials; two spools is a target with limited margin, not a guarantee.

## Which scale makes sense?

| Scale | One complete rigid border | Complete gate | Assessment |
|---|---|---|---|
| 1:5 | 429.12 × 112.56 mm | 541.68 mm square | Too long for the A1 Mini as one border; useful only for a single whole-sheet bay (143.04 × 112.56 mm) |
| 1:10 | 214.56 × 56.28 mm | 270.84 mm square | Border still too long |
| 1:12 | 178.80 × 46.90 mm | 225.70 mm square | Nominally inside 180 mm, but little room for positioning/adhesion margin |
| **1:15** | **143.04 × 37.52 mm** | **180.56 mm square** | **Recommended four-piece assembly model; all four borders and eight keys share one plate** |
| 1:16 | 134.10 × 35.18 mm | 169.28 mm square | A complete one-piece display model could fit; loses the useful assembly exercise |

The A1 Mini's official build volume is 180 × 180 × 180 mm. [Bambu documentation](https://cdn1.bambulab.com/documentation/quick-start-f507128172bdf/Quick%20start%20guide%20-%20A1%20mini-EN.pdf)

## What the miniature represents

The miniature preserves the gate's in-plane dimensions at **1:15**, its four rigid borders, sheet boundaries, pinwheel corner seams and two connectors per seam. It is **not** the full-size production STL scaled down. A 0.8 mm printed face represents the paper, a 2.6 mm rim supplies handling strength, and enlarged 3.6 mm sockets accept removable tapered two-peg bridge keys. The miniature uses friction-fit bridges rather than tiny scaled snap springs. Its opening is **105.52 mm**.

This tests proportions, the four-part assembly and connector access. It does **not** test paper sliding, actual PVC attachment, wind strength, full-scale stiffness or latch fatigue. Those need real-stock, full-size interface samples. Scaling a 0.8 mm paper slot by 15 would make it only 0.053 mm wide, which is neither printable with this setup nor appropriate for normal paper.

For real interface checks use the copied **1:1** channel, receiver, shoe, rib and PVC saddle samples in `full_size_fit_samples/`, printed without scaling. They are the earlier provisional coupons. The pipe saddle still needs a positive keeper and final mounting adapter. Test with actual stock/pipe; do not manufacture a whole gate from these samples. Favor in-plane spring flex for FDM rather than through-layer loading. [Formlabs snap-fit guidance](https://formlabs.com/global/blog/designing-3d-printed-snap-fit-enclosures/)

## Printing the miniature

Use a **0.4 mm nozzle, PLA, 0.20 mm layers, supports off**, all parts flat as supplied. Files already contain their final dimensions: **import at 100% scale**, not 6.67%. Check your selected printer, filament and build plate in Bambu Studio before printing. The supplied plate is arranged for printing by layer, not sequentially by object. For adhesion issues, clean the plate and add a modest brim/rearrange as needed.

1. Print `Mini_Fit_Test_and_Feet_LAYOUT.3mf` first. It contains the gauge, one standard key, one looser key and two optional feet. From the gauge's Y=0 end, paired-hole diameters are 3.4, 3.6 and 3.8 mm; the gate uses **3.6 mm**. Try the middle pair. Stop pushing when snug, and confirm you can remove the key. Use the gentler secure fit. If neither works, adjust the key dimensions/XY compensation and retest; do not scale the whole gate to tune the fit.
2. Print `Mini_1to15_Four_Borders_LAYOUT.3mf`: **four identical borders and eight standard keys**, already placed on one bed. If your test favors the looser key, replace the eight keys with eight copies of `mini_bridge_looser_OPTIONAL.stl`. The layout is single-material; colors in Blender distinguish sections only.
3. Lay the borders out in the illustrated pinwheel with the flat faces downward and raised rims upward. Pair the short end of each border with the first portion of its neighbor's long edge. All sixteen bridge pegs have matching holes; the numerical center-alignment check is recorded in `validation.json`.
4. Press two keys into each seam **from the rim side**. Each key straddles the seam and joins one hole in each border. Do not force the wedges fully down to their crossbars. Pull the crossbars to disassemble.
5. Optional: stand the gate in the two feet. Their 3.0 mm open slots accept the 2.6 mm rim. This is a tabletop model, not a fly-through or outdoor test fixture.

Individual STLs are included if you prefer manual placement: print four borders, eight keys and optionally two feet. The solid-geometry PLA estimate for the four borders/eight keys is about **40 g** before slicing effects; use the supplied slicer report for the actual selected profile. **Bambu Studio 2.8.2.61 slicing verification:** complete model plate 35.24 g PLA / about 73 minutes; fit-test-and-feet plate 7.08 g / about 23 minutes, including the profile’s start/end overhead. Both sliced successfully for the A1 Mini 0.4 mm / Generic PLA / 0.20 mm profile, with supports off and no plate warnings. Totals are about 42.3 g and 96 minutes for both plates; actual printing can vary. Open the corresponding `sliced/` 3MF project to inspect the profile and preview before printing.

## Validation and files

`Rigid_Whole_Sheet_Gate.blend`: six scenes, full-size concept and miniature assembly/print layout. `printable/`: geometry-only 3MF layouts and individual STLs. `sliced/`: Bambu Studio A1 Mini / Generic PLA slice projects and estimates. `slicer_profiles/`: resolved copies of the locally installed Bambu presets used for verification. `validation.json`: manifoldness, bounds, mass geometry and peg/socket alignment.

Digital checks do not replace a real fit print. No print job has been sent to the machine.

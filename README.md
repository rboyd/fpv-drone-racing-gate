# FPV racing gate design

Recommended next print: [24 × 8 inch clickable paper-frame demonstrator](output/full_width_demo/index.html), with [sliced print queue and assembly PDF](output/full_width_demo/Assembly_and_Print_Queue.pdf). Four main part types / 42 pieces; 211 g PETG across five plate runs, plus a small initial fit check.

Latest study: [paper-roll face, picture-frame click joints, magnets and diagonal print stacks](output/paper_roll_study/index.html). Includes [Blender scenes](output/paper_roll_study/Paper_Roll_Joinery_Study.blend), [visual PDF](output/paper_roll_study/Paper_Roll_Study.pdf), [test instructions](output/paper_roll_study/STUDY_AND_TEST_GUIDE.md), and A1 Mini PETG fit plates. Four 2090.4 × 609.6 mm paper strips; one PVC backing frame. Full-gate members are schematic; exported parts are experimental interfaces and manufacturing samples.

Assembly instructions: [two-part PDF — nine-piece prototype and full gate](output/a1_full_size/Assembly_and_Test_Instructions.pdf).

Committed whole-sheet baseline (`732f592`): [full-size whole-posterboard gate for the A1 Mini](output/a1_full_size/index.html), with [Blender assembly](output/a1_full_size/A1_Full_Size_Gate.blend), [19-type / 740-piece BOM](output/a1_full_size/BOM.csv), and a [1:1 interface fit kit](output/a1_full_size/sliced/Fit_Kit_1to1_LAYOUT/Fit_Kit_1to1_LAYOUT_A1Mini_PETG.3mf). Channels are standardized to just two types (120 long, 96 short). Every unique part fits 180 mm cubed and slices without supports. About 2.97 kg PETG per gate, plus 856 ties: substantial workshop labor. Physical validation remains outstanding. Read the [build guide](output/a1_full_size/BUILD_AND_PRINT_GUIDE.md).

The [earlier rigid concept and 1:15 tabletop model](output/rigid_whole_sheet/index.html) remain available. The material estimate and full-size printable geometry in the new iteration supersede that concept.

## Earlier Coroplast design

Open [the visual index](output/START_HERE.html) or [the Blender model](output/FPV_Gate_2700.blend).

Current design: four symmetric six-sided face panels, four 150 mm square corners, one shallow PVC backing frame with four corner braces, printed joints at both ends of each corner brace, and grass/hard-surface base configurations. A shared corner sheet yields 128 squares for 32 gates.

- [Build guide and assumptions](output/BUILD_GUIDE.md)
- [Assembly view PDF](output/Assembly_Views.pdf)
- [Material list](output/BOM.csv)
- [Hard-surface add-on](output/HARD_SURFACE_ADD_ON.csv)
- [PVC cutting list](output/PVC_CUT_LIST.csv)
- [Printable STLs](output/printable/)
- [Sheet and attachment templates](output/cut-layouts/)

Prototype: digital geometry checked; physical fit and wind/base performance require validation before use. See the guide.

Regenerate locally:

```sh
blender -b -t 8 --python scripts/build_gate.py
python3 scripts/validate_layout.py
python3 scripts/package_deliverables.py
```

The package script needs Pillow. Blender geometry uses metres; displayed dimensions and exported STLs use millimetres. To render only specific views, set `RENDER_SCENES` to comma-separated Blender scene names.

Earlier versions are archived under `output/previous_rectangular_design/` and `output/previous_double_frame_design/`. User-supplied screenshots and `WIP-design.md` remain unchanged.

Previous single-frame design: commit `55f2808`. Current iteration: `iteration/symmetric-square-corners`. Three cutting/marking jigs fit the Bambu A1 Mini; see Blender scene `10_CUTTING_JIGS` and the guide.

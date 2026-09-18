# FPV racing gate design

**Next print:** [four-piece A1 Mini click-joint test](output/first_frame_print/index.html) — two identical branch rails and two keys, **80.14 g PETG / about 3 h 20 min**. Test a straight connection, release it, then build a T with the same parts. [Prepared 3MF](output/first_frame_print/sliced/FIRST_FRAME_TEST/FIRST_FRAME_TEST_A1Mini_PETG.3mf), [assembly/test PDF](output/first_frame_print/First_Frame_Test.pdf), [Blender scenes](output/first_frame_print/First_Frame_Print.blend). An alternate plate includes one optional paper pad.

Current attachment iteration: [one-piece PVC sleeve integrated into the frame rung](output/sleeve_paper_gate/index.html), with [Blender model](output/sleeve_paper_gate/Sleeve_Paper_Gate.blend) and [assembly PDF](output/sleeve_paper_gate/Sleeve_Gate_Assembly.pdf). No bolts, nuts or additional cord stays at the face-to-PVC attachment. **With optional front paper pads: 560 pieces / 8 types / 6.995 kg PETG / 286 printer-hours; without pads: 424 / 7 / 6.792 kg / 277 hours.** The frame-side magnet holders retain their plastic skin, and the sleeve retains its peaked roof. After the click test, use [one sleeve print](output/sleeve_paper_gate/sliced/Q_RUNG_SLEEVE_TAIL/Q_RUNG_SLEEVE_TAIL_A1Mini_PETG.3mf): 49.4 g, about 2 h 20 min. This replaces the bolted dock in the preceding iteration.

Preceding bolted-dock iteration: [reinforced paper gate with integral paracord cleats](output/full_paper_gate/index.html), [Blender assembly](output/full_paper_gate/Full_Paper_Gate.blend), and [full assembly PDF](output/full_paper_gate/Full_Gate_Assembly.pdf). **624 pieces / 10 types / 7.13 kg PETG / 295 printer-hours / 112 plate runs.** The new side socket preserves a continuous spine. All parts fit the A1 Mini and slice without supports. Physical testing remains outstanding.

Earlier bracing prototype: [T01 reinforced branch and cleat test](output/full_paper_gate/sliced/T01_BRANCH/T01_BRANCH_A1Mini_PETG.3mf), followed by the reusable full-width X-braced bay described in the guide. The old [24 × 8 inch demonstrator](output/full_width_demo/index.html) is archived at `bb96e74`; its DEMO_EDGE has a weak cross-socket neck and is superseded.

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

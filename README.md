# FPV racing gate design

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

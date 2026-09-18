# Reproduce this study locally

Run from the repository or extracted kit root. Requires local Blender 5.x and Bambu Studio with A1 Mini / Generic PETG profiles at the macOS paths used in the scripts. Packaging uses Python with ReportLab. No command sends a print job.

```sh
blender -b -t 8 --python scripts/build_paper_roll_study.py
python3 scripts/slice_paper_roll_study.py
blender -b -t 8 --python scripts/check_paper_assemblies.py
python3 scripts/validate_paper_roll_study.py
python3 scripts/package_paper_roll_study.py
```

For geometry-only regeneration, use `RENDER_SCENES=''` before the first command. Render later with `blender -b -t 8 --python scripts/render_paper_roll_study.py`. The checked-in reference meshes are needed for scene 10. Build scripts import helper prefixes from `build_gate.py` and `build_a1_full_size.py`; those helper source files and `face_geometry.py` are included in the kit.

Source STL and 3MF coordinates are millimetres; Blender geometry is metres with metric display. Use supplied print orientations and 100% scale.

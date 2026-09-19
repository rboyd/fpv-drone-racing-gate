# GEPRC MK4 drone reference

**Dendy — Printable parts for GEPRC MK4 7in FPV drone frame**

Source: https://www.printables.com/model/1515387-printable-parts-for-geprc-mk4-7in-fpv-drone-frame

Downloaded by the user as `printable-parts-for-geprc-mk4-7in-fpv-drone-frame-model_files.zip`. The supplied [Printables PDF](Printables_Model_1515387.pdf) identifies **Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)**: https://creativecommons.org/licenses/by-nc/4.0/ .

Dendy explicitly states that they are **not the original creator of the MK4 frame** included in the STEP files. Preserve that qualification and underlying third-party rights; the download is used as a dimensional reference, not represented as a newly authored or manufacturer-certified drone design.

The complete `3D STEP/geprc-mk4-7in.stp` assembly was tessellated with OpenCascade, imported into Blender, reoriented upright and positioned in the gate. Source propellers, motors, camera, covers and antennas remain. A clearly identified hypothetical 110 × 40 × 45 mm battery, straps and swept-prop outlines were added for illustration. No scale change was applied beyond unit conversion from millimetres to metres.

The imported drone geometry in `output/drone_clearance_study/Drone_Clearance_Study.blend`, `output/compact_gate_study/Compact_Gate_Study.blend` and its appearances in study renders/PDFs retain the reference's CC BY-NC terms and attribution. Original gate material retains the project's CC BY-NC-SA terms. These components are separately licensed, not relicensed together under a blanket grant. The root project license does not override the drone reference license.

The 174 MB source STEP remains in the user's download, outside Git. `source.json` records its checksum. Recreate the intermediate GLB with `scripts/import_geprc_reference.py`; the resulting Blender study embeds the tessellated geometry and does not require the original STEP to view.

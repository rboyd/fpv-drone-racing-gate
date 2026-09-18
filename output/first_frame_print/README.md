# First frame print: one A1 Mini plate

Print [FIRST_FRAME_TEST_A1Mini_PETG.3mf](sliced/FIRST_FRAME_TEST/FIRST_FRAME_TEST_A1Mini_PETG.3mf): **four pieces, 80.14 g PETG, about 3 h 20 min**. This is the recommended first run. All parts are full-size production geometry, identical to the current sleeve-gate STLs.

[Illustrated assembly and test PDF](First_Frame_Test.pdf) · [Blender scenes](First_Frame_Print.blend) · [Visual index](index.html) · [Complete test kit](First_Frame_Print_Kit.zip)

| Part | Quantity | Dimensions mm | Purpose |
|---|---:|---|---|
| EDGE_BRANCH | 2 identical | 136.314 x 76 x 29 | Test both end and projecting side receivers |
| CLICK_KEY | 2 identical | 66 x 32 x 5 | One connects the rails; one spare/comparison |
| PAPER_PAD | 0; optional 1 | 24 x 24 x 3 | Optional comparison of paper clamping methods |

The first two rows are the entire recommended print: **two unique types**. The spare key is useful if a hook breaks during testing. Straight and T configurations each use two rails and one key; assemble them one at a time. No magnets, cord, PVC, bolts or adhesive are needed for the click test.

## Optional paper-pad plate

Use [FIRST_FRAME_TEST_WITH_PAD_A1Mini_PETG.3mf](sliced/FIRST_FRAME_TEST_WITH_PAD/FIRST_FRAME_TEST_WITH_PAD_A1Mini_PETG.3mf) instead if you also want the pad: **five pieces, 81.63 g, about 3 h 24 min**. Choose one of the two files, not both. The optional pad adds 1.49 g and approximately 3.6 minutes. The frame-side magnet holders are unchanged: the rear magnet stays behind 0.4 mm of plastic. The PVC sleeve retains its peaked roof and is not needed on this first plate.

## Print settings and placement

Open the prepared 3MF as a project in Bambu Studio. Select your actual PETG filament and A1 Mini with 0.4 mm nozzle. The supplied slice uses Generic PETG, 0.20 mm layers, four walls, 20% infill, textured PEI, no supports, no brim, and print by layer. Print one color; render colors only distinguish the parts. The smooth paper faces lie on the bed, with cleat posts upward. Keep the supplied flat orientation and 100% scale. Re-slice if you change filament/profile settings.

The models keep at least 5 mm from every bed edge and have no overlap; maximum height is 29 mm. The keys are rotated 90 degrees within the bed plane, not stood on edge. The tightest model-to-model gap is 1.69 mm; keep print-by-layer rather than sequential object printing. Both variants slice without warnings or support toolpaths. Estimates are from the local Bambu Studio slice; actual filament and elapsed time can vary. No print was sent to the printer.

## 1. Prepare the parts

Let the bed cool and remove the parts. Check for strings or first-layer burrs in the receivers and between the key's two central spring prongs. Remove loose strings/burrs only; do not file away the hook shoulders or thin the prongs to force a fit. Keep the second key untouched as a comparison. Record filament, temperature and any cleanup needed.

## 2. Assemble a straight joint

Place both rails smooth-face down with their side branches pointing the same direction. Align one end of a key with an end receiver. Slide it along the rail axis: its two broad outside runners guide it while the two narrow central prongs flex inward. Keep it flat; do not insert downward from above. Hold close to the joint and press until both hook shoulders have passed the receiver shoulders and returned outward. Check engagement visually; a loud click is not required.

Slide the second rail onto the other half of the key in the same way. The assembled length is 286.63 mm. Both paper faces should share the same plane. Apply a gentle axial hand pull and check that the rails remain latched. Check for obvious looseness and small bending movement while supporting the parts near the joint. Stop if you see whitening or cracking; this is a fit test, not a destructive strength test.

## 3. Release and rebuild as a T

From the open rear of the receiver, press both central hook tips toward the center and slide the rail straight off that end of the key. Release the other end the same way. Do not twist the rail, pry the key upward or bend the whole rail as a lever. If the tips cannot be reached and released comfortably by hand, record that as a design failure rather than forcing the joint.

Insert the same key into one rail's projecting side socket. Connect an end of the other rail to the exposed key at 90 degrees. Keep both smooth faces coplanar. This tests the full gate's actual crossmember interface, although the short test uses a second branch rail in place of a full crossmember. Repeat the pull, play and release checks.

## 4. Repeat and report

Aim for 20 assembly/release cycles in each configuration as an initial screening test. Try the spare key too. Check that both hooks spring back and latch, hand release remains practical, and no new cracks, permanent bending, whitening or increasing play appear. Twenty cycles is a workshop screen, not a fatigue rating. Record which receiver (end or side) is tight/loose, whether one key differs, and photographs of the latch if it fails. Do not scale the whole part to tune clearance; revise the interface after the physical test if needed.

## Optional magnet comparison

Add two 6 x 2 mm magnets and an offcut of the intended paper. Seat one rear magnet in a rail's 6.3 mm pocket, with compatible retaining adhesive if required, observing its cure time. Check attraction before fixing either magnet. The two alternatives are:

- No pad: rear magnet -> unchanged 0.4 mm frame plastic -> paper -> bare front magnet.
- Optional pad: rear magnet -> unchanged 0.4 mm frame plastic -> paper -> 0.4 mm pad plastic -> front magnet in pad.

Use the same front magnet for successive comparisons before bonding it into the optional pad, or use a third magnet to keep both options ready. Compare sliding, peeling, paper marking and ease of removal. The pad spreads contact across a larger area and is easier to handle, but adds a plastic gap. The small plate only tests local grip, not retention of a full paper border.

## After the click test passes

Next print one production RUNG_SLEEVE to test actual PVC fit, then the 609.6 mm-wide braced bay in the [full gate guide](../sleeve_paper_gate/README.md). The four pieces here can be reused; deduct them from the later queue. This plate demonstrates joinery at 1:1 scale; it is not a complete two-foot-wide frame or a wind test. Physical fit, strength and durability remain unverified until you print it.

The current gate BOM and queue label PAPER_PAD as optional: 424 pieces / seven types without pads, or 560 / eight with all 136 pads fitted. All frame-side magnet holders and the peaked sleeve roof remain unchanged.

Rebuild in the repository with scripts/build_first_frame_print.py, scripts/slice_first_frame_print.py, then scripts/package_first_frame_print.py. The build imports the existing production geometry and asserts that its STL exports match the full gate byte-for-byte.

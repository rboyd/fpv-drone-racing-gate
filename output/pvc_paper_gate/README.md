# PVC-dominant paper gate / single and Split-S

The previous reinforced print-track design and first click-test plate were committed as **eda5b20**. This new iteration replaces the printed track with **one outer PVC perimeter and one PVC ring around each opening**, joined by four diagonal PVC spokes at the overall corners. All pipe is nominal 1-inch PVC (33.4 mm OD). Paper hides the structure head-on; only paper and bare front magnets are visible in the face area.

[Blender model](PVC_Paper_Gate.blend) · [Visual design/assembly PDF](PVC_Gate_Study.pdf) · [Rendered single gate](renders/01_SINGLE_FRONT.png) · [Rendered Split-S](renders/03_SPLIT_S_FRONT.png) · [Rear structure](renders/04_SPLIT_S_BACK.png) · [Kit](PVC_Paper_Gate_Kit.zip)

## Recommendation and measured cost

Use the **stack-ready single** as the development baseline: **62 printed pieces in five types, 1.759 kg PETG, 71.0 print-hours, 16 plate runs, and six 10-ft PVC lengths at your $6 price**. The longest cut pipe is 1990.4 mm, retaining the approximately 2.15 m transport limit. Short members disconnect at cord-retained sockets.

| Configuration | Printed pieces | PETG | Print time | PVC sticks / cost | PVC + PETG subtotal* |
|---|---:|---:|---:|---:|---:|
| Basic single; 2.5 m pipes | 64 | 1.370 kg | 56.6 h | 7 / $42 | $69.40 |
| Recommended single; ready to extend | 62 | 1.759 kg | 71.0 h | 6 / $36 | $71.17 |
| Two-level Split-S | 108 | 2.814 kg | 114.5 h | 10 / $60 | $116.27 |

*PETG cost assumes $20/kg, not a current supplier quote. Estimates are actual local A1 Mini slices: 0.4 mm nozzle, 0.20 mm layers, four walls, 20% infill, Generic PETG, supports off. The subtotal covers the **face skeleton only**. Add magnets, paper, cord, adhesive, base/feet, ground stakes or ballast, and external guys. It is not a complete installed-obstacle price. Manual work, failures and reprints are excluded from printer-hours.

Two full 1 kg spools cover the recommended single with 10% allowance (1.935 kg). The Split-S uses 2.814 kg before allowance: three spools nominally, four if budgeting 10% extra. Optional front pads add material and time; they are excluded from these totals.

For a fair printed-face comparison, the prior sleeve design excluding optional pads and PVC-brace clamps used 6.132 kg / 252.4 hours. The new recommended single reduces that PETG by 71.3% and print time by 71.9%. The tradeoff is more PVC and cord work. The no-transport-joints basic option prints less, but needs seven sticks due to offcuts and has 2500 mm pipe pieces. The recommended version costs only $1.77 more in the modeled materials.

## Five printed types

| Part | Single ready | Split-S total | A1 Mini print bounds mm |
|---|---:|---:|---|
| OUTER_90_45 | 4 | 4 | 122.0 x 122.0 x 53.84 |
| STACK_TEE | 4 | 10 | 160.0 x 122.0 x 53.84 |
| EDGE_SLEEVE | 42 | 74 | 20.0 x 62.3 x 52.709 |
| INNER_90_45 | 4 | 4 | 151.489 x 151.488 x 53.84 |
| CORD_SADDLE | 8 | 16 | 34.0 x 20.0 x 12.0 |

**OUTER_90_45** combines two perpendicular sockets and an inward diagonal socket. **INNER_90_45** has the same perpendicular sockets but its diagonal points outward, away from the opening. They cannot be the same rotated part. Each has an integral magnet pocket, broad 32 x 12 mm connecting webs, raised cord eyes, and a two-horn cord cleat. Socket walls are nominally 4 mm, with 30 mm pipe engagement to a positive end stop.

**STACK_TEE** is used in all ten tee locations of the stacked gate: eight divider junctions and two transport joints. It has four available magnet pads so the same part can rotate to either side; populate only the pockets listed in the magnet map. Its unused branch port at a transport joint stays empty and concealed behind paper. The single version includes four tees: two side riser tees for the future divider and two horizontal transport tees.

**EDGE_SLEEVE** slides over bare PVC before fitting the ends. Its 3.2 mm nominal wall and 14 mm axial length support a magnetic pad offset 32 mm from the pipe axis. Use the raised cord eye to set rotation and the indexed cord/stop knots to set position. It is a clearance sleeve, not a friction clamp. **CORD_SADDLE** is a small magnet backing threaded on a seam cord; two span each short paper overlap without an extra PVC member.

Every production part is a connected, manifold mesh and fits inside the A1 Mini's 180 mm cube with the supplied placement margin. Maximum part extent is 160 mm. The pipe axes are only **24 mm behind the paper**, reducing solid material below the sockets. Accepted peaked roofs remain. The magnet pocket remains **6.3 mm diameter with 0.4 mm of plastic between rear magnet and paper**; it is not a flush/open frame-side holder.

## Paper face and magnet alignment

Outside dimensions remain **2700 x 2700 mm** for one opening, or **2700 x 4790.4 mm** for two. Each clear paper opening is **1480.8 x 1480.8 mm**. The shared divider is one 609.6 mm band, not two overlapping full bands. With the illustrative 50 mm ground clearance, the Split-S top is 4840.4 mm above ground.

Use the full 609.6 mm roll width throughout. This iteration changes the pinwheel cutting pattern to simpler horizontal bars and side inserts that also work at the shared divider:

- Single: **two 2700 mm cuts and two 1552.8 mm cuts**. The side inserts overlap the horizontal bands by 36 mm at both ends. Total roll consumption 8.5056 m; three single gates fit on a 100-ft roll.
- Split-S: **three 2700 mm cuts and four 1552.8 mm cuts**. Total 14.3112 m; two stacked gates fit on a 100-ft roll.

The outer PVC axes are 50 mm inside the paper outline. The inner axes sit 50 mm behind the opening boundary in plan. A 32 mm pad offset puts magnets **18 mm inside the paper edges**, and the overlap seam centers are also 18 mm from the side-insert cut ends. No pipe or printed fitting protrudes into the opening or beyond the face in the checked front projection. This is a head-on appearance goal; supports may be visible from oblique/rear views, and paper can deflect in wind.

Use **124 magnets for the single, 216 for the Split-S**, all 6 x 2 mm, paired front/back. Start with the spacing shown (roughly 300-350 mm on long edges); it is a prototype spacing, not established wind retention. The smaller count than the printed-rail design needs physical paper/grip testing.

Bond the rear magnets with compatible adhesive after checking polarity. Stack without optional pads: **rear magnet -> 0.4 mm printed skin -> paper -> bare front magnet**. Optional PAPER_PAD adds its own 0.4 mm skin and a handle around the front magnet. It is a test/comfort option, not required for the paper-only front appearance. No new front pad design is needed.

For accurate placement, use Sleeve_Positions.csv to mark the PVC, rotate each sleeve until its paper face is coplanar with the corner pads, and lock that position on the prethreaded cord with stopper knots on both sides of its eye. Set the paper edge 18 mm beyond the magnet centers. Attach loose front magnets directly over the fixed rear magnets; they self-align. Do not perforate the paper. The Paper_and_Magnet_Map.svg and Magnet_Positions.csv provide the exact layout; the SVG shows magnets at true scale.

## Cord assembly and retention

Use the previously selected **2.4 mm 275 paracord**. Socket draw lines run from fitting to fitting along each PVC member, through the relevant sleeve eyes on straight members. Keep the line on the paper-edge side of the pipe foot, clear of the socket mouth. They pull the fittings against the pipe end stops; bare dry-fit friction is not treated as retention. Wrap diagonal draw cords **over the backs of the socket shells**, then finish on the central cleats, so they do not pass through a solid socket root.

Tie one fixed end, feed slack through the guides, hold the final tail, and pull only enough to seat both pipe ends. Make two figure-eight wraps around the receiving two-horn cleat and finish with a locking half-hitch. Leave a 100 mm tail. To release, hold the tail, undo the hitch and unwrap. Do not tension until PVC bows. Use separate lines for the seam backers and X braces so replacing paper does not loosen pipe joints. The X cords stay inside the side paper bands and never cross an opening.

The supplied centerline drawings show principal routes and raised eye locations; knots, contact bends around the sockets, and every turn through an eye are not simulated. Prototype the routing and hand access before repeating it. The cord scheme has not been load tested. Printed sleeve rotation, cord stretch and knot slip remain physical-test items. Mark socket insertion depth, sleeve position and cord tail after the first successful fit-up; leave sleeves and their locating cords on the pipes in transport.

Cord_Cuts.csv includes generous tie allowances: **38.7 m for the single face, 67.2 m for the stacked face**. External guys are additional. These are cut allowances, not a reason to tension hard. Recheck slack after settling and warm exposure.

## Single gate assembly

1. Print the FIRST_FIT plate and test the actual pipe first. Once it passes, print one INNER_90_45 and one STACK_TEE before committing to the full queue. Neither is included in FIRST_FIT.
2. Cut and label PVC from the stock layout. The six-stick single layout reserves 10 mm per stock end allowance and 3 mm kerf per cut, but several sticks have only about 8.3 mm remaining after those allowances. Measure actual stock and kerf before cutting; do not round all cuts upward. Cuts use **center spacing minus 100 mm** because every fitting's pipe stop is 50 mm from its node center.
3. Slide the indicated EDGE_SLEEVEs onto each labeled bare pipe. Use Sleeve_Positions.csv, measured from the cut start named in PVC_Cuts.csv. Thread the locating cords before fitting the pipe ends. Keep every flat paper face in the same plane.
4. Assemble the outer ring on a flat surface. The top and bottom each use two 1200 mm pipes and one tee transport joint. Each side uses a 1990.4 mm pipe, a tee and a 409.6 mm pipe. The tee's spare port points inward. Outer corner-to-corner pipe-axis spacing is 2600 mm.
5. Assemble the inner square from four 1480.8 mm pipes. Its pipe-axis spacing is 1580.8 mm. Connect corresponding corners with four 620.683 mm diagonal pipes. Lay all corners in the orientations shown in Blender before inserting the diagonals.
6. Seat all pipes 30 mm into their sockets. Tension the socket draw cords gradually, check squareness, then set the side-band X cords. Fit the seam cords and slide on two CORD_SADDLEs per seam. Fix their marked positions with small stopper knots.
7. Install rear magnets and allow adhesive to cure. Lay on the two horizontal paper bands, then the side inserts with their 36 mm overlaps. Work from corners along each edge, adding front magnets directly over the rear pockets. Confirm only paper and magnets show from the front.
8. Test retention and handling flat, then install a suitable base and anchoring system before standing the gate. Do not lift or carry the assembly by paper or magnetic pads.

## Upgrade to a two-level Split-S

The digital cut ledger confirms **every existing pipe length is reused without cutting**. Add **six STACK_TEEs, 32 EDGE_SLEEVEs and eight CORD_SADDLEs**. Add PVC cuts: **two 1990.4 mm, four 1480.8 mm and four 409.6 mm**. Those additions fit four more 10-ft sticks, bringing the total to ten. Add 92 magnets, additional cord, one 2700 mm paper band and two 1552.8 mm side inserts.

With the single gate lying flat, remove its paper and slacken the draw cords. Move the entire outer top bar (including its middle tee), its two outer corner fittings, the inner top corner fittings and the two top diagonal pipes to their new top positions. Keep the original inner top 1480.8 mm pipe as the lower divider-opening rail, replacing its two corner fittings with tees. The old upper outer corners become new tees at the upper divider height. The preinstalled side tees form the lower divider junctions.

Connect each divider rail outward to the side uprights with two 409.6 mm stubs. Retain the original two short side risers between the divider's outer tees. Add the upper outer risers, the upper opening's two inner uprights, and its bottom/top horizontal rails. Check the two divider axis heights: **2140.4 and 2650 mm measured from the paper bottom**, a 509.6 mm spacing. This leaves room for the one 609.6 mm paper divider while the sleeves place magnets at its two opening edges.

Re-thread and tension with the assembly flat; then add the additional paper and magnets. The shared middle uses straight tee connections, so there are no crossing in-plane PVC diagonals. The extra tee ports and aligned pipe stops are what make this a reusable extension system rather than two independent square gates stacked into each other.

## First print and acceptance checks

[Open FIRST_FIT_A1Mini_PETG.3mf](sliced/FIRST_FIT/FIRST_FIT_A1Mini_PETG.3mf): **124.59 g, 4.95 hours**, five pieces: one outer 90+45 corner, one edge sleeve, one cord saddle, one short bore gauge, and one optional front pad. It demonstrates the new PVC socket, magnetic face and cord interface; the earlier click-test plate remains available in the committed iteration.

Use actual clean 33.4 mm OD PVC offcuts, a short paracord length, paper and four magnets for two grip sites. Check the gauge first, then full 30 mm socket seating without force; a short gauge does not prove the full socket fit. Check extraction after relaxing cord, loop clocking, knots, cord access around the 45-degree socket and coplanar magnet faces. Test bare front magnet vs optional pad, then repeat assembly at least 20 times. Check whitening, cracks, looseness, pipe withdrawal and permanent deformation. Scale must stay 100%; revise the bore clearance itself if necessary.

All seven exported masters (five production types, a gauge and an optional pad) are connected/manifold and within A1 Mini bounds. All supplied recipes have 5 mm minimum bed margin, no part overlap, no supports and no slicer warnings. Quantities match the modeled parts, magnet positions match real pockets, and sleeves sit on exposed pipe rather than over a fitting. These are digital checks, not physical strength or fatigue certification.

## Base and outdoor limits

The new face skeleton is a **fabrication prototype and assembly study**, not a wind-qualified complete obstacle. Scene 10 shows the required concept of separate feet/ballast and four external guys; the bag sizes and feet are placeholders and are **not** a ballast prescription. For soil use suitable anchored guys/feet; hard surfaces require attached ballast/feet sized for the actual setup. The 4.79 m face is much taller than the single version, so do not reuse the old single-gate ballast amount as an assumed rating. Keep anchors/guys outside the openings, attach them around structural PVC near nodes, and assemble/raise with helpers.

Ground hardware is deliberately excluded from the face cost/queue. Its sizing and attachment are the next engineering step after the corner/cord prototype works. Paper weather resistance, 6 mm magnet pull through the plastic skin, sleeve clocking and cord preload also remain to be proven in real conditions. A paper face at this size can catch wind even if the PVC joints are rigid.

## Sources and assumptions

- [FORMUFIT PVC sizing](https://formufit.com/pages/pvc-101): nominal 1-inch PVC is approximately 1.315 inch OD. The CAD uses 33.4 mm and a 34.2 mm trial bore; measure your pipe rather than treating that clearance as universal.
- [FORMUFIT assembly guidance](https://formufit.com/pages/building-projects-with-pvc-pipe): dry friction joints are a temporary assembly method, not adequate justification for a loaded structure. Our removable cord retention is an original prototype proposal and is not endorsed or validated by that guidance. PVC solvent cement is not assumed to bond PETG.
- [Prusa modeling guidance](https://help.prusa3d.com/article/modeling-with-3d-printing-in-mind_164135): supports/overhangs and tolerances depend on geometry and settings. Peaked bores were also checked by slicing with supports off; successful real printing is still to be tested.

Your PVC price is used as given. No MultiGP compliance or official course dimensions are claimed; the approved dimensions and reference image determine this concept. Rebuild with build_pvc_paper_gate.py, slice_pvc_paper_gate.py, validate_pvc_paper_gate.py and package_pvc_paper_gate.py. No printer job has been submitted.

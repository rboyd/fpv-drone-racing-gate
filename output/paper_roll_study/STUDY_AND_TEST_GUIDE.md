# Paper-roll gate / picture-frame joinery study

Baseline committed as **732f592**. New work is on `iteration/paper-roll-click-magnet`. Open `Paper_Roll_Joinery_Study.blend` or `index.html`; the visual PDF includes the illustrated views. This is a design comparison and a set of full-scale interface tests, **not yet a production gate kit**. The 25 STL variants include clearance trials and stack experiments, not 25 required gate part types.

## Chosen paper layout

Four identical **2090.4 × 609.6 mm** strips form a pinwheel: 2700 mm outside, 1480.8 mm opening. Use the roll at its full 24-inch width. Make four crosscuts per gate after squaring the roll's leading edge. A 100-ft / 30.48 m roll supplies three complete gates plus two spare strips and approximately 1.21 m remaining. Transport four rigid borders approximately 2.09 m long, with faces attached. No hinges are proposed.

The linked roll was listed at $32.99 when researched. At that illustrative price, paper consumed is $9.05/gate, or $11.00/gate if allocating a whole roll across its three complete gates and treating spare material as reserve. Paper thickness and outdoor durability are unconfirmed. Treat this as a replaceable dry-weather face; it does not brace the frame.

## Three joint combinations

| Option | Frame connections | Paper attachment | Main tradeoff |
|---|---|---|---|
| A | Positive click keys | Snap-over battens | Lowest magnet cost; paper grip and gentle removal need testing |
| B | Keyed magnetic splice caps | Magnetic pads | Easy release, but a peeling load can also release structural splices |
| C — preferred trial | Positive click keys | Magnetic pads | Structural joints stay mechanically latched while paper is removable |

Tony Youngblood's supplied modular picture-frame model is shown in Blender scene 10. Its repeated teeth, modular members and calibrator are useful precedents. Its instructions require supports under some edges, so those source meshes are not included in our print plates. Our new key uses two planar spring forks with pinch release and two rigid dovetail guides. Guides locate the joint and resist lift; hooks resist axial withdrawal. The latch should relax after engagement, rather than remain bent. These are newly modeled parts, not compatible copies of the source frame or Kato train track.

The pictured test key is replaceable if worn. Production rail bodies would use the selected socket clearance and hide no spring under paper. Keep release access on the rear. Shared keys and sockets should also serve straight splices, corner nodes and the PVC dock; the final corner/diagonal node family remains to be detailed after fit testing.

## Connecting the inner and outer edges

Scenes 11 and 14 compare ten longitudinal bays, a middle paper-support rail and two half-width rows. Rail centerlines are 12 mm inside the paper perimeter: 2066.4 × 585.6 mm. Each half-bay is 206.64 × 292.8 mm; a diagonal is 358.37 mm, so it needs at least two printable segments plus its joint allowance. Those are node-to-node spans, not final STL cut lengths.

| Arrangement | Member length per border | Per gate | Interpretation |
|---|---:|---:|---|
| Ladder | 12.64 m | 50.56 m | Fewest members; relies heavily on stiff joints to resist racking |
| Alternating diagonals | 19.81 m | 79.23 m | Preferred starting geometry: triangles connect both edges through the center rail |
| Full crosshatch | 26.98 m | 107.90 m | 36% more member length than alternating diagonals, plus crossing details |

These are geometric comparisons, not measured stiffness results. Diagonals need positive connections and adequate compression/bending stiffness; loose splices can defeat the triangulation. Full crosshatch also needs a crossing node or a deliberate offset between crossing members. It is shown as a concept, not overlapping production solids.

**Do not make every web as heavy as the stack-test rail.** The 12 mm diamond section slices at roughly 57 g/m after removing its starter-foot allowance. Using it everywhere in the alternating layout would consume roughly 4.5 kg before nodes, docks and magnet pads. At an assumed $20/kg, that is about $90 for members alone. Narrower web sections and fewer bays supported by the PVC are the next cost optimization; they need a representative braced-panel test. This study does not substantiate a one- or two-spool finished gate.

## Half-cylinder magnet holders

Scene 12 and `D_MAGNET_LUG` implement a D-shaped projection toward the paper. Its 10 mm radius half-cylinder contains a rear-loaded 6.3 mm pocket for a 6 × 2 mm disc behind a **0.4 mm local face skin**. The straight flange has two M3 holes for a bench test; in production this lug should be integral with the rail/node, eliminating separate mounting bolts. Rotate the same holder around edges and corners. Pocket position and paper contact stay consistent.

A 24 mm-wide removable `PAPER_PAD` spreads front pressure. It adds another 0.4 mm skin. Thus the actual magnet gap is **0.8 mm + paper + adhesive**, not just paper thickness. Compare the pad against a bare counter-magnet in a controlled bench trial to quantify that extra skin's effect. The final arrangement must retain both magnets: check polarity and dimensions first, then bond them into the pockets against the thin face. No hot-print insertion is needed. Adhesive thickness adds to the magnetic gap.

Use `MAGNET_POCKET_GAUGE` first: with bores upward and its long axis horizontal, diameters run **6.1 / 6.3 / 6.5 mm** from left to right. The gauge pockets are 2.2 mm deep. Measure the actual magnets and the paper; 6 × 2 is a nominal size.

For a given maximum perimeter pitch, each strip also has six interior pads on the middle rail at less than 300 mm pitch. Corner sites are counted only once:

| Maximum edge pitch | Clamp pairs/gate | Individual magnets | Magnet cost at $0.10 / $0.20 / $0.30 each |
|---|---:|---:|---:|
| 300 mm | 96 | 192 | $19.20 / $38.40 / $57.60 |
| 150 mm — pictured | 168 | 336 | $33.60 / $67.20 / $100.80 |
| 100 mm | 240 | 480 | $48.00 / $96.00 / $144.00 |

These are trial spacings, not wind ratings. The cost assumptions exclude shipping, printed pads, PVC and hardware. Magnet-held frame splices would add **four magnets per splice** beyond the paper counts. Dense magnetic retention can cost more and take longer to install than the cheap paper saves. Keep pads and paper on the four borders for transport; only border joins and PVC docks should be operated at the field.

## Frame to PVC: actual mating test parts

Scene 13 shows assembled and exploded versions. `PVC_HALF_33` targets 33.4 mm OD pipe; print two identical halves. Measure your pipe—nominal trade size is not its OD. `PVC_HALF_27` is an alternative collar experiment for 26.67 mm OD, not a second required main-frame collar.

1. Put two `PVC_HALF_33` halves around the pipe, opposed by 180°. Join their ears using two M3 × 25 mm bolts, nuts and washers. The 0.8 mm ear gap allows closing movement; check grip rather than assuming full closure means tight. Test sliding and rotation on the actual pipe.
2. Bolt `DOCK_SOCKET` to one collar's flat pad using two M3 × 25 mm bolts, nuts and washers. Its two round mounting holes register with the pad. Point its open fork entrance away from the pipe. Keep the release throat exposed.
3. Bolt `DOCK_TONGUE` to the middle of `FRAME_DOCK_NODE` using two M3 × 16 mm bolts, nuts and washers. The flange faces register and both holes align. The frame node's two end sockets are for later rail connections using the common click key.
4. Slide the tongue's two rigid runners and central forks into the socket together. Seat the shoulder and inspect both hooks beyond their catches. Pinch the two fork tips inward to withdraw; do not pry the rigid runners upward.
5. Leave the collar/receiver on PVC and the tongue/node on the border during transport. These workshop fasteners are not part of field setup.

For one complete dock: **4 × M3×25, 2 × M3×16, 6 nuts, 12 washers**, plus the five printed pieces (two collar halves, receiver, tongue and node). Horizontal bolt passages have 4.8 mm diamond diagonals, giving about 3.39 mm inscribed circular clearance; the vertical round passages are 3.4 mm. Fit still depends on your printer. Bolt/nut access is external; no heat-set inserts or zip ties are required.

The intended load path is paper → lugs/edge rails → diagonal webs/center rail → spaced frame docks → one PVC square and four corner braces → feet/ground anchoring. Four docks per border are depicted as a starting arrangement. Only the small dock assembly is detailed, not all full-gate interfaces. Keep the previously studied staked grass base or ballasted hard-surface feet; the paper/PETG iteration does not establish a wind/ballast rating. Production angled PVC-brace nodes and gate-corner release joints still need integration.

## Print and test in this order

All source STLs use millimetres. Use the supplied sliced **A1 Mini / 0.4 mm / PETG** projects at 100% scale. Supports are off. No files have been sent to a printer.

1. **Latest concept first — plate `05_D_MAGNET_AND_DOCK`: seven pieces**, approximately 33 g / 1 h 53 min. It contains one D lug, one front pad, two collar halves, one dock socket, one tongue and one frame node. Add two 6 × 2 magnets, a paper scrap, the hardware above and actual PVC. This directly tests your latest holder/dock idea without printing the other variants.
2. **Click and magnetic comparison — plate `01_CLICK_AND_MAGNET_JOINTS`: six pieces**, approximately 24 g / 65 min. Join the two clearance sockets with the double key; test each end separately first. Both spring tips must move freely and return after clicking. For the magnetic comparison, butt two identical rail-end samples together and flip the keyed cap onto them so its four pins enter the holes. Four magnets complete that splice. Test pull, sliding and peel separately.
3. **Paper retention — plate `02_PAPER_CLAMP_TESTS`: eight pieces**, approximately 33 g / 2 h 4 min. Compare 0.4, 0.8 and 1.2 mm frame skins using the same magnets/paper/pad. The two snap-batten caps provide 0.15 and 0.30 mm central paper clearances. Lay paper over the base's central face, push the cap down until its lips catch under the side ledges, and check actual paper grip. A cap that latches but lets thin paper slide has not passed. The end-up battens have small footprints; if adhesion is poor, add a modest brim in Bambu Studio and recheck placement.
4. **Stack strategy — plate `03_STACK_SEPARATION_TESTS`: three short stacks**, approximately 33 g / 94 min. Follow `PRINT_STRATEGY.md`. The tabbed sample now includes terminal tabs and slices without warnings; its 8 mm bridges still need physical testing. Start with the continuous-neck versions. Only then try a single long rail, a taller stack and finally the 26-rail plate.

For each click joint, record insertion force qualitatively, fully seated play and release accessibility. As an initial workshop screen, repeat 20 assembly/release cycles and inspect whitening, cracking and permanent opening. That count is a comparison procedure, not a fatigue-life specification. A magnetic clamp needs three separate observations: straight pull-off, edge peeling and sliding. Use the same slowly applied measured load for comparisons, record the failure load and failure mode, and do not convert that result directly into a gate wind rating. Record whether paper tears before a magnet lets go. Test a short real-paper span at both 150 and 300 mm pad spacing before choosing the full count.

## Verification and limits

`print_checks.json` records 25 manifold positive-volume STL masters, 31 plate/individual layouts and corresponding actual slices. Every exported part and supplied plate fits within the 180 mm cube with bed margin. All current slices are warning-free with supports disabled. Terminal tabs removed an earlier cantilever warning; that does not prove the bridging will print successfully. Continuous stacks have extrusion at every neck layer. Twenty nominal assembled-pair checks find no material intersections above the 0.05 mm³ numerical tolerance, including the assembled dock and PVC pipe. These checks establish digital fit and toolpath presence—not print success, separation quality, latch fatigue, magnetic holding force or outdoor stability.

The production next step is to select one successful key clearance, magnet window and stack neck, then detail the rail endpoints, shared corner/diagonal nodes and brace collars around those measured results. The full-gate Blender scenes label their members and dock sites as schematic so they are not confused with the tested export geometry.

Sources and source-model attribution are in `RESEARCH.md` and `../../reference/picture_frame/ATTRIBUTION.md`.

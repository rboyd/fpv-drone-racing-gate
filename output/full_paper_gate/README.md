# Reinforced paper gate — full design and fabrication prototype

The old demo was committed as `bb96e74`. This iteration replaces its weak perpendicular socket, retains the shared click key, adds integrated paracord cleats, and carries actual printable parts through to a complete PVC-backed gate. The prior DEMO_EDGE is superseded for this construction. This is a digitally checked fabrication prototype, not a physically proven gate or a wind-rated structure.

Open [Blender](Full_Paper_Gate.blend), [assembly PDF](Full_Gate_Assembly.pdf), or [visual guide](index.html). The primary render is [fully assembled](renders/01_ASSEMBLED_FRONT.png); the [rear view](renders/02_REAR_STRUCTURE.png) exposes the structure.

## Decision and cost

The complete reinforced design needs **7.13 kg PETG, 295.0 printer-hours, 112 manual plate runs, 624 pieces and 10 unique printed types**. These are actual local Bambu Studio estimates, not solid-volume guesses. At a planning price of $20/kg, deposited PETG costs about $143; buying eight 1 kg spools is $160. A 10% allowance gives 7.84 kg, so eight spools are appropriate. One or two spools cannot make this design. Shipping, electricity, paper, magnets, PVC and hardware are additional.

This is a large printing commitment. The reinforced frame is not yet a compelling low-cost gate compared with a simpler PVC/Coroplast construction. The value of this iteration is a complete, inspectable load path and reusable test parts. Print the first bay before buying all gate materials. Keep optimization separate from an unproven reduction in the material around the sockets. At 12 printing hours/day the production queue alone takes about 25 days, plus plate handling/retries; continuous time is about 12.3 days.

The selected profile is A1 Mini, 0.4 mm nozzle, 0.20 mm layers, Generic PETG, textured PEI, **4 walls / 20% infill / supports off / no brim**. All 21 supplied plate recipes sliced without warnings. Every mesh and plate fits 180 x 180 x 180 mm with at least 5 mm XY plate margin. Largest individual height is 37 mm. Ordinary flat plates are the production baseline. The earlier diagonal sacrificial stacks remain experiments; their separation and joint preservation have not been validated, so their overnight counts are not used in these estimates.

## What changed at the weak junction

The old cross socket left a nominal 4 x 5 mm neck. The new branch socket projects inward, with its rear pocket ending at local Y=28 mm; the continuous spine spans Y=-8..8 mm and is 12 mm deep. End receiver pads are 8 mm deep and 40 mm wide. A wide triangular root distributes the branch load. The 16 x 12 mm geometric section is not a tested strength multiplier. The replaceable key remains a deliberately small, physically unverified flexure; repeated click and load tests still matter.

Two raised cord-eye posts form a permanent two-horn cleat on every branch rail. Their 45-degree expanding caps and diamond through-holes are designed for support-free printing. Smooth the cord-contact edges. The updated holes accept 2.4 mm cord; this version is not specified for ordinary 4 mm 550 paracord.

## Printed bill of materials

| Part | Gate quantity | Print bounds mm |
|---|---:|---|
| EDGE_PLAIN | 64 | 136.314 × 49.95 × 12.0 |
| EDGE_BRANCH | 48 | 136.314 × 76.0 × 29.0 |
| RUNG | 72 | 133.867 × 49.95 × 12.0 |
| CLICK_KEY | 200 | 66.0 × 32.0 × 5.0 |
| PAPER_PAD | 136 | 24.0 × 24.0 × 3.0 |
| PVC_HALF_33 | 32 | 65.8 × 31.5 × 12.0 |
| DOCK_SOCKET | 16 | 48.0 × 40.0 × 8.0 |
| DOCK_TONGUE | 16 | 46.0 × 32.0 × 37.0 |
| V_BLOCK | 32 | 24.0 × 64.0 × 22.0 |
| CROSS_PLATE | 8 | 70.0 × 70.0 × 6.0 |

Per border: 16 EDGE_PLAIN, 12 EDGE_BRANCH, 18 RUNG, 50 CLICK_KEY, 34 PAPER_PAD, 8 PVC_HALF_33, 4 DOCK_SOCKET, 4 DOCK_TONGUE = 146 pieces. Four borders = 584. Eight brace crossings add 32 V_BLOCK and 8 CROSS_PLATE = 40. Total 624. Empty magnet pockets on outer rung segments are intentional: one universal RUNG replaces extra part variants. Populate only the six middle-rung pockets per border.

## Print a test first

1. **T01_BRANCH once:** one reinforced branch, two click keys and one pad. Check both end and side sockets. Pull through the chosen cord, wrap the cleat and check release. The previous 0.40 mm fit coupon and magnet gauge remain useful, but this receiver has taller walls.
2. **A full-width I-shaped member:** T01 twice plus T02 once gives two branches, three rungs, four keys and two pads (11 pieces). The three rungs and four exposed 14 mm key middles join the two branches across a true 609.6 mm paper width.
3. **One X-braced bay:** T01 four times, T02 twice and T05 twice = 32 pieces: four branch rails, two plain rails, six rungs, twelve keys and eight pads. This is 436.943 x 609.6 mm. Add sixteen magnets, a 609.6 x 436.943 mm paper rectangle and one 3.3 m cord.
4. **Add a PVC dock:** T03 once adds two collar halves, one receiver and one tongue (36 total printed pieces). Add four M3 x 25 cap/pan bolts, two M3 x 25 flat-head bolts, six nuts and ten washers; use a 33.4 mm OD PVC offcut. Test-bay plus dock: 426.7 g, 18.79 h, nine plate runs.
5. **Test a corner brace:** T04 once supplies four V blocks and one crossing plate. Add two M4 x 80 and two M4 x 70 bolts, four nuts, eight washers, main/brace pipe offcuts. Try both +/-45 hole pairs.
6. Build one complete 2090.4 mm border only after the bay and dock behave well. Then finish the other three borders and the backbone. Test parts are production parts and can be reused. Full production queue quantities are gross: subtract accepted test pieces from it; do not print both queues blindly.

## Cord choice, threading and tightening

Use 2.4 mm 275 paracord as the handling-oriented prototype choice. Micro cord (about 1.18 mm) or braided polyester kite line is the lighter option. Supplier fiber recipes vary; 'paracord' is not a precise stretch specification. A line's advertised breaking load is not a working load for our printed cleat. The thicker cord makes threading and gripping easier, but knots and wraps consume more length than the earlier kite-line estimate.

Cut **twenty identical 3.3 m lengths** for the face and **four 4 m lengths** for the guys. Total 82 m; three 100-ft hanks provide 91.44 m. Face alone uses 66 m; calculated routes plus 600 mm knot/wrap allowance would use 63 m, but uniform 3.3 m cuts reduce assembly mistakes. Use a 3.3 m measuring mark on the bench, cut all twenty, and finish ends as appropriate for the purchased material. Do not cut only the visible diagonals.

Each bay uses one continuous cord and one tensioning station. Viewed from the rear with its long dimension horizontal, label its eyes LL (lower left), UR (upper right), LR (lower right), UL (upper left). Use the inward-facing post on each branch: the right post at the left end of the bay and the left post at the right end.

- Tie a double-overhand stopper larger than the eye at the starting end. Thread LL -> UR -> LR -> UL -> LL. This makes two crossing diagonals and two short return legs along the bay ends. At LL the two strands share the eye; keep them side-by-side. Leave the other end as the adjustment tail. For thinner kite/micro line, a stopper may pull through: use an appropriately sized backing washer or tie a fixed anchor loop around the post, then verify the anchor under load.
- Thread through the transverse holes, then turn outside the post; do not drag the line over the magnet pocket or across an exposed click hook. At the X crossing let one cord rest over the other, without a knot. Both cords remain behind the paper.
- Lay the border flat. Measure its two overall diagonals; make them equal before tensioning. Hand-feed slack through all four eyes, beginning at the stopper, then pull the tail. Friction at the bends means simply pulling hard on the last end does not tension every span evenly.
- Hold the tail with one hand. With the other, make two figure-eight turns around the two posts of the lower-left branch rail. Finish with a locking half-hitch around the last post: take the tail around the post, pass it under its own turn and snug it. Leave at least 100 mm tail, tucked under a wrap. The posts are the tensioning fixture; no separate screw, ratchet or loose part is required.
- Use only enough tension to remove slack. Stop if the rail bows or click gaps close unevenly. To adjust, hold the tail, lift off the half-hitch, unwrap, feed slack around the bay, and rewrap. Keep cords installed and lightly tensioned during transport.

There are five independent adjustments per border, twenty per gate. Independence prevents one long, friction-loaded lace from being difficult to balance. It also confines a slipped cord to one bay. Four purchased mini guy-line tensioners can simplify external setup; their cord range must include 2.4 mm. They are separate from the integral face cleats.

## Bench acceptance before scaling

Use the actual printer, PETG, magnets, paper and cord. Smooth burrs rather than enlarging latch shoulders. Seat the rigid guide runners and verify both catches; pinch both spring tips to release straight. Cycle representative joints 50 times, checking for whitening, cracks, missing hooks and growing play. A warning-free slice does not prove snap life or strength.

For a cleat check, hang about 0.5 kg from a cord test tail, secure the wraps, mark the cord at the eye, and observe for 30 minutes and again after an overnight hold. Test ten releases/re-tensions. Reject visible sliding, groove damage, fraying or a bent post. On the full bay, apply modest diagonal hand loads in both directions; joints must remain seated and the rectangle must return square. This is a fit/slip screen, not a structural load certification. Recheck after warm outdoor exposure because PETG and cord can relax.

Check the dock on real pipe for axial sliding and rotation before it supports a border. The collar has 0.4 mm diametral clearance and an ear gap for clamping. Tighten evenly with washers, without crushing the plastic. Verify the brace V clamps grip both ODs. If either clamp slips before adequate grip is obtained, revise its seat/liner and repeat the test rather than overtightening.

Test magnet polarity before bonding. Rear magnet -> 0.4 mm rail skin -> paper -> 0.4 mm pad skin -> front magnet. Magnetic attraction depends on that complete gap and coating; 6 x 2 mm dimensions alone do not specify holding force. Test peeling, sideways slip, a fan and repeated pad removal. The paper is replaceable and can tear or soften when wet; it is not a structural brace.

## Assemble each full border on the bench

Make two 2090.4 mm long edges. Each uses fourteen 136.314 mm rail bodies and thirteen keys, whose exposed central spacers are 14 mm. At zero-based positions 0, 2, 5, 8, 11, 13 use EDGE_BRANCH; all other positions use EDGE_PLAIN. Turn the second long edge 180 degrees so all branches and D lugs face inward. The symmetric index pattern keeps the six branch axes aligned.

Join three identical 133.867 mm RUNG pieces for each of six crossmembers. Use four keys per crossmember: two internal and one at each end. Crossmember axes are 68.157, 368.786, 819.729, 1270.671, 1721.614 and 2022.243 mm from the panel end. Seat the second long edge evenly across all six members. Check overall dimensions 2090.4 x 609.6 mm and equal diagonals. Thread/tension the five X bays as above.

At the middle segment of crossmembers 2, 3, 4 and 5, attach a DOCK_TONGUE with two M3 x 25 flat-head screws through the paper face, flush in the countersinks. Nuts and washers sit behind the tongue flange. The outer two crossmembers have no dock. Keep all open latches accessible from the back.

Load 28 rear magnets into the long-edge D lugs and six into the middle-rung D lugs. Leave the twelve outer-rung pockets empty. Bond 34 matching magnets into 34 front pads. Cut one 2090.4 mm strip from the full 609.6 mm roll width, lay it against the smooth flat face and apply the pads without stretching the paper. Repeat for four identical borders. Magnets and cord stay with each transport border.

## PVC backbone and cut list

One square has 2090.4 mm centerline spacing. It lies about 98.9 mm behind the paper; four 3/4-inch corner braces lie another 60.475 mm behind it. Its lower centerline is 354.8 mm above ground and upper centerline 2445.2 mm. Paper bottom is 50 mm, top 2750 mm. Two guy masts extend the PVC to 3100 mm, so front guys clear the paper's upper edge. Masts are extensions of the single backing frame, not a second square.

Use 1-inch Schedule 40 PVC (33.4 mm OD), 3/4-inch braces (26.67 mm OD), four main-corner tees and two foot tees. Printed collars require these outside diameters, not 1-inch-OD tubing. Purchased fitting envelopes in Blender are illustrative; actual fitting engagement must be measured before cutting.

The example below assumes g=17.4625 mm from each fitting center to the fully seated pipe end. For a rail between two fittings, cut = center spacing - 2g. For a mast or foot with one fitting, cut = end-to-center length - g. Mark seating depths, test a corner, and update cuts if the purchased fittings differ. Leave allowance for saw kerf; all listed stock nests have spare length.

- 4 x 2055.48 mm 1-inch Schedule 40 PVC, 33.4 mm OD: Square rails.
- 2 x 294.88 mm 1-inch Schedule 40 PVC: Lower legs.
- 2 x 637.34 mm 1-inch Schedule 40 PVC: Upper guy masts.
- 4 x 582.54 mm 1-inch Schedule 40 PVC: Grass half-feet.
- 4 x 1182.54 mm 1-inch Schedule 40 PVC: Hard-surface half-feet (swap for grass).
- 4 x 645.69 mm 3/4-inch Schedule 40 PVC, 26.67 mm OD: Corner braces.

For BOTH foot sets, buy six 10-ft sticks of 1-inch PVC: sticks 1-2 each yield one square rail + one mast + one leg; sticks 3-4 each yield one square rail + one grass half-foot; sticks 5-6 each yield two hard half-feet + one grass half-foot. One 10-ft stick of 3/4-inch yields all four braces. Grass-only can use five 1-inch sticks with the hard-foot cuts omitted.

Dry-assemble square and foot tees. Fully seat and mark each joint, square the frame, then drill 4.5 mm retention holes through each structural fitting/pipe interface for an M4 x 60 bolt and wingnut (18 occupied ports total). Orient bolts so they clear other sockets and feet. No solvent welding is required for this prototype. Add one M4 cross-bolt at about 3085 mm height on each mast; guy loops tie around the pipe below this stop. Six caps finish the four feet and two masts. Model hardware shows positional envelopes rather than thread detail.

## Corner braces: positively clamped at both ends

Each brace connects points 400 mm along the two adjoining square sides, with 40 mm pipe overhang past each crossing. Cut length is sqrt(400²+400²)+80 = 645.69 mm. Four braces need eight joints.

Each joint uses one 6 mm CROSS_PLATE and four identical V_BLOCKs. Put two V blocks around the 33.4 mm main pipe on one face of the plate; their flat outer faces and plate holes align. Use the plate's straight hole pair and two M4 x 80 bolts, washers and nuts. On the other face, rotate another V-block pair +/-45 degrees, align its holes with the appropriate diagonal pair, and clamp the 26.67 mm brace with two M4 x 70 bolts. The other diagonal holes stay empty. Tighten alternately until gripping; do not crush the pipe. Check both ends for rotation and axial slip. The main/brace axes are about 60.475 mm apart in depth. This replaces the earlier cross-lashing entirely.

## Align the sixteen face docks

Each dock uses two PVC_HALF_33 halves, one DOCK_SOCKET and one DOCK_TONGUE already fitted to the middle rung. Bolt the receiver's two base holes to the mounting pad on the inward collar half (two M3 x 25 cap/pan bolts, washers, nuts). Assemble the halves loosely around the appropriate square rail with two more M3 x 25 cap/pan bolts. The receiver mouth faces toward the gate front.

Use the finished border as the alignment jig: engage all four tongues in their receivers, place the paper rectangle at its intended pinwheel position, and slide/rotate the collars until all docks sit without strain. Then tighten the collar bolts evenly and label their positions. Do not independently measure and tighten sixteen collars and expect all four-panel interfaces to register perfectly.

Each face border snaps to the common PVC square at four points; neighboring face borders meet at butt seams. They do not need separate frame-to-frame corner snaps: the shared backbone locates them. The four 2090.4 x 609.6 rectangles rotate 90 degrees successively in a pinwheel, producing the 2700 mm outside / 1480.8 mm opening with no corner paper patches.

## Field setup and teardown

Assemble marked PVC square rails and tees with retention bolts. Fit feet and masts, clamp the four corner braces, and check the square. On soil use the 1200 mm fore-aft foot set and four appropriate ground anchors. On hard ground use the 2400 mm foot set, rubber pads, and four weighed 15 kg ballast bags secured to the feet with straps. This 60 kg arrangement is a test starting point, not a certified wind limit or universal ballast prescription.

Tie front/rear guy pairs below the mast stop bolts and run them to stakes or the far foot ends. Start guy attachment at about 3075 mm: for the front hard-surface anchor 1150 mm from the pipe plane, the straight guy crosses the paper plane above 2810 mm, clearing the 2750 mm face top. Do not instead tie front guys to the 2445 mm upper square rail, which routes them through the paper. Keep guys outside the flight opening, tension evenly with optional mini line runners, and verify stakes/ballast do not move.

With two people, hold each rigid border against its four receivers, press the tongues home and visually check all hooks. Keep paper in the pinwheel layout. Adjust only slack X bays, check feet, all PVC fasteners, paper pads and the clear flight opening. Start testing in calm conditions, then controlled mild airflow; withdraw the paper face if it flaps, slips or destabilizes the frame. No wind rating is claimed for this prototype. As a sizing screen only, the 5.097 m² paper face at 5 m/s, air density 1.225 kg/m³ and assumed drag coefficient 1.3 gives about 101 N drag using the NASA drag equation. Doubling that force for a simple allowance gives about 284 N·m at 1.4 m height. Ideal centered 60 kg ballast with a 1.2 m lever arm gives 706 N·m, but this ignores joint flexibility and depends on ballast attachment; sliding would require friction coefficient above about 0.35. These assumptions are not a measured wind limit. Verify actual ground grip and assembly behavior.

For teardown, support a border, pinch both spring tips of each dock from behind and pull it forward evenly. Never pull against a still-latched dock. Leave each border's rails, X cords, tongue flanges and magnetic paper clamps assembled. Protect paper/pads for transport. Release guys and remove marked PVC bolts/brace clamps as needed. Stored borders are roughly 2.09 m long, 0.61 m wide and about 0.10 m deep with tongues; they are not intended to fold.

## Hardware, quantity and verification files

[Hardware_BOM.csv](Hardware_BOM.csv) lists all purchased pieces, [PVC_Cuts.csv](PVC_Cuts.csv) all cuts, [Print_Queue.csv](Print_Queue.csv) the recipes/repetitions, and [Every_Plate_Run.csv](Every_Plate_Run.csv) all 112 runs in order. The queue below includes full gate quantities, no allowance for spares or rejected prototypes.

| Plate recipe | Runs | Pieces/run | PETG/run | Time/run |
|---|---:|---:|---:|---:|
| Q_EDGE_PLAIN_FULL | 21 | 3 | 73.2 g | 170 min |
| Q_EDGE_PLAIN_TAIL | 1 | 1 | 24.5 g | 62 min |
| Q_EDGE_BRANCH_FULL | 24 | 2 | 73.4 g | 180 min |
| Q_RUNG_FULL | 24 | 3 | 73.4 g | 175 min |
| Q_CLICK_KEY_FULL | 25 | 8 | 26.9 g | 86 min |
| Q_PAPER_PAD_FULL | 3 | 36 | 53.6 g | 140 min |
| Q_PAPER_PAD_TAIL | 1 | 28 | 41.7 g | 110 min |
| Q_PVC_HALF_33_FULL | 3 | 10 | 72.3 g | 200 min |
| Q_PVC_HALF_33_TAIL | 1 | 2 | 14.5 g | 46 min |
| Q_DOCK_SOCKET_FULL | 1 | 12 | 106.7 g | 256 min |
| Q_DOCK_SOCKET_TAIL | 1 | 4 | 35.6 g | 90 min |
| Q_DOCK_TONGUE_FULL | 1 | 12 | 101.8 g | 278 min |
| Q_DOCK_TONGUE_TAIL | 1 | 4 | 34.0 g | 100 min |
| Q_V_BLOCK_FULL | 2 | 12 | 194.4 g | 441 min |
| Q_V_BLOCK_TAIL | 1 | 8 | 129.6 g | 297 min |
| Q_CROSS_PLATE_FULL | 2 | 4 | 70.8 g | 155 min |

Validation: ten closed manifold masters with positive volume; bed dimensions/margins and plate non-overlap; exact BOM vs plate quantity; full-scene counts vs BOM; four sampled key/socket mating checks; every supplied plate sliced with no warnings and supports disabled. Source JSON reports are [geometry_checks.json](geometry_checks.json), [print_checks.json](print_checks.json) and [scene_counts.json](scene_counts.json). The interface sampling is not exhaustive collision proof. No physical pull, fatigue, magnetic grip, wind, creep or stability test has yet been performed. Purchased fitting envelopes and fastener heads are simplified; measure real components.

## Research used

- [Atwood 275 cord](https://atwoodrope.com/products/275-tactical-mystery-spools-1000ft): 2.4 mm, polyester/nylon, manufacturer tensile specification; this does not rate printed parts.
- [Atwood micro cord](https://atwoodrope.com/products/1-18mm-white): 1.18 mm, 125-ft spool, $6.99 observed September 17, 2026. Two spools cover the 66 m face allowance, about $13.98 before shipping; not enough for the whole face-plus-guys cut list.
- [Atwood 550 paracord](https://atwoodrope.com/products/550-x-100ft-paracord-infiltrate): 4 mm. This larger size needs a different printed cord guide.
- [Into the Wind kite line](https://intothewind.com/catalogsearch/result/?q=Braided+dacron): 500-ft 50-lb braided Dacron listed $24; about $10.39 allocated to 66 m, versus the cost of buying a whole spool. Verify actual diameter and cleat hold.
- [Clamcleat mini Line-Lok](https://www.clamcleat.com/mini-line-lok.html): commercial small-line adjustment option. Use a model whose stated range includes 2.4 mm; four optional units are for the external guys.
- [NASA drag equation](https://www1.grc.nasa.gov/beginners-guide-to-aeronautics/drag-equation/): equation used only for the explicitly assumed stability screen.
- [Charlotte Pipe product knowledge](https://www.charlottepipe.com/uploads/documents/technical/BR-PK.pdf): nominal sizing and outside diameters; actual purchased socket engagement governs cut length.
- [K&J magnetic closures](https://www.kjmagnetics.com/blog/magnetic-closures): magnetic retention depends on geometry/gap. Prototype the complete frame/paper/pad stack.
- Earlier click-joint research and user picture-frame attribution remain in [the committed study](../paper_roll_study/RESEARCH.md). New reinforced CAD is original geometry; the downloaded example is reference only.

Rebuild from repository root: `blender --background --python scripts/build_full_paper_gate.py -- --no-render`, `python3 scripts/slice_full_paper_gate.py`, `blender --background --python scripts/render_full_paper_gate.py`, `python3 scripts/validate_full_paper_gate.py`, then run `scripts/package_full_paper_gate.py` with Python containing ReportLab. No printer job has been submitted.

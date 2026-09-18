# Full-size whole-sheet gate — A1 Mini iteration

[Download the two-part assembly and test PDF](Assembly_and_Test_Instructions.pdf).

Every printed component now has an STL at full size and in its intended print orientation. **19 unique files, 740 printed pieces per gate.** All fit inside **180 × 180 × 180 mm**, with no diagonal packing required. Longest piece: **144.2 mm**. The assembly remains a physical-test prototype; volume checks and successful slices do not demonstrate snap fatigue, assembled stiffness or wind performance.

Open [the Blender model](A1_Full_Size_Gate.blend), [visual guide](A1_Full_Size_Visual_Guide.pdf), or [visual index](index.html). The complete per-file quantities and print dimensions are in [BOM.csv](BOM.csv); geometry and slicing evidence is in [print_checks.json](print_checks.json).

## What changed

- The previous oversized rear ribs are now 126.867 mm horizontal pieces and 144.2 mm vertical pieces, joined with alternating 16 mm lap overlaps and paired tie holes.
- A stepped cross node separates the perpendicular ribs. Integral shoes support the paper from behind; two lightly tensioned cord runs retain it from the front.
- **Only two channel types:** `CHANNEL_LONG`, 140.84 mm (120 per gate), and `CHANNEL_SHORT`, 138 mm (96 per gate). Common symmetric mounting windows and cord notches replace the earlier nine variants. Extra accessory windows slightly reduce material; the end windows that locate splint bosses remain unchanged. Every previous attachment position is checked against the common window layout.
- Edge channels are 140.84 or 138 mm long. Registered splints locate their ends; two ties retain each splice. All node, rib, dock and corner attachments have modeled holes.
- One common two-fork snap bridge releases the **eight gate-corner connections and sixteen PVC docks**. Workshop splices use ties and stay assembled. This is not an entirely snap-assembled kit.
- Both ends of every diagonal PVC brace have a printed flat 45° link with two pipe saddles. No cross-lashed pipe-to-pipe brace connections.
- No hinges, no second PVC square, no cutting or punching of the twelve posterboard sheets.

## Dimensions and materials

| Dimension | Value |
|---|---:|
| Whole paper insert | 711.2 × 558.8 mm / 28 × 22 inches |
| Inserts per rigid border | 3 |
| Rigid border | 2151.6 × 564.8 mm |
| Gate outside | 2716.4 mm square |
| Nominal face opening | 1586.8 mm square |
| PVC frame centerlines | 2100 mm square |
| Main pipe / brace pipe outside diameter | 33.40 / 26.67 mm |
| Main pipe axis behind front face | 55 mm |
| Paper slot | 0.8 mm, designed around approximately 0.4 mm posterboard |

The gate grew slightly to accommodate stronger channel spines and sheet clearance. Measure your actual sheets and thickness before printing more than the fit kit. The slot has about 3 mm of edge capture at the nominal sheet position. Do not scale all parts to correct a stock-thickness mismatch; change the slot parameter and recheck the joins.

## Print and material findings

Local **BambuStudio 2.8.2.61** sliced all 19 unique parts and the 12-piece interface fit plate without warnings, using the resolved **A1 Mini / 0.4 mm / 0.20 mm Standard / Generic PETG / Textured PEI Plate** presets. Three walls, 15% infill, supports off, brim off. Preset files are included. The export units are millimeters; print at **100%**.

All source meshes have zero nonmanifold edges. All exported meshes sit on Z=0 and have positive volume. A triangle-orientation check found no downward-facing surfaces steeper than 45° above the bed, excluding bed-contact faces. This checks geometric support intent; it does not prove adhesion or every small overhang's print quality. Verify the preview and actual first print. If adhesion needs a brim, parts have substantial bed margin; re-slice after adding one.

**Sliced part material: 2967.6 g PETG per gate.** With 10% reserve: **3264.3 g**, so buy **four 1 kg spools**. Three spools leave only about 32 g before startup waste, prototypes or failed prints; use four with reserve. This supersedes the earlier schematic 1.84 kg estimate: that allowance omitted the completed joints and full rib system.

At an assumed $20/kg, consumed printed material is **$59.35**, or **$65.29 including reserve**. Twelve sheets at your $0.99 price add **$11.88**. Thus printed plastic plus paper is **$71.23**, or **$77.17 with filament reserve**, before ties, cord, PVC, fittings, anchoring, electricity and labor. Buying four complete $20 spools plus paper is **$91.88 cash** with filament left over. These are arithmetic assumptions, not current supplier quotes.

Summing model-only slicer times gives about **146.0 printer-hours**; running every piece as its own job gives **228.6 hours** including repeated startup. Batch printing reduces startup overhead, but actual packed-plate travel and cooling alter these estimates. Production plates have not been optimized. The individual sliced projects are verification samples, not an instruction to run 740 separate jobs.

The all-printed framing solution preserves whole-sheet yield and four-border field assembly, but **does not minimize workshop labor**. It uses **856 ties**. If low crew effort is the priority, the earlier Coroplast/PVC design is the more promising route. This iteration establishes a complete printable baseline for testing, rather than evidence that the posterboard approach is the cheapest finished gate.

## Full-size printed parts

| File / part | Quantity | Print X × Y × Z, mm |
|---|---:|---|
| [SPLINT](printable/SPLINT.stl) | 168 | 40 × 8 × 4.4 |
| [CORNER_NODE](printable/CORNER_NODE.stl) | 48 | 34 × 34 × 7 |
| [RIB_ANCHOR](printable/RIB_ANCHOR.stl) | 48 | 40 × 26 × 7 |
| [RIB_CROSS](printable/RIB_CROSS.stl) | 12 | 48 × 48 × 6 |
| [BORDER_BRIDGE](printable/BORDER_BRIDGE.stl) | 16 | 60 × 12 × 3 |
| [FIELD_RECEIVER](printable/FIELD_RECEIVER.stl) | 16 | 40 × 24 × 6.4 |
| [SNAP_BRIDGE](printable/SNAP_BRIDGE.stl) | 24 | 36 × 16.8 × 3 |
| [RIB_H_LOW](printable/RIB_H_LOW.stl) | 32 | 126.867 × 17.825 × 12 |
| [RIB_H_LOW_DOCK](printable/RIB_H_LOW_DOCK.stl) | 16 | 126.867 × 17.825 × 16 |
| [RIB_H_HIGH](printable/RIB_H_HIGH.stl) | 24 | 126.867 × 20.825 × 12 |
| [RIB_V_LOW](printable/RIB_V_LOW.stl) | 24 | 144.2 × 17.825 × 12 |
| [RIB_V_HIGH](printable/RIB_V_HIGH.stl) | 24 | 144.2 × 20.825 × 12 |
| [PIPE_33](printable/PIPE_33.stl) | 24 | 61 × 43.899 × 16 |
| [PIPE_27](printable/PIPE_27.stl) | 8 | 44 × 35.8 × 16 |
| [DOCK_CAP](printable/DOCK_CAP.stl) | 16 | 24 × 18 × 2.4 |
| [DOCK_PEDESTAL](printable/DOCK_PEDESTAL.stl) | 16 | 7 × 12.35 × 22 |
| [BRACE_LINK_45](printable/BRACE_LINK_45.stl) | 8 | 103.51 × 127.51 × 3 |
| [CHANNEL_LONG](printable/CHANNEL_LONG.stl) | 120 | 140.84 × 14 × 6 |
| [CHANNEL_SHORT](printable/CHANNEL_SHORT.stl) | 96 | 138 × 14 × 6 |

Quantities include every printed face, dock and brace connector. The base uses purchased PVC/fittings and has no additional printed pieces. Presentation copies are excluded.

## Purchased fasteners and stock

| Item | Working quantity | Use |
|---|---:|---|
| Whole 22 × 28 inch posterboard | 12 | Three per border |
| Standard ties, 2.5 mm wide | 744 | Workshop splices, nodes, laps, bridges, receivers and docks; approximately 100 mm lengths |
| Releasable ties, at most 2.5 mm wide | 48 | Four per removable top cap; use removable cord loops if suitable narrow releasable ties are unavailable |
| Pipe keeper ties, approximately 3.6 × 250 mm | 32 | One around every pipe saddle; releasable type permits backing-frame disassembly |
| Brace-link retaining ties, approximately 3.6 × 150 mm | 32 | Four per link |
| Smooth 0.8 mm cord/monofilament | 20 m purchased | 24 front spans, plus routing and knots |
| Main PVC square | Four 1-inch nominal sides | 2100 mm centerline square; see cutting list |
| Diagonal braces | Four 3/4-inch nominal tubes | About 425.7 mm each; changed from earlier design |
| Main frame fittings | Two upper elbows, two lower tees | Lower tees continue to legs |
| Base | Two legs, two foot tees, four caps | Same anchored/ballasted base arrangement as earlier design |
| Grass feet / alternative hard-floor feet | Four half-feet of each length for dual-surface kit | Install one set at a time |

Buy spare ties beyond these exact working quantities. Narrow hole clearances are designed for the strap, not the head; heads remain outside the part. Confirm your chosen tie's width and thickness in the fit kit.

Tie accounting: 336 at channel splints; 96 at corner nodes; 96 at rib anchors; 168 across rib endpoints/laps/cross nodes; 32 at permanent cell bridges; 32 at field receivers; 32 at dock caps; 32 heavy brace-link ties; 32 pipe keepers. Total **856**, including the **48 reusable top-cap ties**.

## Print the minimum nine-piece concept test first

The [nine-piece concept test](MINIMAL_CONCEPT_TEST.md) is the recommended first print: **32.4 g PETG / about 95 minutes**. It contains a complete working PVC dock, two channel types, a splint and a corner node. Print one of each listed part and reuse them between tests. The earlier twelve-piece plate below samples more individual shapes but omits the docking rib; use the nine-piece plate to test a complete dock.

## Earlier twelve-piece interface sampler

Open [Fit_Kit_1to1_LAYOUT_A1Mini_PETG.3mf](sliced/Fit_Kit_1to1_LAYOUT/Fit_Kit_1to1_LAYOUT_A1Mini_PETG.3mf). It contains twelve actual full-size components on one A1 Mini plate: one universal long channel and one universal short channel, one splint, one snap bridge, two socket caps, one 1-inch pipe saddle, one rib cross, one field receiver, one corner node, one horizontal rib and one dock pedestal. **38.5 g PETG, about 113 minutes.** Check the printer, nozzle, filament and plate setting before printing. No print has been sent to a printer.

1. Slide your actual paper stock into both channels; it should move without creasing or forcing the lips apart.
2. Butt the long and short sample channels with a 0.2 mm gap. Fit the four splint bosses into the rear windows. Each side of the joint gets one tie threaded through its two hollow bosses. Check registration and resist hand bending/sliding; the ties retain the splint, while the bosses bear against the windows.
3. Hold the two socket caps with centers 24 mm apart. Insert the snap bridge until its rigid stops seat. The 2.4 mm plate is caught behind the hooks, with 0.4 mm nominal axial clearance. Pinch one fork's two prongs inward and lift that end, then the other. Check release access in a complete dock as well as loose caps. Blunt tweezers can assist testing; easy repeated hand release is still to be demonstrated.
4. The 1.6 mm fork split has a rounded root. Each hook needs roughly 0.7 mm inward movement including clearance. Do not force a binding print: deburr first, measure and adjust the socket/clearance locally. Perform repeated assembly/release and a pull test; inspect for cracks and permanent set.
5. Trial the pipe saddle on measured 33.4 mm OD PVC and install its keeper tie. Check for axial slip and rotation. The open C profile alone is not the keeper.
6. Inspect the rib's integral contact shoe and smooth its paper-facing edges. Then build **one complete whole-sheet bay** before printing the remaining eleven. Evaluate racking, paper flutter and the top-cap removal process.

The earlier [1:15 tabletop model](../rigid_whole_sheet/index.html) remains useful for the four-border assembly idea. It represents the prior concept and enlarged model joints; it is not a scaled copy or a fit test of these new full-size interfaces.

## Workshop assembly

Lay the first border face-down with bay 1 at the left and bay 3 at the right. A bay measures 717.2 × 564.8 mm. Every bay uses the same two channel types:

| Sheet edge | Channel | Pieces per edge | Total per gate |
|---|---|---:|---:|
| Long edges | `CHANNEL_LONG` / 140.84 mm | 5 | 120 |
| Short edges | `CHANNEL_SHORT` / 138 mm | 4 | 96 |

The first channel starts 6.1 mm from the mathematical corner; adjacent bodies have 0.2 mm gaps. [CHANNEL_ASSEMBLY_MAP.json](CHANNEL_ASSEMBLY_MAP.json) gives every start position. Read edges counterclockwise around a face-down bay: bottom left-to-right, right bottom-to-top, top right-to-left, left top-to-bottom. Keep paper lips facing the paper and the deep spine facing the rear.

Every long channel has the same symmetric windows and center cord notch. Every short channel has the same symmetric windows and end cord notches. There are no position-specific channel files to sort. Accessory windows are wider where earlier hole patterns overlapped; at least 2 mm of web remains between windows, and the registered splice windows stay 6 mm wide. [CHANNEL_FEATURES.json](CHANNEL_FEATURES.json) records their geometry. Physical stiffness remains part of the bay test.

1. Build the four edge chains with registered splints, then the four inside corner nodes. Corner-node fences locate against the inward rail face. Tie each corner to both adjoining rails using the node hole and corresponding rear-spine window; do not cover the paper slot with a strap. Leave the top edge removable.
2. Install the four midpoint rib anchors. Each has two rail ties and one paired-hole rib attachment. Locate the cross node at the sheet center with its taller seats along the short sheet dimension.
3. Each horizontal half-rib, from the outer edge to the center, uses **LOW–HIGH–LOW**, overlapping 16 mm at each joint. Each vertical half uses **LOW–HIGH**. One tie passes through both aligned hole pairs at each overlap. The horizontal ends sit on the lower cross seats; vertical ends sit on the higher seats. The two opposing halves stop short of each other.
4. Replace selected low horizontal pieces with `RIB_H_LOW_DOCK`: bay 1 right-half innermost piece, bay 2 outermost piece on each half, bay 3 left-half innermost piece. This yields four dock stations per border. Place the pedestal on the rib, cap over the pedestal, and retain with two ties through the cap and rib's matching holes. The open pedestal clears the snap fork tips.
5. Slide in the whole paper sheet. Refit the five-piece top cap. Its two corner attachments and two rib-anchor attachments use the four reusable ties. To replace paper later, loosen those four ties and the associated cord, lift the cap chain and slide the sheet out. The rib anchor can remain on the rib; it clears the paper plane.
6. Add two front cord spans per sheet, one each direction. Route over the edge-midpoint V-grooves, around the exterior edge to the rear windows, and tie off behind the frame. The short-edge groove is split across the central rail joint. Use only enough tension to retain the sheet against the rear shoes; excessive tension bows the frame or marks the paper. Knots and wraparound ends are not fully modeled in the presentation.
7. Join adjacent bays with two `BORDER_BRIDGE` pieces per seam, one near each long edge, through the spare paired holes in the corner nodes. Two ties per bridge. These joints stay assembled for transport.
8. Install four field receivers per border: two on bay 1's bottom edge and two on bay 3's right edge, 64 mm from the ends of the 564.8 mm seam. The required positions lie within the universal channel windows; unused accessory windows need no fasteners. Seat their fences inward and retain with two rail ties each.

## PVC and field assembly

Build one 2100 mm centerline square. The [PVC cutting list](PVC_CUT_LIST.csv) uses the earlier example fitting take-up, but actual fittings determine final tube cuts. Upper corners have elbows; lower corners have tees continuing down to the feet. Reuse the earlier positive socket-retention method. These commercially purchased fittings are described in the BOM; the new views simplify the stock pipe runs and omit fitting bodies and bases.

Each diagonal has a theoretical 400 × 400 mm span. Cut its tube approximately **425.7 mm**: 565.7 mm diagonal minus 70 mm at each end. At each end, the `BRACE_LINK_45` carries one `PIPE_33` on the main frame and one `PIPE_27` on the diagonal. The brace-saddle axis is 90 mm from the theoretical main-pipe intersection, so its clamp sits 20 mm from the trimmed tube end. Flip the link face as needed at mirrored corners; it has no handed fasteners. Use four heavy ties per link to secure the saddle feet and one keeper around each saddle/pipe. For full backing-frame teardown, use releasable keepers so braces can detach without cutting ties.

Set up and anchor/ballast the PVC backing before relying on the paper face for stability. Seat each rigid border's four saddles on the corresponding pipe. Align dock sockets and click in four snap bridges. Connect each neighboring border seam with two additional snap bridges. Total field face connections: **16 docks + 8 corners**. Release these to transport four rigid 2.15 m borders. Tied workshop splices remain intact.

Retain the previous [grass and hard-surface base arrangements](../BUILD_GUIDE.md): 1.2 m fore–aft feet with opposing staked guys on soil; 2.4 m feet, anti-slip pads, strapped ballast and guys on hard ground. The frame bottom center is now 308.2 mm above face datum; legs grow **8.2 mm** compared with the previous gate when keeping feet at the same height. The earlier 60 kg ballast starting configuration is not a wind rating for this new paper face. Physical anchor, slip, uplift and joint tests remain necessary. Paper is a dry-use consumable; the design does not make ordinary posterboard weatherproof.

## Rebuild

```sh
blender -b -t 8 --python scripts/build_a1_full_size.py
python3 scripts/validate_a1_full_size.py  # also creates the 1:1 fit layout
python3 scripts/slice_a1_full_size.py
python3 scripts/validate_a1_full_size.py
python3 scripts/package_a1_full_size.py
```

Blender source coordinates are meters; CAD calculations and exports use millimeters. Slicing uses locally installed BambuStudio profiles with inheritance/includes resolved. Packaging requires Pillow. The full geometry, ten presentation scenes, BOM, channel map, slicer settings and validation results are included.

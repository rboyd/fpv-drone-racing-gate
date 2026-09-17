# FPV gate — four pentagons, shared corners, single backing frame

**Current design:** four identical five-sided Coroplast border panels, four triangular corner infills, and one 1-inch PVC backing frame with four ¾-inch corner braces. Two 8 × 4 ft sheets supply the four main panels. A shared third sheet supplies corners for **16 gates**. Both grass and hard-surface bases are included. Printed connectors now locate **both ends of every corner brace**; crossed lashings have been replaced.

Open `FPV_Gate_2700.blend`. Its nine scenes show the assembled gate, backing structure, exploded assembly, sheet nesting, face saddle, dimensions, ballasted hard-surface base, brace connector detail, and separated pentagon/corner pieces. `START_HERE.html` is the visual index. The earlier two-frame version is archived in `previous_double_frame_design/`; the original rectangular-panel version remains in `previous_rectangular_design/`. Both are superseded.

This is a digitally checked design prototype. Print fit, fastening strength, pipe/fitting dimensions, panel stiffness and installed wind performance still need a first-build test. No wind rating is asserted.

## Geometry

| Feature | Size |
|---|---:|
| Outer face | 2700 × 2700 mm |
| Clear front opening | 1500 × 1500 mm |
| Border | 600 mm |
| Main pentagon blank | 2400 × 600 mm |
| Corner infill | Right triangle, 300 mm perpendicular legs |
| Sheet thickness | 4 mm assumed |
| Single PVC backing frame centerlines | 2100 × 2100 mm |
| Body thickness, including face fasteners and brace ties | About 94 mm; excludes feet and guys |
| Main frame / corner braces | 1 inch / ¾ inch Schedule 40 |
| Face clearance above ground | 50 mm |
| Overall height above ground / opening bottom | 2750 / 650 mm |
| Grass foot pipe span | 1200 mm, plus caps |
| Hard-surface foot pipe span | 2400 mm, plus caps |

The screenshots specify 2700 outer, 1500 inner and 260 mm depth. Your latest instruction removes the second square frame and depth links: this revision deliberately has a **shallow single backing frame, about 94 mm thick including fasteners**, rather than a 260 mm body. The 2700 mm face and 1500 mm opening dimensions are retained. There are no solid tunnel walls or rear face.

Datum: face X = −1350…1350, Z = 0…2700, Y = 0…4 mm. Opening X = −750…750, Z = 600…2100. Y increases rearward. Ground is Z = −50. The feet pass below the face instead of through notches in it. Foot and anchor footprints extend beyond the shallow gate body.

## Identical pentagons and the 8-foot sheet limit

The actual nominal stock is **2438.4 × 1219.2 mm**. Mark two 2400 × 600 rectangles per sheet. In each rectangle, use these five vertices, measured from its lower-left corner, in millimetres:

**(0, 600), (2400, 600), (2400, 300), (2100, 0), (600, 0).**

Cut off the left 600 × 600 right triangle and the right 300 × 300 right triangle. Keep those offcuts. All four main panels are identical; rotate them by 90° around the opening, without mirroring. Each panel has a continuous 1500 mm inner edge. The four 300 mm corner triangles fill the small gaps at the outer corners.

Each pentagon has area 1.215 m²; each corner triangle has area 0.045 m². **4 × 1.215 + 4 × 0.045 = 5.04 m²**, exactly the 2700 mm square minus the 1500 mm square opening. The polygon verification checks pairwise overlap and area, not merely a bounding box.

This arrangement keeps all four middle spans continuous and concentrates joints near the frame corners. That is a useful construction advantage, although improved stiffness still depends on the backers and attachments; panel shape alone is not a load test. The former six-piece rectangular face has been replaced by eight face pieces.

### Shared corner sheet

Divide sheet 3 into a **2400 × 1200 mm** grid of thirty-two 300 × 300 squares. Cut each square diagonally: **64 identical triangles = 16 gates**. A 38.4 mm end strip and 19.2 mm side strip remain. Knife cuts assume negligible kerf. Saw-cut production needs a revised spacing/yield calculation.

For N gates, buy **2N + ceil(N/16) sheets** for face panels and shared corners, before spares. Examples: 1 gate = 3 purchased sheets with most of sheet 3 left; 4 gates = 9 sheets; 16 gates = 33 sheets. Allocated sheet use at a full batch is **2.0625 sheets per gate**.

**Optional waste reduction:** the four large triangular offcuts from the main panels can each supply a 300 mm corner triangle as well as a 600 × 100 backer. Thus a careful one-off build can recover all its corners without buying a third sheet. The baseline retains your shared-corner-sheet approach because repeated 300 mm grid cuts are faster to batch and give consistent replacement stock. The offcut SVG shows the optional recovery.

## Backing the corner joints

Per gate, cut from the main-panel offcuts:

| Part | Qty | Size | Role |
|---|---:|---|---|
| B1 | 4 | 600 × 100 mm | Diagonal seam backer, including the three-piece junction |
| B2 | 4 | 140 × 100 mm | Short seam between pentagon and corner triangle |
| A-pad | 24 | 70 × 50 mm | Reinforcement behind the face saddles |
| Stitch pads | As needed | about 25 × 25 mm | Local front spreaders under seam ties |

A 600 × 100 rectangular strip fits diagonally inside each 600-leg triangular offcut. The exact offcut layout is supplied as SVG. A 140 × 100 tab fits in each smaller 300-leg offcut; use remaining scrap for pads. These are all Coroplast, not large printed plates.

At the top-right corner, the long diagonal joint runs from (750, 2100) toward (1350, 2700). Center the 600 × 100 backer at **(1050, 2400)**, with its long axis at 45°. Center the 140 × 100 short-joint tab at **(1050, 2620)**. Rotate this arrangement through the other three corners. The two backers do not overlap. Their rear surfaces share Y = 8 mm.

Use **three tie stitches** along each diagonal backer, at −230, 0 and +230 mm along its centerline, and **two** along each short-joint tab, 25 mm above/below its center. The tie legs straddle the seam. Add small front scrap spreaders, especially at the three-panel junction. Butt the visible face edges together; do not lap the front panels. Close the seam with matching tape after fastening. The lightly different blue tones in Blender identify pieces; use the same sheet color in production.

Do not rely on tape as the structural connection. Polypropylene can be difficult to bond; the backers and ties connect the panels. [Coroplast bonding guidance](https://www.coroplast.com/resources/)

## PVC structure

Use US **solid-wall Schedule 40** pipe. Nominal diameter is not outside diameter: 1 inch is **33.40 mm OD**, ¾ inch is **26.67 mm OD**. Those are the connector groove dimensions. The 1-inch section has about 2.36 times the bending second moment of the ¾-inch section; use it for the loaded front frame and feet. [Charlotte Pipe dimensions](https://www.charlottepipe.com/uploads/documents/technical/BR-PK.pdf)

The single 2100 mm backing frame uses 1-inch pipe. Its top corners use elbows and its lower corners use tees continuing down to the feet. Each of its four sides is now one continuous pipe: the midpoint reducing tees, connecting pipes, and rear square have been removed. Four short ¾-inch diagonal braces stiffen the corners, each joined by two of the existing printed 45° connectors.

The main frame pipe axis is Y ≈ **31.9005 mm**, set by the face/pad/saddle stack. Brace axes sit at Y ≈ **72.336 mm**; the furthest rear tie surface is near Y = 90 mm. Front washers/ties project a few millimetres ahead of the face, making overall body thickness approximately **94 mm**. The feet and guy lines are excluded from that dimension. The current geometry is measured in `validation.json`.

### Purchased fittings

- 1 inch only: **2 elbows, 4 tees, 4 end caps** — ten fittings total.

The Blender fittings are dimensional envelopes, not printable fittings. Pressure sockets may be tapered and may not dry-seat to their catalog stops. Measure repeatable actual engagement and mark it before cutting. Do not hammer a dry pipe to the stop.

### Cutting formula and example lengths

**Pipe cut = required fitting-center span − g at each end**, where **g = center-to-mouth − actual pipe engagement**. Do not subtract socket depth itself.

Catalog examples: the 1-inch 406-010 elbow and 401-010 tee each have G = **17.4625 mm**. These produce the full-seat examples below. Use actual measured engagement if it differs. [Charlotte fitting catalog, printed pages 31 and 36](https://www.charlottepipe.com/uploads/documents/technical/DC-PR.pdf)

| Part | Qty | Pipe | Example cut, mm |
|---|---:|---|---:|
| Horizontal rails | 2 | 1 inch | **2065.075** |
| Uprights | 2 | 1 inch | **2065.075** |
| Legs, 325 mm center span | 2 | 1 inch | **290.075** |
| Grass half-feet | 4 | 1 inch | **582.5375** |
| Corner braces | 4 | ¾ inch | **646** |
| Hard-surface half-feet, replace grass feet | 4 | 1 inch | **1182.5375** |

Each frame rail/upright is **2100 − 2 × 17.4625 = 2065.075 mm**. Shop precision of 0.1 mm is not required; the extra digits make the derivation reproducible. Cut against the actual fitting/centerline jig. If the previous half-pipes have already been cut, they cannot replace these continuous members without added couplers and recalculated engagement; the supplied revision assumes fresh continuous rails.

**Stock allocation:** buy **four 10-foot 1-inch sticks and one 10-foot ¾-inch stick** for the grass gate. Each 1-inch stick supplies one main rail/upright and one short half-foot. Sticks 1–2 also supply one leg each. Worst use including three 3 mm kerfs is **2946.7 of 3048 mm**, leaving about 101.3 mm. The ¾-inch stick supplies all four 646 mm braces; with four 3 mm kerfs this uses **2596 mm**. The hard-floor set adds **two** 10-foot 1-inch sticks, each yielding two 1182.5375 mm halves plus kerf, about **2371.1 mm** used.

Each working socket needs positive retention: a predrilled short stainless pan-head screw (e.g. #6 × ½ inch, chosen for actual fitting wall), pin, or correctly made permanent solvent joint. The fully removable prototype has **16 working socket interfaces**, plus the four low-load end caps. Do not rely on friction alone. Preassemble selected corner/foot modules in an alignment jig and retain transport joints with screws/pins to reduce field work. This is non-pressure structural use of plumbing components.

## Face-to-pipe saddles

Print **24 one-inch saddles and 24 front washers**. The open saddle is tie-retained; no spring snap carries the load. Print flat face down with no supports. Starting settings: PETG, 0.20–0.24 mm layers, four walls, five top/bottom layers, 25–30% infill. Four 0.4 mm extrusion lines are about 1.6–1.8 mm, not 3.2 mm. Use the filament maker's profile. PETG is a practical tough functional material; ASA is an outdoor alternative where the printer supports it. [Prusa PETG](https://help.prusa3d.com/article/petg_2059?product=mini), [ASA](https://help.prusa3d.com/article/asa_1809?product=mk3-5)

| STL | Qty | Geometry |
|---|---:|---|
| `saddle_1in_OD33p40_mm.stl` | 24 | 60 × 40 × 18 mm; groove OD 33.801 mm |
| `front_load_washer_mm.stl` | 24 | 60 × 40 × 2.5 mm |
| `optional_saddle_3_4in_OD26p67_mm.stl` | Optional | Not needed for the baseline face |

Stack: front washer → 4 mm face → 4 mm scrap pad → saddle → pipe. Use two 4.8 mm UV-rated ties per saddle, through matching **3.2 × 6 mm** slots. Slot centers are transverse ±23 mm and along-pipe ±10 mm. The 1:1 SVG is a drilling/slot template. Tie heads face rearward. Hand-tighten without crushing the flutes. Transfer slots through the sheet during fabrication; the large-sheet model does not subtract every field-made hole.

Positions relative to face datum:

- Horizontal pipe at Z = 300 and 2400: X = **−840, −500, −160, 160, 500, 840 mm**.
- Vertical pipe at X = ±1050: Z = **450, 850, 1150, 1550, 1850, 2250 mm**.

These positions clear the brace connectors and maintain distributed face support. Print one complete saddle/washer pair and test on actual pipe and sheet before producing the batch. Cut Coroplast front spreaders can substitute for printed washers to save printing time, but maintain the same broad load distribution.

## Printed joints at both brace ends

Each brace crosses the frame **400 mm from its corner**. Its two crossings are 400 × 400 mm apart, so the centerline span is 565.7 mm. A 646 mm pipe leaves about 40 mm beyond each connector center.

Print **four +45° and four −45° joints**. Each single printed body is **60 × 60 × 24 mm**, with a 33.801 mm groove on the main-pipe side and a 27.07 mm groove on the opposite brace side. The two groove axes cross at 45°. The geometric separation between pipe axes is **40.4355 mm**. This is a rigid locator; the pipe cannot simply rotate across a loose crossed lashing.

**How it attaches:**

1. Seat the large groove on the 1-inch frame pipe, at the marked crossing.
2. Thread the two main-pipe ties: through the main-side slots and internal return passages, around the main pipe, and back through the paired slots. Main slots are centered at X = ±25 and Y = ±21 mm in connector coordinates.
3. Lay the ¾-inch brace into the other groove. Choose the +45 or −45 part so the brace points toward the matching connector at its other end.
4. Thread two more ties through the brace-side slots and internal passages, around the brace. Their locations are ±23 mm across the brace and ±12 mm along it. Align both ends before tightening.
5. Confirm the brace cannot slide by hand, both pipes are seated, and there is roughly 40 mm of pipe beyond the crossing. Repeat at all eight ends. Reinspect after an impact.

The **four enclosed transverse tie-return passages** are 6 mm wide × 2.8 mm high, centered at local Z = 13 mm. They keep the return straps between the pipe seats instead of routing a strap through the other pipe. The two tie directions intersect inside the body; thread one pair first, then the other. The channel height accommodates two thin crossing straps; verify actual tie thickness (target no more than about 1.2 mm each) with a print sample. Do not force a thick strap through or reduce the body thickness indiscriminately. The seat-to-seat web is 10 mm before channels, leaving about 3.6 mm of skin on either side of a channel at the deepest seats.

The joint STLs are exported **standing on a 60 × 24 mm edge**, so their printed bounding box is 60 × 24 × 60 mm. Use a brim and check support needs at groove overhangs in the slicer. Keep support out of the enclosed 2.8 mm passages; use the printer's short-bridge capability and verify clear passages on the first print. Four walls and 35–40% infill are a reasonable starting point. These are prototype connectors, not tested structural clamps.

Allow roughly **0.8–1.2 kg PETG and 24–40 printer-hours** for all saddles, washers and brace joints including spare parts on a typical desktop printer. These are planning estimates, not measured slicer results. Slice the supplied STLs with your profile. A 0.6 mm nozzle and scrap front washers reduce time. The exact solid volumes and manifold checks are in `validation.json`.

## Grass / soil base

Use the short 1200 mm feet and four opposing guy lines, tied around upper **PVC corner fittings**. Stake at X = ±1600, Y = front-frame axis ±1200 mm. Each line stays outside the 1500 mm flight opening. About 4 m of 4 mm low-stretch cord per line allows knots/adjustment. Keep lines just taut so they do not bow the frame. Brightly mark anchors. Roughly 450 mm ground anchors are an initial purchase size, not proof of holding in a particular soil; verify installed resistance in the line direction.

## Hard-surface base

Swap in the four long half-feet, giving **2400 mm** fore–aft pipe span. Reuse the tees/caps and cords. Attach each guy to the corresponding foot end about 1150 mm from the center, and strap a **weighed 15 kg bag** to that pipe end, with anti-slip rubber underneath. Four bags total **60 kg**. Bags center about 1100 mm from the frame plane. The complete bag footprint is approximately **2.52 m wide × 2.6 m deep**.

The foot, bag and guy attachment must be physically connected; do not tie the guy to a small loose bag nearby. Straps encircle both the bag and the actual foot pipe. Keep guy tension modest. This is a self-contained braced base, rather than a collection of independently sliding guy weights.

### Wind and ballast check — planning, not a rating

The face area is still 5.04 m². With assumed air density 1.225 kg/m³ and Cd = 1.3, the drag equation gives about **100 N at 5 m/s (11 mph)** and **257 N at 8 m/s**. At a 1.40 m center of pressure above ground, corresponding moments are about **140 and 360 N·m**. The coefficient is a flat-plate approximation; the ring, gusts, flexibility and local loads have not been characterized. [NASA drag equation](https://www1.grc.nasa.gov/beginners-guide-to-aeronautics/drag-equation/), [flat-plate coefficient](https://www1.grc.nasa.gov/beginners-guide-to-aeronautics/shape-effects-on-drag/)

Using twice the 5 m/s load as a prototype planning check gives 200 N and 280 N·m. For grass, the two active guys each see roughly 130 N tension with this geometry, before pretension/unequal sharing; a proposed installation check is **300 N pull per anchor in its guy direction** without creep.

For the hard-floor setup, nominal tipping resistance from 60 kg about a foot end is **60 × 9.81 × 1.2 ≈ 706 N·m**, ignoring gate weight. Sliding requires an effective friction coefficient of at least **200/(60 × 9.81) ≈ 0.34**; verify this on the actual floor. Each active guy has approximately 134 N tension and 121 N vertical component at a foot end. A 15 kg bag weighs 147 N, so local uplift margin is limited under unequal sharing or excess pretension. Check all feet for lift and increase ballast if required. The pipe joints must also retain these internal forces.

**60 kg is a starting test configuration, not a universal safe ballast prescription.** Check slip, lift, joint movement, sheet tearing and flutter under reversible loading. Begin use in low wind and lay the gate down if it moves or the anchors loosen. No operating wind-speed limit has been established. Rated fixed venue anchors can avoid ballast transport where available and permitted.

## Assembly

1. Measure sheet thickness, actual pipe OD and fitting engagement. Print one face saddle/washer and one of each brace joint. Verify pipe seating and all tie passages.
2. Mark/cut two identical pentagons on each of two sheets. Batch-cut the shared corner sheet. Cut seam backers and pads from the main-panel offcuts.
3. On a flat jig, rotate the four pentagons around a 1500 mm square opening and add four corner triangles. Fit the diagonal backers and short tabs. Stitch mechanically, with spreaders, then tape the front seams. Check 2700 mm outer dimensions.
4. Cut PVC from the measured socket formula. Assemble the single backing frame, legs and selected feet. Check 2100 mm frame centerlines and square diagonals. Retain sockets positively.
5. Fit the eight printed brace joints and four diagonal braces. Thread/seat both pipe-retaining tie pairs at each end. Tighten only after the frame is square.
6. Position the face and install 24 saddle/washer assemblies with pads and 48 ties at the listed locations. Keep tie heads and sharp tails behind the face; flush-trim tails.
7. Lift with two people. On grass, install four stakes and guys. On hard ground, install four strapped 15 kg bags, anti-slip mats, and guys to the foot ends.
8. Check the opening **1500 ± 10 mm**, nominal diagonals **2121 mm** and diagonal difference below 10 mm. Check that no brace, connector or guy enters the clear opening. Load gently from both directions, inspect every joint, and perform the anchor/base checks above before a low-wind trial.

The first gate will likely take **2–3 hands-on hours**, plus printing; templates and preassembled pipe modules can shorten repeats. This is an estimate. Largest face part is 2400 × 600 mm; longest loose pipe is now 2065.1 mm. An assembled face is still 2700 mm square. Leave its ties/backers installed when storage allows; repeated full sheet disassembly consumes ties and time.

## Cost and material efficiency

Planning USD before tax, shipping, labor, tools, and ballast fill. Pickup quotes matter: shipping full sheets can dominate. Most entries below are allowances, not verified live quotations.

| Item | Quantity / allowance | Per-gate estimate |
|---|---|---:|
| Main 4 mm Coroplast | 2 sheets × $30 | $60.00 |
| Shared corner sheet | 1/16 sheet × $30 | $1.88 |
| 1-inch Sch40 | 4 × 10 ft at $13.50 | $54 |
| ¾-inch Sch40 | 1 × 10 ft at $10 allowance | $10 |
| All fittings | 10 fittings total, allowance | $24 |
| PETG and spare prints | Allowance, slice to confirm | $22 |
| UV ties / retaining screws | ~100 working ties + spares; 16 socket screws | $20 |
| Tape | Allocated share | $8 |
| Guy cord / adjustment | About 16 m | $12 |
| Ground anchors | 4 | $20 |
| **Grass gate, allocated batch cost** | | **about $232** |
| Hard-surface add-on | 2 extra 1-inch pipes + bag/strap/rubber allowance | **about $57** |
| **Dual-surface allocated cost** | Before ballast fill | **about $289** |

For one gate with a freshly purchased shared corner sheet, cash outlay is about **$260 grass / $317 dual-surface**, leaving 60 unused corner triangles for subsequent gates. Recovering the four corners from main-panel scrap avoids that third-sheet purchase. At a full batch, face-sheet allocation is 2.0625 sheets per gate. Existing cord/stakes, cut scrap washers, and local sheet pricing can reduce cost.

A Home Depot search result displayed $13.50 for the 1-inch 10-foot pipe. A sheet supplier listed $22.99 at its minimum 10-sheet tier; this is not a one-sheet quote. The $30 sheet and other amounts above are explicit budgeting assumptions. [Pipe listing](https://www.homedepot.com/p/100348473), [sheet supplier](https://corrugatedplastics.net/48x96_Blue4mmCorrugatedPlasticSheets.html), checked 2026-09-17.

Removing the second square and its depth links saves **three 10-foot ¾-inch pipes, twelve fittings, and 32 retained socket interfaces** versus the preceding two-frame design. With the same price allowances, that saves **about $52 per gate**. The tradeoffs are the shallower body, longer continuous main members for transport, and removal of the rear square’s stiffness. The four braces and both anchoring configurations remain; prototype checks are still required.

## WIP reference: retained and changed

Retained: correct outer/inner dimensions, repairs concentrated near corners, actual pipe OD for printed fits, and zip-tie retention. Changed: four identical pentagons and batch corner infills; one 1-inch backing square with ¾-inch corner braces; commercial fitting geometry in the cut calculations; printed positive-angle brace joints at both ends; scrap-sheet seam backers; PETG rather than reliance on PLA snap action; and explicit anchored/ballasted bases. The WIP's “outer size minus twice socket depth” is not a valid general cut formula. Its proposed third-sheet straight-strip layout for four 140 mm and four 260 mm strips needs 1600 mm width, exceeding a 1219.2 mm sheet; that tunnel-wall concept is no longer used.

## Files and validation

- `FPV_Gate_2700.blend`: nine editable scenes; fonts and build guide embedded.
- `renders/`, `Assembly_Views.pdf`, `START_HERE.html`: visual assembly references.
- `printable/`: face saddle, washer, two handed brace connectors, and optional ¾-inch saddle. STL coordinates are millimetres.
- `cut-layouts/`: main pentagon layout, shared corners, offcut backers, attachment template and polygon JSON.
- `BOM.csv`, `HARD_SURFACE_ADD_ON.csv`, `PVC_CUT_LIST.csv`: quantities and cost/cut assumptions.
- `validation.json`, `polygon_validation.json`: printable topology, stock use, polygon coverage and overlap checks.
- `../scripts/build_gate.py`: regenerates the current model and STL/render outputs with local Blender.

All printable meshes are closed/manifold. Face polygons and stock layouts are checked geometrically. Fitting envelopes, soft bags, screws, zip-tie bodies and knots are schematic. Their geometry does not substitute for physical fit/load testing or slicer inspection.

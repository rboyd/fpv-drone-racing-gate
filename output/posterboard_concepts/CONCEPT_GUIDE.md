# Uniform posterboard inserts / four folding gate concepts

This Blender package develops the posterboard study into four comparable exoskeleton concepts. The earlier Coroplast gate remains unchanged at `output/FPV_Gate_2700.blend`. These are design options, with seven printable fit coupons—not a complete, load-tested manufacturing kit.

User choices incorporated: small changes to gate size are allowed; transport pieces should be about 1.2 m or shorter; cardstock stays in four folding bundles; printed parts target support-free A1 Mini printing, reversible clicks and rapid field assembly.

## Four options

| Option | Every cardstock insert, mm | Inserts | Stock sheets | Straight cuts¹ | Outer / opening, mm | Folded bundle, approx. mm |
|---|---|---:|---:|---:|---|---|
| A — quarter sheets | 355.6 × 279.4 (14 × 11 in) | 48 | 12 | 36 | 2724.4 / 1590.8 | 1079 × 567 × 40 |
| **B — half sheets** | **355.6 × 558.8 (14 × 22 in)** | **24** | **12** | **12** | **2720.4 / 1594.8** | **1079 × 563 × 40** |
| C — whole sheets | 711.2 × 558.8 (28 × 22 in) | 12 | 12 | 0 | 2708.4 / 1582.8 | 715 × 563 × 65 |
| D — exact gate dimensions | 346 × 196 | 72 | 18 | 90 | 2700 / 1500 | 1050 × 600 × 40 |

¹ Individual straight separations without stacked cutting; repeated knife passes on the same line are not extra cuts. Quartering is one full crosscut plus one cut through each resulting half = three. For D, trim the sheet to 392 × 692, then quarter it: five cuts per sheet. All inserts within each option are identical; no special corner cards or narrow fillers.

**B is the recommended prototype:** twelve cuts total, half as many inserts as A, and one fold rather than C's two. A has smaller individually edge-retained cards and shorter insertion travel; B and C use rear ribs to reach similar nominal support-bay sizes. C minimizes cutting completely but needs eight fold lines across the gate instead of four, and additional rear ribs. D retains the exact prior dimensions but sacrifices the stock-size labor savings.

Stock is nominal 22 × 28 in cardstock at the user's $0.99 price, verified against [Hobby Lobby](https://www.hobbylobby.com/Art-Supplies/Project-Supplies/Poster-Projects/Poster-Board---22-x-28/p/81118411). Confirm actual thickness, size and squareness before choosing slot tolerances. The listing does not supply a weatherproof rating; treat it as replaceable dry-weather material.

## Why the four sections fit together

Four **identical rectangular cassettes** form a pinwheel. If cassette length is L and width is W, outside dimension is L+W and opening is L−W. Each cassette owns one complete outside corner. There are only four cassette-to-cassette seams, rather than four triangular/square infills to assemble separately.

Each cardstock cell uses **paper size + 4 mm** pitch in both directions. Two 1.2 mm channel backs plus 1.6 mm total insertion clearance account for the extra pitch. Card edges sit 2 mm inside the nominal cell boundary and overlap retaining lips by about 4 mm. Consequently the stock-based outer/opening dimensions are slightly different; the model does not hide those changes or pretend paper edges can occupy the same space as rail webs.

The channel sample has a **0.8 mm card slot**, 1.2 mm lips, 6 mm edge capture width and a 10 mm rear spine. A 0.4 mm paper thickness is the working assumption. Measure the actual stock and test before scaling production. Gate geometry uses actual paper dimensions and channel offsets; physical tolerance and factory sheet variation remain to be checked.

## Slide-in loading and repair

Assemble each leaf's side channels and fixed bottom stop on a flat bench. The outer end-cap rail is removable. Slide the cardstock through the parallel side channels, seat it against the stop, then click the end cap back into its rear-accessible receivers. For B and C, rear ribs and light keepers support the center; keepers must permit sliding clearance and support both pressure directions.

For multi-row A and D, replacing an interior card can require unloading its neighboring row first; B and C have only one row and direct access to every card.

Two **opposed U channels** serve a shared paper seam. This uses more plastic than the earlier idealized one-piece H rail but can be printed on the channel spines without an enclosed slot roof. Each U channel is segmented into equal pieces below 150 mm; most options need only two segment lengths. Short release keys and workshop corner nodes keep them joined permanently between flying sessions. The straight channel coupon omits final end-node interfaces; those require the fit-prototype pass after selecting an option.

## Joinery choice and release

Use **load-bearing sliding dovetails with a separate, replaceable in-plane cantilever latch**. The dovetail carries shear and separation loads; the spring only prevents withdrawal and should return near neutral after engagement. The catch has an accessible thumb/thumbnail edge. Press the spring sideways to clear the open notch, then slide the shoe out. No destructive snap tabs or inaccessible one-way barbs are intended.

The female track has a flat print base, an open groove, and 45° inward walls. The male shoe prints with its broad cover on the bed; its runner widens at 45°. The spring lies in the print XY plane. Receiver and shoe STL coupons are actual modeled solids. Their dimensional fit, operating force, wear and cycling still need a real PETG print.

At the four cassette seams, use **two bridge keys per seam**, inserted along the seam from its outer/inner ends after positioning the four cassettes. This avoids the assembly trap of four permanently projecting male dovetails around a closed ring. The bridge uses two parallel receivers; its full twin-runner implementation is a concept in the model, while the supplied single-runner coupon tests the common fit/latch mechanism.

At each fold, two removable bridge locks hold the leaves straight. Hinges position the leaves during folding; the locked bridge interfaces carry the unfolded joint loads. Release controls stay at the rear and clear of the flight opening.

This direction follows published guidance to use favorable layer orientation, stress relief and locating features that unload a snap arm; it is our proposed gate mechanism, not a certified joint. [Protolabs snap-fit guidance](https://www.hubs.com/knowledge-base/how-design-snap-fit-joints-3d-printing/), [Formlabs FDM orientation guidance](https://formlabs.com/blog/designing-3d-printed-snap-fit-enclosures/)

Clickfinity is useful as a modular-joint reference, but the examined implementation uses desk-trapped underside keys. A vertical, vibrating gate needs positively retained keys of its own. [Clickfinity reference](https://github.com/IamMrCupp/clickfinity-openscad/blob/main/README.md)

## Folding and transport

- A and B: six columns per cassette, book-fold between columns three and four. No card crosses a fold. Fold front-to-front; the axis sits in front of the face to leave clearance.
- C: three whole-sheet columns, accordion-fold at both column boundaries. One front-offset and one rear-offset hinge keep the paper flat and allow the rear spines to clear each other. Do not crease the middle of a whole sheet to force a two-leaf fold.
- D: six columns, book-fold after column three. Both halves are 1050 mm long.

The hinge concept uses separate flat printed eye-knuckles plus a removable flat split pin. Printing each eye with its axis vertical avoids horizontal barrel roofs or unsupported interleaved knuckles. The flat fork pin flexes in the bed plane; squeeze its exposed tips to remove it. Two hinges and two straightening locks serve each fold line. Pin/eye play and axial spacing need fit checks; the coupon illustrates the construction rather than supplying a finished hinge-to-rail adapter.

**Transport is four face bundles plus a PVC parts bag.** PVC saddles remain on the pipes, and low docking receivers remain on the faces. The single PVC square splits at four midpoints, giving eight main members below 1.2 m. Commercial inline couplings need positive, quick-release retention; cut lengths must be recalculated from the chosen fittings' actual engagement. Existing 1183 mm hard-surface half-feet are close to the stated transport limit before end caps; remove caps if necessary. The original one-piece 2065 mm PVC rails cannot be carried as-is under this transport requirement.

The 2100 mm PVC frame centerline remains the working baseline. Stock-based cassettes need docking offsets of up to about 29 mm; mounting tabs should accommodate this rather than forcing the paper grid to match the PVC. No second backing square is added. Keep four corner braces. Their new support-free clamp concept uses separate axial-printed pipe rings and a flat 45° link rather than a single underside-grooved block; its interfaces remain to be detailed after the saddle fit test.

## PVC attachment

The coupon is a C-saddle with a nominal **33.9 mm inside diameter** for 33.4 mm OD pipe, printed along the pipe axis. It can flex to admit the pipe; release by spreading its accessible ears. A **positive mouth keeper is required before field use**; the keeper interface is not yet manufactured by the coupon set. Backup tie passages are included. A loose C clip alone is not claimed to resist drone impact or cyclic wind.

Saddles carry docking receivers/shoes, so detaching the face does not require repeatedly flexing the pipe clip. The mounting flange and axial stops must prevent rotation/sliding on the pipes. Those retention details are part of the next prototype pass. PVC, ballast/guy anchors and four braces remain the primary support system; paper and latch springs are not substitutes for it.

## Parts families and support-free orientation

| Part family | Print approach | Status here |
|---|---|---|
| Straight U-channel with rear spine | Lay on 150 × 10 mm spine; channel opens upward | 150 mm coupon; actual assemblies show segment locations |
| Workshop nodes/end-cap receivers | Open features on bed; use the same dovetail/latch interface | Concept geometry; final adapters pending |
| Dovetail receiver | Flat floor down; open groove with 45° walls | Fit coupon supplied |
| Dovetail shoe / spring | Broad plate down, runner up; XY spring | Fit coupon supplied |
| Field bridge and fold lock | Two parallel dovetail runners with rear release | Concept envelope; based on coupon interface |
| Hinge knuckle | Eye axis vertical; separate knuckles | Fit coupon supplied |
| Hinge pin | Flat fork on bed | Fit coupon supplied |
| PVC saddle | Pipe axis vertical; planar ring | Fit coupon supplied; keeper and dock adapter pending |
| Rear ribs | Flat on broad side | Coupon supplied; paper keepers remain to be detailed |

The largest coupon is 150 mm long. All seven coupon STLs are in millimetres and fit the A1 Mini individually with brim room. No support scaffolding is intended. Dovetail overhangs target 45°; everything else uses bed-supported open profiles. Physical slicing and print quality still need confirmation. Do not print a complete gate's quantity from these coupon files.

## Cost / effort update

Support-free channels, four independent cassettes and folding hardware are more substantial than the earlier simplified shared-grid estimate. The current planning model counts channel plastic at **23.52 mm²**, 20% additional channel mass for workshop joints, 250 g for docks, 60 g per fold line, 120 g for the eight field bridge assemblies, rear ribs and 10% printing waste. It is not a slicer-derived BOM.

| Option | PETG planning mass | Whole 1 kg spools | Paper | Consumed materials at $20/kg | Whole-spool cash |
|---|---:|---:|---:|---:|---:|
| A | 3.12 kg | 4 | $11.88 | $74 | $92 |
| B | 2.55 kg | 3 | $11.88 | $63 | $72 |
| C | 2.37 kg | 3 | $11.88 | $59 | $72 |
| D | 3.82 kg | 4 | $17.82 | $94 | $98 |

Excludes PVC, fittings, brace clamps, bases, anchors, labor, power, coatings, shipping and tax. These estimates can change substantially with joint sizes and print settings. PETG density is 1.28 g/cm³; $20/kg is a budget assumption. [Density source](https://eu.store.bambulab.com/en-mt/products/petg-hf?variant=49068714557788)

Approximate equal U-channel segment quantities: A 480, B 336, C 216, D 720. These are slender parts that can be batch printed; the counts are not print-job counts. Long-term assembly labor is moved to the workshop: small nodes and channel joints stay together for transport. The C option avoids paper cuts but adds four fold lines and more release locks, so it does not automatically minimize field labor.

Field sequence for B: assemble/anchor the PVC frame; unfold four face cassettes and engage eight fold locks; lay out the pinwheel and insert eight corner bridges; engage sixteen PVC docks with two people supporting the face; verify locks and wind restraints. Reverse for packing without touching the paper inserts or permanent channel joints.

## What to decide next

Select B unless zero paper cutting (C) or smaller replaceable paper areas (A) outweigh the extra joints/handling. A physical half-sheet stock sample and the channel/dovetail/PVC coupons are the next useful validation, followed by one complete folding cassette. The full-gate material quantities should follow its stiffness, slot-fit and release-cycle results.

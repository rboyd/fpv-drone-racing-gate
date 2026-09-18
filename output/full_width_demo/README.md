# Recommended print: full-width paper-frame demonstrator

This kit assembles into a **24 × 8 inch (609.6 × 203.2 mm)** paper-frame sample. The 24-inch dimension uses the full roll width; cut just 8 inches along the roll. It demonstrates working-scale click connections, four crossmembers, integral half-cylinder magnet holders, removable front pads, and handling a real full-width paper face. It is a small gate-face specimen, not a full 2.09 m border or a wind-qualified gate.

Open `Full_Width_Demo.blend` or `Assembly_and_Print_Queue.pdf` to see the actual exported parts assembled. Blue/orange are explanatory display colors; all jobs use one PETG filament and need no filament changes.

## What to queue

Use the sliced A1 Mini PETG 3MF files in `sliced/`, at 100% scale.

| File | Print runs | PETG per run | Time per run |
|---|---:|---:|---:|
| `00_FIT_CHECK_A1Mini_PETG.3mf` | 1 first, if fit not already established | 16.0 g | 47 min |
| `01_FRAME_REPEAT_4_TIMES_A1Mini_PETG.3mf` | **4** | 45.2 g | 1 h 58 min |
| `02_KEYS_AND_PADS_ONCE_A1Mini_PETG.3mf` | **1** | 30.4 g | 1 h 32 min |

The frame kit totals **211.3 g / 9 h 24 min** across five plate runs. Including the initial fit check: **227.3 g / 10 h 12 min**, six runs. These are Bambu Studio estimates including startup, excluding your bed-change time. The A1 Mini needs manual plate clearing between runs. The files are prepared; no print job has been sent.

**Best first substantial job:** after the fit check, print `01_FRAME_REPEAT_4_TIMES` once. Its two edge rails, one crossmember and two keys make a complete small I-shaped bay; its two pads test magnetic paper retention. If that behaves well, print the remaining three copies and the keys/pads plate to complete the full 24-inch sample. Do not assume successful slicing proves the PETG click fit.

The old 198/220 mm stack samples are plain manufacturing coupons. This new kit has real mating connectors and does not rely on break-apart stacking.

## Four main printed types / exact quantities

| Part | Quantity | Purpose |
|---|---:|---|
| `DEMO_EDGE` | 8 | Identical 141.9 mm edge rails, each with three receiving sockets and two integral magnet lugs |
| `DEMO_RUNG` | 4 | Identical 111.2 mm crossmembers with a socket at each end |
| `CLICK_KEY` | 14 | Shared removable double-ended connector; six for the long edges, eight for the crossmembers |
| `PAPER_PAD` | 16 | Removable magnetic pressure pads |
| **Total** | **42** | **Four unique main part types** |

Each repeat plate has two edges, one rung, two keys and two pads: seven pieces. Four repeats produce 28 pieces. The second plate supplies the remaining six keys and eight pads: fourteen pieces. Fit-check parts are extra: a key, two clearance receivers, a magnet gauge and a pad. The extra key and pad can be kept as spares; the main plates already supply the exact full kit.

## Nonprinted supplies

- **32 axially magnetized 6 mm diameter × 2 mm magnets:** sixteen in the rail lugs and sixteen in the pads.
- One **609.6 × 203.2 mm** paper sheet, cut from the roll at its full width.
- A small amount of magnet-retaining adhesive suitable for your PETG and magnet coating. Dry-fit and verify polarity first. There are no screws, zip ties, hinges or separate lug fasteners in this demo frame.

Fewer magnet pairs can test one bay first. The full quantity gives two pairs per edge rail so edge retention can be compared by removing alternate pads.

## Assemble and test

1. **Print and identify the fit-check pieces.** Use Bambu's object names to distinguish `FIT_SOCKET_25` and `FIT_SOCKET_40`. Insert each end of the key straight into a receiver; the rigid guide runners and central spring forks must enter together. Both hooks should engage beyond their shoulders and return after being pinched for removal. The frame uses the **0.40 mm** receiver clearance. If that fit jams, does not latch, or requires damaging force, resolve the fit before the repeat runs. Do not scale the model to adjust clearance.
2. **Check your magnets.** The gauge bores are 6.1, 6.3 and 6.5 mm, left-to-right in its source orientation. Rail/pad pockets are 6.3 mm. Confirm a magnet sits flat against the thin pocket floor; check the mating pair attracts through the actual paper and both skins. Do this before bonding any magnets.
3. **Build two long edges.** Join four `DEMO_EDGE` pieces end-to-end using three keys for each edge. All D-shaped holders face the same side along each edge. Each edge measures `4 × 141.9 + 3 × 14 = 609.6 mm`. The 14 mm is the seated exposed middle of each key, not an arbitrary gap to estimate by eye. Keep the remaining end sockets empty.
4. **Add the four crossmembers.** Fit one key into each end of each `DEMO_RUNG` (eight keys). Lay one long edge with its D lugs pointing inward. Insert the four crossmembers into the four perpendicular sockets. Bring the other long edge onto all four free keys with its lugs also facing inward. Work evenly across the four joints so the last connection is not forced by bending the frame. Overall size is 609.6 × 203.2 mm. The crossmembers lie inward of the open ends, as shown in the assembly view.
5. **Fit the paper.** The rear is the side showing the spring forks and magnet pockets. The paper rests against the opposite, smooth front face. Dry-arrange all pairs, mark a consistent polarity, then retain the rear magnets in the integral D lugs and the front magnets in their separate pads. Seat magnets against their pocket floors. After the adhesive cures, place the paper on the front and add the sixteen pads. Each pair has 0.4 mm rail skin + paper + 0.4 mm pad skin between magnets; adhesive may add more gap.
6. **Exercise the main concepts.** Lift and handle the full-width specimen; note sag, twist and joint play. Pull a paper edge gently to compare sliding, peeling and tearing. Remove alternate pads to compare lower attachment density. Release and reconnect representative joints repeatedly, recording whitening, cracks, permanent opening or hooks that stop returning. To dismantle, pinch both fork tips of a key end from the rear and withdraw along the rigid guides. Do not pry the guides upward.

This ladder specimen deliberately exposes joint play and racking. It does not establish the stiffness of the later diagonal/crosshatch border or an outdoor wind limit. It also does not demonstrate the PVC dock or sacrificial stacks; those remain separate optional plates in `output/paper_roll_study/`. The current demo crossmembers have no dedicated PVC-dock mounting interface.

## Print settings and checks

Prepared for **A1 Mini, 0.4 mm nozzle, Generic PETG, 0.20 mm layers, 3 walls, 15% infill, textured PEI, supports off, no brim**. Preserve the flat orientation of the click keys so their flexures lie in the layer plane. Use the PETG settings appropriate to the filament you actually load. All parts and all supplied plates fit the 180 mm cube with at least 5 mm bed margin.

`print_checks.json` records seven manifold, positive-volume STL masters (four main types plus three fit-only types), ten successful warning-free individual/batch slices, plate placement checks and exact output quantities. Assembled source geometry measures 609.600 × 203.200 mm. Four representative mating arrangements were checked by point sampling with ray classification and nearest-surface distances; the method and sampling resolution are recorded in `assembly_checks.json`. This is a digital screening check, not an exhaustive collision proof or a physical fit/load test.

To regenerate from the repository root:

```sh
blender -b -t 8 --python scripts/build_full_width_demo.py
python3 scripts/slice_full_width_demo.py
python3 scripts/validate_full_width_demo.py
python3 scripts/package_full_width_demo.py
```

Packaging requires ReportLab. The builder reuses the current paper-study joint helper functions; earlier output files remain unchanged.

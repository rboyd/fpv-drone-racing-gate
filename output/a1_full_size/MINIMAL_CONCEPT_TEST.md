# Smallest useful first concept test

[Download the two-part assembly and test PDF](Assembly_and_Test_Instructions.pdf).

Print **one of each of these nine parts**, at full size:

| Part | Quantity | What it tests |
|---|---:|---|
| CHANNEL_LONG | 1 | Paper slot and long-channel geometry |
| CHANNEL_SHORT | 1 | Short-channel geometry; mate for splice/corner tests |
| SPLINT | 1 | Registered straight channel splice |
| CORNER_NODE | 1 | A 90-degree paper-frame corner |
| RIB_H_LOW_DOCK | 1 | Paper-contact shoe and actual rib-to-dock mounting holes |
| DOCK_PEDESTAL | 1 | Standoff and clearance under the snap |
| DOCK_CAP | 1 | Rib-side snap socket |
| PIPE_33 | 1 | Clip fit on 1-inch nominal / 33.4 mm OD PVC |
| SNAP_BRIDGE | 1 | Connecting and releasing the complete PVC dock |

[Open the sliced A1 Mini test plate](sliced/Minimal_Concept_Test_9_Parts/Minimal_Concept_Test_9_Parts_A1Mini_PETG.3mf), or [download the geometry-only layout](printable/Minimal_Concept_Test_9_Parts.3mf). **32.4 g PETG, approximately 95 minutes.** One plate, 0.4 mm nozzle, 0.20 mm layers, three walls, 15% infill, Textured PEI Plate, supports off. Verify your filament and plate settings before printing. All nine parts have been volume-checked and sliced with no warnings; no physical print is claimed.

Bring your actual posterboard, a short piece of 1-inch nominal PVC (33.4 mm outside diameter), six narrow 2.5 mm ties, and one approximately 3.6 × 250 mm pipe keeper tie. Releasable ties make the sequential tests easier. You do not need to cut up a complete posterboard sheet: use its edge and corner.

1. Slide the paper edge into each channel and check for free movement without creasing. Clear burrs rather than forcing the paper.
2. Place the two channels end-to-end with a 0.2 mm gap. Seat the splint's four bosses in the end windows and retain it with two ties. Long-to-short is a test combination; production uses the same interface between equal-length channels. Check sliding and bending by hand.
3. Remove the splint and rearrange the same channels at 90 degrees, with each channel starting 6.1 mm back from the virtual corner. Seat the CORNER_NODE with its fences against the inward channel spines, and tie each arm to its channel. Check paper fit at the corner. This samples the sheet-frame corner, not a full field seam between borders.
4. Assemble the dock: pedestal on the broad docking rib, cap on top, two ties through their matching holes. The pedestal's open space must remain under the cap's central socket. Seat PIPE_33 on the PVC and install its keeper tie. Align the cap and pipe-saddle sockets at 24 mm centers, with their rear surfaces level, then insert SNAP_BRIDGE until both rigid stops seat.
5. Check that the dock retains the rib and releases repeatedly. Pinch one fork and lift that end, then the other. Assess finger access in the assembled dock; blunt tweezers can help diagnose fit. Stop if a prong cracks or permanently bends. The rib shoe can also be checked against the back of the paper for sharp edges.

The same parts are reused between tests. This is the smallest useful **paper / splice / corner / complete dock** test, not a full test of long-rib stiffness or the assembled gate.

Optional second-stage additions:

- **Brace endpoint:** add one BRACE_LINK_45 and one PIPE_27. Reuse PIPE_33 from the dock test, and bring a piece of 3/4-inch nominal PVC (26.67 mm OD), four heavy brace-link ties and a second pipe keeper tie. This tests one printed brace-end joint.
- **Rear rib joints:** add one each of RIB_H_HIGH, RIB_V_HIGH, RIB_CROSS and RIB_ANCHOR. Reuse RIB_H_LOW_DOCK to test a lap joint, then the lower cross seat; use RIB_V_HIGH on the raised cross seat. Test the anchor against a long channel's center mounting windows. Reuse components between these checks.

A complete sheet bay is the next structural prototype after these interfaces work. Neither this small set nor the tabletop miniature establishes full-sheet flutter, border racking or wind performance.

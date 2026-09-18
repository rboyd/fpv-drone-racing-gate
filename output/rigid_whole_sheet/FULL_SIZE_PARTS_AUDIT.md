# Full-size rigid gate: parts and A1 Mini audit

Audited the saved Blender file, scene `01_RIGID_GATE`, at full size. Miniature geometry and repeated presentation scenes are excluded. The A1 Mini has a nominal 180 × 180 × 180 mm build volume ([Bambu specifications](https://us.store.bambulab.com/products/a1-mini?id=543566369394393101)). Bounds below are each object's unrotated envelope, sorted longest first; rails can be placed on their 10 mm spines.

**Result: the current full-size concept is not a complete printer-ready kit.** It has 11 modeled geometry variants, totaling 376 mesh objects intended to represent printed components or assemblies. This is not 376 production parts: node markers overlap, some boxes represent multi-part assemblies, and several interfaces are absent. Two rib variants do not fit the printer at all. All five supplied full-size *test samples* fit, but that does not validate every full-size component.

| Modeled type | Quantity per gate | Envelope, mm | A1 Mini assessment |
|---|---:|---|---|
| Long edge-channel segment | 120 | 142.84 × 10 × 6 | Fits; final end connections absent |
| Short edge-channel segment | 96 | 140.50 × 10 × 6 | Fits; final end connections absent |
| Long rear rib | 12 | 715.20 × 5 × 2 | **Does not fit** |
| Short rear rib | 12 | 562.80 × 5 × 2 | **Does not fit** |
| Workshop corner-node marker | 48 markers | 10 × 10 × 4 | Placeholder fits; not a physical node BOM |
| Paper keeper | 24 | 16 × 6 × 1.2 | Placeholder envelope fits; interface unfinished |
| Face docking receiver | 16 | 55 × 32 × 6 | Placeholder envelope fits; actual adapter unfinished |
| Permanent border splice bridge | 16 | 70 × 22 × 8 | Placeholder envelope fits; actual joint unfinished |
| Removable gate-corner bridge | 8 assemblies | 65 × 40 × 9 | Placeholder envelope fits; twin-runner bridge unfinished |
| Pipe-side docking assembly | 16 assemblies | 56.8 × 40 × 25 | Placeholder envelope fits; saddle, keeper and adapter need separate BOM |
| PVC brace-end clamp | 8 assemblies | 40 × 30 × 25 | Placeholder envelope fits; split clamp bodies/link need separate BOM |

Lengths of the two rail meshes are 0.2 mm shorter than their segment pitch, leaving a small splice gap: long edge pitch 715.2 / 5 = 143.04 mm; short edge pitch 562.8 / 4 = 140.70 mm. Two long edges and two short edges on each of twelve sheets give 12 × 2 × 5 = 120 long channel pieces and 12 × 2 × 4 = 96 short ones. Removable paper end-cap rails are included in these 216 pieces, not another twelve full-length printed bars.

## Missing details that change production quantities

- **168 channel splice locations:** each sheet has 2 × (5−1) + 2 × (4−1) = 14 intermediate channel joints. These need integrated joint ends or separate couplers. The sixteen large border splices do not account for these 168 rail joints. Separate couplers would add 168 parts, but integrated ends would instead change the rail geometry/type count.
- **Corner nodes are duplicated markers:** four markers per sheet create 48 boxes. Within four separate borders, there are only 32 distinct corner/junction positions: 16 end corners and 16 internal seam junctions. In the assembled gate four more positions coincide across separable borders, yielding 28 world-space centers. Those coincidences need proper adjoining geometry, not simply printing overlapping blocks.
- **Rear ribs need segmentation and junctions.** A possible pitch scheme is five long-rib pieces per bay (60 × 143.04 mm) and four short-rib pieces per bay (48 × 140.70 mm), all with 5 × 2 mm nominal section. This would turn 24 oversized ribs into 108 printable-length rib blanks and introduce 84 inline rib joints. It is a proposed scheme, not implemented manufacturing geometry; tongue/lap/sleeve allowances can change the lengths.
- **Twelve rear rib crossings** need a cross-junction or depth offset; the current two perpendicular solids overlap at each center. Endpoint attachments and the center crossing must be included in the final rib design.
- **Paper caps and keepers** still need release/retention interfaces and a defined part split.
- **Eight gate-corner bridges** need their mating receiver sets and latches specified; the simple bridge envelopes do not represent all constituent parts.
- **Sixteen PVC docking assemblies** need actual saddle-to-shoe adapters and positive mouth keepers; eight brace-end clamp assemblies need their separate bodies/links/retainers counted. Bounds of a schematic assembly are not proof that every finished support-free component fits.

Because these details affect material use, the previous 1.84 kg/two-spool estimate remains a preliminary allowance, not a verified total.

## Full-size STL samples actually checked

| Sample | Supplied print orientation bounds, mm | Volume fit |
|---|---|---|
| Straight U channel | 150 × 10 × 6 | Pass |
| Dovetail receiver | 50 × 25.4 × 7 | Pass |
| Dovetail shoe and release spring | 45 × 29.2 × 5.6 | Pass |
| PVC C saddle | 37.215 × 40.288 × 8 | Pass |
| Support rib blank | 150 × 5 × 2 | Pass |

These five files are 1:1 fit samples. Their quantities are chosen for testing; they are not five part types sufficient to manufacture the gate. Bounds were read directly from the binary STLs. Volume fit does not establish physical clearance, support-free print quality, stiffness or latch durability.

## Nonprinted materials

The face uses 12 uncut 22 × 28 in posterboard sheets. The backing uses 1-inch nominal PVC and 3/4-inch nominal PVC braces, commercial fittings, the earlier selected base/anchoring system and optional zip ties. The conceptual scene depicts eight half-members for the one square backing frame, four braces, four midpoint couplings, two legs and two short feet; fitting engagement, corner fittings, and the chosen grass/hard-surface base remain governed by the earlier build design. Scene lengths are not a new PVC cutting list. None of these purchased materials needs to fit a printer.

The JSON/CSV alongside this report preserve exact model counts and sample bounds. Audit reproduction: `blender -b output/rigid_whole_sheet/Rigid_Whole_Sheet_Gate.blend --python scripts/audit_rigid_gate_parts.py`.

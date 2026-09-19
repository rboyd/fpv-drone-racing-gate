"""Generate the public project README and cost ledger from validated production data."""
from pathlib import Path
import json,csv,math
R=Path(__file__).resolve().parents[1];O=R/'output/corner_guide_elbow';P='output/corner_guide_elbow'
b=json.loads((O/'BOM.json').read_text());v=json.loads((O/'print_checks.json').read_text());c=json.loads((R/'docs/material_costs.json').read_text())
s=v['gates']['single'];d=v['gates']['split_s'];petg=c['petg_pack_usd']/(1000*c['petg_pack_kg']);mag=c['magnet_pack_usd']/c['magnet_pack_quantity']
def duration(minutes):
 n=round(minutes);return f'{n//60} h {n%60:02d} min'
def money(x):return f'${x:.2f}'
names={'ELBOW':'Bottom elbow','DUAL_GUY_ELBOW':'Top guy elbow','TEE':'Three-way tee','CROSS':'Four-way cross','MAG_SLEEVE':'Magnetic sleeve'}
rows=[]
for code,label in names.items():
 a=v['slices']['ONE_'+code];bounds=next(p['print_bounds_mm'] for p in b['parts'] if p['code']==code)
 rows.append(f'| [{label}]({P}/printable/{code}.stl) | {b["gates"]["single"]["counts"][code]} | {b["gates"]["split_s"]["counts"][code]} | {a["grams"]:.2f} g | {duration(a["minutes"])} | {money(a["grams"]*petg)} |')
part_table='\n'.join(rows)
rows=[]
for recipe in dict.fromkeys([*b['gates']['single']['print_queue'],*b['gates']['split_s']['print_queue']]):
 a=v['slices'][recipe];runs=[b['gates'][k]['print_queue'].get(recipe,0) for k in ['single','split_s']]
 rows.append(f'| [{recipe}]({P}/sliced/{recipe}/{recipe}_A1Mini_PETG.3mf) | {len(b["plates"][recipe])} | {runs[0]} | {runs[1]} | {a["grams"]:.2f} g | {duration(a["minutes"])} |')
queue_table='\n'.join(rows)
ledger=[]
for kind,stats in [('single',s),('split_s',d)]:
 for item,qty,unit,price in [('Black PETG',stats['grams']/1000,'kg',petg*1000),('6 x 2 mm magnets',stats['magnet_pairs']*2,'individual',mag),('1 inch PVC',stats['pipe_sticks'],'10-ft stick',c['pvc_10ft_stick_usd'])]:
  ledger.append({'configuration':kind,'item':item,'quantity':qty,'unit':unit,'unit_cost_usd':price,'cost_usd':round(qty*price,2)})
with (R/'docs/Cost_BOM.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=list(ledger[0]));w.writeheader();w.writerows(ledger)
readme=f'''# FPV Drone Racing Gate

A modular FPV race gate built from **1-inch PVC, five types of PETG fittings, roll paper and magnets**. Print the fittings on a Bambu A1 Mini, cut two standard pipe lengths, and assemble a single gate or a two-level Split-S obstacle.

**Current design:** three-magnet top elbows with independent front/rear guy eyes and recessed paper alignment guides. **Prototype status:** the 33.5 mm magnetic sleeve bore has been physically tested on the purchased PVC and fits well. Full-gate assembly, friction-joint retention and guy loads still need physical validation.

![Assembled single gate, front view rendered in Blender]({P}/renders/05_SINGLE_FRONT.png)

*Blender assembly render—not a photograph of a completed build. Blue parts in the renders represent the black PETG used for printing. Ground anchoring and feet are not shown.*

| | Single gate | Stacked Split-S, total |
|---|---:|---:|
| Paper outline | 2700 × 2700 mm | 2700 × 4790.4 mm |
| Clear square opening | 1480.8 × 1480.8 mm | Two 1480.8 × 1480.8 mm openings |
| Paper band width | 609.6 mm / 24 in | 609.6 mm / 24 in |
| Printed parts / unique types | 64 / 5 | 104 / 5 |
| PETG, full batch queue | {s['grams']/1000:.3f} kg | {d['grams']/1000:.3f} kg |
| Estimated printer time | {duration(s['minutes'])} | {duration(d['minutes'])} |
| Plate runs on one A1 Mini | {s['plate_runs']} | {d['plate_runs']} |
| Priced materials: PETG + magnets + PVC | **{money(s['priced_materials_usd'])}** | **{money(d['priced_materials_usd'])}** |

Paper, guy lines and ground support are additional. Prices are the owner's approximate purchase costs, detailed below. The two guy ears extend about 28.6 mm beyond the adjacent paper edges.

## Files to start with

- [Current Blender model]({P}/Corner_Guide_Elbow.blend), including assembled gates, paper alignment, cord routing and the five-part overview.
- [Illustrated assembly and test PDF]({P}/Corner_Guide_Elbow.pdf) and [detailed current guide]({P}/README.md).
- [Printable STL parts]({P}/printable/) and [prepared A1 Mini PETG projects]({P}/sliced/).
- [Single-gate print queue]({P}/single_Print_Queue.csv), [PVC stock layout]({P}/single_PVC_Stock_Layout.csv), [paper cuts]({P}/single_Paper_Cuts.csv) and [magnet positions]({P}/single_Magnet_Positions.csv).
- [Stacked print queue]({P}/split_s_Print_Queue.csv) and [cost BOM](docs/Cost_BOM.csv).

Use **`output/corner_guide_elbow/`** for the current build. Other output folders preserve earlier iterations; their quantities, interfaces and prices may differ.

## Five printed parts

![Bottom elbow, top guy elbow, tee, cross and sleeve at the same scale]({P}/renders/11_ALL_PRODUCTION_PARTS.png)

| Part / STL | Single qty | Stacked total qty | PETG per individual print | Individual print time | PETG cost per individual print |
|---|---:|---:|---:|---:|---:|
{part_table}

Individual print estimates include each plate's overhead. The full-gate totals use **seven-sleeve batches**, which are substantially faster than printing sleeves one at a time. Values come from local Bambu Studio slices, not elapsed measurements of completed prints. Full queues start from zero; subtract parts already printed.

The bottom elbow, tee, cross and sleeve are unchanged from the accepted-bore iteration. All sockets use **33.5 mm bores** for the project's nominal 1-inch PVC (modeled OD 33.4 mm). Elbows, tees and crosses have 30 mm pipe engagement; the sleeve has 16 mm engagement. Friction retains the joints—no bolts, nuts or zip ties in this frame.

The top elbow adds two separate 10.5 mm eyes for front and rear guys, three 6 × 2 mm magnet seats, and an L-shaped paper guide recessed 0.4 mm into the face. The magnet pockets retain 0.4 mm plastic skins. Bare front magnets clamp the paper against those skins; front paper pads are optional and excluded from the required BOM.

## Material BOM and costs

These are **prices paid by the project owner**, not current store quotes or product recommendations. Exact brands/listings were not supplied.

| Material purchased | Pack price | Unit rate used |
|---|---:|---:|
| Black PETG, four 1 kg spools | $39.59 / 4 kg | $9.8975 / kg |
| Neodymium magnets, 6 mm diameter × 2 mm thick | $19.99 / 800 | $0.0249875 / magnet |
| Nominal 1-inch PVC, 10 ft / 3048 mm stick | $5.34 each | $5.34 / stick |

| Material | Single quantity | Single cost | Stacked total quantity | Stacked cost |
|---|---:|---:|---:|---:|
| PETG consumed by supplied queue | {s['grams']/1000:.5f} kg | {money(s['PETG_cost_usd'])} | {d['grams']/1000:.5f} kg | {money(d['PETG_cost_usd'])} |
| Magnets, including both sides of paper | 152 / 76 pairs | {money(s['magnet_cost_usd'])} | 240 / 120 pairs | {money(d['magnet_cost_usd'])} |
| PVC stock, including cutting waste | 8 sticks | {money(s['pipe_cost_usd'])} | 14 sticks | {money(d['pipe_cost_usd'])} |
| **Priced material subtotal** | | **{money(s['priced_materials_usd'])}** | | **{money(d['priced_materials_usd'])}** |
| 24-inch paper roll | 8.5056 m used | Unpriced | 14.3112 m used | Unpriced |
| Front/rear guys and suitable ground support | 4 guys + supports | Unpriced | 4 guys + supports | Unpriced |

These subtotals allocate only the filament and magnets used, plus all PVC sticks purchased. Starting from no supplies, buying **one 4 kg filament pack + one 800-magnet pack + the PVC** costs **$102.30 single / $134.34 stacked**, leaving filament, magnets and pipe offcuts. The stacked queue fits nominally within 4 kg, with about 309 g spare before failed prints or other additions. Tax, shipping, adhesive, electricity, optional pads, tools, failed prints, paper and ground support are excluded.

Machine-readable inputs: [material_costs.json](docs/material_costs.json). [Cost_BOM.csv](docs/Cost_BOM.csv) contains the calculated line items. Older guides retain their historical pricing assumptions.

## A1 Mini printing

Prepared projects use the **180 × 180 × 180 mm A1 Mini**, a 0.4 mm nozzle, 0.20 mm layers, four walls, 20% infill, Generic PETG, a textured PEI plate and no supports. All supplied plate layouts have at least 5 mm bed margin. The largest fitting is the top guy elbow at **168.614 × 168.614 × 53.345 mm**. Retain the supplied orientations; the socket roofs are shaped for support-free printing.

For a new printer/pipe combination, start with [one magnetic sleeve]({P}/sliced/ONE_MAG_SLEEVE/ONE_MAG_SLEEVE_A1Mini_PETG.3mf), then test [one tee]({P}/sliced/ONE_TEE/ONE_TEE_A1Mini_PETG.3mf) and [one top guy elbow]({P}/sliced/ONE_DUAL_GUY_ELBOW/ONE_DUAL_GUY_ELBOW_A1Mini_PETG.3mf). The project owner's sleeve fit is confirmed; it does not establish the longer sockets' fit on every pipe brand.

| Prepared plate | Parts / run | Single runs | Stacked total runs | PETG / run | Time / run |
|---|---:|---:|---:|---:|---:|
{queue_table}

The single queue is about **94.5 printer-hours**, and the stacked queue about **150.4 printer-hours**, before plate changes, setup and downtime. Slicer estimates depend on the selected machine, filament and process settings.

## PVC cuts and assembly

| PVC cut length | Single qty | Stacked total qty |
|---|---:|---:|
| 389.6 mm | 16 | 24 |
| 1560.8 mm | 8 | 14 |

The [single]({P}/single_PVC_Stock_Layout.csv) and [stacked]({P}/split_s_PVC_Stock_Layout.csv) stock layouts reserve 3 mm per cut and 10 mm per stick for trimming. The workshop cutter is a **Husky 1-1/4-inch ratcheting PVC cutter**; hand-saw cuts are also accommodated by the allowance. Mark and verify one master piece of each length before using it for repeated marking. Square and deburr the cuts; mark 30 mm socket insertion depth.

1. Slide the magnetic sleeves onto each pipe **before** inserting both pipe ends into fittings. Use the [sleeve-position CSV]({P}/single_Sleeve_Positions.csv) to set their positions and clock the magnet faces into the paper plane.
2. Build horizontal rows with four fittings and short / long / short pipes. The bottom corners use plain elbows; top corners use guy elbows; perimeter junctions use tees; interior junctions use crosses. The [assembly map]({P}/single_Assembly_Map.svg) and [node list]({P}/single_Nodes.csv) identify every location and rotation.
3. Join the rows with vertical pipes while working flat. Seat the sockets to the witness marks and check equal diagonals and coplanarity.
4. Install backing magnets at the listed paper attachment positions, checking polarity before bonding. Some tee/cross pockets are unused in a given orientation; **populate the magnet-position list, not every physical pocket**.
5. Cut 24-inch-wide paper into two 2700 mm horizontal bands and two 1552.8 mm side inserts for the single gate. Side inserts overlap the horizontal bands by 36 mm at each end. The stacked version uses three horizontal bands and four side inserts. A 100-ft roll yields three singles or two stacked paper sets, before spoilage.
6. At each top elbow, align the paper edges with the **centerlines** of the recessed L. Place the corner magnet first, then the top/side magnets and remaining edge magnets. Paper is held as rear magnet → plastic skin → paper → front magnet.
7. Attach separate front and rear guys at each upper corner. Fit and test suitable stakes for soil or ballast/base supports for hard surfaces before flight. The current frame kit does not specify a complete footing or anchor design, and no wind/load rating is assigned. Paper is a replaceable face; wet-weather durability has not been established.

![Top corner with three magnets and separate front/rear guy attachments]({P}/renders/08_TOP_CORNER_ROUTING.png)

## Extend to a two-level Split-S

![Assembled two-level Split-S paper face rendered in Blender]({P}/renders/12_SPLIT_S_FRONT.png)

Move the complete top row upward, reusing its guy elbows, tees, sleeves and magnets. Add **4 tees, 4 crosses, 32 sleeves, 8 short pipes, 6 long pipes and 44 magnet pairs**. The added PVC fits six more 10-ft sticks. Add one horizontal paper band and two side inserts. All existing gate parts and pipe cuts are reused; stacked totals above include the original gate.

The finished paper outline is **2.70 m wide × 4.7904 m tall**, before any feet. This is a tall obstacle, and its supports must be tested for the actual installation.

![Rear PVC structure of the stacked gate]({P}/renders/06_STACKED_REAR.png)

## What is verified

- Actual printed magnetic sleeve: good friction fit on the purchased PVC at a 33.5 mm design bore.
- Digital geometry: connected manifold STL meshes, A1 Mini bounds and plate clearances, aligned magnet pockets, paper-guide depth, cord routing clearance and matching PVC ports.
- Slicing: every supplied recipe generates with supports off and no slicer warnings.
- Assembly accounting: part counts, full print queues, pipe stock nesting, paper positions and reuse when extending to Split-S.

Physical elbow/tee/cross fit, magnet retention, full-frame stiffness, guy-eye strength and outdoor performance remain prototype tests. The images are CAD renders of the current design.

## Rebuild and repository layout

The checked-in Blender scenes, STLs, 3MF projects, PDFs and CSVs are ready to inspect. Geometry is authored in millimetres and converted to metres in Blender; exported STLs/3MFs use millimetres.

```sh
# Blender 5.0.1 was used locally; --no-render builds geometry and scenes only.
blender -b -t 8 --python scripts/build_corner_guide_elbow.py -- --no-render

# Slice with the locally installed Bambu Studio and its A1 Mini presets.
python3 scripts/slice_corner_guide_elbow.py
python3 scripts/validate_corner_guide_elbow.py

# Render the full scene set (omit --no-render).
blender -b -t 8 --python scripts/build_corner_guide_elbow.py

# Documentation packaging requires ReportLab.
python3 -m pip install reportlab
python3 scripts/package_corner_guide_elbow.py
python3 scripts/publish_project_docs.py
```

Scripts currently target **macOS**: the Blender helpers use system Arial fonts and the slicer wrapper uses `/Applications/BambuStudio.app`. Adapt those paths for other operating systems. `RENDER_SCENES` can restrict rendering to a comma-separated scene list. PDFs embed rendered images, so render before packaging.

- `output/corner_guide_elbow/`: current gate, five production types and print queues.
- `scripts/`: reproducible geometry, slicing, validation and packaging.
- `docs/`: current material prices and cost ledger.
- [DESIGN_HISTORY.md](DESIGN_HISTORY.md): earlier Coroplast, posterboard, click-track and PVC iterations.
- `reference/` and `WIP-design.md`: design references; they are not current fabrication instructions.

Generated loose G-code, logs, Blender backup files and duplicate kit ZIPs are excluded from Git. Sliced 3MF projects are included; the packaging script can regenerate the current ZIP locally.

## Reference attribution

The archived snap-together picture-frame study includes Tony Youngblood's reference model under **CC BY-SA 4.0**; see [its attribution and source links](reference/picture_frame/ATTRIBUTION.md). The current PVC fittings use newly constructed geometry. No blanket license is asserted here for the rest of the repository.
'''
(R/'README.md').write_text(readme)
print('Public README and cost ledger generated:',s['priced_materials_usd'],d['priced_materials_usd'])

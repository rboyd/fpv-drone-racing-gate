"""Package accepted-bore gate fittings, tee savings and repeat-cut measuring tools."""
from pathlib import Path
import json,csv,html,re,zipfile,collections
from reportlab.platypus import SimpleDocTemplate,Paragraph,Image,Table,TableStyle,PageBreak,Spacer
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib.colors import HexColor
ROOT=Path(__file__).resolve().parents[1];O=ROOT/'output/tee_pvc_gate'
b=json.loads((O/'BOM.json').read_text());v=json.loads((O/'print_checks.json').read_text())
parts={p['code']:p for p in b['parts']};gates=b['gates'];stats=v['gates'];s=stats['single'];d=stats['split_s']
previous=json.loads((ROOT/'output/orthogonal_pvc_gate/print_checks.json').read_text())
sl=v['slices'];kit=sl['MEASURING_KIT'];tee=sl['ONE_TEE'];guy=sl['ONE_GUY_ELBOW'];cross=sl['ONE_CROSS']
def csvout(name,rows):
 with (O/name).open('w') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
for kind,g in gates.items():
 csvout(f'{kind}_Printed_BOM.csv',[{'part':c,'quantity':n,'description':parts[c]['description'],'print_bounds_mm':' x '.join(map(str,parts[c]['print_bounds_mm']))} for c,n in g['counts'].items()])
 csvout(f'{kind}_PVC_Cuts.csv',[{'piece':i+1,'name':e['name'],'from_node':e['a'],'to_node':e['b'],'length_mm':e['length_mm']} for i,e in enumerate(g['edges'])])
 csvout(f'{kind}_PVC_Stock_Layout.csv',[{'stock':r['stock'],'cut_order':i+1,'name':e['name'],'length_mm':e['length_mm'],'reserved_cut_allowance_mm':3,'reserved_end_allowance_mm':10} for r in g['stock_plan'] for i,e in enumerate(r['cuts'])])
 csvout(f'{kind}_Print_Queue.csv',[{'recipe':n,'runs':r,'pieces_per_run':len(b['plates'][n]),'grams_per_run':v['slices'][n]['grams'],'minutes_per_run':v['slices'][n]['minutes'],'file':f'sliced/{n}/{n}_A1Mini_PETG.3mf'} for n,r in g['print_queue'].items()])
 csvout(f'{kind}_Sleeve_Positions.csv',[{'pipe':p['pipe'],'distance_from_cut_start_mm':p['from_cut_end_mm'],'face_x_mm':round(p['xy'][0],3),'face_y_mm':round(p['xy'][1],3),'part_angle_degrees':p['angle']} for p in stats[kind]['sleeves']])
 csvout(f'{kind}_Magnet_Positions.csv',[{'pair':i+1,'x_from_left_mm':x,'y_from_bottom_mm':y,'frame_skin_mm':.4,'front':'Bare 6 x 2 mm magnet; front pad optional'} for i,(x,y) in enumerate(g['magnets'])])
 csvout(f'{kind}_Paper_Cuts.csv',[{'piece':i+1,'x_mm':x,'y_mm':y,'width_mm':w,'height_mm':h,'roll_cut_length_mm':max(w,h),'role':'horizontal band' if w==2700 else 'side insert with 36 mm overlap at each end'} for i,(x,y,w,h) in enumerate(g['paper_rectangles'])])
 csvout(f'{kind}_Nodes.csv',[{'node':n,'x_mm':q['xy'][0],'y_mm':q['xy'][1],'part':q['code'],'rotation_degrees':q['angle']} for n,q in g['nodes'].items()])
 H=g['height_mm'];shapes=[]
 for x,y,w,h in g['paper_rectangles']:shapes.append(f'<rect x="{x}" y="{H-y-h}" width="{w}" height="{h}" fill="#f5aa67" stroke="#9a622f" stroke-width="2"/>')
 for x,y in g['magnets']:shapes.append(f'<circle cx="{x}" cy="{H-y}" r="3" fill="#17374c"/>')
 (O/f'{kind}_Paper_and_Magnet_Map.svg').write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-50 -50 2800 {H+100}" width="600"><title>Paper and actual 6 mm magnet positions</title>'+''.join(shapes)+'</svg>')
 shapes=[]
 for e in g['edges']:
  a=g['nodes'][e['a']]['xy'];z=g['nodes'][e['b']]['xy'];color='#007b9c' if e['length_mm']>1000 else '#e28132'
  shapes.append(f'<line x1="{a[0]}" y1="{H-a[1]}" x2="{z[0]}" y2="{H-z[1]}" stroke="{color}" stroke-width="24"/>')
  shapes.append(f'<text x="{(a[0]+z[0])/2+25}" y="{H-(a[1]+z[1])/2-25}" font-size="42" fill="{color}">{e["length_mm"]}</text>')
 for n,q in g['nodes'].items():
  x,y=q['xy'];shapes.append(f'<circle cx="{x}" cy="{H-y}" r="35" fill="#17374c"/><text x="{x+45}" y="{H-y+55}" font-size="44">{n}</text>')
 (O/f'{kind}_Assembly_Map.svg').write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-70 -70 2950 {H+160}" width="750"><title>Front-coordinate node map; orange 389.6 mm, blue 1560.8 mm PVC cuts</title><rect x="-70" y="-70" width="2950" height="{H+160}" fill="white"/>'+''.join(shapes)+'</svg>')
csvout('Upgrade_Additional_Parts.csv',[{'part':c,'quantity':n} for c,n in v['upgrade']['additional_parts'].items()])
csvout('Upgrade_Additional_PVC.csv',[{'cut_length_mm':c,'quantity':n} for c,n in v['upgrade']['additional_pipe_cuts'].items()])
csvout('Comparison.csv',[{'configuration':k,**{n:x for n,x in q.items() if n!='sleeves'}} for k,q in stats.items()])
partrows=[[c,gates['single']['counts'][c],gates['split_s']['counts'][c],' x '.join(map(str,parts[c]['print_bounds_mm']))] for c in b['production_codes']]
parttable='\n'.join('| '+' | '.join(map(str,r))+' |' for r in partrows)
costrows=[[k,q['printed_pieces'],f'{q["grams"]/1000:.3f}',f'{q["minutes"]/60:.1f}',q['plate_runs'],f'{q["pipe_sticks"]} / ${q["pipe_cost_usd"]}',f'${q["frame_PVC_plus_PETG_usd"]:.2f}'] for k,q in stats.items()]
costtable='\n'.join('| '+' | '.join(map(str,r))+' |' for r in costrows)
queuerows=[[n,gates['single']['print_queue'].get(n,0),gates['split_s']['print_queue'].get(n,0),len(b['plates'][n]),sl[n]['grams'],round(sl[n]['minutes']/60,2)] for n in dict.fromkeys([*gates['single']['print_queue'],*gates['split_s']['print_queue']])]
queuetable='\n'.join('| '+' | '.join(map(str,r))+' |' for r in queuerows)
newplates=['MEASURING_KIT','ONE_TEE','ONE_GUY_ELBOW','ONE_DEPTH_30','MEASURING_KIT_PLUS_DEPTH']
csvout('New_Parts_Print_Queue.csv',[{'recipe':n,'pieces':len(b['plates'][n]),'grams':sl[n]['grams'],'minutes':sl[n]['minutes'],'file':f'sliced/{n}/{n}_A1Mini_PETG.3mf'} for n in newplates])
csvout('Workshop_Tools.csv',[{'code':c,'required_for_length_jig':c!='DEPTH_30','quantity':1,'print_bounds_mm':' x '.join(map(str,parts[c]['print_bounds_mm'])),'purpose':parts[c]['description']} for c in ['JIG_ZERO','JIG_MARK','DEPTH_30']])
readme=f'''# Accepted 33.5 mm bore / tees, top guy elbows and measuring tools

The user confirmed that the printed MAG_SLEEVE fits the purchased PVC perfectly on 2026-09-18. **33.5 mm is now the fixed design bore for every PVC interface in this iteration. The MAG_SLEEVE STL is byte-for-byte unchanged.** The deeper fitting sockets and workshop tools still need their first physical checks; no further bore-selection samples are included.

[Blender model](Tee_PVC_Gate.blend) · [Visual index](index.html) · [Assembly and measuring PDF](Tee_Gate_and_Measuring_Guide.pdf) · [Kit](Tee_PVC_Gate_Kit.zip)

## Workshop status / 2026-09-19

The user printed MAG_SLEEVE and confirmed a perfect fit on purchased PVC; retain 33.5 mm throughout. The selected next job is ONE_TEE in PETG, opened in Bambu Studio (98.49 g / 226.45 minutes). No successful tee print or strength test has been reported, and the assistant has not submitted a job to the printer.

For the two fixed PVC lengths, accurately cut and checked PVC master pieces are the preferred simple marking templates. The printed measuring jig is optional and deferred; prioritize production fittings. The current guy elbow has one eye behind the face. The next design request is simultaneous front/rear tie-down access with a diagonal extension and top/side magnet pads; that revision is not part of this baseline.

## Print these new parts

- [Two-head measuring kit](sliced/MEASURING_KIT/MEASURING_KIT_A1Mini_PETG.3mf): **{kit['grams']:.2f} g / {kit['minutes']/60:.2f} hours**. JIG_ZERO + JIG_MARK only. Use these with a straight spare piece of 1-inch PVC and a metric tape measure.
- [One three-way tee](sliced/ONE_TEE/ONE_TEE_A1Mini_PETG.3mf): **{tee['grams']:.2f} g / {tee['minutes']/60:.2f} hours**.
- [One top guy elbow](sliced/ONE_GUY_ELBOW/ONE_GUY_ELBOW_A1Mini_PETG.3mf): **{guy['grams']:.2f} g / {guy['minutes']/60:.2f} hours**.
- [Optional 30 mm insertion-depth gauge](sliced/ONE_DEPTH_30/ONE_DEPTH_30_A1Mini_PETG.3mf): **{sl['ONE_DEPTH_30']['grams']:.2f} g / {sl['ONE_DEPTH_30']['minutes']/60:.2f} hours**. This marks engagement depth on every pipe end; it is not another bore-selection sample.

[MEASURING_KIT_PLUS_DEPTH](sliced/MEASURING_KIT_PLUS_DEPTH/MEASURING_KIT_PLUS_DEPTH_A1Mini_PETG.3mf) combines the two heads and optional depth gauge. Use supplied orientations. All plates fit the A1 Mini with at least 5 mm bed margin and slice with supports off and no warnings. Estimates use Generic PETG, 0.4 mm nozzle, 0.20 mm layers, four walls and 20% infill. No printer job has been submitted.

## Measuring tools for the Husky ratcheting PVC cutter

The cutter is the user's **Husky 1-1/4-inch ratcheting PVC cutter**. This jig establishes a repeatable pencil line; the pipe is removed before cutting. There is no blade slot or attachment to the cutter.

Two small heads turn a length of existing PVC into a reusable length gauge. It avoids printing a multi-foot telescoping ruler: the PVC carries the spacing, a trusted metric tape establishes the actual length, and the heads transfer that length repeatedly. Printed telescoping segments would introduce extra joints and would still need calibration. This design improves repeatability; it does not promise perfect absolute accuracy from a printed scale.

**JIG_ZERO** has a 32 mm-long friction sleeve on the reference rail, an open cradle for the workpiece and an end-stop wall. The workpiece end contacts the wall's inner face, which is **X = 0**. A single witness groove on the connecting foot identifies the datum. Both pipe axes are 24 mm above the table and 70 mm apart.

**JIG_MARK** has a 32 mm-long reference sleeve and a 12 mm-long, full circular marking collar. The **collar face nearest the zero stop is the marking plane, also local X = 0**. Its three small grooves distinguish it from the stop. Both bores are 33.5 mm; this tool prints standing on its datum end face, giving circular vertical holes without support. The gate fittings keep their existing horizontal peaked bores. Keep the supplied jig orientation when slicing.

### Set up once for each length

1. Use a straight, clean reference pipe at least **1650 mm long**, preferably an uncut 10-ft stick already on hand. Slip the zero head and then the marking head onto it, both with feet flat on the same surface and their workpiece openings on the same side. Do not cut this reference rail while it is carrying the jig.
2. Put the zero head near one end. With the workpiece absent, measure along the workpiece axis from the **inside contact face of the stop** to the **near face of the marking collar**. Set **389.6 mm** for short cuts or **1560.8 mm** for long cuts. The fronts of the printed parts, their centers and their far faces are not interchangeable measurement references.
3. Support the rail and long stock so they stay straight and level. Mark each head's position on the reference pipe with a fine witness line. Hold the marking head while threading stock through its collar toward the zero stop, so the reference sleeve cannot creep during loading. Press the pipe end gently against the stop.
4. Draw a fine line along the near face of the collar. Rotate the workpiece while keeping its end against the stop to continue the line around its circumference. Use a fine mechanical pencil or fine marker; a broad marker line reduces repeatability.
5. Pull the stock free of the marking collar while holding the head in place. **Remove it from the jig**, then support it and use the Husky cutter on the marked line. Keep the blade perpendicular to the pipe; the jig transfers length but cannot correct cutter drift or a slanted cut.
6. Measure the first finished piece and check that its ends are square. If the finished piece differs from the target, move the marking head by the measured error and repeat a trial. This calibrates the complete tape / pencil / cutter process, including the line edge you consistently cut to. Compare repeated pieces side-by-side and recheck the rail witness lines during the batch.
7. Cut all long pieces, reset and verify the short setting, then cut the short pieces. The reference rail can be one of the budgeted sticks: after the other cuts are complete, remove the heads and transfer lengths from an accepted finished piece to cut the rail itself. No permanently dedicated extra stick is necessary.

Friction retains both heads. The reference sleeves are longer than the workpiece collar to help them stay put, but this is not a positive locking mechanism. Calibration and witness marks matter. Keep a consistent light touch, and support rather than bend long stock. If a tool binds, clean/deburr it and check the printing result rather than forcing it; the accepted design bore remains 33.5 mm.

**Optional DEPTH_30:** push a deburred pipe end into the gauge until it contacts the closed stop. Mark around the open face, exactly 30 mm from the end in CAD. These marks show when the elbow, tee and cross sockets are fully seated. It also provides a small first check of the longer 30 mm engagement before printing all fittings. The gauge has the accepted 33.5 mm bore.

## Three-way tee placement and material savings

The new **TEE** has three sockets and two magnet pads on the side without a socket. Rotate the same part at every outside three-way junction: its missing branch points away from the gate. It replaces **8 crosses on the single** and **12 on the stacked gate**. Crosses remain at all true four-way inner junctions.

A tee uses **{tee['grams']:.2f} g** versus **{cross['grams']:.2f} g** for the cross: **{cross['grams']-tee['grams']:.2f} g and {(cross['minutes']-tee['minutes']):.1f} minutes saved per replacement**. The magnetic pad coordinates, paper coverage, pipe stops and cut lengths remain the same. The assembly maps and node CSVs identify every tee and its rotation.

## Top elbow with guy attachment

**GUY_ELBOW** replaces the two overall top outside elbows. The two bottom corners retain ELBOW. The same top part rotates for left and right; no mirrored file is needed.

The attachment is a **10.5 mm nominal passage** with a printable peaked roof, in a **14 mm-thick, 36 mm-wide eye** rising directly from the thick central elbow body. The hole center is 31 mm behind the paper plane; the complete eye remains behind the paper. It is separate from the magnetic flange and neither changes the PVC bore nor consumes a magnet pocket.

Thread the guy through the rear eye and tie it around that eye. Use a smooth compatible cord or a protected loop at the plastic; bare tensioned metal wire should not saw against the printed edge. The Blender view shows a short threading segment, not a finished knot or a prescribed anchor arrangement. Smooth any rough printed edge before threading. Check hand access and the actual line with one printed top elbow before repeating it.

Top guy lines are newly authorized in this iteration; **internal PVC joints remain friction-only**. Bench-test the eye and watch the pipe engagement marks as tension is introduced. The printed eye has no assigned load rating, and adding it does not establish a wind rating or size the ground anchors/ballast. The tall stacked frame still needs a suitable installation design for the actual surface.

## Full gate parts and costs

| Part | Single | Stacked total | A1 Mini print bounds, mm |
|---|---:|---:|---|
{parttable}

There are **five required gate part types**, with **64 pieces single / 104 stacked**. Workshop tools and optional front pads are additional and excluded from these counts. Your already-printed sleeve counts toward the required 48 or 80. The supplied full production queues assume printing the whole BOM from zero; subtract accepted pieces already in hand when planning batches.

| Configuration | Pieces | PETG kg | Print h | Plate runs | 10-ft PVC / cost | PVC + PETG subtotal |
|---|---:|---:|---:|---:|---|---:|
{costtable}

PVC uses your $6/stick price; PETG assumes $20/kg. Add paper, magnets, adhesive, workshop tooling and ground support. Compared with the previous all-cross version, the new single saves **{previous['gates']['single']['grams']-s['grams']:.2f} g / {(previous['gates']['single']['minutes']-s['minutes'])/60:.2f} hours**, including the added top eyes. The stacked gate saves **{previous['gates']['split_s']['grams']-d['grams']:.2f} g / {(previous['gates']['split_s']['minutes']-d['minutes'])/60:.2f} hours**. Three 1-kg spools cover the single with 10% allowance. The stacked gate needs {d['grams']/1000:.3f} kg nominally; a 10% allowance is {d['grams']*1.1/1000:.3f} kg, slightly above four full spools, so keep spare filament available if budgeting that allowance.

## Production print queue

| Recipe | Single runs | Stacked runs | Pieces/run | g/run | h/run |
|---|---:|---:|---:|---:|---:|
{queuetable}

Each configuration's Print_Queue.csv links to the prepared A1 Mini PETG 3MFs. The sleeve batch contains seven identical sleeves; tail recipes avoid overprinting. New_Parts_Print_Queue.csv lists only the new fitting/tool test jobs. Inspect one tee and one guy elbow first; your accepted sleeve fit is preserved, but the 30 mm-long sockets have not yet been physically checked.

## Cuts, assembly and paper

The two finished PVC lengths remain **389.6 mm** and **1560.8 mm**. Single: **16 short + 8 long**, from eight 10-ft sticks. Stacked: **24 short + 14 long**, from fourteen sticks. Each pipe enters its sockets 30 mm; the stop is 35 mm from the fitting center. Pipe-center spacing is therefore the cut length plus 70 mm.

The stock ledger reserves 10 mm per stick plus 3 mm per cut for conservative trimming/measurement allowance. **The 3 mm is not a saw-kerf instruction for the Husky cutter, and is not added to a finished cut length.** Mark every finished piece from its actual squared starting end. No need to trim an extra 3 mm off between good cuts.

1. Use the jig to mark and verify cuts, then deburr and label the pipes using PVC_Cuts.csv. Mark 30 mm insertion depth at each end. Slide sleeves on before adding fittings.
2. A short pipe gets one sleeve at **194.8 mm** from its cut end. A long pipe gets four at **291.16, 617.32, 943.48 and 1269.64 mm** from the named cut start. Keep all magnetic faces coplanar; Sleeve_Positions.csv supplies every location and rotation.
3. Assemble each horizontal row with four nodes and short / long / short PVC. Single row heights from the paper bottom are **75, 534.6, 2165.4 and 2625 mm**. Bottom ends use ELBOW, top ends GUY_ELBOW, outside three-way nodes TEE, inner four-way nodes CROSS. Both pads on a tee face the outside paper edge.
4. Work flat with the paper faces down. Join successive rows using four vertical pipes at a time, seating them evenly to their insertion marks. Single vertical intervals use short / long / short pipes. Check coplanarity and equal diagonals while assembling.
5. Populate magnet pockets according to the magnet CSV. Front appearance and paper sizes are unchanged: **2700 mm square single**, or **2700 x 4790.4 mm stacked**, **1480.8 mm openings**, and **609.6 mm bands**. All fittings and pipes stay behind paper in the checked front projection.
6. Single paper: two 2700 mm bars and two 1552.8 mm side inserts, all full 609.6 mm roll width. Stacked: three bars and four inserts. Put bars on first, then side inserts overlapping 36 mm at each end. Use **72 pairs / 144 magnets** single, or **116 pairs / 232 magnets** stacked, all 6 x 2 mm. Rear magnet -> 0.4 mm printed skin -> paper -> bare front magnet. Retain the old optional front pads if desired.
7. Thread guys through the two top eyes with the frame accessible. Keep pipe joints fully seated during installation. Footing and anchor details are separate from the face-frame print queue.

## Upgrade from single to stacked

Move the **complete top row** upward, including both GUY_ELBOWs, its two tees, its three pipes and their sleeves. Add a replacement row at y = 2625 mm, with two tees at the outside and two crosses inside. Four new long verticals connect to another new row at y = 4255.8 mm, again with two tees and two crosses. Four new short verticals connect that row to the retained top row at y = 4715.4 mm.

Add **4 tees + 4 crosses + 32 sleeves**, **8 short + 6 long pipes**, and **44 magnet pairs**. Every original pipe, printed gate fitting, sleeve and populated magnet location is reused. The added PVC fits six more sticks. Add one 2700 mm paper bar and two 1552.8 mm side inserts. The two divider rows stay 459.6 mm apart on center, maintaining the shared 609.6 mm face band.

## Verification and sources

The supplied geometry is connected/manifold. Plate bounds, part separation, exact print quantities, support-off slicing, tee-port orientation, magnet-pocket alignment, top-eye placement, paper concealment and reuse on extension were checked. The accepted MAG_SLEEVE STL is unchanged. New tool fit, marking repeatability, deeper socket fit and eye loads await physical tests.

- [Kreg: repeatable cuts using stops](https://learn.kregtool.com/learn/make-repeatable-cuts-using-stops/) describes the general measure-once/repeat-stop approach. This two-head PVC marking jig is an original project design, not a Kreg accessory.
- [Husky 1-1/4-inch ratcheting PVC cutter](https://www.homedepot.com/p/304217581) is the tool-family reference; the jig does not depend on its external dimensions because cutting occurs off the jig.
- [Prusa: modeling with 3D printing in mind](https://help.prusa3d.com/article/modeling-with-3d-printing-in-mind_164135) discusses orientation and print geometry. Supports being disabled and absent from the supplied toolpaths is a digital check, not a physical strength result.

Rebuild using scripts/build_tee_pvc_gate.py, slice_tee_pvc_gate.py, validate_tee_pvc_gate.py and package_tee_pvc_gate.py. Previous iterations remain in their original folders. The bore is fixed at 33.5 mm in this builder; it does not inherit an environment override from an earlier fit study.
'''
(O/'README.md').write_text(readme)
styles=getSampleStyleSheet();styles.add(ParagraphStyle(name='Body',fontName='Helvetica',fontSize=10,leading=14,spaceAfter=8,textColor=HexColor('#17374c')))
story=[]
def para(t,style='Body'):story.append(Paragraph(t,styles[style]))
def pic(n):story.append(Image(str(O/'renders'/f'{n}.png'),width=510,height=340))
def table(rows,widths):
 t=Table([[Paragraph(html.escape(str(x)),styles['Body']) for x in r] for r in rows],colWidths=widths,repeatRows=1)
 t.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('BACKGROUND',(0,0),(-1,0),HexColor('#dce9ee')),('LINEBELOW',(0,0),(-1,-1),.35,HexColor('#a5bbc5')),('BOTTOMPADDING',(0,0),(-1,-1),6)]));story.append(t)
para('33.5 mm accepted / new fittings and measuring tools','Title');pic('05_PART_FAMILY')
para('The successful magnetic sleeve is unchanged. Add a material-saving tee, an elbow with a rear guy eye at each top corner, and a two-head marking jig for the Husky ratcheting cutter.')
para(f'Single gate: {s["grams"]/1000:.3f} kg PETG / {s["minutes"]/60:.1f} hours. Net saving versus the previous version: {previous["gates"]["single"]["grams"]-s["grams"]:.0f} g and {(previous["gates"]["single"]["minutes"]-s["minutes"])/60:.1f} hours. Workshop tools are additional.')
for n,title,cap in [
 ('11_MEASURING_KIT','Print the two-head marking kit',f'JIG_ZERO + JIG_MARK only: {kit["grams"]:.2f} g / {kit["minutes"]/60:.2f} hours. The optional 30 mm depth gauge is a separate job or part of the expanded kit.'),
 ('09_LONG_LENGTH_JIG','A full-length gauge on existing PVC','Set the head datum faces 1560.8 mm apart for long cuts, or 389.6 mm for short cuts. Use a trusted metric tape for the initial setting. Keep the PVC rail straight and supported. Friction retains the heads; watch the witness marks.'),
 ('10_JIG_DATUM_DETAIL','Locate the actual zero face','Butt the pipe gently against the inside end-stop face. Measure from this face to the near face of the marking collar. Hold the marking head while feeding or withdrawing stock. Rotate the stock against the stop to mark around it.'),
 ('08_MEASURING_HEADS','Use the Husky cutter off the jig','Mark first, remove the stock, then cut. Check the finished trial piece and adjust the marking head for the measured error. DEPTH_30, at right, is optional and marks 30 mm socket insertion depth.'),
 ('06_TEE_DETAIL','Replace only the three-way intersections',f'A tee saves {cross["grams"]-tee["grams"]:.2f} g and {cross["minutes"]-tee["minutes"]:.1f} minutes versus a cross. The same tee rotates around all four outside edges. Its absent branch faces outward; its two magnetic pads remain behind the paper.'),
 ('07_GUY_ELBOW','Attach guys to the thick elbow body','The 10.5 mm peaked passage is in a 14 mm-thick eye rooted directly in the central core. Use GUY_ELBOW at the two top outside corners. Thread through the eye, not the magnet arm. Physical load testing and installation sizing remain outstanding.'),
 ('02_SINGLE_FRAME','Single gate with tees and top eyes','2 bottom elbows, 2 top guy elbows, 8 tees, 4 crosses and 48 magnetic sleeves. All pipe bores stay 33.5 mm; the 389.6 / 1560.8 mm cuts and paper dimensions are unchanged.'),
 ('04_SPLIT_S_FRAME','Extend using the same five fitting types','Move the complete top row upward. Add 4 tees, 4 crosses, 32 sleeves, 8 short pipes and 6 long pipes. Every existing pipe, fitting and sleeve is reused.')]:
 story.append(PageBreak());para(title,'Heading1');pic(n);para(cap)
story.append(PageBreak());para('Fabrication quantities and production queue','Heading1')
table([['Part','Single','Stacked','Print bounds mm']]+partrows,[110,45,60,295])
table([['Version','Pieces','PETG kg','Hours','Runs','PVC','Subtotal']]+costrows,[70,43,55,48,40,120,134])
para('PVC + PETG subtotal assumes $6 per 10-ft stick and $20/kg PETG. Paper, magnets, adhesive, workshop tools and ground support are additional. Full queues are from zero; count the accepted sleeve already printed toward the BOM.')
table([['Recipe','Single','Stacked','Pieces/run','g/run','h/run']]+queuerows,[180,55,55,80,70,70])
story.append(PageBreak());para('Measuring and assembly instructions','Heading1')
include=False
for block in readme.split('\n\n'):
 if block.startswith('## Measuring tools'):include=True
 if not include or block.startswith('|'):continue
 if block.startswith('## '):para(block[3:],'Heading2');continue
 if block.startswith('### '):para(block[4:],'Heading3');continue
 block=re.sub(r'\[([^\]]+)\]\(([^)]+)\)',r'\1',block);block=html.escape(block).replace('\n','<br/>');block=re.sub(r'\*\*(.*?)\*\*',r'<b>\1</b>',block);para(block)
def foot(c,d):c.setFont('Helvetica',8);c.drawString(51,22,'FPV PVC gate / tees, guy eyes and measuring tools / 2026-09-18');c.drawRightString(560,22,str(d.page))
SimpleDocTemplate(str(O/'Tee_Gate_and_Measuring_Guide.pdf'),pagesize=(612,792),leftMargin=51,rightMargin=51,topMargin=36,bottomMargin=40).build(story,onFirstPage=foot,onLaterPages=foot)
links=[]
for k in gates:
 links.append(f'<h3>{k}</h3><p>'+ ' · '.join(f'<a href="{k}_{n}.csv">{label}</a>' for n,label in [('Printed_BOM','Parts'),('Print_Queue','Print queue'),('PVC_Cuts','PVC cuts'),('PVC_Stock_Layout','Stock layout'),('Nodes','Nodes'),('Sleeve_Positions','Sleeve positions'),('Magnet_Positions','Magnets'),('Paper_Cuts','Paper cuts')])+f' · <a href="{k}_Assembly_Map.svg">Assembly map</a> · <a href="{k}_Paper_and_Magnet_Map.svg">Paper map</a></p>')
figs=''.join(f'<figure><a href="renders/{p.name}"><img src="renders/{p.name}" alt="{p.stem}"></a></figure>' for p in sorted((O/'renders').glob('*.png')))
rows=''.join('<tr>'+''.join(f'<td>{html.escape(str(x))}</td>' for x in r)+'</tr>' for r in costrows)
pr=''.join('<tr>'+''.join(f'<td>{html.escape(str(x))}</td>' for x in r)+'</tr>' for r in partrows)
newlinks=''.join(f'<li><a href="sliced/{n}/{n}_A1Mini_PETG.3mf">{n}</a> — {sl[n]["grams"]:.2f} g / {sl[n]["minutes"]/60:.2f} hours</li>' for n in newplates)
(O/'index.html').write_text(f'''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>33.5 mm PVC: tees, guy eyes and measuring jig</title><style>body{{font:17px/1.6 system-ui;max-width:1150px;margin:35px auto;padding:0 24px;color:#17374c;background:#f4f7f9}}img{{width:100%}}figure{{margin:24px 0}}a{{color:#006f91}}aside{{padding:20px;background:#e1edf2}}table{{width:100%;border-collapse:collapse}}td,th{{padding:10px;border-bottom:1px solid #bcced6;text-align:left}}h1{{line-height:1.2}}</style><h1>Keep the fit. Save material. Measure repeated cuts.</h1><p>Your accepted 33.5 mm sleeve is unchanged. Tees replace unused fourth branches. Two top elbows gain integral rear guy eyes. A small two-head jig uses existing PVC as a reference rail for marking cuts with the Husky ratcheting cutter.</p><p><a href="Tee_PVC_Gate.blend">Blender model</a> · <a href="Tee_Gate_and_Measuring_Guide.pdf">Measuring and assembly PDF</a> · <a href="README.md">Full guide</a> · <a href="Tee_PVC_Gate_Kit.zip">Download kit</a></p><aside><b>New print jobs</b><ul>{newlinks}</ul><p>The standard measuring kit has only two heads. Set it with a metric tape, mark the pipe, then remove the pipe to cut. The 30 mm insertion gauge is optional.</p></aside><table><tr><th>Part</th><th>Single</th><th>Stacked</th><th>Print bounds mm</th></tr>{pr}</table><table><tr><th>Configuration</th><th>Pieces</th><th>PETG kg</th><th>Hours</th><th>Runs</th><th>$6 PVC sticks</th><th>Subtotal*</th></tr>{rows}</table><p>*PVC + PETG at $20/kg. Add paper, magnets, adhesive, tooling and ground support. Net single-gate savings versus the all-cross version: {previous['gates']['single']['grams']-s['grams']:.0f} g and {(previous['gates']['single']['minutes']-s['minutes'])/60:.1f} hours, including the new top eyes.</p>{figs}<h2>Fabrication ledgers</h2>{''.join(links)}<p><a href="New_Parts_Print_Queue.csv">New print jobs</a> · <a href="Workshop_Tools.csv">Workshop tools</a> · <a href="Upgrade_Additional_Parts.csv">Upgrade parts</a> · <a href="Upgrade_Additional_PVC.csv">Upgrade PVC</a> · <a href="print_checks.json">Digital checks</a></p><p>All parts fit the A1 Mini and all supplied plates slice without supports or warnings. The longer sockets, new tools and guy eyes need physical testing. The eye has no assigned load rating. No printer job has been submitted.</p></html>''')
with zipfile.ZipFile(O/'Tee_PVC_Gate_Kit.zip','w',zipfile.ZIP_DEFLATED) as z:
 for p in O.rglob('*'):
  if not p.is_file() or p.suffix in ['.zip','.log','.gcode','.blend1']:continue
  if 'sliced' in p.parts and p.suffix!='.3mf':continue
  z.write(p,Path('tee_pvc_gate')/p.relative_to(O))
print('PACKAGED',s['grams'],s['minutes'],d['grams'],d['minutes'],'measuring kit',kit)

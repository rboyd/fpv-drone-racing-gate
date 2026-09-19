"""Publish the friction-fit, three-type rectangular PVC gate iteration."""
from pathlib import Path
import json,csv,html,re,zipfile,collections
from reportlab.platypus import SimpleDocTemplate,Paragraph,Image,Table,TableStyle,PageBreak,Spacer
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib.colors import HexColor
ROOT=Path(__file__).resolve().parents[1];O=ROOT/'output/orthogonal_pvc_gate'
b=json.loads((O/'BOM.json').read_text());v=json.loads((O/'print_checks.json').read_text())
parts={p['code']:p for p in b['parts']};gates=b['gates'];stats=v['gates'];s=stats['single'];d=stats['split_s'];fit=v['slices']['FIRST_FRICTION_FIT'];second=v['slices']['CROSS_AND_SLEEVE']
def csvout(name,rows):
 with (O/name).open('w') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
for kind,g in gates.items():
 csvout(f'{kind}_Printed_BOM.csv',[{'part':c,'quantity':n,'description':parts[c]['description'],'print_bounds_mm':' x '.join(map(str,parts[c]['print_bounds_mm']))} for c,n in g['counts'].items()])
 csvout(f'{kind}_PVC_Cuts.csv',[{'piece':i+1,'name':e['name'],'from_node':e['a'],'to_node':e['b'],'length_mm':e['length_mm']} for i,e in enumerate(g['edges'])])
 csvout(f'{kind}_PVC_Stock_Layout.csv',[{'stock':r['stock'],'cut_order':i+1,'name':e['name'],'length_mm':e['length_mm'],'kerf_mm':3,'reserved_end_allowance_mm':10} for r in g['stock_plan'] for i,e in enumerate(r['cuts'])])
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
partrows=[[c,gates['single']['counts'][c],gates['split_s']['counts'][c],' x '.join(map(str,parts[c]['print_bounds_mm']))] for c in gates['single']['counts']]
parttable='\n'.join('| '+' | '.join(map(str,r))+' |' for r in partrows)
costrows=[[k,q['printed_pieces'],f'{q["grams"]/1000:.3f}',f'{q["minutes"]/60:.1f}',q['plate_runs'],f'{q["pipe_sticks"]} / ${q["pipe_cost_usd"]}',f'${q["frame_PVC_plus_PETG_usd"]:.2f}'] for k,q in stats.items()]
costtable='\n'.join('| '+' | '.join(map(str,r))+' |' for r in costrows)
queues='\n'.join(f'| {n} | {gates["single"]["print_queue"].get(n,0)} | {gates["split_s"]["print_queue"].get(n,0)} | {len(b["plates"][n])} | {v["slices"][n]["grams"]:.2f} | {v["slices"][n]["minutes"]/60:.2f} |' for n in dict.fromkeys([*gates['single']['print_queue'],*gates['split_s']['print_queue']]))
readme=f'''# Three-type PVC gate / friction-fit iteration

The gate now uses **one elbow, one cross and one magnetic sleeve design**. All pipe connections and sleeve positioning use friction. Straight PVC links join the inner and outer perimeters into a rectangular grid. The earlier corded iteration remains in ../pvc_paper_gate for comparison.

[Blender model](Orthogonal_PVC_Gate.blend) · [Visual index](index.html) · [Assembly PDF](Orthogonal_Gate_Assembly.pdf) · [Complete kit](Orthogonal_PVC_Gate_Kit.zip)

## Required parts and actual slicing estimates

| Part | Single gate | Two-level total | Print bounds, mm |
|---|---:|---:|---|
{parttable}

There are **3 unique required printed types**. Fit gauges are tooling. PAPER_PAD is optional. Quantities above exclude both. The same cross serves four-way and three-way junctions; leave an unused socket empty. Elbows are only at the four overall outside corners. Inner opening corners use crosses because their other two ports connect directly to the outer perimeter.

| Configuration | Printed pieces | PETG kg | Print hours | Plate runs | 10-ft PVC sticks / cost | PVC + PETG subtotal |
|---|---:|---:|---:|---:|---|---:|
{costtable}

Your PVC price is $6 per 10-ft stick. PETG is an assumed $20/kg, not a supplier quote. Subtotals cover the face skeleton only; magnets, paper, adhesive and a ground-support system are additional. Print estimates come from local Bambu Studio slicing: A1 Mini, 0.4 mm nozzle, 0.20 mm layers, Generic PETG, four walls, 20% infill, no supports, no brim. Failed prints and manual work are not included. Three 1-kg spools cover the single with 10% allowance; the double requires five spools ({d['grams']*1.1/1000:.3f} kg with 10% allowance).

This simplifies assembly and inventory but **does not lower the modeled material or printer time versus the previous corded version**. That single used 5 types, 62 pieces, 1.759 kg, 71.0 hours and six PVC sticks ($71.17 PVC + PETG). This single uses 3 types, 64 pieces, {s['grams']/1000:.3f} kg and {s['minutes']/60:.1f} hours (${s['frame_PVC_plus_PETG_usd']:.2f}). Universal crosses print unused sockets at the perimeter, and straight seam links consume more PVC. In return there is no tying, cord routing, cord tensioning or special seam saddle.

## Geometry and connection details

Single outside dimensions: **2700 x 2700 mm**. Stacked: **2700 x 4790.4 mm**, before a base. Each opening is **1480.8 x 1480.8 mm**. All paper bands, including the shared divider, are **609.6 mm / 24 inches** wide.

The PVC axes sit **75 mm inside the paper boundary** and **24 mm behind its face**. Opposing pipe axes across a band are 459.6 mm apart. Each socket mouth is 65 mm from its fitting center, leaving the unused perimeter socket behind paper with 10 mm to spare. Pad centers offset 57 mm from pipe axes put magnets 18 mm inside the paper edges. The model checks every printed vertex in front projection and every front magnet center against the paper rectangles. PVC follows the same concealed grid. Structure may be visible from an oblique view.

Socket engagement is **30 mm**, against a stop **35 mm from the fitting center**. Nominal pipe OD is 33.4 mm. The provisional friction bore is **{b['bore_trial_mm']:.1f} mm**; printed fit must be selected using real pipe. Nominal socket walls are 4 mm, central webs are 32 mm wide and 12 mm thick, and magnetic arms have 20 mm-wide continuous 3 mm flanges with thicker roots. The peaked roof is retained for support-free horizontal printing. Magnet windows alone retain the requested 0.4 mm skin.

MAG_SLEEVE engages 16 mm of pipe. Its friction fit locates the magnet and resists rotation; it has no separate fastener. Leave accepted sleeves on their marked pipes during transport. All three production meshes fit the A1 Mini. The largest is CROSS at 136.627 x 136.627 x 53.345 mm; supplied plates maintain at least 5 mm bed margin.

## First print and fit test

[FIRST_FRICTION_FIT_A1Mini_PETG.3mf](sliced/FIRST_FRICTION_FIT/FIRST_FRICTION_FIT_A1Mini_PETG.3mf): **{fit['grams']:.2f} g / {fit['minutes']/60:.2f} hours**. Five pieces: one 33.5 mm-bore ELBOW, full 30 mm-long FIT_333 / FIT_335 / FIT_337 coupons, and one optional PAPER_PAD. The three samples are 33.3 / 33.5 / 33.7 mm bores, ordered from front to rear on the right side of the plate. Label them before removing them. The coupons have no end stop; test 30 mm engagement. Their shape and print orientation match the sockets.

1. Measure and deburr an actual pipe offcut. Test each coupon by hand; choose the fit that seats the full 30 mm and releases deliberately while resisting pull-out and rotation. Do not hammer a tight sample onto the pipe. If none meets that behavior, revise the bore rather than accepting a loose or forced fit.
2. Test both elbow sockets to their stops, with a 30 mm insertion mark on each pipe. Check that the elbow stays square and its paper face stays flat. Repeat fitting and release at least 20 times; check for cracking, whitening, increasing looseness and movement past witness marks.
3. The supplied elbow and production files use 33.5 mm. If another sample fits better, regenerate with PVC_FIT_BORE set to that diameter and re-slice before production. Do not scale an STL; that also changes centers, magnet pockets and cut lengths.
4. Then print [CROSS_AND_SLEEVE](sliced/CROSS_AND_SLEEVE/CROSS_AND_SLEEVE_A1Mini_PETG.3mf): **{second['grams']:.2f} g / {second['minutes']/60:.2f} hours**. It tests all four socket directions and the shorter sleeve. A coupon result alone does not prove sleeve grip.
5. For a two-foot band demonstration, join the elbow to the cross with one **389.6 mm** pipe and place the sleeve at **194.8 mm from its cut end**. Orient both printed faces into the same plane. The elbow's outward pad and the cross's opposite-side pad span the paper band with 18 mm edge margins. Lay a 609.6 mm-wide paper strip over them and mark the 18 mm margins. Use six magnets for three grip sites, adding a short perpendicular pipe offcut to each fitting to test square alignment.
6. Bond rear magnets after checking polarity; let the adhesive cure. Test magnetic grip with the real paper, both a bare front magnet and the optional front pad. Pull/rotate the sleeve, flex the paper gently and repeat assembly. After that passes, build one short square grid cell (four 389.6 mm pipes, one elbow, three crosses) flat and check racking and joint withdrawal before producing the complete gate.

The fit and handling tests above are prototype checks, not a rated wind/load test. The first two test plates are separate from the production queue below; accepted production pieces from them can count toward the final BOM.

## Full production queue

| Recipe | Single runs | Double runs | Pieces/run | g/run | h/run |
|---|---:|---:|---:|---:|---:|
{queues}

Each CSV queue links to the corresponding prepared PETG 3MF. BATCH_MAG_SLEEVE holds seven identical sleeves; it is one part type. The six- and three-piece tails avoid overprinting. All plates passed the bed-clearance, non-overlap and support-off slicing checks. Open prepared 3MFs as projects and confirm your actual filament profile before printing. No job has been sent to a printer.

## PVC cuts and assembly

Only **two finished pipe lengths** are used: **389.6 mm** and **1560.8 mm**. The single needs **16 short + 8 long**; the double needs **24 short + 14 long**. Their respective center spacings are 459.6 and 1630.8 mm, because the two stop offsets add 70 mm. The longest loose pipe is 1.561 m.

The stock ledgers reserve 10 mm total end allowance per stick and 3 mm kerf per cut. Two long pieces cannot fit one 3048 mm stick, so eight long pieces require at least eight sticks; fourteen require fourteen. All short pieces fit alongside those long pieces. Label cuts using PVC_Cuts.csv; node coordinates and Assembly_Map.svg use the front view, measured from the bottom-left paper corner.

1. Print and qualify the selected fit, then cut, deburr and label all PVC. Mark 30 mm engagement at both ends. Mark sleeve stations from Sleeve_Positions.csv before covering the cut starts with fittings.
2. Slide **one sleeve onto each short pipe**, centered at 194.8 mm from its cut start. Put **four sleeves on each long pipe** at **291.16, 617.32, 943.48 and 1269.64 mm** from the cut start. Rotate them to the direction shown in Blender; their flat paper faces must be coplanar with the fitting faces. The sleeve positions are clear of every socket.
3. Work on a flat surface with all paper-facing surfaces down. Build each horizontal row from four nodes and three pipes in **short / long / short** order. The single has four rows at y = 75, 534.6, 2165.4 and 2625 mm. Only the ends of its bottom/top row use elbows; every other node is a cross. A node's unused cross socket simply stays empty.
4. Place four vertical pipes into each row, then press the next complete row onto them together, keeping the mating sockets aligned. Single vertical gaps use **short / long / short** pipes, from bottom to top. Seat all four connections evenly to their marks; avoid levering one partially engaged socket to close another. Check equal diagonals and coplanar paper pads as each row goes on.
5. Populate only the magnet pockets shown by Magnet_Positions.csv. The cross has four available pads for symmetry, but not all are used at every node. A straightedge across the fixed fitting pads helps clock the sliding sleeves; mark accepted positions on the pipe for repeat assembly.
6. Install the paper as described below. For transport, remove the paper and separate rows/long members as needed, pulling at socket bodies. Leave sleeves on their labeled pipes. Fully assembled horizontal rows are about 2.7 m wide, so remove an end stub or separate at an inner cross to remain within the earlier approximately 2.15 m transport size.

## Paper and magnets

Use untrimmed 609.6 mm roll width. Single: **two 2700 mm horizontal bars and two 1552.8 mm side inserts**. Double: **three 2700 mm bars and four 1552.8 mm inserts**. Each side insert overlaps a horizontal bar by **36 mm at each end**. Consumption is 8.5056 m per single or 14.3112 m per double: three singles or two doubles from a 100-ft roll, before cutting waste.

Lay horizontal bars first, then side inserts. Align paper edges 18 mm beyond the corresponding magnet centers. The straight short PVC links carry magnets along the overlap seams, so no suspended seam parts are needed. Use **72 magnet pairs / 144 magnets** for a single, or **116 pairs / 232 magnets** for a double, all 6 mm diameter x 2 mm thick. Long-span sleeve spacing is 326.16 mm; grip at that spacing needs testing with the actual roll.

The stack is **rear magnet -> 0.4 mm frame plastic -> paper -> bare front magnet**. Frame pockets remain 6.3 mm diameter and are rear-loaded. Secure rear magnets with a compatible adhesive; the pocket clearance is not a guaranteed press fit. Check polarity before bonding. Only populate selected pockets. The bare front magnets align directly with the fixed rear magnets. The existing PAPER_PAD is an optional handle/protector around a front magnet; it adds another 0.4 mm skin and is excluded from the BOM, mass and time totals.

## Extend to the two-level gate

Reuse **every existing pipe without cutting**, all 48 sleeves, all 12 crosses and all four elbows. Add **8 CROSS + 32 MAG_SLEEVE**, **8 short + 6 long PVC cuts**, and **44 magnet pairs / 88 magnets**. The additional PVC needs six more 10-ft sticks. Add one 2700 mm paper bar and two 1552.8 mm side inserts.

Lay the single frame flat and remove its paper. Detach its complete top horizontal row (both elbows, both crosses, all three pipes and their sleeves) from the four short verticals below it. Move that complete row upward to the new top height, y = 4715.4 mm. This preserves its populated magnet pads and sleeve directions together; label its new node positions using the double map.

Build a replacement all-cross row at the old top height, y = 2625 mm, using four new crosses and short / long / short pipes. It becomes the upper row of the shared divider. Add four long verticals to a second new all-cross row at y = 4255.8 mm, also using four new crosses and short / long / short horizontal pipes. Add four short verticals above it and seat the retained top row onto them. This accounts for all eight additional crosses, six long pipes and eight short pipes. No special divider fitting is required.

The divider's two pipe rows are y = 2165.4 and 2625 mm: **459.6 mm axis spacing**, supporting the same 609.6 mm band as every other border. Use the double assembly and magnet maps when relocating/populating magnets at the former top edge.

## What is checked and what remains

Digital checks cover connected manifold masters, actual A1 Mini placements, no overlapping plate parts, no generated supports or slicer warnings, exact queue quantities, socket-free sleeve positions, backing-pocket alignment, front concealment, orthogonal PVC, and reuse of all single-height pipe lengths on extension. Nine Blender scenes show both finished faces, both PVC frames, the three part types, connections, magnetic stack, first test plate and shared divider.

This is a **friction-fit face-frame prototype**. Actual pull-out, sleeve rotation, PETG wear, paper grip and frame racking still require physical tests. Feet and ground restraint for soil or hard surfaces have not been sized in this iteration; the 4.79 m frame is not yet a qualified freestanding outdoor obstacle. No cord is included in this design.

## References and regeneration

- [FORMUFIT PVC sizing](https://formufit.com/pages/pvc-101) explains nominal pipe size versus OD; nominal 1-inch PVC is approximately 1.315 inches outside diameter. Measure the actual pipe used for this print.
- [Prusa modeling guidance](https://help.prusa3d.com/article/modeling-with-3d-printing-in-mind_164135) covers print orientation, overhangs and tolerances. The peaked sockets and proposed clearances are this project's prototype geometry.

Regenerate with scripts/build_orthogonal_pvc_gate.py in Blender, then scripts/slice_orthogonal_pvc_gate.py, scripts/validate_orthogonal_pvc_gate.py and scripts/package_orthogonal_pvc_gate.py. Set PVC_FIT_BORE on the Blender build command to change the bore. The package script uses ReportLab. A changed bore requires rebuilding and re-slicing; the supplied files currently use {b['bore_trial_mm']:.1f} mm.
'''
(O/'README.md').write_text(readme)
styles=getSampleStyleSheet();styles.add(ParagraphStyle(name='Body',fontName='Helvetica',fontSize=10,leading=14,spaceAfter=8,textColor=HexColor('#17374c')))
story=[]
def para(t,style='Body'):story.append(Paragraph(t,styles[style]))
def pic(n):story.append(Image(str(O/'renders'/f'{n}.png'),width=510,height=340))
def table(rows,widths):
 t=Table([[Paragraph(html.escape(str(x)),styles['Body']) for x in r] for r in rows],colWidths=widths,repeatRows=1)
 t.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('BACKGROUND',(0,0),(-1,0),HexColor('#dce9ee')),('LINEBELOW',(0,0),(-1,-1),.35,HexColor('#a5bbc5')),('BOTTOMPADDING',(0,0),(-1,-1),6)]));story.append(t)
para('Three-type PVC gate / friction fit','Title');pic('01_SINGLE_FRONT')
para(f'Single: 4 elbows, 12 crosses, 48 magnetic sleeves. {s["grams"]/1000:.3f} kg PETG / {s["minutes"]/60:.1f} printer-hours / eight $6 PVC sticks. PVC + PETG subtotal ${s["frame_PVC_plus_PETG_usd"]:.2f} at $20/kg; paper, magnets and ground support additional.')
para('Equal 609.6 mm paper bands; 2700 mm square outside and 1480.8 mm opening. All joining and sleeve location use friction. First confirm the bore with the actual pipe. The following views and instructions cover the single and its two-level extension.')
for n,title,cap in [
 ('05_THREE_PART_TYPES','Three required printed types','Elbow only at the four overall outside corners. Universal cross at every other junction; unused sockets remain empty. One sleeve design holds every intermediate magnet. Front pads are optional.'),
 ('08_FIRST_FRICTION_FIT','First test plate',f'Five pieces / {fit["grams"]:.2f} g / {fit["minutes"]/60:.2f} hours. Label the three full-length coupons before removing them: 33.3, 33.5 and 33.7 mm from front to rear. The included elbow uses 33.5 mm.'),
 ('06_ELBOW_CROSS_DETAIL','Straight sockets / one square band','Pipe ends engage 30 mm. Stops are 35 mm from node centers. A 389.6 mm pipe gives 459.6 mm center spacing across a 609.6 mm paper band. Both printed faces must be coplanar.'),
 ('07_SLEEVE_AND_PAPER','Positioning and paper attachment','Thread sleeves before end fittings. Clock flat faces against a straightedge. Rear magnet / 0.4 mm plastic / paper / bare front magnet. Magnet centers are 18 mm from paper edges. Test rotation resistance on actual PVC.'),
 ('02_SINGLE_FRAME','Single frame / row-by-row assembly','Four horizontal rows, each with short / long / short PVC. Build each row first, then engage four vertical members and the next row together. Work flat and seat evenly against the 30 mm insertion marks.'),
 ('03_SPLIT_S_FRONT','Same borders / two openings','2700 x 4790.4 mm before feet. The one shared middle band remains 609.6 mm wide. Paper and magnets cover the complete front projection.'),
 ('04_SPLIT_S_FRAME','Reuse the single gate',f'Add 8 crosses, 32 sleeves, 8 short and 6 long pipes. Move the complete top row upward. Double total: {d["grams"]/1000:.3f} kg PETG / {d["minutes"]/60:.1f} hours / fourteen PVC sticks. All original pipe lengths are reused.'),
 ('09_SHARED_MIDDLE','Shared divider / standard crosses','Move the old top row to the new top. Two new all-cross rows form the upper divider edge and the upper opening top edge. Divider axis heights are 2165.4 and 2625 mm from the paper bottom.')]:
 story.append(PageBreak());para(title,'Heading1');pic(n);para(cap)
story.append(PageBreak());para('Fabrication quantities','Heading1');table([['Part','Single','Double','Print bounds mm']]+partrows,[110,45,45,310])
table([['Configuration','Pieces','PETG kg','Hours','Runs','PVC','Subtotal']]+costrows,[80,44,57,48,42,114,125])
para('The three-type grid costs more material and print time than the prior five-type corded design. Its benefit is simpler assembly and inventory. Counts exclude optional front pads and prototype tooling. Ground support is separate. See the CSV ledgers for exact labeled cuts and plate recipes.')
table([['Recipe','Single runs','Double runs','Pieces/run','g/run','h/run']]+[[n,gates['single']['print_queue'].get(n,0),gates['split_s']['print_queue'].get(n,0),len(b['plates'][n]),v['slices'][n]['grams'],round(v['slices'][n]['minutes']/60,2)] for n in dict.fromkeys([*gates['single']['print_queue'],*gates['split_s']['print_queue']])],[180,65,65,70,65,65])
story.append(PageBreak());para('Assembly and test instructions','Heading1')
include=False
for block in readme.split('\n\n'):
 if block.startswith('## First print'):include=True
 if not include or block.startswith('|'):continue
 if block.startswith('## '):para(block[3:],'Heading2');continue
 block=re.sub(r'\[([^\]]+)\]\(([^)]+)\)',r'\1',block);block=html.escape(block).replace('\n','<br/>');block=re.sub(r'\*\*(.*?)\*\*',r'<b>\1</b>',block);para(block)
def foot(c,d):c.setFont('Helvetica',8);c.drawString(51,22,'Friction-fit PVC gate / fabrication prototype / 2026-09-17');c.drawRightString(560,22,str(d.page))
SimpleDocTemplate(str(O/'Orthogonal_Gate_Assembly.pdf'),pagesize=(612,792),leftMargin=51,rightMargin=51,topMargin=36,bottomMargin=40).build(story,onFirstPage=foot,onLaterPages=foot)
links=[]
for k in gates:
 links.append(f'<h3>{k}</h3><p>'+ ' · '.join(f'<a href="{k}_{n}.csv">{label}</a>' for n,label in [('Printed_BOM','Parts'),('Print_Queue','Print queue'),('PVC_Cuts','PVC cuts'),('PVC_Stock_Layout','Stock layout'),('Nodes','Nodes'),('Sleeve_Positions','Sleeve positions'),('Magnet_Positions','Magnets'),('Paper_Cuts','Paper cuts')])+f' · <a href="{k}_Assembly_Map.svg">Assembly map</a> · <a href="{k}_Paper_and_Magnet_Map.svg">Paper map</a></p>')
figs=''.join(f'<figure><a href="renders/{p.name}"><img src="renders/{p.name}" alt="{p.stem}"></a></figure>' for p in sorted((O/'renders').glob('*.png')))
rows=''.join('<tr>'+''.join(f'<td>{html.escape(str(x))}</td>' for x in r)+'</tr>' for r in costrows)
pr=''.join('<tr>'+''.join(f'<td>{html.escape(str(x))}</td>' for x in r)+'</tr>' for r in partrows)
(O/'index.html').write_text(f'''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Three-type friction-fit PVC gate</title><style>body{{font:17px/1.6 system-ui;max-width:1150px;margin:35px auto;padding:0 24px;color:#17374c;background:#f4f7f9}}img{{width:100%}}figure{{margin:24px 0}}a{{color:#006f91}}aside{{padding:20px;background:#e1edf2}}table{{width:100%;border-collapse:collapse}}td,th{{padding:10px;border-bottom:1px solid #bcced6;text-align:left}}h1{{line-height:1.2}}</style><h1>One elbow. One cross. One magnetic sleeve.</h1><p>A friction-fit rectangular grid with equal 609.6 mm paper bands, extending to two stacked openings using the same three printed types.</p><p><a href="Orthogonal_PVC_Gate.blend">Blender model</a> · <a href="Orthogonal_Gate_Assembly.pdf">Assembly PDF</a> · <a href="README.md">Full guide</a> · <a href="Orthogonal_PVC_Gate_Kit.zip">Download kit</a></p><table><tr><th>Part</th><th>Single</th><th>Double</th><th>Print bounds mm</th></tr>{pr}</table><table><tr><th>Configuration</th><th>Pieces</th><th>PETG kg</th><th>Hours</th><th>Runs</th><th>$6 PVC sticks</th><th>Subtotal*</th></tr>{rows}</table><p>*PVC + PETG at $20/kg. Add paper, magnets, adhesive and ground support. Actual A1 Mini slice estimates; optional front pads and test tooling excluded. Simpler assembly, but more material and printer time than the preceding corded design.</p><aside><b>First print:</b> <a href="sliced/FIRST_FRICTION_FIT/FIRST_FRICTION_FIT_A1Mini_PETG.3mf">Friction-fit test plate</a> — {fit['grams']:.2f} g / {fit['minutes']/60:.2f} hours. One elbow, three full-length bore samples and an optional front pad. Then test <a href="sliced/CROSS_AND_SLEEVE/CROSS_AND_SLEEVE_A1Mini_PETG.3mf">one cross and sleeve</a>. Supplied production bore: 33.5 mm; choose by physical fit, then regenerate if needed.</aside>{figs}<h2>Fabrication files</h2>{''.join(links)}<p><a href="Upgrade_Additional_Parts.csv">Upgrade parts</a> · <a href="Upgrade_Additional_PVC.csv">Upgrade PVC</a> · <a href="Comparison.csv">Comparison</a> · <a href="print_checks.json">Digital checks</a></p><p>All provided plates fit the A1 Mini and slice without supports or warnings. Actual friction, wear and paper grip remain to be tested. This iteration models the face frame; ground support is not yet sized for either surface. No printer job has been submitted.</p></html>''')
with zipfile.ZipFile(O/'Orthogonal_PVC_Gate_Kit.zip','w',zipfile.ZIP_DEFLATED) as z:
 for p in O.rglob('*'):
  if not p.is_file() or p.suffix in ['.zip','.log','.gcode','.blend1']:continue
  if 'sliced' in p.parts and p.suffix!='.3mf':continue
  z.write(p,Path('orthogonal_pvc_gate')/p.relative_to(O))
print('PACKAGED',s['grams'],s['minutes'],d['grams'],d['minutes'])

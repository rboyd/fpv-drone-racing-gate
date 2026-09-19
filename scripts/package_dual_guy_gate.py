"""Package the diagonal dual-guy elbow iteration and its gate integration."""
from pathlib import Path
import json,csv,html,re,zipfile
from reportlab.platypus import SimpleDocTemplate,Paragraph,Image,Table,TableStyle,PageBreak
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib.colors import HexColor
ROOT=Path(__file__).resolve().parents[1];O=ROOT/'output/dual_guy_gate'
b=json.loads((O/'BOM.json').read_text());v=json.loads((O/'print_checks.json').read_text());gates=b['gates'];stats=v['gates'];s=stats['single'];d=stats['split_s']
parts={p['code']:p for p in b['parts']};part=parts['DUAL_GUY_ELBOW'];estimate=v['slices']['ONE_DUAL_GUY_ELBOW']
previous=json.loads((ROOT/'output/tee_pvc_gate/print_checks.json').read_text());old=previous['slices']['ONE_GUY_ELBOW']
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
partrows=[[c,gates['single']['counts'][c],gates['split_s']['counts'][c]] for c in b['production_codes']]
parttable='\n'.join('| '+' | '.join(map(str,r))+' |' for r in partrows)
queuerows=[[n,gates['single']['print_queue'].get(n,0),gates['split_s']['print_queue'].get(n,0),v['slices'][n]['grams'],round(v['slices'][n]['minutes']/60,2)] for n in dict.fromkeys([*gates['single']['print_queue'],*gates['split_s']['print_queue']])]
queuetable='\n'.join('| '+' | '.join(map(str,r))+' |' for r in queuerows)
readme=f'''# Dual front/rear guy elbow / diagonal ear

The previous PVC/tee design and workshop status were documented and committed as **6a7fb47** before this revision. That record includes the physically accepted 33.5 mm sleeve fit, the selected ONE_TEE PETG job opened in Bambu Studio, and the preference for checked PVC master pieces instead of printing measuring tools first. Tee completion has not been reported.

This revision replaces only the two top GUY_ELBOWs with **DUAL_GUY_ELBOW**. It adds simultaneous independent front and rear tie-downs, and moves the single corner magnet to one top-edge and one side-edge holder. All other production STLs are byte-for-byte identical to the committed tee iteration. PVC bores remain **33.5 mm**, with **30 mm engagement** and **35 mm center-to-stop**.

[Blender model](Dual_Guy_Gate.blend) · [Visual index](index.html) · [Assembly/test PDF](Dual_Guy_Assembly.pdf) · [Kit](Dual_Guy_Gate_Kit.zip)

## First print

[ONE_DUAL_GUY_ELBOW_A1Mini_PETG.3mf](sliced/ONE_DUAL_GUY_ELBOW/ONE_DUAL_GUY_ELBOW_A1Mini_PETG.3mf): **{estimate['grams']:.2f} g PETG / {estimate['minutes']/60:.2f} hours**. One required top corner, with both eyes and both magnet holders. Print one and test before making the second. No new job was opened or submitted, so the previously selected tee job is not replaced in Bambu Studio.

Bounds are **168.614 x 168.614 x 53.345 mm**. The supplied A1 Mini layout places it at X=5, Y=5, leaving at least 5 mm bed margin. Use the supplied flat-face-down orientation, 0.4 mm nozzle, 0.20 mm layers, four walls, 20% infill and Generic PETG. All supplied recipes slice without supports or warnings. The PVC sockets retain the accepted peaked roofs; both tie-down holes print vertically through the flat ear.

The old guy elbow used {old['grams']:.2f} g / {old['minutes']/60:.2f} hours. Each replacement adds **{estimate['grams']-old['grams']:.2f} g / {estimate['minutes']-old['minutes']:.2f} minutes**. Two replacements add **{2*(estimate['grams']-old['grams']):.2f} g / {2*(estimate['minutes']-old['minutes'])/60:.2f} hours** per gate, whether single or stacked.

## What changed

A **32 mm-wide, 14 mm-thick diagonal arm** runs from the central elbow body toward the outside paper corner. A sloped root rib rises to 28 mm behind the paper plane. The arm ends in a rounded ear containing **two 10.5 mm through-holes**, 18 mm apart on center. Each hole has a **0.8 mm, 45-degree chamfer** on both entrances, giving a 12.1 mm mouth. The straight bores have 8 mm outer edge material and 7.5 mm between holes; at the chamfer mouths these reduce to 7.2 mm and 5.9 mm respectively.

One hole takes the **front guy**, the other the **rear guy**. Each cord gets its own eye and attachment loop, so both can remain attached and be adjusted independently. The through-hole axes point front-to-back through the ear. There is no hidden rear-only eye requiring the front line to pass through paper. The same part rotates into both top corners; no mirrored file is needed.

The hole mouths lie completely beyond the paper outline. The ear projects up to **28.614 mm past the adjacent top/side edges**. This is an intentional visible exception to the earlier paper-only front: the paper remains uncut, and the PVC, body and magnet pads remain concealed behind it. Paper dimensions stay **2700 mm square single**, or **2700 x 4790.4 mm stacked**. Including the two ears, the hardware reaches about **2757.2 mm wide** and **2728.6 / 4819.0 mm high**, before feet.

The diagonal ear occupies the old corner-magnet direction. Its replacement pads lie along the **top and side edges**, each **18 mm inside the edge and 90 mm from the paper corner**. Both keep the existing 6.3 mm rear magnet pocket and **0.4 mm frame-side plastic skin**. Use the same 6 x 2 mm magnets. Optional front paper pads remain optional and are available in the earlier kit.

## Fit and thread both lines

1. Print one DUAL_GUY_ELBOW. Inspect the 0.4 mm magnetic skins, two vertical through-holes, diagonal arm and root rib. Clear loose strings and smooth any rough entrance edges without enlarging the PVC bores.
2. Fit two actual PVC offcuts and seat both sockets the full 30 mm, using insertion witness marks. The design bore stays 33.5 mm; the longer socket fit still needs its first physical check despite the successful sleeve print.
3. Thread a separate attachment loop through each eye and around its adjacent outside rim. Lead one guy toward the front of the gate and the other toward the rear. The orange/teal Blender lines show this routing; they are schematic loops, not a knot prescription. Choose appropriate secure knots/loops for the actual line and confirm knot clearance with both fitted simultaneously.
4. Use smooth cord or a protected connection at the plastic. Bare metal wire should not abrade directly against a printed edge. The modeled line diameter is **3 mm**; test the actual chosen cord or protected wire loop rather than treating this as a universal hardware fit.
5. Lay a paper corner over the fitting without a hole or notch. Align its two edges with the 18 mm magnet inset. Fit the two rear/front magnet pairs, and check that both cords can be connected and released with the paper in place. Bond rear magnets only after checking polarity and fit.
6. With the corner supported, try each guy independently, then both together, watching the elbow root and the pipe engagement marks. Check for visible flex that does not recover, whitening, cracks, cord-edge wear and socket withdrawal. Opposing guys do not remove the loads in the printed part. Repeat attachment/release and inspect again before committing to the second corner or an outdoor setup.

The digital routing check sampled **{v['front_projection_check']['local_cord_routing']['samples']} points** on the illustrated loops and local tails against the actual printed mesh, with a minimum centerline distance of **{v['front_projection_check']['local_cord_routing']['minimum_centerline_distance_to_mesh_mm']:.3f} mm** for 3 mm cord. The sampled paper crossings also clear the paper. Knots, flexible deformation and real line loads are not simulated. **This is a fabrication prototype with no assigned eye or wind load rating.** Ground support and anchor sizing remain separate installation work, particularly for the tall Split-S frame.

## Replace the top corners in the gate

Install two DUAL_GUY_ELBOWs in place of the two old GUY_ELBOWs. The native part has PVC ports +X and +Y; the assembly maps rotate it 270 degrees at upper left and 180 degrees at upper right. The ears point outside the overall corners. All stop positions, PVC lengths and paper cuts remain identical.

Facing the gate, the new top-left magnet centers are **(18, H-90)** and **(90, H-18)** mm from the paper's bottom-left origin. Top-right centers are **(2700-18, H-90)** and **(2700-90, H-18)**. H is 2700 mm for single or 4790.4 mm for stacked. The updated Magnet_Positions.csv files include these changes; remove the old single corner position at each top corner.

Each top elbow now needs two magnet pairs instead of one. Totals become **74 pairs / 148 magnets single**, or **118 pairs / 236 magnets stacked**: **four more individual magnets** than the committed tee design. Paper roll usage, overlap seams and all other magnet positions are unchanged.

| Required part | Single | Stacked total |
|---|---:|---:|
{parttable}

The gate still has **five required printed types**, **64 pieces single / 104 stacked**. Single production estimate: **{s['grams']/1000:.3f} kg / {s['minutes']/60:.1f} hours**, 23 plate runs. Stacked: **{d['grams']/1000:.3f} kg / {d['minutes']/60:.1f} hours**, 36 plate runs. Count the sleeve already printed toward the BOM; full queues are from zero.

PVC requirements remain 16 short + 8 long cuts for single, or 24 short + 14 long for stacked, at **389.6 / 1560.8 mm**. Eight or fourteen 10-ft sticks at the supplied $6 price. At an assumed $20/kg PETG, PVC + PETG face-frame subtotals are **${s['frame_PVC_plus_PETG_usd']:.2f} / ${d['frame_PVC_plus_PETG_usd']:.2f}**, excluding magnets, paper, cord, adhesive and ground support.

## Full print queue

| Recipe | Single runs | Stacked runs | g/run | h/run |
|---|---:|---:|---:|---:|
{queuetable}

Each CSV queue links to prepared A1 Mini PETG projects. Only ONE_DUAL_GUY_ELBOW is a new part/job; the other geometry matches the committed files. No print has been submitted.

## Assembly and extension

The row-by-row assembly from the [committed tee guide](../tee_pvc_gate/README.md) still applies, substituting the two new top elbows and new top magnet locations. Use checked PVC master pieces for repeated marking as recorded in the baseline; the optional jig is not required.

To extend upward, move the complete top row with both dual-guy elbows, its two tees, three pipes and sleeves. Add **4 tees, 4 crosses, 32 sleeves, 8 short PVC cuts and 6 long cuts**. Every existing pipe, fitting and populated magnetic attachment is reused. Two top elbows still provide four guys total: front and rear at each corner. Anchor endpoints and tension settings are not prescribed by the illustrative Blender views.

## Verification and source

Checks cover connected manifold masters; A1 Mini plate bounds, clearances and support-free toolpaths; exact queues and node ports; unchanged non-guy STLs; matching magnetic pockets; full hole-mouth clearance beyond paper; sampled cord/body and cord/paper clearance; and reuse of all single-height parts on extension. The exposed diagonal ear is explicitly allowed in the front-projection check; other protrusions fail it.

[Prusa's modeling guidance](https://help.prusa3d.com/article/modeling-with-3d-printing-in-mind_164135) discusses how geometry and print orientation affect mechanical behavior. The arm dimensions and cord layout here are original prototype choices, not a strength rating derived from that source.

Rebuild with scripts/build_dual_guy_gate.py, slice_dual_guy_gate.py, validate_dual_guy_gate.py and package_dual_guy_gate.py. Baseline commit: **6a7fb47**. The new iteration is separate in output/dual_guy_gate; earlier printable parts and documentation remain intact.
'''
(O/'README.md').write_text(readme)
styles=getSampleStyleSheet();styles.add(ParagraphStyle(name='Body',fontName='Helvetica',fontSize=10,leading=14,spaceAfter=8,textColor=HexColor('#17374c')))
story=[]
def para(t,style='Body'):story.append(Paragraph(t,styles[style]))
def pic(n):story.append(Image(str(O/'renders'/f'{n}.png'),width=510,height=340))
def table(rows,widths):
 t=Table([[Paragraph(html.escape(str(x)),styles['Body']) for x in row] for row in rows],colWidths=widths,repeatRows=1)
 t.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('BACKGROUND',(0,0),(-1,0),HexColor('#dce9ee')),('LINEBELOW',(0,0),(-1,-1),.35,HexColor('#a5bbc5')),('BOTTOMPADDING',(0,0),(-1,-1),6)]));story.append(t)
para('Front + rear guys / one revised top elbow','Title');pic('01_DUAL_GUY_PART')
para(f'Baseline documented and committed as 6a7fb47. New print: {estimate["grams"]:.2f} g PETG / {estimate["minutes"]/60:.2f} hours. Two independent 10.5 mm through-eyes, two edge magnet pads, and the same 33.5 mm PVC sockets. Print two per gate, after testing one.')
for n,title,caption in [
 ('02_FRONT_AND_REAR','Two separate lines at the same corner','Each eye carries a separate attachment loop. Orange leads toward the front and teal toward the rear. The illustrated 3 mm loops clear the printed body; knots and physical loads remain to be tested.'),
 ('03_PAPER_FRONT','Clear the paper / move the magnets','The ear projects about 28.6 mm beyond the adjacent top/side paper edges. Both holes are fully accessible without piercing paper. Magnet centers are 18 mm inside the top/side edges and 90 mm from the corner.'),
 ('08_TOP_CORNER_ROUTING','Install both guys together','The installed upper-left corner is shown with a paper cutaway. Both top corners use the same rotated part. Route the lines through their separate eyes and clear of the magnetic pads.'),
 ('07_A1_MINI_PLATE','Print one on the A1 Mini','168.614 x 168.614 x 53.345 mm. Supplied layout has at least 5 mm bed margin. PETG / 0.20 mm / four walls / 20% infill / no supports. Retain the supplied orientation.'),
 ('05_SINGLE_FRONT','Same paper gate / two new top corners','Single: 64 printed pieces in five types and 74 magnet pairs. Stacked: 104 pieces and 118 pairs. PVC cut lengths and paper dimensions remain unchanged.')]:
 story.append(PageBreak());para(title,'Heading1');pic(n);para(caption)
story.append(PageBreak());para('Parts and production queue','Heading1');table([['Part','Single','Stacked']]+partrows,[280,100,130]);table([['Recipe','Single','Stacked','g/run','h/run']]+queuerows,[240,65,65,70,70])
para(f'Single: {s["grams"]/1000:.3f} kg / {s["minutes"]/60:.1f} hours. Stacked: {d["grams"]/1000:.3f} kg / {d["minutes"]/60:.1f} hours. The two revised elbows add {2*(estimate["grams"]-old["grams"]):.2f} g and {2*(estimate["minutes"]-old["minutes"])/60:.2f} hours versus the committed tee design. Four additional individual magnets are needed.')
story.append(PageBreak());para('Assembly and testing','Heading1')
include=False
for block in readme.split('\n\n'):
 if block.startswith('## Fit and thread'):include=True
 if not include or block.startswith('|'):continue
 if block.startswith('## '):para(block[3:],'Heading2');continue
 block=re.sub(r'\[([^\]]+)\]\(([^)]+)\)',r'\1',block);block=html.escape(block).replace('\n','<br/>');block=re.sub(r'\*\*(.*?)\*\*',r'<b>\1</b>',block);para(block)
def foot(c,d):c.setFont('Helvetica',8);c.drawString(51,22,'FPV gate / dual front and rear guy elbow / 2026-09-19');c.drawRightString(560,22,str(d.page))
SimpleDocTemplate(str(O/'Dual_Guy_Assembly.pdf'),pagesize=(612,792),leftMargin=51,rightMargin=51,topMargin=36,bottomMargin=40).build(story,onFirstPage=foot,onLaterPages=foot)
links=[]
for kind in gates:
 links.append(f'<h3>{kind}</h3><p>'+' · '.join(f'<a href="{kind}_{n}.csv">{label}</a>' for n,label in [('Printed_BOM','Parts'),('Print_Queue','Print queue'),('PVC_Cuts','PVC cuts'),('PVC_Stock_Layout','Stock layout'),('Nodes','Nodes'),('Sleeve_Positions','Sleeve stations'),('Magnet_Positions','Magnets'),('Paper_Cuts','Paper cuts')])+f' · <a href="{kind}_Assembly_Map.svg">Node map</a> · <a href="{kind}_Paper_and_Magnet_Map.svg">Paper map</a></p>')
figs=''.join(f'<figure><a href="renders/{p.name}"><img src="renders/{p.name}" alt="{p.stem}"></a></figure>' for p in sorted((O/'renders').glob('*.png')))
rows=''.join('<tr>'+''.join(f'<td>{html.escape(str(x))}</td>' for x in r)+'</tr>' for r in partrows)
(O/'index.html').write_text(f'''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Dual front/rear guy elbow</title><style>body{{font:17px/1.6 system-ui;max-width:1150px;margin:35px auto;padding:0 24px;color:#17374c;background:#f4f7f9}}img{{width:100%}}figure{{margin:24px 0}}a{{color:#006f91}}aside{{padding:20px;background:#e1edf2}}table{{width:100%;border-collapse:collapse}}td,th{{padding:10px;border-bottom:1px solid #bcced6;text-align:left}}h1{{line-height:1.2}}</style><h1>Front and rear support / two independent eyes</h1><p>Baseline committed as <b>6a7fb47</b>. A reinforced diagonal ear extends beyond each top paper corner, with one 10.5 mm eye per guy. Top and side magnet pads replace the corner pad. The accepted 33.5 mm PVC sockets remain.</p><p><a href="Dual_Guy_Gate.blend">Blender model</a> · <a href="Dual_Guy_Assembly.pdf">Assembly/test PDF</a> · <a href="README.md">Full guide</a> · <a href="Dual_Guy_Gate_Kit.zip">Download kit</a></p><aside><b>First print:</b> <a href="sliced/ONE_DUAL_GUY_ELBOW/ONE_DUAL_GUY_ELBOW_A1Mini_PETG.3mf">ONE_DUAL_GUY_ELBOW / PETG / A1 Mini</a> — {estimate['grams']:.2f} g / {estimate['minutes']/60:.2f} hours. One piece, supports off. Print one and test both sockets and both guy attachments before making the second. The earlier tee job has not been replaced or submitted.</aside><p>The ear is intentionally visible about 28.6 mm beyond each adjacent paper edge. Its two holes let the front guy clear the paper without a cutout. Two top elbows add four individual magnets per gate. All other production STLs are unchanged.</p><table><tr><th>Part</th><th>Single</th><th>Stacked</th></tr>{rows}</table>{figs}<h2>Fabrication files</h2>{''.join(links)}<p><a href="print_checks.json">Digital checks</a> · <a href="geometry_checks.json">Cord and paper clearance</a> · <a href="Upgrade_Additional_Parts.csv">Upgrade parts</a></p><p>The routed 3 mm cord loops clear the mesh and paper in the sampled geometry. Knots, eye strength, friction retention under guy loads and outdoor anchoring remain to be tested. No new print job has been sent.</p></html>''')
with zipfile.ZipFile(O/'Dual_Guy_Gate_Kit.zip','w',zipfile.ZIP_DEFLATED) as z:
 for p in O.rglob('*'):
  if not p.is_file() or p.suffix in ['.zip','.log','.gcode','.blend1']:continue
  if 'sliced' in p.parts and p.suffix!='.3mf':continue
  z.write(p,Path('dual_guy_gate')/p.relative_to(O))
 z.write(ROOT/'output/tee_pvc_gate/README.md','tee_pvc_gate/README.md')
 z.write(ROOT/'output/tee_pvc_gate/Tee_Gate_and_Measuring_Guide.pdf','tee_pvc_gate/Tee_Gate_and_Measuring_Guide.pdf')
print('PACKAGED',estimate,'single',s['grams'],s['minutes'])

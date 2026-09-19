"""Package the diagonal dual-guy elbow iteration and its gate integration."""
from pathlib import Path
import json,csv,html,re,zipfile
from reportlab.platypus import SimpleDocTemplate,Paragraph,Image,Table,TableStyle,PageBreak
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib.colors import HexColor
ROOT=Path(__file__).resolve().parents[1];O=ROOT/'output/corner_guide_elbow'
b=json.loads((O/'BOM.json').read_text());v=json.loads((O/'print_checks.json').read_text());gates=b['gates'];stats=v['gates'];s=stats['single'];d=stats['split_s']
parts={p['code']:p for p in b['parts']};part=parts['DUAL_GUY_ELBOW'];estimate=v['slices']['ONE_DUAL_GUY_ELBOW']
previous=json.loads((ROOT/'output/dual_guy_gate/print_checks.json').read_text());old=previous['slices']['ONE_DUAL_GUY_ELBOW']
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
readme=f'''# Three-magnet guy elbow / paper alignment guides

This iteration adds a corner magnet and shallow paper alignment grooves to the preceding [two-magnet dual-guy elbow](../dual_guy_gate/README.md). The earlier committed PVC/tee baseline is 6a7fb47. This is the current production-file revision; the sleeve fit is confirmed and full-gate tests remain outstanding.

[All five parts](renders/11_ALL_PRODUCTION_PARTS.png) · [Blender](Corner_Guide_Elbow.blend) · [Rendered views](index.html) · [Assembly PDF](Corner_Guide_Elbow.pdf) · [One-elbow PETG print](sliced/ONE_DUAL_GUY_ELBOW/ONE_DUAL_GUY_ELBOW_A1Mini_PETG.3mf)

## Three magnet positions

One 6 x 2 mm magnet now sits at the corner, **18 mm inside both paper edges**. The existing top and side magnets remain 18 mm inside their respective edge and 90 mm along it from the corner. Use three rear magnets and three opposing front magnets per elbow. Front paper pads remain optional.

The new seat is cut into the existing 32 mm-wide diagonal arm. Its **6.3 mm bore** retains a **0.4 mm plastic skin** facing the paper. A **10 mm rear access well** opens down to Z=2.6 mm; the 6.3 mm seat runs from Z=0.4 to 2.6 mm. The 2 mm magnet rests on the skin with its rear face at Z=2.4 mm. Insert it from the rear with a small nonmagnetic dowel, then use a small amount of suitable adhesive after checking polarity. There is no hole through the paper-side skin. The rear access well leaves nominally 11 mm of arm width on each side at its center section; the new pocket still requires a physical guy-load test.

Native CAD magnet centers are (-57,15), (15,-57), and (-57,-57) mm. The native paper corner is (-75,-75) mm, with paper extending toward +X and +Y. Installed at upper left, the new corner magnet is (18,H-18) mm from the paper's bottom-left; at upper right it is (2700-18,H-18). H=2700 single / 4790.4 stacked.

## Exact paper alignment

The paper-facing underside has a recessed **L-shaped guide, 0.8 mm wide and 0.4 mm deep**, extending about 22 mm along each edge. Its centerlines are exactly X=-75 and Y=-75 mm. Their intersection is the intended paper corner. Align the paper edges to the **middle of the grooves**, not their inside or outside walls. The outer half of each groove remains visible beside correctly aligned paper. The marks locate the local corner and edge directions; they are not full-length cutting guides.

The orange guide color in the paper-face render illustrates optional marker rubbed into the actual groove floors; the printable file is a single PETG part. The guide is recessed so the paper can sit flat. It does not cut across a magnet skin or either guy hole. With the supplied face-down print orientation, the 0.8 mm grooves require small bridges; the supplied slice generates them without supports. Actual first-layer squish can soften these fine marks, so inspect them on the first print. Optional contrasting marker rubbed into the recess improves visibility without adding a ridge.

## First print and assembly check

1. Print **one** elbow using the supplied A1 Mini PETG 3MF, 0.4 mm nozzle, 0.20 mm layers, four walls and 20% infill. Use the supplied orientation. The guides are on the bed-facing surface; flip the finished part over to see them.
2. Inspect the recessed L and all three 0.4 mm magnet skins. Fit the purchased PVC into both **33.5 mm** sockets, using full 30 mm insertion and witness marks. The successfully printed sleeve bore is preserved; this elbow's socket fit still needs checking.
3. Check all magnet polarities. Lower the new corner magnet through its access well into the smaller seat using a nonmagnetic dowel. Inspect the seat before bonding. Install the other two backing magnets as before.
4. Place the paper corner at the intersection of the guide centerlines. Align both edges with the groove centerlines, and attach the corner front magnet first. Then attach the top and side front magnets. These are three separate magnet pairs.
5. Attach separate front and rear guys through the two 10.5 mm eyes. They remain outside the paper outline, with no paper notch required. Check the actual knots or loops with paper and all magnets fitted.
6. Check both guys separately and together while supporting the corner. Inspect the diagonal arm around the new access well, the groove intersection, and pipe witness marks for cracking, permanent deformation or socket withdrawal. No eye or wind load rating has been established.

## Print estimate and full-gate effect

One revised elbow: **{estimate['grams']:.2f} g PETG / {estimate['minutes']:.2f} minutes** (about 4 hours). Dimensions remain **168.614 x 168.614 x 53.345 mm**, fitting the 180 mm A1 Mini with at least 5 mm layout margin. The slice has no warnings and no generated supports.

Compared with the preceding two-magnet elbow: **{estimate['grams']-old['grams']:+.2f} g / {estimate['minutes']-old['minutes']:+.2f} minutes per elbow**. Cutting a hole can slightly increase sliced material because the new hole adds perimeters. Two elbows per gate add **four individual magnets** (two additional pairs).

Single gate: **76 pairs / 152 individual magnets**, **{s['grams']/1000:.3f} kg PETG / {s['minutes']/60:.2f} print-hours**. Stacked: **120 pairs / 240 individual magnets**, **{d['grams']/1000:.3f} kg / {d['minutes']/60:.2f} hours**. All other STLs, PVC cuts, paper cuts, node positions and production counts remain unchanged. The exposed guy ear still reaches about 28.6 mm beyond adjacent paper edges.

| Part | Single | Stacked |
|---|---:|---:|
{parttable}

| Recipe | Single runs | Stacked runs | g/run | h/run |
|---|---:|---:|---:|---:|
{queuetable}

Full queues count from zero. Count the sleeve already printed toward the BOM. Prepared files do not submit a job to the printer.

## Current material costs

Using the owner's approximate purchase prices (4 kg black PETG for $39.59, 800 magnets for $19.99, and 10-ft PVC sticks at $5.34), priced materials are **${s['priced_materials_usd']:.2f} single / ${d['priced_materials_usd']:.2f} stacked**. This counts sliced PETG consumption, the individual magnets used and all required PVC stock including offcuts. Paper, guy lines, anchors/ballast, adhesive, electricity, failed prints, tax and shipping are excluded. See the [project README](../../README.md) for full costs and pack-purchase totals. Prior iteration guides retain historical prices.

## License

Original designs and documentation: **CC BY-NC-SA 4.0**, https://creativecommons.org/licenses/by-nc-sa/4.0/ . Credit Robert Boyd (@rboyd), link the project and license, identify changes, and use the permitted ShareAlike terms for shared adaptations. Commercial use of protected material requires separate permission. Source scripts use **PolyForm Noncommercial 1.0.0**. Third-party components retain their own terms. See [scope and commercial permissions](../../LICENSING.md) and the [full design license](../../LICENSE).

## Verification

Connected manifold geometry, plate bounds and clearances, support-free slicing, unchanged non-elbow STLs, aligned magnetic pockets, exact production counts and Split-S reuse checks pass. Ray probes of the actual mesh verify the groove floors at Z=0.4 mm, adjacent face at Z=0, magnet seat floor at Z=0.4 and access-well shoulder at Z=2.6. The prior 3 mm cord routing still clears the modified mesh and the paper. This checks geometry, not physical strength or printer accuracy.

The full assembly follows the preceding dual-guy guide, substituting this elbow and adding its corner magnets. The complete top row can still be moved upward for Split-S. See the updated CSVs for complete counts and magnet positions. Rebuild with build_corner_guide_elbow.py, slice_corner_guide_elbow.py, validate_corner_guide_elbow.py and package_corner_guide_elbow.py in scripts/.
'''
(O/'README.md').write_text(readme)
styles=getSampleStyleSheet();styles.add(ParagraphStyle(name='GuideBody',fontName='Helvetica',fontSize=10,leading=14,spaceAfter=8))
story=[]
def para(t,style='GuideBody'):story.append(Paragraph(t,styles[style]))
para('Corner magnet + paper alignment guides','Title')
para(f'Three magnet pairs per top elbow. Same 33.5 mm PVC sockets and two independent guy eyes. One elbow: {estimate["grams"]:.2f} g PETG / approximately 4 hours.')
for i,(scene,title,caption) in enumerate([
 ('11_ALL_PRODUCTION_PARTS','All five current production parts','Bottom elbow, three-magnet top guy elbow, tee, cross and magnetic sleeve, shown at the same scale. Counts are single / stacked; total 64 / 104 printed pieces.'),
 ('09_PAPER_GUIDES','Paper-facing surface / recessed L','The groove centerlines meet at the exact paper corner. Align paper edges to those centerlines; the marks are recessed 0.4 mm.'),
 ('10_CORNER_MAGNET_SEAT','Rear access / new corner magnet','Lower the 6 x 2 mm magnet through the 10 mm well into its 6.3 mm seat. A 0.4 mm skin remains between the rear magnet and paper. The silver magnet is shown lifted for clarity.'),
 ('08_TOP_CORNER_ROUTING','Installed / all three magnets','The paper cutaway shows the corner, top and side magnets. Both guys remain independently accessible outside the paper.'),
 ('07_A1_MINI_PLATE','A1 Mini / supplied orientation','168.614 x 168.614 x 53.345 mm; PETG, 0.20 mm, four walls, 20% infill. No supports. Flip the print over to see the paper guides.')]):
 if i:story.append(PageBreak())
 para(title,'Heading2');story.append(Image(str(O/'renders'/f'{scene}.png'),width=510,height=340));para(caption)
story.append(PageBreak())
for block in readme.split('\n\n')[3:]:
 if block.startswith('|'):continue
 if block.startswith('## '):para(block[3:],'Heading2');continue
 block=re.sub(r'\[([^\]]+)\]\(([^)]+)\)',r'\1',block)
 block=html.escape(block).replace('\n','<br/>');block=re.sub(r'\*\*(.*?)\*\*',r'<b>\1</b>',block);para(block)
def foot(c,d):
 c.setFont('Helvetica',8);c.drawString(51,22,'FPV gate / corner magnet and recessed paper guides');c.drawRightString(560,22,str(d.page))
SimpleDocTemplate(str(O/'Corner_Guide_Elbow.pdf'),pagesize=(612,792),leftMargin=51,rightMargin=51,topMargin=36,bottomMargin=40).build(story,onFirstPage=foot,onLaterPages=foot)
figs=''.join(f'<figure><a href="renders/{n}.png"><img src="renders/{n}.png" alt="{n}"></a></figure>' for n in ['05_SINGLE_FRONT','12_SPLIT_S_FRONT','06_STACKED_REAR','11_ALL_PRODUCTION_PARTS','09_PAPER_GUIDES','10_CORNER_MAGNET_SEAT','08_TOP_CORNER_ROUTING','03_PAPER_FRONT','01_DUAL_GUY_PART','07_A1_MINI_PLATE'])
links=''.join(f'<p>{kind}: '+' · '.join(f'<a href="{kind}_{name}.csv">{name.replace("_"," ")}</a>' for name in ['Printed_BOM','Print_Queue','PVC_Cuts','Magnet_Positions','Paper_Cuts'])+'</p>' for kind in gates)
(O/'index.html').write_text(f'''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Corner magnet and paper guides</title><style>body{{font:17px/1.6 system-ui;max-width:1150px;margin:35px auto;padding:0 24px;color:#17374c;background:#f4f7f9}}img{{width:100%}}figure{{margin:24px 0}}a{{color:#006f91}}aside{{padding:20px;background:#e1edf2}}</style><h1>One more magnet / exact paper alignment</h1><p>Original designs: <a href="../../LICENSE">CC BY-NC-SA 4.0</a> · <a href="../../LICENSING.md">License scope and commercial permissions</a></p><p>A third magnet 18 mm inside both edges, plus a recessed L marking the exact paper corner. Both guy eyes and the accepted 33.5 mm PVC bores remain.</p><p><a href="Corner_Guide_Elbow.blend">Blender</a> · <a href="Corner_Guide_Elbow.pdf">Assembly PDF</a> · <a href="README.md">Full guide</a> · <a href="Corner_Guide_Elbow_Kit.zip">Kit</a></p><aside><a href="sliced/ONE_DUAL_GUY_ELBOW/ONE_DUAL_GUY_ELBOW_A1Mini_PETG.3mf">Print one revised elbow</a>: {estimate['grams']:.2f} g PETG / {estimate['minutes']:.2f} minutes. Fits A1 Mini, no supports. This job has not been opened or sent.</aside><p>Align paper edges to the centers of the 0.8 mm-wide, 0.4 mm-deep grooves. Install the corner magnet from the rear access well; its 0.4 mm plastic skin remains intact.</p>{figs}<h2>Updated fabrication files</h2>{links}<p><a href="geometry_checks.json">Geometry probes</a> · <a href="print_checks.json">Print and assembly checks</a></p><p>Physical guide visibility, socket fit and guy loads require a first-print check.</p></html>''')
with zipfile.ZipFile(O/'Corner_Guide_Elbow_Kit.zip','w',zipfile.ZIP_DEFLATED) as z:
 for p in O.rglob('*'):
  if not p.is_file() or p.suffix in ['.zip','.log','.gcode','.blend1']:continue
  if 'sliced' in p.parts and p.suffix!='.3mf':continue
  z.write(p,Path('output/corner_guide_elbow')/p.relative_to(O))
 for folder,names in [('dual_guy_gate',['README.md','Dual_Guy_Assembly.pdf']),('tee_pvc_gate',['README.md','Tee_Gate_and_Measuring_Guide.pdf'])]:
  for name in names:z.write(ROOT/'output'/folder/name,Path('output')/folder/name)
 for name in ['LICENSE','LICENSING.md','NOTICE','README.md']:
  z.write(ROOT/name,name)
 for name in ['LICENSE','NOTICE']:
  z.write(ROOT/'scripts'/name,Path('scripts')/name)
 z.write(ROOT/'reference/picture_frame/LICENSE','reference/picture_frame/LICENSE')
 z.write(ROOT/'reference/picture_frame/ATTRIBUTION.md','reference/picture_frame/ATTRIBUTION.md')
print('PACKAGED',estimate)

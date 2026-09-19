"""Verify reused/new print recipes and publish six compact gate material studies."""
from pathlib import Path
import json,collections,math,csv,zipfile,xml.etree.ElementTree as ET,functools,html
from reportlab.pdfgen import canvas
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph,Table,TableStyle
from reportlab.lib.colors import HexColor
R=Path(__file__).resolve().parents[1];O=R/'output/compact_gate_study';B=R/'output/corner_guide_elbow'
d=json.loads((O/'layouts.json').read_text());G=d['gates'];checks=json.loads((O/'geometry_checks.json').read_text());v=json.loads((B/'print_checks.json').read_text());cost=json.loads((R/'docs/material_costs.json').read_text());slices=v['slices'].copy();baseline=v['gates']['single']
ns={'m':'http://schemas.microsoft.com/3dmanufacturing/core/2015/02'};new_checks={}
for file in sorted((O/'printable').glob('*.3mf')):
 with zipfile.ZipFile(file) as z:doc=ET.fromstring(z.read('3D/3dmodel.model'))
 objects=doc.findall('.//m:object',ns);count=int(file.stem.rsplit('_',1)[1]);assert len(objects)==count
 boxes=[]
 for ob in objects:
  vs=[[float(n.get(k)) for k in ['x','y','z']] for n in ob.findall('.//m:vertex',ns)];lo=[min(p[k] for p in vs) for k in range(3)];hi=[max(p[k] for p in vs) for k in range(3)]
  assert min(lo[:2])>=4.999 and max(hi[:2])<=175.001 and abs(lo[2])<.001 and hi[2]<=180
  for a,b in boxes:assert any(min(hi[k],b[k])-max(lo[k],a[k])<-.01 for k in [0,1])
  boxes.append((lo,hi))
 result=json.loads((O/'sliced'/file.stem/'result.json').read_text());assert result['return_code']==0
 sl=result['sliced_plates'][0];assert not sl['warning_message']
 gc=(O/'sliced'/file.stem/'plate_1.gcode').read_text()
 for q in ['; enable_support = 0','; printer_model = Bambu Lab A1 mini','; nozzle_diameter = 0.4','; filament_type = PETG','; wall_loops = 4']:assert q in gc
 assert '; FEATURE: Support' not in gc
 slices[file.stem]={'grams':round(sum(f['total_used_g'] for f in sl['filaments']),2),'minutes':round(sl['total_predication']/60,2),'supports':False,'warnings':[]}
 new_checks[file.stem]={'pieces':count,'A1_Mini_bounds_pass':True,'parts_nonoverlapping':True,**slices[file.stem]}

def writecsv(name,rows):
 with (O/name).open('w') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
def duration(m):
 n=round(m);return f'{n//60}h {n%60:02d}m'
def minimum_sticks(short,long):
 patterns=[(a,b) for a in range(17) for b in range(9) if a+b>0 and a*(short+3)+b*(long+3)<=3038.001]
 @functools.lru_cache(None)
 def f(a,b):
  if not a and not b:return 0
  return 1+min(f(a-x,b-y) for x,y in patterns if x<=a and y<=b)
 return f(16,8)
rows=[]
for g in G:
 queue=[];made=collections.Counter()
 for name,n in g['print_queue'].items():
  cap=7 if name=='BATCH_MAG_SLEEVE' else int(name.rsplit('_',1)[1]) if name.startswith('TAIL_') else 1
  code='MAG_SLEEVE' if 'MAG_SLEEVE' in name else name[4:];made[code]+=n*cap
  folder='.' if (O/'sliced'/name).exists() else '../corner_guide_elbow'
  queue.append({'recipe':name,'runs':n,'pieces_per_run':cap,'PETG_g_per_run':slices[name]['grams'],'minutes_per_run':slices[name]['minutes'],'project':f'{folder}/sliced/{name}/{name}_A1Mini_PETG.3mf'})
 assert dict(made)==g['counts'];assert minimum_sticks(g['short_cut_mm'],g['long_cut_mm'])==g['PVC_sticks']
 grams=round(sum(slices[n]['grams']*qty for n,qty in g['print_queue'].items()),2);minutes=round(sum(slices[n]['minutes']*qty for n,qty in g['print_queue'].items()),2)
 petg=grams*cost['petg_pack_usd']/(1000*cost['petg_pack_kg']);magnets=g['magnet_pairs']*2*cost['magnet_pack_usd']/cost['magnet_pack_quantity'];pvc=g['PVC_sticks']*cost['pvc_10ft_stick_usd']
 g.update(grams=grams,minutes=minutes,plate_runs=sum(g['print_queue'].values()),PETG_cost_usd=round(petg,2),magnets_cost_usd=round(magnets,2),PVC_cost_usd=round(pvc,2),priced_materials_usd=round(petg+magnets+pvc,2),PETG_reduction_pct=round((1-grams/baseline['grams'])*100,1),time_reduction_pct=round((1-minutes/baseline['minutes'])*100,1),paper_visible_m2=round((g['outer_mm']**2-g['opening_mm']**2)/1e6,4))
 writecsv(g['id']+'_Print_Queue.csv',queue)
 rows.append({k:g[k] for k in ['id','opening_mm','band_inches','outer_mm','printed_pieces','magnet_pairs','grams','minutes','plate_runs','PVC_sticks','PVC_m','paper_m','paper_m2','gates_per_100ft_roll','priced_materials_usd','PETG_reduction_pct','time_reduction_pct','maximum_magnet_gap_mm']})
writecsv('Comparison.csv',rows)
(O/'study.json').write_text(json.dumps({'baseline':{k:baseline[k] for k in ['grams','minutes','printed_pieces','priced_materials_usd']},'slices':slices,'new_plate_checks':new_checks,'geometry_checks':checks,'gates':G},indent=2))

def row(g):return f"| {g['opening_mm']} | {g['band_inches']} in | {g['outer_mm']:.1f} | {g['counts']['MAG_SLEEVE']} / {g['printed_pieces']} | {g['grams']/1000:.3f} | {duration(g['minutes'])} | {g['PVC_sticks']} | ${g['priced_materials_usd']:.2f} |"
main_table='\n'.join(row(g) for g in G)
material_table='\n'.join(f"| {g['opening_mm']} / {g['band_inches']} in | {g['short_cut_mm']:.1f} | {g['long_cut_mm']:.1f} | {g['PVC_m']:.3f} | {g['paper_m']:.4f} | {g['paper_m2']:.3f} | {g['gates_per_100ft_roll']} | {g['magnet_pairs']*2} |" for g in G)
queue_table='\n'.join(f"| {w} in | 2 | 2 | 8 | 4 | {G[i]['print_queue']['BATCH_MAG_SLEEVE']} | {G[i]['counts']['MAG_SLEEVE']%7} | {G[i]['plate_runs']} |" for i,w in enumerate([24,18,12]))
filelinks='\n'.join(f"- **{g['opening_mm']} mm / {g['band_inches']} in:** [print queue]({g['id']}_Print_Queue.csv), [PVC cuts + sleeve positions]({g['id']}_PVC_Cuts.csv), [stock nesting]({g['id']}_Stock_Layout.csv), [paper cuts]({g['id']}_Paper_Cuts.csv), [magnet map]({g['id']}_Magnet_Positions.csv)." for g in G)
readme=f'''# Compact gates: 1000 / 800 mm openings and 24 / 18 / 12-inch paper

**Use fewer sleeves, not the original 48.** With the current accepted fittings and a trial maximum edge-magnet gap of 350 mm, the compact gates need **32 / 24 / 16 sleeves** for **24 / 18 / 12-inch paper**, respectively. Both openings use these counts. Smaller paper bands reduce PVC, paper and sleeve requirements while keeping the chosen opening unchanged.

**Suggested next build: 1000 mm opening with 12-inch paper.** It uses **32 printed parts, {G[2]['grams']/1000:.3f} kg PETG and {duration(G[2]['minutes'])}**, versus 64 parts, 2.325 kg and 94h 28m for the current large gate. It retains about 299 mm centered side clearance to the imported MK4's full propeller sweep. The 800 mm version has 199 mm side clearance and saves one more PVC stick, but uses the same printed parts at this magnet-spacing target.

![Six gates at the same scale](renders/01_SIX_PAPER_LAYOUTS.png)

[Blender study](Compact_Gate_Study.blend) · [Visual PDF](Compact_Gate_Study.pdf) · [Render gallery](index.html) · [Comparison CSV](Comparison.csv) · [Detailed data and checks](study.json)

**Workshop cutting:** [PVC cut guide PDF](PVC_Cut_Guide.pdf) and [cut tables / ratchet stock layouts](PVC_Cut_Guide.md). The ratcheting-cutter guide reduces the 1000 mm / 24-inch variant to five PVC sticks; the comparisons below retain the earlier conservative saw allowance of six.

## Material and print comparison

| Opening mm | Paper width | Outer mm | Sleeves / all parts | PETG kg | Print time | PVC sticks | Priced subtotal |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 1480.8 current | 24 in | 2700.0 | 48 / 64 | 2.325 | 94h 28m | 8 | $69.53 |
{main_table}

Times and PETG use local **Bambu Studio A1 Mini PETG slices**, with seven-sleeve batch plates and exact tail quantities. No new fitting shapes are needed. 0.4 mm nozzle, 0.20 mm layer, four walls, 20% infill, textured PEI and supports disabled. The new two- and four-sleeve plates were sliced and verified; other recipes reuse the current verified production slices. These are slicer estimates, not measured machine runtimes. Full quantities assume printing from zero; subtract already printed fittings.

Costs use the owner's prices: $39.59 / 4 kg PETG, $19.99 / 800 magnets and $5.34 / 10-ft PVC stick. Subtotals include allocated PETG, both magnets of every pair, and whole PVC sticks. **Paper prices for each width were not supplied and are excluded**, along with guy lines, ground support, tax, electricity and failures. Roll yields below help compare actual paper prices without inventing prices.

## Where the parts disappear

![1000 mm frames with paper removed](renders/02_FRAME_1000.png)

All versions retain **2 bottom elbows + 2 top guy elbows + 8 tees + 4 crosses = 16 structural fittings**. These carry the orthogonal PVC grid and outer/inner paper supports. All accepted 33.5 mm bores, 30 mm insertion depths, guy eyes, paper alignment guides and magnet skins stay unchanged. This is a compatible layout reduction rather than a new lightweight fitting design.

- **24-inch band:** 16 sleeves on eight long pipes (two each), plus 16 sleeves on short pipes.
- **18-inch band:** 16 long-pipe sleeves, plus eight short-pipe sleeves at the paper overlap seams. Eight outer-corner sleeves disappear.
- **12-inch band:** 16 long-pipe sleeves. All sixteen short-pipe sleeves disappear; the fitting-mounted magnets cover the short sections and overlap seams.

Blue fittings and orange sleeves are render colors for identification; the user's filament is black. Magnets remain 18 mm in from the paper edges. Lowering sleeve count removes the sleeve and its two magnets. Empty, unused cross pockets stay unpopulated.

**Why 800 mm does not yet print faster than 1000 mm:** two intermediate magnets per long edge produce maximum long-edge gaps of **278.7 mm** and **345.3 mm**, respectively. One sleeve on an 800 mm long edge would create **418 mm** gaps, exceeding this study's 350 mm target. A later sparse-retention test could try that; it is not included in these six layouts.

**The next bottleneck is the large fittings.** The 16 structural pieces alone consume **1.661 kg / 63h 51m**, about 88% of the 12-inch version's PETG. The 12-inch layout halves the total part count but reduces PETG by **19.0%** and printer time by **21.3%**. Major further print savings require redesigning those fittings, not merely making the paper narrower. The complete 12-inch queue fits nominally within two 1 kg spools, with about 117 g spare before failures. No version here fits one spool. The 18-inch queue nearly exhausts two spools, so allow reserve.

## Paper, PVC and magnets

| Opening / band | 16 short PVC cuts mm | 8 long PVC cuts mm | PVC used m | Paper used m | Paper area m² | Gates / 100-ft roll | Individual magnets |
|---:|---:|---:|---:|---:|---:|---:|---:|
{material_table}

Each gate uses **four rectangular paper strips and four crosscuts**, keeping the full roll width: two top/bottom strips as long as the outer square, and two side strips as long as opening + 72 mm. Each side overlaps the top and bottom strips by 36 mm. No lengthwise ripping or corner patches are required. Roll yields assume a usable 30.48 m roll with negligible trimming allowance; allow extra for repairs or damaged paper. Paper area includes overlap. Compare roll cost per gate as **roll price divided by the whole-gate yield**, with leftover paper retained.

For 12-inch paper the short PVC cut is **84.8 mm**. Insert 30 mm at each end, leaving **24.8 mm** exposed between socket mouths. Do not attempt to add a short-pipe sleeve there. The actual fitted meshes were checked at these positions: no intersecting fitting pairs, and no unintended plastic visible beyond the paper. The diagonal guy ears intentionally remain exposed. Dry-fit one corner with your cutter before cutting all sixteen short pieces.

The stock layouts use 3048 mm sticks with 10 mm trimming reserve and 3 mm per cut allowance. A two-length integer packing check confirms the listed stick counts are minimal under those allowances. A ratcheting cutter does not remove a saw kerf; keeping the allowance provides a conservative measuring/trim margin. Pipe budgets exclude feet or other ground support.

A narrower band uses less material and presents less solid area to the wind, but does not establish a wind rating. The 350 mm edge-magnet target is a **layout assumption**, not a measured paper peel/tear limit. Paper grade, dampness, tension and gusts matter. Start with the 12-inch layout and test one full border using the actual roll and magnets; add long-pipe sleeves if edges flap or lift. Retain front/rear guys and suitable grass anchors or hard-surface ballast from the current design.

## Full print queues

Counts below apply to either opening with the given paper width. Each large fitting prints individually. Each full sleeve batch contains seven sleeves.

| Paper | Bottom elbow jobs | Guy elbow jobs | Tee jobs | Cross jobs | Seven-sleeve batches | Tail sleeves on one plate | Total plate runs |
|---:|---:|---:|---:|---:|---:|---:|---:|
{queue_table}

[Bottom elbow](../corner_guide_elbow/sliced/ONE_ELBOW/ONE_ELBOW_A1Mini_PETG.3mf) · [Guy elbow](../corner_guide_elbow/sliced/ONE_DUAL_GUY_ELBOW/ONE_DUAL_GUY_ELBOW_A1Mini_PETG.3mf) · [Tee](../corner_guide_elbow/sliced/ONE_TEE/ONE_TEE_A1Mini_PETG.3mf) · [Cross](../corner_guide_elbow/sliced/ONE_CROSS/ONE_CROSS_A1Mini_PETG.3mf) · [Seven sleeves](../corner_guide_elbow/sliced/BATCH_MAG_SLEEVE/BATCH_MAG_SLEEVE_A1Mini_PETG.3mf)

Tail plates: [2 sleeves for 12-inch paper](sliced/TAIL_MAG_SLEEVE_2/TAIL_MAG_SLEEVE_2_A1Mini_PETG.3mf) · [3 sleeves for 18-inch paper](../corner_guide_elbow/sliced/TAIL_MAG_SLEEVE_3/TAIL_MAG_SLEEVE_3_A1Mini_PETG.3mf) · [4 sleeves for 24-inch paper](sliced/TAIL_MAG_SLEEVE_4/TAIL_MAG_SLEEVE_4_A1Mini_PETG.3mf).

These projects are prepared locally; no job was sent to a printer. The current production folder remains unchanged.

## Build the selected size

1. Choose the opening and paper width; use the corresponding files below. Print only the missing parts.
2. Dry-fit one 84.8 mm corner section if using 12-inch paper. Confirm full 30 mm insertion at both ends and correct paper guide alignment.
3. Cut eight long and sixteen short PVC pieces. Slide sleeves onto each pipe **before** closing its ends with fittings. The cut CSV lists each sleeve center's distance from the pipe's cut start, with the start node encoded in its name.
4. Assemble the 4 × 4 node grid shown in scenes 02/03, placing the two guy elbows at the top. The cross has four ports; perimeter tees face into the grid. Clock sleeves toward the corresponding outer edge, opening edge or overlap seam as shown in Blender. The magnet CSV gives front-facing coordinates measured from the lower-left paper outline.
5. Cut the four paper rectangles. Align the outside corners and 36 mm side overlaps, then clamp at each populated magnet position. Confirm polarity before fixing magnets into their pockets.
6. Add suitable ground support and independent front/rear guys. Measure the actual opening and check friction retention, paper sag and magnet holding before flying. The render omits ground supports and guys for visibility.

{filelinks}

## Blender, source and checks

Five scenes: six paper-on variants at the same scale; three bare 1000 mm frames; three bare 800 mm frames; both 12-inch-paper gates with the drone; and the compact lower-left corner. The source meshes are the actual accepted production parts. Geometry checks cover fitting-to-fitting intersections, paper coverage and magnet locations; queue checks cover exact quantities, bed fit and support-free slicing. Physical corner assembly, full-gate loads and paper retention remain untested.

The imported 7-inch MK4 is from Dendy / Printables 1515387, **CC BY-NC 4.0**, with the uploader's qualification that they did not create the underlying frame. The top battery is an assumed 110 × 40 × 45 mm addition. [Drone attribution and licenses](../../reference/geprc_mk4/ATTRIBUTION.md). Gate material and source code retain the project licenses. Clearances use the imported swept prop envelope, not just a static blade orientation.

Rebuild: `python scripts/plan_compact_gates.py`, `python scripts/slice_compact_gate_tails.py`, `blender -b -t 8 --python scripts/build_compact_gate_study.py`, then `python scripts/package_compact_gate_study.py` (ReportLab required for packaging). Existing production slices and the preceding drone Blender study are dependencies.
'''
(O/'README.md').write_text(readme)
imgs=sorted((O/'renders').glob('*.png'))
table_html='<table><tr><th>Opening</th><th>Paper</th><th>Parts</th><th>PETG</th><th>Time</th><th>Subtotal*</th></tr>'+''.join(f"<tr><td>{g['opening_mm']} mm</td><td>{g['band_inches']} in</td><td>{g['printed_pieces']}</td><td>{g['grams']/1000:.3f} kg</td><td>{duration(g['minutes'])}</td><td>${g['priced_materials_usd']:.2f}</td></tr>" for g in G)+'</table>'
figs=''.join(f'<figure><a href="renders/{p.name}"><img src="renders/{p.name}" alt="{html.escape(p.stem)}"></a><figcaption>{html.escape(p.stem.replace("_"," "))}</figcaption></figure>' for p in imgs)
(O/'index.html').write_text('''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Compact FPV gate study</title><style>body{font:17px/1.6 system-ui;background:#edf1f3;color:#193247;max-width:1400px;margin:40px auto;padding:0 24px}a{color:#066a95}img{width:100%;display:block}figure{margin:30px 0}td,th{padding:10px 16px;border-bottom:1px solid #ccd5db;text-align:left}table{background:white;width:100%}figcaption{font-size:14px}h1{line-height:1.2}</style><h1>Smaller gates with fewer sleeves</h1><p>Try a 1000 mm opening with 12-inch paper: 32 printed parts, 1.883 kg PETG and about 74 hours. The 800 mm version uses the same prints and one fewer PVC stick. Both keep the accepted fittings and 33.5 mm bores.</p><p><a href="Compact_Gate_Study.blend">Blender model</a> · <a href="Compact_Gate_Study.pdf">PDF</a> · <a href="README.md">Build study and print queue links</a> · <a href="Comparison.csv">Comparison CSV</a></p>'''+table_html+'''<p>*PETG consumed, magnets and whole PVC sticks at the owner's prices. Paper, ground support and guys are additional. Magnet spacing is a design trial, not a tested retention rating.</p>'''+figs+'''<p>Blue structural fittings and orange sleeves represent the user's black PETG. Drone reference: Dendy / Printables 1515387, CC BY-NC 4.0; battery assumed. <a href="../../reference/geprc_mk4/ATTRIBUTION.md">Attribution</a>.</p></html>''')
c=canvas.Canvas(str(O/'Compact_Gate_Study.pdf'),pagesize=(1000,650));c.setTitle('Compact FPV gates / material and print study')
style=ParagraphStyle('body',fontName='Helvetica',fontSize=12,leading=18,textColor=HexColor('#193247'))
def para(s,y):
 p=Paragraph(s,style);_,h=p.wrap(900,600);p.drawOn(c,50,y-h);return y-h-15
c.setFont('Helvetica-Bold',26);c.drawString(50,596,'Compact gates / fewer sleeves and narrower paper')
y=para('Suggested trial: <b>1000 mm opening, 12-inch paper</b>. 16 structural fittings + 16 sleeves = 32 prints. Compared with the current large gate: half the printed pieces, 19.0% less PETG and 21.3% less printer time. The 800 mm version needs the same prints but saves one PVC stick.',561)
tdata=[['Opening','Paper','Outer mm','Sleeves / total','PETG kg','Print time','PVC sticks','Subtotal*']]+[[g['opening_mm'],f"{g['band_inches']} in",f"{g['outer_mm']:.1f}",f"{g['counts']['MAG_SLEEVE']} / {g['printed_pieces']}",f"{g['grams']/1000:.3f}",duration(g['minutes']),g['PVC_sticks'],f"${g['priced_materials_usd']:.2f}"] for g in G]
t=Table(tdata,colWidths=[90,80,105,125,105,115,100,110],rowHeights=30);t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),HexColor('#193247')),('TEXTCOLOR',(0,0),(-1,0),HexColor('#ffffff')),('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),('GRID',(0,0),(-1,-1),.4,HexColor('#c4ced7')),('VALIGN',(0,0),(-1,-1),'MIDDLE')]));_,h=t.wrap(900,500);t.drawOn(c,50,y-h);y-=h+18
y=para('*PETG consumed + both magnets per clamp + whole PVC sticks, at the owner\'s purchase prices. Paper, guys and ground supports are excluded. Slicer estimates use exact batch quantities, including the two new partial sleeve plates.',y)
y=para('The 350 mm maximum edge-magnet gap is an untested layout target. The 800 mm gate could use fewer long-rail sleeves only by accepting wider gaps (418 mm with one per rail). Test paper retention before trying that reduction. All six variants retain the accepted 33.5 mm fitting bores.',y)
para('The accompanying README includes full print queues, pipe cuts, paper cuts and sleeve positions. Original fitting geometry is unchanged. Dendy / Printables 1515387 drone reference: CC BY-NC 4.0; battery assumed. Ground supports and guys are omitted from renders.',y);c.showPage()
for p in imgs:c.drawImage(str(p),0,0,width=1000,height=650,preserveAspectRatio=True,anchor='c');c.showPage()
c.save()
for g in G:print(g['id'],g['grams'],duration(g['minutes']),g['priced_materials_usd'])
print('PASS: exact queues, no support warnings, A1 Mini bounds, minimum PVC stock counts.')

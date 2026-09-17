from pathlib import Path
from PIL import Image
import json,html,math,shutil,zipfile
from face_geometry import PANEL, OFFCUT, STRIP, PATCH, PATCH_PADS, STRIP_PADS, PATCH_SPREADERS, STRIP_SPREADERS
R=Path(__file__).resolve().parents[1];O=R/'output'; D=O/'cut-layouts';layout=json.loads((D/'nesting.json').read_text())
def begin(w,h,title):
 return [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w/10}mm" height="{h/10}mm" viewBox="0 0 {w} {h}">',f'<rect width="{w}" height="{h}" fill="white"/>',f'<text x="60" y="65" font-family="Arial" font-size="38" font-weight="bold" fill="#142e47">{html.escape(title)}</text>']
def poly(svg,pts,fill,stroke='#19334e',sw=3): svg.append('<polygon points="'+' '.join(f'{x:.4f},{y:.4f}' for x,y in pts)+f'" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')
def txt(svg,x,y,t,size=30,color='#18334e'): svg.append(f'<text x="{x}" y="{y}" font-family="Arial" font-size="{size}" fill="{color}">{html.escape(t)}</text>')
for sh in [1,2,3]:
 s=begin(2700,1500,f'SHEET {sh} / '+('2 SYMMETRIC PANELS' if sh<3 else '128 SQUARES = 32 GATES')+' / SCALE 1:10')
 s.append('<rect x="100" y="140" width="2438.4" height="1219.2" fill="#e0eddf" stroke="#142e47" stroke-width="3"/>')
 for i,r in enumerate([a for a in layout if a['sheet']==sh]):
  pts=[(100+x,1359.2-y) for x,y in r['polygon_mm']];poly(s,pts,'#2c5dbe' if i%2==0 else '#4b7acf')
  if sh<3:txt(s,800,1080 if i==0 else 480,'2400 x 600 mm blank / matching ends',38,'white')
 txt(s,100,1430,'Two matching 450 x 450 right-triangle offcuts per panel. Keep all eight.' if sh<3 else '150 x 150 mm squares. 16 columns x 8 rows. Knife cuts; allow for kerf if sawing.',28)
 s.append('</svg>');(D/f'sheet_{sh:02}_layout.svg').write_text('\n'.join(s))
s=begin(1400,900,'OFFCUT RECOVERY / 4 OF EACH TYPE / SCALE 1:10')
for idx,parts in enumerate([[PATCH]+PATCH_PADS+PATCH_SPREADERS,[STRIP]+STRIP_PADS+STRIP_SPREADERS]):
 ox=80+idx*650
 tf=lambda p:(ox+p[0],650-p[1])
 poly(s,[tf(p) for p in OFFCUT],'#e0eddf')
 for j,p in enumerate(parts):poly(s,[tf(q) for q in p],'#91b9d0' if j==0 else ('#4b7acf' if j<4 else '#e8a96f'),sw=1)
 txt(s,ox,145,'220 square patch' if idx==0 else '350 x 80 diagonal strip',30)
 txt(s,ox,715,'+ 3 pads (70 x 50) + 8 spreaders (25 x 25)',23)
 txt(s,ox,765,'Use 4 identical 450-leg offcuts',25)
 txt(s,ox,815,'Coordinates in reinforcement_nesting.json',22)
s.append('</svg>');(D/'offcut_reinforcement.svg').write_text('\n'.join(s))
(D/'reinforcement_nesting.json').write_text(json.dumps({'units':'mm','copies_of_each':4,'offcut':OFFCUT,'type_A':{'backer':PATCH,'saddle_pads':PATCH_PADS,'spreaders':PATCH_SPREADERS},'type_B':{'backer':STRIP,'saddle_pads':STRIP_PADS,'spreaders':STRIP_SPREADERS}},indent=2))
s=begin(2700,1050,'SYMMETRIC MAIN PANEL / CUT 4 / TWO PER SHEET / SCALE 1:10')
poly(s,[(100+x,800-y) for x,y in PANEL],'#dce7f7')
s.append('<rect x="100" y="200" width="2400" height="600" fill="none" stroke="#e38639" stroke-width="3" stroke-dasharray="12 8"/>')
for x,y in PANEL:
 dx=10 if x<2000 else -260;dy=-20 if y>0 else 50
 txt(s,100+x+dx,800-y+dy,f'({x}, {y})',29)
txt(s,780,470,'1500 inner / 2400 outer / 600 border',38)
txt(s,810,545,'Equal 45-degree cuts / 150 mm shoulders',33)
s.append('<path d="M1300,150 L1300,850" stroke="#e38639" stroke-width="2" stroke-dasharray="10 8"/>')
txt(s,100,930,'Coordinates from lower-left of blank. Mirror symmetry about x = 1200. Rotate panels during assembly.',27)
txt(s,100,995,'150 mm corner squares complete the 2700 mm outer dimension. All measurements are millimetres.',27)
s.append('</svg>');(D/'main_panel_vertices.svg').write_text('\n'.join(s))
for obsolete in ['pentagon_vertices.svg','offcut_backers_and_optional_corners.svg']:
 (D/obsolete).unlink(missing_ok=True)
if not (D/'attachment_template_1to1.svg').exists():
 shutil.copy2(O/'previous_rectangular_design/cut-layouts/attachment_template_1to1.svg',D/'attachment_template_1to1.svg')
scenes=[('01_ASSEMBLED','Grass / assembled'),('02_REAR_STRUCTURE','Rear structure'),('03_EXPLODED','Exploded assembly'),('04_SHEET_LAYOUT','Shared-sheet cutting layout'),('05_CLIP_DETAIL','Face attachment'),('06_DIMENSIONS','Dimensions'),('07_HARD_SURFACE','Hard surface / ballast'),('08_BRACE_JOINT','Printed brace-end joints'),('09_FACE_PARTS','Symmetric panels and square corners'),('10_CUTTING_JIGS','A1 Mini cutting jigs')]
css='''*{box-sizing:border-box}body{margin:0;background:#f4f5f3;color:#142d43;font:16px/1.55 -apple-system,BlinkMacSystemFont,Arial,sans-serif}header,main{max-width:1250px;margin:auto;padding:32px}h1{font-size:48px;line-height:1.1;margin:14px 0}p{max-width:900px}a{color:#174eb9}nav{display:flex;flex-wrap:wrap;gap:8px;margin:26px 0}nav a,.button{display:inline-block;border:1px solid #b5c3d2;border-radius:6px;padding:8px 12px;text-decoration:none;background:white}.primary{background:#1648b1;color:white}figure{margin:22px 0 40px}figure img{display:block;width:100%;border:1px solid #c5cdd2;border-radius:9px}figcaption{padding:8px 0;color:#4b6073}table{border-collapse:collapse;width:100%;margin:20px 0}th,td{text-align:left;border-bottom:1px solid #ced6de;padding:12px}.note{border-left:4px solid #df7929;padding:12px 20px;background:white}small{color:#566b7c}@media(max-width:650px){header,main{padding:20px}h1{font-size:34px}}@media print{nav,.downloads{display:none}figure{break-inside:avoid;page-break-before:always}}'''
s=['<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>FPV gate / symmetric panel design</title>',f'<style>{css}</style><header><small>FIELDWORK / FPV RACING GATE</small><h1>Symmetric cuts.<br>Square corners.</h1><p>2700 mm square face, 1500 mm clear opening and one braced PVC backing frame (about 96 mm body thickness). Two identical panels per sheet; two main sheets per gate. A third sheet yields 128 corner squares for 32 gates.</p><div class="downloads"><a class="button primary" href="FPV_Gate_2700.blend">Blender model</a> <a class="button" href="BUILD_GUIDE.md">Build guide</a> <a class="button" href="Assembly_Views.pdf">Assembly PDF</a> <a class="button" href="BOM.csv">BOM</a> <a class="button" href="PVC_CUT_LIST.csv">PVC cuts</a> <a class="button" href="JIGS.csv">Jig list</a></div><nav>']
s +=[f'<a href="#{f}">{label}</a>' for f,label in scenes]
s+=['</nav></header><main><table><tr><th>Shared structure</th><th>Grass / soil</th><th>Hard ground</th></tr><tr><td>1-inch frame / ¾-inch braces<br>24 saddle and washer pairs<br>8 printed brace-end joints</td><td>1200 mm feet<br>Four opposing guy stakes<br>About $231 allocated</td><td>2400 mm feet<br>Four guys to ballasted feet<br>Four weighed 15 kg bags</td></tr></table><p>About <strong>$288 for the dual-surface kit</strong> at batch allocation, before tax, shipping and ballast fill. A first kit purchasing a whole corner sheet is about $317; its remaining corners serve later gates. Estimates and sources are in the guide.</p><p class="note">The eight STL designs are manifold and the face/stock polygons are checked. Physical fit, tie passages, anchor holding and wind performance still need a prototype test. No wind rating is asserted.</p>']
for f,label in scenes: s.append(f'<figure id="{f}"><a href="renders/{f}.png"><img src="renders/{f}.png" alt="{label}" loading="lazy"></a><figcaption>{label} — editable in the corresponding Blender scene.</figcaption></figure>')
s.append('<h2>Fabrication files</h2><p>')
for f,label in [('main_panel_vertices.svg','Symmetric panel vertices'),('sheet_01_layout.svg','Main sheet 1'),('sheet_02_layout.svg','Main sheet 2'),('sheet_03_layout.svg','Shared corners'),('offcut_reinforcement.svg','Offcut reinforcement nesting'),('attachment_template_1to1.svg','1:1 attachment template')]:s.append(f'<a class="button" href="cut-layouts/{f}">{label}</a> ')
s.append('</p><p>')
for f in sorted((O/'printable').glob('*.stl')): s.append(f'<a class="button" href="printable/{f.name}">{f.stem.replace("_"," ")}</a> ')
s.append('</p><p>All STL coordinates are millimetres. The handed brace connectors have separate pipe grooves and internal tie-return tunnels; the brace detail includes a cutaway. Print a fit sample first. The three marking jigs fit the A1 Mini; use a clamped metal straightedge for long knife cuts.</p></main></html>')
(O/'START_HERE.html').write_text('\n'.join(line.rstrip() for line in s)+'\n')
if all((O/f'renders/{f}.png').exists() for f,_ in scenes):
 images=[Image.open(O/f'renders/{f}.png').convert('RGB') for f,_ in scenes]
 images[0].save(O/'Assembly_Views.pdf',save_all=True,append_images=images[1:],resolution=150,quality=94)
 for im in images:im.close()
 print('PDF contains 10 Blender plates')
else:print('Some renders still pending; rerun after render completion')
print('Wrote six SVGs and current HTML index')
with zipfile.ZipFile(O/'FPV_Gate_Kit.zip','w',zipfile.ZIP_DEFLATED,compresslevel=6) as archive:
 for path in sorted(O.rglob('*')):
  if path.is_file() and not any(p.startswith('previous_') for p in path.relative_to(O).parts) and path.suffix not in ['.zip','.log','.blend1']:
   archive.write(path,Path('FPV_Gate_Kit')/path.relative_to(R))
 for name in ['build_gate.py','validate_layout.py','package_deliverables.py','face_geometry.py','cutting_jigs.py']:
  archive.write(R/'scripts'/name,Path('FPV_Gate_Kit/scripts')/name)
 archive.write(R/'README.md','FPV_Gate_Kit/README.md')
print('Packaged current model, fabrication files, views and generation scripts')

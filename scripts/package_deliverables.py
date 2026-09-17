from pathlib import Path
from PIL import Image
import json,html,math,shutil,zipfile
R=Path(__file__).resolve().parents[1];O=R/'output'; D=O/'cut-layouts';layout=json.loads((D/'nesting.json').read_text())
def begin(w,h,title):
 return [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w/10}mm" height="{h/10}mm" viewBox="0 0 {w} {h}">',f'<rect width="{w}" height="{h}" fill="white"/>',f'<text x="60" y="65" font-family="Arial" font-size="38" font-weight="bold" fill="#142e47">{html.escape(title)}</text>']
def poly(svg,pts,fill,stroke='#19334e',sw=3): svg.append('<polygon points="'+' '.join(f'{x:.4f},{y:.4f}' for x,y in pts)+f'" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')
def txt(svg,x,y,t,size=30,color='#18334e'): svg.append(f'<text x="{x}" y="{y}" font-family="Arial" font-size="{size}" fill="{color}">{html.escape(t)}</text>')
for sh in [1,2,3]:
 s=begin(2700,1500, f'SHEET {sh} / '+('2 IDENTICAL PENTAGONS' if sh<3 else '64 CORNERS = 16 GATES')+' / SCALE 1:10')
 s.append('<rect x="100" y="140" width="2438.4" height="1219.2" fill="#e0eddf" stroke="#142e47" stroke-width="3"/>')
 for i,r in enumerate([a for a in layout if a['sheet']==sh]):
  pts=[(100+x,1359.2-y) for x,y in r['polygon_mm']];poly(s,pts,'#2c5dbe' if i%2==0 else '#4b7acf')
  if sh<3: txt(s,950,1080 if i==0 else 480,'2400 x 600 mm blank / 5 sides',40,'white')
 if sh<3:
  txt(s,100,1430,'Same five vertices in each blank: (0,600) (2400,600) (2400,300) (2100,0) (600,0)',27)
 else: txt(s,100,1430,'300 x 300 mm squares, each split diagonally. Knife cuts; saw kerf reduces yield.',30)
 s.append('</svg>');(D/f'sheet_{sh:02}_layout.svg').write_text('\n'.join(s))
# One large offcut supports a diagonal backer and optional corner; one small offcut supports a short tab.
s=begin(1600,1000,'OFFCUT RECOVERY / 4 OF EACH OFFCUT PER GATE / SCALE 1:10')
transform=lambda p:(100+p[0],800-p[1])
poly(s,[transform(p) for p in [(0,0),(600,0),(0,600)]],'#e0eddf')
u=(1/math.sqrt(2),-1/math.sqrt(2));v=(1/math.sqrt(2),1/math.sqrt(2))
back=[(250+a*u[0]+b*v[0],250+a*u[1]+b*v[1]) for a,b in [(-300,-50),(300,-50),(300,50),(-300,50)]]
poly(s,[transform(p) for p in back],'#b9d4e4');poly(s,[transform(p) for p in [(0,0),(300,0),(0,300)]],'#4b7acf')
txt(s,80,160,'600 mm-leg offcut',32);txt(s,250,520,'600 x 100 backer',25);txt(s,105,735,'Optional 300 corner',24,'white')
trans2=lambda p:(900+p[0],800-p[1])
poly(s,[trans2(p) for p in [(0,0),(300,0),(300,300)]],'#e0eddf')
poly(s,[trans2(p) for p in [(160,0),(300,0),(300,100),(160,100)]],'#b9d4e4');txt(s,880,465,'300 mm-leg offcut',30);txt(s,930,840,'140 x 100 short tab',27)
txt(s,70,910,'Diagonal strip: center (250,250), 600 long x 100 wide, long axis at -45 degrees.',25)
txt(s,70,952,'Green remainder supplies 70 x 50 saddle pads and smaller stitch pads. Shared sheet remains baseline.',24)
s.append('</svg>');(D/'offcut_backers_and_optional_corners.svg').write_text('\n'.join(s))
# Separate pentagon dimension/vertex drawing; no ambiguity about how the corners are cut.
s=begin(2700,1000,'MAIN PENTAGON / CUT 4 IDENTICAL / TWO PER SHEET / SCALE 1:10')
p=[(0,600),(2400,600),(2400,300),(2100,0),(600,0)]
poly(s,[(100+x,800-y) for x,y in p],'#dce7f7')
s.append('<rect x="100" y="200" width="2400" height="600" fill="none" stroke="#e38639" stroke-width="3" stroke-dasharray="12 8"/>')
for x,y in p:
 s.append(f'<circle cx="{100+x}" cy="{800-y}" r="8" fill="#1c3a56"/>')
 dx=10 if x<2000 else -250;dy=-20 if y>0 else 50
 txt(s,100+x+dx,800-y+dy,f'({x}, {y})',30)
txt(s,820,510,'1500 mm inner edge / 2400 mm outer edge',37)
txt(s,100,925,'Coordinates from lower-left of the dashed 2400 x 600 blank. Rotate completed panels; do not mirror.',29)
s.append('</svg>');(D/'pentagon_vertices.svg').write_text('\n'.join(s))
if not (D/'attachment_template_1to1.svg').exists():
 shutil.copy2(O/'previous_rectangular_design/cut-layouts/attachment_template_1to1.svg',D/'attachment_template_1to1.svg')
scenes=[('01_ASSEMBLED','Grass / assembled'),('02_REAR_STRUCTURE','Rear structure'),('03_EXPLODED','Exploded assembly'),('04_SHEET_LAYOUT','Shared-sheet cutting layout'),('05_CLIP_DETAIL','Face attachment'),('06_DIMENSIONS','Dimensions'),('07_HARD_SURFACE','Hard surface / ballast'),('08_BRACE_JOINT','Printed brace-end joints'),('09_FACE_PARTS','Pentagons and corners')]
css='''*{box-sizing:border-box}body{margin:0;background:#f4f5f3;color:#142d43;font:16px/1.55 -apple-system,BlinkMacSystemFont,Arial,sans-serif}header,main{max-width:1250px;margin:auto;padding:32px}h1{font-size:48px;line-height:1.1;margin:14px 0}p{max-width:900px}a{color:#174eb9}nav{display:flex;flex-wrap:wrap;gap:8px;margin:26px 0}nav a,.button{display:inline-block;border:1px solid #b5c3d2;border-radius:6px;padding:8px 12px;text-decoration:none;background:white}.primary{background:#1648b1;color:white}figure{margin:22px 0 40px}figure img{display:block;width:100%;border:1px solid #c5cdd2;border-radius:9px}figcaption{padding:8px 0;color:#4b6073}table{border-collapse:collapse;width:100%;margin:20px 0}th,td{text-align:left;border-bottom:1px solid #ced6de;padding:12px}.note{border-left:4px solid #df7929;padding:12px 20px;background:white}small{color:#566b7c}@media(max-width:650px){header,main{padding:20px}h1{font-size:34px}}@media print{nav,.downloads{display:none}figure{break-inside:avoid;page-break-before:always}}'''
s=['<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>FPV gate / pentagon design</title>',f'<style>{css}</style><header><small>FIELDWORK / FPV RACING GATE</small><h1>Four pentagons.<br>One shared corner sheet.</h1><p>2700 mm square face, 1500 mm clear opening and one braced PVC backing frame (about 94 mm body thickness). Two identical panels per sheet; two main sheets per gate. A third sheet yields 64 corner triangles for 16 gates.</p><div class="downloads"><a class="button primary" href="FPV_Gate_2700.blend">Blender model</a> <a class="button" href="BUILD_GUIDE.md">Build guide</a> <a class="button" href="Assembly_Views.pdf">Assembly PDF</a> <a class="button" href="BOM.csv">BOM</a> <a class="button" href="PVC_CUT_LIST.csv">PVC cuts</a></div><nav>']
s +=[f'<a href="#{f}">{label}</a>' for f,label in scenes]
s+=['</nav></header><main><table><tr><th>Shared structure</th><th>Grass / soil</th><th>Hard ground</th></tr><tr><td>1-inch frame / ¾-inch braces<br>24 saddle and washer pairs<br>8 printed brace-end joints</td><td>1200 mm feet<br>Four opposing guy stakes<br>About $232 allocated</td><td>2400 mm feet<br>Four guys to ballasted feet<br>Four weighed 15 kg bags</td></tr></table><p>About <strong>$289 for the dual-surface kit</strong> at batch allocation, before tax, shipping and ballast fill. A first kit purchasing a whole corner sheet is about $317; its remaining corners serve later gates. Estimates and sources are in the guide.</p><p class="note">The five STL designs are manifold and the face/stock polygons are checked. Physical fit, tie passages, anchor holding and wind performance still need a prototype test. No wind rating is asserted.</p>']
for f,label in scenes: s.append(f'<figure id="{f}"><a href="renders/{f}.png"><img src="renders/{f}.png" alt="{label}" loading="lazy"></a><figcaption>{label} — editable in the corresponding Blender scene.</figcaption></figure>')
s.append('<h2>Fabrication files</h2><p>')
for f,label in [('pentagon_vertices.svg','Pentagon vertices'),('sheet_01_layout.svg','Main sheet 1'),('sheet_02_layout.svg','Main sheet 2'),('sheet_03_layout.svg','Shared corners'),('offcut_backers_and_optional_corners.svg','Offcut backers and optional corners'),('attachment_template_1to1.svg','1:1 attachment template')]:s.append(f'<a class="button" href="cut-layouts/{f}">{label}</a> ')
s.append('</p><p>')
for f in sorted((O/'printable').glob('*.stl')): s.append(f'<a class="button" href="printable/{f.name}">{f.stem.replace("_"," ")}</a> ')
s.append('</p><p>All STL coordinates are millimetres. The handed brace connectors have separate pipe grooves and internal tie-return tunnels; the brace detail includes a cutaway. Print a fit sample first.</p></main></html>')
(O/'START_HERE.html').write_text('\n'.join(s))
if all((O/f'renders/{f}.png').exists() for f,_ in scenes):
 images=[Image.open(O/f'renders/{f}.png').convert('RGB') for f,_ in scenes]
 images[0].save(O/'Assembly_Views.pdf',save_all=True,append_images=images[1:],resolution=150,quality=94)
 for im in images:im.close()
 print('PDF contains 9 Blender plates')
else:print('Some renders still pending; rerun after render completion')
print('Wrote six SVGs and current HTML index')
with zipfile.ZipFile(O/'FPV_Gate_Kit.zip','w',zipfile.ZIP_DEFLATED,compresslevel=6) as archive:
 for path in sorted(O.rglob('*')):
  if path.is_file() and not any(p.startswith('previous_') for p in path.relative_to(O).parts) and path.suffix not in ['.zip','.log','.blend1']:
   archive.write(path,Path('FPV_Gate_Kit')/path.relative_to(R))
 for name in ['build_gate.py','validate_layout.py','package_deliverables.py']:
  archive.write(R/'scripts'/name,Path('FPV_Gate_Kit/scripts')/name)
 archive.write(R/'README.md','FPV_Gate_Kit/README.md')
print('Packaged current model, fabrication files, views and generation scripts')

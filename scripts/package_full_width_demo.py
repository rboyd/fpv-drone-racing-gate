from pathlib import Path
import json,zipfile,html
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph,Table,TableStyle
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import HexColor
O=Path(__file__).resolve().parents[1]/'output/full_width_demo';r=json.loads((O/'print_checks.json').read_text())
style=ParagraphStyle('body',fontName='Helvetica',fontSize=12,leading=17,textColor=HexColor('#18324a'))
c=canvas.Canvas(str(O/'Assembly_and_Print_Queue.pdf'),pagesize=(900,600));c.setTitle('24-inch paper-frame demo: print queue and assembly')
def title(t):c.setFont('Helvetica-Bold',26);c.setFillColor(HexColor('#18324a'));c.drawString(42,548,t)
def para(t,y):
 p=Paragraph(t,style);_,h=p.wrap(810,500);p.drawOn(c,42,y-h);return y-h-16
def table(rows,y,widths):
 t=Table(rows,colWidths=widths);t.setStyle(TableStyle([('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),('BACKGROUND',(0,0),(-1,0),HexColor('#dae6ed')),('FONTSIZE',(0,0),(-1,-1),11),('TOPPADDING',(0,0),(-1,-1),9),('BOTTOMPADDING',(0,0),(-1,-1),9),('LINEBELOW',(0,0),(-1,-1),.5,HexColor('#c4d0d8'))]));_,h=t.wrap(810,500);t.drawOn(c,42,y-h);return y-h-18
title('Queue a real 24-inch-wide demonstration')
y=para('The assembled sample is <b>609.6 x 203.2 mm / 24 x 8 inches</b>. It demonstrates releasable click joints, four crossmembers and magnetic paper retention across the full roll width.',506)
rows=[['A1 Mini / PETG plate','Runs','PETG per run','Time per run']]
for name,count in [('00_FIT_CHECK',1),('01_FRAME_REPEAT_4_TIMES',4),('02_KEYS_AND_PADS_ONCE',1)]:
 p=r['slices'][name];rows.append([name,str(count),f"{p['grams']:.1f} g",f"{round(p['minutes'])} min"])
y=table(rows,y,[440,65,135,170])
y=para('<b>Frame kit:</b> 211.3 g and about 9 h 24 min, across five manual plate runs. With fit check: 227.3 g and about 10 h 12 min, six runs. No job has been sent to a printer.',y)
y=para('<b>Start small:</b> check the fit first. Then one repeat plate makes an I-shaped bay using two edge rails, one rung and two keys, with two magnetic pads. Print the other three repeats and the final keys/pads plate after that behaves well.',y)
y=table([['Main part','Quantity'],['DEMO_EDGE - identical edge rails with integral lugs','8'],['DEMO_RUNG - identical crossmembers','4'],['CLICK_KEY - shared connectors','14'],['PAPER_PAD - magnetic front pads','16']],y,[680,130])
c.setFont('Helvetica',10);c.drawString(42,30,'Four main types / 42 pieces. Add 32 magnets (6 x 2 mm), retaining adhesive and one 24 x 8 inch paper sheet.');c.showPage()
title('Assembly and first checks')
y=506
for t in [
 '<b>1. Check fit:</b> the final frame uses the 0.40 mm socket clearance. Rigid guides and both spring tips must engage together. Pinch the tips and withdraw straight. Keep the two fit-check receiver variants identified by their Bambu object names.',
 '<b>2. Make two long edges:</b> four identical edge rails and three keys per edge. Point all D lugs toward the inside. The assembled length is 4 x 141.9 + 3 x 14 = 609.6 mm.',
 '<b>3. Connect four crossmembers:</b> put a key at both ends of every rung. Attach them to the four perpendicular sockets on one long edge. Work the opposite long edge onto all four free keys evenly, with its lugs facing inward.',
 '<b>4. Attach paper:</b> check magnet polarity and fit before bonding. Sixteen magnets go into the integral rail holders; sixteen go into the removable pads. Let the adhesive cure. Paper lies against the smooth front face, opposite the open latches; pads go on the front of the paper.',
 '<b>5. Observe behavior:</b> handle the full-width frame, check sag and joint play, peel and slide the paper gently, and compare retention with alternate pads removed. Repeatedly release a few joints and inspect the spring roots and hooks.',
 '<b>Digital checks:</b> all supplied masters and plates fit the A1 Mini. All ten slices have supports disabled and no warnings. The assembled geometry and representative mating interfaces were checked digitally; physical fit, repeated release and magnetic grip remain untested.',
 '<b>Scope:</b> this is a ladder-shaped demonstration, not a complete gate border or a wind-rated assembly. It has no dedicated PVC-dock interface. The sacrificial stacks and PVC dock remain separate optional experiments.'
]:y=para(t,y)
c.setFont('Helvetica',10);c.drawString(42,30,'Read README.md for print settings, magnet gauge interpretation, detailed assembly and verification limits.');c.showPage()
for p in sorted((O/'renders').glob('*.png')):c.drawImage(str(p),0,0,900,600);c.showPage()
c.save()
links=''
for name,count in [('00_FIT_CHECK',1),('01_FRAME_REPEAT_4_TIMES',4),('02_KEYS_AND_PADS_ONCE',1)]:
 p=r['slices'][name];links+=f'<tr><td><a href="sliced/{name}/{name}_A1Mini_PETG.3mf">{name}</a></td><td>{count}</td><td>{p["grams"]:.1f} g</td><td>{p["minutes"]:.0f} min</td></tr>'
figs=''.join(f'<img src="renders/{p.name}" alt="{html.escape(p.stem)}">' for p in sorted((O/'renders').glob('*.png')))
(O/'index.html').write_text('''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>24-inch paper frame demonstration</title><style>body{background:#f3f6f8;color:#19334a;font:17px/1.55 system-ui;margin:40px auto;max-width:1150px;padding:0 24px}a{color:#006b98}img{width:100%;margin:20px 0}table{border-collapse:collapse;background:white;width:100%}td,th{padding:12px;border-bottom:1px solid #ccd6df;text-align:left}aside{background:#fff1da;padding:18px}h1{line-height:1.15}</style><h1>Print a real 24 × 8 inch paper-frame specimen</h1><p>Four main part types, 42 pieces. Click joints connect the long edges and crossmembers. Integral D-shaped holders and removable pads sandwich the paper using 32 magnets.</p><p><a href="Full_Width_Demo.blend">Blender assembly</a> · <a href="Assembly_and_Print_Queue.pdf">Print queue and assembly PDF</a> · <a href="README.md">Detailed instructions</a> · <a href="Full_Width_Demo_Kit.zip">Download kit</a></p><table><tr><th>Sliced A1 Mini / PETG plate</th><th>Runs</th><th>PETG/run</th><th>Time/run</th></tr>'''+links+'''</table><p><b>Five frame plate runs:</b> 211.3 g, about 9 h 24 min. Including the fit check: 227.3 g, about 10 h 12 min. Manual plate clearing is required between runs; no job has been sent.</p><aside>Check click fit first. One repeat plate makes a small I-shaped bay; finish the remaining runs after testing it. This specimen tests full-width handling and paper attachment, not the stability of an outdoor gate. Stack coupons and the PVC dock are separate experiments.</aside>'''+figs+'''<p><a href="BOM.csv">Exact quantities</a> · <a href="print_checks.json">Digital checks</a>. 0.4 mm nozzle, 0.2 mm layers, Generic PETG, textured PEI, 3 walls, 15% infill, supports off. All ten prepared slices are warning-free.</p></html>''')
with zipfile.ZipFile(O/'Full_Width_Demo_Kit.zip','w',zipfile.ZIP_DEFLATED) as z:
 for p in O.rglob('*'):
  if not p.is_file() or p.name.endswith(('.zip','.blend1','.log','.gcode')):continue
  if 'sliced' in p.parts and p.suffix!='.3mf':continue
  z.write(p,Path('output/full_width_demo')/p.relative_to(O))
 for name in ['build_full_width_demo.py','slice_full_width_demo.py','validate_full_width_demo.py','package_full_width_demo.py','build_paper_roll_study.py','build_a1_full_size.py','build_gate.py','face_geometry.py']:
  z.write(O.parents[1]/'scripts'/name,Path('scripts')/name)
print('Packaged 6-page instructions, local index and prototype kit.')

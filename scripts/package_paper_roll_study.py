"""Publish a local illustrated study, review PDF and experimental print package."""
from pathlib import Path
import json,html,zipfile
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph,Table,TableStyle
ROOT=Path(__file__).resolve().parents[1];O=ROOT/'output/paper_roll_study'
checks=json.loads((O/'print_checks.json').read_text());slices=checks['slices']
photos=sorted((O/'renders').glob('*.png'))
labels={
 '01_PAPER_GATE':'Paper layout and three retention strategies',
 '02_CLICK_JOINT':'Replaceable click key and clearance samples',
 '03_MAGNETIC_SPLICE':'Magnet-held structural splice alternative',
 '04_PAPER_MAGNET_STACK':'Magnetic paper sandwich and skin thickness',
 '05_MECHANICAL_PAPER_CLAMP':'Magnet-free snap-over batten',
 '06_NO_TIE_PVC_COLLAR':'Bolted PVC collar halves',
 '07_DIAGONAL_STACK':'Eight 220 mm rails stacked vertically',
 '08_STACK_COUPONS':'Short separation tests',
 '09_A1_DIAGONAL_ENVELOPE':'Diagonal bed-fit calculation',
 '10_PICTURE_FRAME_REFERENCE':'Tony Youngblood picture-frame reference',
 '11_BRACING_COMPARISON':'Ladder, alternating diagonals and crosshatch',
 '12_HALF_CYLINDER_LUG':'Half-cylinder magnet holder',
 '13_FRAME_TO_PVC':'Assembled and exploded PVC quick-release dock',
 '14_GATE_BACKING_AND_LOAD_PATH':'Rear frame, triangulation and proposed docks',
 '15_TWO_STACKS_OVERNIGHT':'26-rail overnight manufacturing trial'}
# Two review pages, then all native Blender presentation renders.
c=canvas.Canvas(str(O/'Paper_Roll_Study.pdf'),pagesize=(900,600));c.setTitle('Paper-roll FPV gate: click joints, magnets and diagonal stacks');c.setAuthor('FPV gate design study; reference model by Tony Youngblood, CC BY-SA 4.0')
style=ParagraphStyle('body',fontName='Helvetica',fontSize=12,leading=17,textColor=HexColor('#24364b'))
def title(t,sub):
 c.setFillColor(HexColor('#142b43'));c.setFont('Helvetica-Bold',27);c.drawString(42,548,t)
 c.setFont('Helvetica',11);c.drawString(42,523,sub)
def para(t,y):
 p=Paragraph(t,style);_,h=p.wrap(810,500);p.drawOn(c,42,y-h);return y-h-14
def table(rows,y,widths):
 t=Table(rows,colWidths=widths);t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),HexColor('#173750')),('TEXTCOLOR',(0,0),(-1,0),HexColor('#ffffff')),('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),('FONTSIZE',(0,0),(-1,-1),11),('BOTTOMPADDING',(0,0),(-1,-1),9),('TOPPADDING',(0,0),(-1,-1),9),('ROWBACKGROUNDS',(0,1),(-1,-1),[HexColor('#e9f0f4'),HexColor('#f5f7f9')])]));_,h=t.wrap(810,500);t.drawOn(c,42,y-h);return y-h-18
title('Paper-roll gate / design comparison','Baseline commit 732f592  |  New experimental branch: iteration/paper-roll-click-magnet')
y=para('<b>Preferred trial:</b> positive mechanical click joints, alternating diagonal webs, and removable magnetic paper pads. One PVC backing square and four corner braces remain the backbone.',492)
y=para('<b>Approved layout:</b> four identical 2090.4 x 609.6 mm paper strips, 2700 mm outside and 1480.8 mm opening. Three gates plus spare paper per 100-foot roll. Four rigid borders travel with their paper attached.',y)
y=table([['Arrangement','Members per border','Main tradeoff'],['Ladder','12.64 m','Lowest material; depends on joint stiffness'],['Alternating diagonals','19.81 m','Triangles resist racking; preferred trial'],['Full crosshatch','26.98 m','36% more length than alternating; crossing nodes']],y,[205,175,430])
y=para('<b>Cost caution:</b> at 150 mm maximum edge-pad spacing plus middle pads, the gate uses 168 clamp pairs / 336 magnets. At an assumed $0.20 per magnet that is $67.20, before plastic and PVC. At 300 mm spacing the trial count is 192 magnets. Holding and paper flutter need testing.',y)
y=para('The heavy 12 mm diamond sample would use roughly 4.5 kg for all members in the alternating layout, before nodes. Lighter webs and a sparser structure need testing; a one- or two-spool finished gate is not established.',y)
c.setFont('Helvetica',10);c.drawString(42,32,'Detailed assembly, costs, sources and limitations: STUDY_AND_TEST_GUIDE.md, RESEARCH.md, PRINT_STRATEGY.md');c.showPage()
title('Print the interfaces before the gate','25 experimental STL variants, not 25 required production part types. No printer job has been sent.')
y=para('<b>Start with plate 05:</b> seven pieces test the D-shaped magnetic holder and complete PVC dock. Add a paper scrap, two 6 x 2 mm magnets and actual 33.4 mm OD PVC. The dock needs four M3x25 and two M3x16 bolts, six nuts and twelve washers.',492)
rows=[['Plate / experiment','PETG','Slicer estimate']]
for name in ['05_D_MAGNET_AND_DOCK','01_CLICK_AND_MAGNET_JOINTS','03_STACK_SEPARATION_TESTS','DIAGONAL_8x220','06_OVERNIGHT_26_RAILS']:
 p=slices[name];rows.append([name,f"{p['PETG_g']:.1f} g",f"{int(round(p['minutes']))//60} h {int(round(p['minutes']))%60:02d} min"])
y=table(rows,y,[475,115,220])
y=para('<b>Diagonal batch:</b> two stacks of thirteen 198 mm rails fit 169.7 x 169.7 x 161.8 mm. They are plain manufacturing samples, without final rail-end joints. Test short stacks before the overnight plate.',y)
y=para('<b>Stack findings:</b> 0.4 mm necks vanished in the standard slicer profile. Current continuous trials use 0.6 and 0.8 mm; every neck layer has extrusion. End tabs removed an initial cantilever warning. All current slices have supports off and no warnings; physical bridging and PETG separation remain untested.',y)
y=para('<b>Verified digitally:</b> 25 manifold masters, 31 actual A1 Mini/PETG slices and 20 assembled-pair interference checks. The gate overview is schematic; production corner/diagonal nodes and brace interfaces remain to be integrated after measured fit tests.',y)
c.setFont('Helvetica',10);c.drawString(42,32,'Source picture-frame scene: Tony Youngblood, CC BY-SA 4.0. See reference/picture_frame/ATTRIBUTION.md.');c.showPage()
for p in photos:
 c.bookmarkPage(p.stem);c.addOutlineEntry(labels[p.stem],p.stem,level=0);c.drawImage(str(p),0,0,900,600);c.showPage()
c.save()
# Local HTML review: links and figures work without a server or internet access.
rows=''
for name in ['05_D_MAGNET_AND_DOCK','01_CLICK_AND_MAGNET_JOINTS','02_PAPER_CLAMP_TESTS','03_STACK_SEPARATION_TESTS','04_PVC_COLLAR_TEST','DIAGONAL_1x220','DIAGONAL_8x220','06_OVERNIGHT_26_RAILS']:
 p=slices[name];link=f'sliced/{name}/{name}_A1Mini_PETG.3mf'
 rows+=f'<tr><td><a href="{link}">{name}</a></td><td>{p["PETG_g"]:.1f} g</td><td>{p["minutes"]:.0f} min</td><td>{"Experimental overhang warning" if p["warning"] else "No slicing warning"}</td></tr>'
figs=''.join(f'<figure id="{p.stem}"><img loading="lazy" src="renders/{p.name}" alt="{html.escape(labels[p.stem])}"><figcaption>{html.escape(labels[p.stem])}</figcaption></figure>' for p in photos)
nav=''.join(f'<a href="#{p.stem}">{p.stem[:2]} {html.escape(labels[p.stem])}</a>' for p in photos)
(O/'index.html').write_text('''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Paper-roll FPV gate study</title><style>body{margin:0;background:#f2f5f7;color:#18324a;font:16px/1.55 system-ui,sans-serif}main{max-width:1150px;margin:40px auto;padding:0 24px}h1{font-size:38px;line-height:1.15}a{color:#0b618c}nav{display:flex;flex-wrap:wrap;gap:8px}nav a{padding:7px 12px;background:white;border:1px solid #b9cbd6;border-radius:8px;text-decoration:none;font-size:13px}figure{margin:30px 0;background:white;border-radius:12px;overflow:hidden;scroll-margin-top:16px}img{display:block;width:100%}figcaption{padding:10px 20px}table{width:100%;border-collapse:collapse;background:white;font-size:14px}th,td{padding:12px;text-align:left;border-bottom:1px solid #d5e0e7}.note{background:#fff3df;border-left:5px solid #ed922c;padding:15px 22px}.links{font-size:18px}code{font-size:.9em}</style><main><p>FPV RACING GATE / EXPERIMENTAL ITERATION</p><h1>Paper face, click frame and magnetic clamps</h1><p>Four identical 2090.4 × 609.6 mm strips. One PVC back. Compare three bracing layouts, reversible joints and diagonal break-apart print stacks.</p><p class="links"><a href="Paper_Roll_Joinery_Study.blend">Open Blender model</a> · <a href="Paper_Roll_Study.pdf">Visual study PDF</a> · <a href="STUDY_AND_TEST_GUIDE.md">Assembly and test guide</a> · <a href="Paper_Roll_Study_Kit.zip">Download study kit</a></p><p><b>Preferred trial:</b> mechanical click joints + alternating diagonal webs + magnetic paper pads. Magnets can dominate cost: 336 discs at the pictured spacing. See the guide for wider spacing and magnet-free retention.</p><p class="note"><b>Experimental parts, not a production gate kit.</b> Gate rails and full-gate dock sites are schematic. The exact exported interfaces fit the A1 Mini and have been sliced, but physical strength, latch fatigue, magnet grip and PETG stack separation have not been tested. The source picture-frame meshes are reference-only.</p><h2>Start with the seven-piece D-lug and PVC dock plate</h2><p>Use plate 05 for the latest concept. A second optional test is the small stack plate. Do not print all 25 variants: they include clearance comparisons and alternative processes.</p><table><tr><th>Sliced A1 Mini / PETG project</th><th>Material</th><th>Time</th><th>Notes</th></tr>'''+rows+'''</table><p>0.4 mm nozzle, 0.2 mm layers, 3 walls, 15% infill, textured PEI; supports off. No job has been sent to a printer. Source STLs/3MFs: <a href="printable/">printable folder</a>. <a href="print_checks.json">Digital checks</a> · <a href="PRINT_STRATEGY.md">Stack findings</a> · <a href="RESEARCH.md">Research</a>.</p><h2>Explore the Blender views</h2><nav>'''+nav+'</nav>'+figs+'''<p>Baseline committed as <code>732f592</code>; new work on <code>iteration/paper-roll-click-magnet</code>. The embedded picture-frame reference is by Tony Youngblood, CC BY-SA 4.0; <a href="../../reference/picture_frame/ATTRIBUTION.md">attribution and license</a>. Test-coupon geometry is newly modeled.</p></main></html>''')
# Include only complete useful delivery files; gcode remains inside sliced 3MF projects.
with zipfile.ZipFile(O/'Paper_Roll_Study_Kit.zip','w',zipfile.ZIP_DEFLATED) as z:
 for p in O.rglob('*'):
  if not p.is_file() or p.name.endswith(('.zip','.blend1','.log','.gcode')):continue
  if 'sliced' in p.parts and p.suffix!='.3mf':continue
  z.write(p,Path('output/paper_roll_study')/p.relative_to(O))
 for p in (ROOT/'reference/picture_frame').iterdir():
  if p.is_file():z.write(p,Path('reference/picture_frame')/p.name)
 for name in ['build_paper_roll_study.py','render_paper_roll_study.py','slice_paper_roll_study.py','check_paper_assemblies.py','validate_paper_roll_study.py','package_paper_roll_study.py','build_a1_full_size.py','build_gate.py','face_geometry.py']:
  z.write(ROOT/'scripts'/name,Path('scripts')/name)
print('Packaged',len(photos),'Blender views;',len(photos)+2,'PDF pages.')

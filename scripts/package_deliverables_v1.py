from pathlib import Path
import json, html, csv, zipfile
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]; O=ROOT/'output'
layout=json.loads((O/'cut-layouts/nesting.json').read_text())
colors={'Face':'#245aca','Stile':'#245aca','Cap':'#4875d2','Splice':'#bdd5e7','Joint':'#bdd5e7','Return':'#dce9ed'}
for sheet in [1,2,3]:
 parts=[r for r in layout if r['sheet']==sheet]
 svg=['<svg xmlns="http://www.w3.org/2000/svg" width="280mm" height="150mm" viewBox="0 0 2800 1500">', '<rect width="2800" height="1500" fill="white"/>',f'<text x="100" y="65" font-family="Arial" font-size="44" font-weight="bold">SHEET {sheet} / 2438.4 x 1219.2 mm / DRAWING SCALE 1:10</text>', '<rect x="100" y="140" width="2438.4" height="1219.2" fill="#e2eddf" stroke="#26374b" stroke-width="3"/>']
 for r in parts:
  x,y=100+r['y'],140+r['x']; w,h=r['h'],r['w']; key=next((k for k in colors if r['name'].startswith(k)), 'Face')
  fill=colors[key]; ink='white' if key in ['Face','Stile','Cap'] else '#13273e'
  svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="#18314d" stroke-width="2"/>')
  if key=='Splice':
   svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="75" fill="#ffb78c" stroke="#d45d16" stroke-dasharray="8 6" stroke-width="2"/>')
  if key=='Joint':
   svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="40" fill="#ffb78c" stroke="#d45d16" stroke-dasharray="8 6" stroke-width="2"/>')
  if key=='Return':
   svg.append(f'<line x1="{x}" y1="{y+30}" x2="{x+w}" y2="{y+30}" stroke="#db6617" stroke-width="3" stroke-dasharray="10 6"/>')
  label=f"{r['h']} x {r['w']}"; label2={'Face':'MAIN','Stile':'STILE','Cap':'CAP','Splice':'BACKER','Joint':'JOINT','Return':'RETURN'}[key]
  fs=27 if w>=180 else 22
  svg.append(f'<text x="{x+w/2}" y="{y+h/2-12}" text-anchor="middle" fill="{ink}" font-family="Arial" font-size="{fs}">{label2}</text>')
  svg.append(f'<text x="{x+w/2}" y="{y+h/2+26}" text-anchor="middle" fill="{ink}" font-family="Arial" font-size="{fs}">{label}</text>')
 notes={1:'Knife cuts. Two 600 mm strips; trim length to 2400. Green = spare. Confirm actual stock size.',2:'Orange trim: 75 mm from 600 x 180 backers; 40 mm from 600 x 150 joint backers. Trim the end matching assembly.',3:'Orange dashed line: 30 mm outward flange. 256 mm wall + 4 mm face = 260 mm body. Calibrate a sample fold.'}
 svg.append(f'<text x="100" y="1430" font-family="Arial" font-size="27" fill="#24394d">{html.escape(notes[sheet])}</text>');svg.append('</svg>')
 (O/f'cut-layouts/sheet_{sheet:02}_layout.svg').write_text('\n'.join(svg))
# Exact print-scale slot template, usable as a handheld marking jig.
svg=['<svg xmlns="http://www.w3.org/2000/svg" width="180mm" height="120mm" viewBox="0 0 180 120">','<rect width="180" height="120" fill="white"/>','<g font-family="Arial" fill="#152c43">','<text x="10" y="12" font-size="5" font-weight="bold">SADDLE / WASHER SLOT TEMPLATE — 1:1</text>','<text x="10" y="21" font-size="3.3">Print at 100%. Verify the 50 mm scale bar before marking.</text>','<rect x="30" y="37" width="60" height="40" fill="none" stroke="black" stroke-width=".25"/>']
for x in [-23,23]:
 for y in [-10,10]: svg.append(f'<rect x="{60+x-1.6}" y="{57+y-3}" width="3.2" height="6" fill="#888" stroke="black" stroke-width=".2"/>')
svg += ['<line x1="60" y1="31" x2="60" y2="83" stroke="#999" stroke-width=".2" stroke-dasharray="2 1"/>','<text x="99" y="42" font-size="3.5">60 x 40 footprint</text>','<text x="99" y="50" font-size="3.5">Slots: 3.2 x 6 mm</text>','<text x="99" y="58" font-size="3.5">Centers: +/-23, +/-10</text>','<text x="99" y="66" font-size="3.5">Dashed line = pipe axis</text>','<path d="M30 90 v5 M30 93 h50 M80 90 v5" fill="none" stroke="black" stroke-width=".4"/>','<text x="49" y="101" font-size="4">50 mm</text>','<text x="10" y="113" font-size="3.2">Use a scrap pad behind the face; keep tie heads on the rear. Do not crush the flutes.</text>','</g></svg>']
(O/'cut-layouts/attachment_template_1to1.svg').write_text('\n'.join(svg))
scenes=[('01_ASSEMBLED','Grass / assembled'),('02_REAR_STRUCTURE','Rear structure'),('03_EXPLODED','Exploded assembly'),('04_SHEET_LAYOUT','Sheet layout'),('05_CLIP_DETAIL','Printed attachment'),('06_DIMENSIONS','Dimensions'),('07_HARD_SURFACE','Hard surface / ballasted')]
style='''*{box-sizing:border-box}body{margin:0;background:#f4f5f3;color:#142d43;font:16px/1.55 -apple-system,BlinkMacSystemFont,Arial,sans-serif}header,main{max-width:1250px;margin:auto;padding:32px}h1{font-size:48px;line-height:1.1;margin:14px 0}h2{margin-top:40px}p{max-width:850px}a{color:#174eb9}nav{display:flex;flex-wrap:wrap;gap:8px;margin:26px 0}nav a,.button{display:inline-block;border:1px solid #b5c3d2;border-radius:6px;padding:8px 12px;text-decoration:none;background:white}.primary{background:#1648b1;color:white;border-color:#1648b1}figure{margin:22px 0 40px}figure img{display:block;width:100%;border:1px solid #c5cdd2;border-radius:9px}figcaption{padding:8px 0;color:#4b6073}table{border-collapse:collapse;width:100%;margin:20px 0}th,td{text-align:left;border-bottom:1px solid #ced6de;padding:12px}.note{border-left:4px solid #df7929;padding:12px 20px;background:white}small{color:#566b7c}@media(max-width:650px){header,main{padding:20px}h1{font-size:34px}}@media print{nav,.downloads{display:none}figure{break-inside:avoid;page-break-before:always}}'''
page=['<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>FPV Gate 2700 — build package</title>',f'<style>{style}</style><header><small>FIELDWORK / FPV RACING GATE</small><h1>2700 mm. One face.<br>Two surface setups.</h1><p>A 1500 mm square clear opening, 260 mm deep. Two sheets form the face; a third forms the folded opening walls. Supported 2400 + 300 mm splices solve the 8-foot stock limit.</p><div class="downloads"><a class="button primary" href="FPV_Gate_2700.blend">Open Blender model</a> <a class="button" href="BUILD_GUIDE.md">Build guide</a> <a class="button" href="Assembly_Views.pdf">Assembly views PDF</a> <a class="button" href="BOM.csv">Grass BOM</a> <a class="button" href="HARD_SURFACE_ADD_ON.csv">Hard-surface add-on</a></div><nav>']
page += [f'<a href="#{f}">{label}</a>' for f,label in scenes];page+=['</nav></header><main>','<table><thead><tr><th>Shared gate</th><th>Grass / soil</th><th>Hard surface</th></tr></thead><tbody><tr><td>3 sheets, 1-inch PVC frame,<br>¾-inch corner braces,<br>20 printed saddle/washer pairs</td><td>1200 mm feet<br>4 opposing guy stakes<br>About $242</td><td>2400 mm feet<br>4 guys tied to ballasted foot ends<br>4 × 15 kg bags</td></tr></tbody></table><p>Dual-surface kit: approximately <strong>$299 before tax, shipping and ballast fill</strong>, using the explicit allowances in the guide. Face sits 50 mm above ground so the feet pass below it.</p><p class="note">Digital design and manifold STLs checked. Physical fit, sheet folds, anchors and wind response remain prototype checks. No wind rating is asserted; 60 kg ballast is a starting test configuration.</p>']
for f,label in scenes: page += [f'<figure id="{f}"><a href="renders/{f}.png"><img src="renders/{f}.png" alt="{label}" loading="lazy"></a><figcaption>{label} — also available as an editable Blender scene.</figcaption></figure>']
page += ['<h2>Fabrication files</h2><p><a href="PVC_CUT_LIST.csv">PVC cuts</a> · <a href="cut-layouts/sheet_01_layout.svg">Sheet 1</a> · <a href="cut-layouts/sheet_02_layout.svg">Sheet 2</a> · <a href="cut-layouts/sheet_03_layout.svg">Sheet 3</a> · <a href="cut-layouts/attachment_template_1to1.svg">1:1 slot template</a></p><p><a href="printable/saddle_1in_OD33p40_mm.stl">1-inch saddle STL</a> · <a href="printable/front_load_washer_mm.stl">Front washer STL</a> · <a href="printable/optional_saddle_3_4in_OD26p67_mm.stl">Optional ¾-inch saddle STL</a></p><p>STL units are millimetres. Print one fit sample before making the set. The build guide includes fitting engagement corrections, assembly steps, wind-load assumptions, cost allowances, and review of the teammate’s WIP.</p></main></html>']
(O/'START_HERE.html').write_text('\n'.join(page))
# PDF of all Blender plates, as a portable assembly reference.
if all((O/f'renders/{f}.png').exists() for f,_ in scenes):
 ims=[Image.open(O/f'renders/{f}.png').convert('RGB') for f,_ in scenes]
 ims[0].save(O/'Assembly_Views.pdf',save_all=True,append_images=ims[1:],resolution=150,quality=94)
 for im in ims: im.close()
 print('PDF: 7 assembly plates')
else: print('Renders still pending; rerun packaging after Blender finishes')
print('Wrote SVG layouts, 1:1 template and HTML index')

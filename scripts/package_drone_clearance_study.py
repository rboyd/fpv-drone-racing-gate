"""Package the measured Blender sizing study. Requires reportlab."""
from pathlib import Path
import json, html
from reportlab.pdfgen import canvas
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph, Table, TableStyle
from reportlab.lib.colors import HexColor

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'output/drone_clearance_study'
d = json.loads((OUT / 'clearance.json').read_text())
rows = d['variants']
for r in rows:
    assert abs(r['outer_mm'] - r['opening_mm'] - 1219.2) < 1e-6
    assert abs(2*r['left_right_clearance_mm'] + d['main_envelope_mm'][0] - r['opening_mm']) < 1e-6
    assert abs(2*r['top_bottom_clearance_mm'] + d['main_envelope_mm'][1] - r['opening_mm']) < 1e-6
    assert r['level_worst_yaw_side_clearance_mm'] > 0

table = '\n'.join(f"| {r['opening_mm']:.1f} | {r['outer_mm']:.1f} | {r['left_right_clearance_mm']:.0f} | {r['top_bottom_clearance_mm']:.0f} | {r['level_worst_yaw_side_clearance_mm']:.0f} |" for r in rows)
cuts = '\n'.join(f"| {r['opening_mm']:.1f} | 8 × {r['long_pvc_cut_mm']:.1f} | 2 × {r['outer_mm']:.1f} | 2 × {r['opening_mm']+72:.1f} |" for r in rows)
readme = f'''# MK4 7-inch drone / gate size study

The downloaded STEP assembly measures **401.3 mm across its full propeller sweep**. The current 1480.8 mm square opening leaves **539.8 mm on each side** when centered and approaching straight. A **1000 mm opening** is the suggested next trial: 299.4 mm per side and 54.4% less opening area. The 800 mm version is a tighter alternative, with 199.4 mm per side. These are geometry comparisons; approach speed, attitude and pilot accuracy determine the flying challenge.

![Drone centered in the current gate](renders/01_CURRENT_GATE_PASS.png)

[Open the Blender study](Drone_Clearance_Study.blend) · [Visual PDF](Drone_Clearance_Study.pdf) · [Render gallery](index.html) · [CSV measurements](Clearance_Comparison.csv) · [Raw calculations](clearance.json)

## Equal-scale comparison

![Four opening sizes with the same drone](renders/04_OPENING_DETAIL.png)

All dimensions below are millimetres. Main pose: **20° forward pitch, zero yaw and roll**, with the projected swept envelope centered. Side and vertical values are gaps **per edge**, not total spare space. The outer dimensions retain 609.6 mm / 24-inch paper bands.

| Square opening | Outer square | Left / right gap | Top / bottom gap | Minimum side gap over level yaw |
|---:|---:|---:|---:|---:|
{table}

The last column considers the propeller envelope over every yaw angle with the drone level. It is a separate case, not a bound for every possible flight attitude. At 45° yaw, 30° roll and 20° pitch, the example envelope is **392 × 279 mm** in the gate plane; see scene 07. Centering means centering the projected envelope, which can differ from centering the flight controller.

## What was measured

- Imported the actual 119-component STEP assembly from the user-supplied ZIP; preserved dimensions and applied only unit conversion and upright orientation.
- Motor diagonal: **294.3 mm**. The manufacturer lists a nominal 295 mm wheelbase for its [Mark4-7](https://geprc.com/product/gep-mark4-frame/); this is a cross-check, not certification that the downloaded assembly matches the user's exact build.
- The downloaded blades reach a **179.9 mm swept diameter**, slightly above nominal seven inches (177.8 mm). Calculations use the larger measured CAD radius and a complete rotating disc at every motor, not the blades' static orientation.
- Main projected envelope: **401.3 mm wide × 169.7 mm high**, including the supplied antenna/camera geometry and an explicitly assumed **110 × 40 × 45 mm battery** with straps. The download has no battery. A different battery, antenna or propeller can change the result.
- Blender mesh tessellation uses a 0.4 mm deflection setting. Numbers are suitable for a sizing study, not submillimetre inspection. Clearances are to nominal paper opening edges, without flight error, paper flutter or structural deflection allowances.
- Cyan circles illustrate swept propeller boundaries; they are not physical guards. Feet, ground anchors and guys are omitted from these clearance views.

## How the smaller gates reuse the current parts

All four scenes retain the same **64 fittings / five part types**, accepted 33.5 mm bores, actual PVC diameter and 24-inch paper bands. For a size change, replace the eight long PVC members and shorten the paper; the sixteen 389.6 mm PVC members remain. Four sleeves per long member remain in this comparison. Print quantities and slicer estimates therefore stay unchanged; later sleeve optimization is separate work.

| Opening | Long PVC cuts | Top + bottom paper lengths | Side paper lengths |
|---:|---:|---:|---:|
{cuts}

All paper strips are 609.6 mm wide. Side strips include 36 mm overlap at each end. Pipe lengths retain the production design's 30 mm socket engagement and center offsets. This is a study cut schedule, not a replacement for the current production kit: dry-fit and verify assembled opening dimensions before batch cutting.

## Blender views

1. `01_CURRENT_GATE_PASS` — current full gate and drone at crossing.
2. `02_CURRENT_CLEARANCE` — straight-on dimensions to the paper edges.
3. `03_FOUR_OPENINGS` — four complete gates at equal scale.
4. `04_OPENING_DETAIL` — equal-scale opening close-ups; paper bands are cropped for visibility.
5. `05_DRONE_REFERENCE` — enlarged imported assembly, assumed battery and swept props.
6. `06_SMALLER_GATE_PASS` — suggested 1000 mm trial opening.
7. `07_ATTITUDE_COMPARISON` — straight and banked/turned examples in a 1000 mm opening.

Scenes 01 and 06 have a simple translation animation, frames **1–80**, crossing at **40**. This illustrates passage through the opening, not a flight dynamics simulation. The saved Blender file embeds the drone mesh and can be opened without the source ZIP.

## Source, license and reproduction

Drone reference: **Dendy**, [Printable parts for GEPRC MK4 7in FPV drone frame](https://www.printables.com/model/1515387-printable-parts-for-geprc-mk4-7in-fpv-drone-frame), supplied under **CC BY-NC 4.0**. Dendy explicitly disclaims original authorship of the included MK4 frame. See [attribution, license and modifications](../../reference/geprc_mk4/ATTRIBUTION.md) and the [supplied model PDF](../../reference/geprc_mk4/Printables_Model_1515387.pdf). Original gate material retains this project's separate license. No endorsement is implied.

Rebuild from the repository root after installing `cadquery-ocp` (conversion tested with OCP 8) and `reportlab` into an appropriate Python environment:

```sh
python scripts/import_geprc_reference.py --zip ~/Downloads/printable-parts-for-geprc-mk4-7in-fpv-drone-frame-model_files.zip
blender -b -t 8 --python scripts/build_drone_clearance_study.py
python scripts/package_drone_clearance_study.py
```

Conversion intermediates default to `/tmp/fpv-geprc-reference`; the 174 MB source STEP is not copied into this repository. The current production kit remains in `output/corner_guide_elbow/`.
'''
(OUT / 'README.md').write_text(readme)

images = sorted((OUT / 'renders').glob('*.png'))
table_html = '<table><tr><th>Opening</th><th>Outer size</th><th>Side gap</th><th>Vertical gap</th></tr>' + ''.join(f"<tr><td>{r['opening_mm']:.1f} mm</td><td>{r['outer_mm']:.1f} mm</td><td>{r['left_right_clearance_mm']:.0f} mm</td><td>{r['top_bottom_clearance_mm']:.0f} mm</td></tr>" for r in rows) + '</table>'
figures = ''.join(f'<figure><a href="renders/{p.name}"><img loading="lazy" src="renders/{p.name}" alt="{html.escape(p.stem)}"></a><figcaption>{html.escape(p.stem.replace("_", " "))}</figcaption></figure>' for p in images)
(OUT / 'index.html').write_text('''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>MK4 drone / gate clearance study</title><style>body{font:17px/1.6 system-ui;background:#edf1f3;color:#193247;max-width:1200px;margin:40px auto;padding:0 24px}a{color:#066a95}img{width:100%;display:block}figure{margin:32px 0}td,th{padding:10px 20px;border-bottom:1px solid #ccd5db;text-align:left}table{background:white;width:100%}figcaption{font-size:14px}h1{line-height:1.2}</style><h1>7-inch MK4 / four gate sizes</h1><p>The imported drone has a 401.3 mm swept-prop width. Try a 1000 mm opening next: about 299 mm clearance per side when centered and approaching straight, versus 540 mm in the current gate.</p><p><a href="Drone_Clearance_Study.blend">Blender model</a> · <a href="Drone_Clearance_Study.pdf">Visual PDF</a> · <a href="README.md">Measurements and cut schedule</a> · <a href="Clearance_Comparison.csv">CSV</a></p><p>Gaps below are per edge, with 20° forward pitch and no yaw or roll. The 110 × 40 × 45 mm battery is assumed. Cyan circles show full prop sweep, not guards.</p>''' + table_html + figures + '''<p>Reference: Dendy / Printables 1515387, CC BY-NC 4.0; Dendy is not the original creator of the included MK4 frame. <a href="../../reference/geprc_mk4/ATTRIBUTION.md">Attribution and separate component licenses</a>. Geometry study; physical build and flight behavior remain to be tested.</p></html>''')

c = canvas.Canvas(str(OUT / 'Drone_Clearance_Study.pdf'), pagesize=(900,600))
c.setTitle('MK4 7-inch drone / gate clearance study')
c.setAuthor('FPV racing gate project; drone reference Dendy / Printables 1515387')
style = ParagraphStyle('body',fontName='Helvetica',fontSize=12,leading=18,textColor=HexColor('#193247'))
def para(text,y):
    p=Paragraph(text,style); _,h=p.wrap(804,500);p.drawOn(c,48,y-h);return y-h-16
c.setFont('Helvetica-Bold',25);c.drawString(48,548,'One drone, four opening sizes')
y=para('The imported MK4 assembly has a <b>401.3 mm full propeller-sweep width</b>. A <b>1000 mm opening</b> is the suggested next trial, with 299 mm per side on a centered straight approach. The current opening gives 540 mm per side. The 800 mm option is tighter at 199 mm per side.',514)
data=[['Opening (mm)','Outer (mm)','Side gap (mm)','Vertical gap (mm)']]+[[f"{r['opening_mm']:.1f}",f"{r['outer_mm']:.1f}",f"{r['left_right_clearance_mm']:.0f}",f"{r['top_bottom_clearance_mm']:.0f}"] for r in rows]
t=Table(data,colWidths=[180,180,180,210],rowHeights=29)
t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),HexColor('#193247')),('TEXTCOLOR',(0,0),(-1,0),HexColor('#ffffff')),('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),('GRID',(0,0),(-1,-1),.4,HexColor('#c4ced7')),('VALIGN',(0,0),(-1,-1),'MIDDLE')]))
_,h=t.wrap(804,400);t.drawOn(c,48,y-h);y-=h+20
y=para('All gaps are <b>per edge</b>, at 20-degree forward pitch, zero yaw and roll. The projected envelope is centered. Battery dimensions (110 x 40 x 45 mm) are assumed; confirm against your build. These are geometric gaps, not guaranteed flight margins.',y)
y=para('Keep the existing printed fittings and 24-inch paper bands. Replace eight long PVC members: 1560.8 mm current, 1280 mm for 1200 opening, 1080 mm for 1000, or 880 mm for 800. Sixteen short 389.6 mm members remain. Dry-fit before batch cutting. Full methods and paper cuts: accompanying README.md.',y)
para('Drone reference: Dendy / Printables 1515387, CC BY-NC 4.0; the uploader disclaims original authorship of the included MK4 frame. Original gate material retains the separate project license. Cyan rings are prop-sweep envelopes, not physical guards.',y)
c.showPage()
for p in images:
    c.drawImage(str(p),0,0,width=900,height=600,preserveAspectRatio=True,anchor='c');c.showPage()
c.save()
print('Packaged study, seven render pages plus measurement summary; geometric checks passed.')

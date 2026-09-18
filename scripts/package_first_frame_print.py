"""Validate and package the one-plate production-interface prototype."""
from pathlib import Path
import json,zipfile,xml.etree.ElementTree as ET,hashlib,html
from reportlab.platypus import SimpleDocTemplate,Paragraph,Image,PageBreak,Spacer
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib.colors import HexColor
ROOT=Path(__file__).resolve().parents[1];O=ROOT/'output/first_frame_print'
b=json.loads((O/'BOM.json').read_text());report={'plates':{},'production_meshes':{},'physical_test':'Not yet printed or tested'}
for p in b['parts']:
 c=p['code'];d=(O/'printable'/p['file']).read_bytes()
 assert d==(ROOT/'output/sleeve_paper_gate/printable'/p['file']).read_bytes(),c
 report['production_meshes'][c]={'identical_to_gate':True,'sha256':hashlib.sha256(d).hexdigest()}
for name,items in b['plates'].items():
 with zipfile.ZipFile(O/'printable'/f'{name}.3mf') as z:r=ET.fromstring(z.read('3D/3dmodel.model'))
 assert r.get('unit')=='millimeter';boxes=[]
 for ob in r.findall('.//{*}object'):
  vs=[tuple(float(v.get(k)) for k in ['x','y','z']) for v in ob.findall('.//{*}vertex')];lo=[min(v[j] for v in vs) for j in range(3)];hi=[max(v[j] for v in vs) for j in range(3)]
  assert min(lo[:2])>=4.999 and max(hi[:2])<=175.001 and abs(lo[2])<.001 and hi[2]<=180
  boxes.append((lo,hi))
 assert len(boxes)==len(items)
 for i,(lo,hi) in enumerate(boxes):
  for a,c in boxes[i+1:]:assert any(min(hi[j],c[j])-max(lo[j],a[j])<0 for j in range(2))
 dest=O/'sliced'/name;res=json.loads((dest/'result.json').read_text());assert res['return_code']==0 and len(res['sliced_plates'])==1
 sl=res['sliced_plates'][0];assert not sl['warning_message']
 gc=(dest/'plate_1.gcode').read_text()
 for line in ['; enable_support = 0','; brim_type = no_brim','; print_sequence = by layer','; printer_model = Bambu Lab A1 mini','; nozzle_diameter = 0.4','; filament_type = PETG','; wall_loops = 4','; sparse_infill_density = 20%']:assert line in gc,(name,line)
 assert '; FEATURE: Support' not in gc
 with zipfile.ZipFile(dest/f'{name}_A1Mini_PETG.3mf') as z:
  assert z.testzip() is None
  assert any(n.endswith('.gcode') for n in z.namelist())
 report['plates'][name]={'pieces':len(items),'grams':round(sum(f['total_used_g'] for f in sl['filaments']),2),'minutes':round(sl['total_predication']/60,2),'minimum_bed_margin_mm':5,'maximum_height_mm':29,'overlap':False,'supports':False,'slicer_warnings':[],'prepared_3mf':f'sliced/{name}/{name}_A1Mini_PETG.3mf'}
(O/'print_checks.json').write_text(json.dumps(report,indent=2))
a=report['plates']['FIRST_FRAME_TEST'];p=report['plates']['FIRST_FRAME_TEST_WITH_PAD']
def duration(m):
 n=round(m);return f'{n//60} h {n%60:02d} min'
readme=f'''# First frame print: one A1 Mini plate

Print [FIRST_FRAME_TEST_A1Mini_PETG.3mf]({a['prepared_3mf']}): **four pieces, {a['grams']:.2f} g PETG, about {duration(a['minutes'])}**. This is the recommended first run. All parts are full-size production geometry, identical to the current sleeve-gate STLs.

[Illustrated assembly and test PDF](First_Frame_Test.pdf) · [Blender scenes](First_Frame_Print.blend) · [Visual index](index.html) · [Complete test kit](First_Frame_Print_Kit.zip)

| Part | Quantity | Dimensions mm | Purpose |
|---|---:|---|---|
| EDGE_BRANCH | 2 identical | 136.314 x 76 x 29 | Test both end and projecting side receivers |
| CLICK_KEY | 2 identical | 66 x 32 x 5 | One connects the rails; one spare/comparison |
| PAPER_PAD | 0; optional 1 | 24 x 24 x 3 | Optional comparison of paper clamping methods |

The first two rows are the entire recommended print: **two unique types**. The spare key is useful if a hook breaks during testing. Straight and T configurations each use two rails and one key; assemble them one at a time. No magnets, cord, PVC, bolts or adhesive are needed for the click test.

## Optional paper-pad plate

Use [FIRST_FRAME_TEST_WITH_PAD_A1Mini_PETG.3mf]({p['prepared_3mf']}) instead if you also want the pad: **five pieces, {p['grams']:.2f} g, about {duration(p['minutes'])}**. Choose one of the two files, not both. The optional pad adds {p['grams']-a['grams']:.2f} g and approximately {p['minutes']-a['minutes']:.1f} minutes. The frame-side magnet holders are unchanged: the rear magnet stays behind 0.4 mm of plastic. The PVC sleeve retains its peaked roof and is not needed on this first plate.

## Print settings and placement

Open the prepared 3MF as a project in Bambu Studio. Select your actual PETG filament and A1 Mini with 0.4 mm nozzle. The supplied slice uses Generic PETG, 0.20 mm layers, four walls, 20% infill, textured PEI, no supports, no brim, and print by layer. Print one color; render colors only distinguish the parts. The smooth paper faces lie on the bed, with cleat posts upward. Keep the supplied flat orientation and 100% scale. Re-slice if you change filament/profile settings.

The models keep at least 5 mm from every bed edge and have no overlap; maximum height is 29 mm. The keys are rotated 90 degrees within the bed plane, not stood on edge. The tightest model-to-model gap is 1.69 mm; keep print-by-layer rather than sequential object printing. Both variants slice without warnings or support toolpaths. Estimates are from the local Bambu Studio slice; actual filament and elapsed time can vary. No print was sent to the printer.

## 1. Prepare the parts

Let the bed cool and remove the parts. Check for strings or first-layer burrs in the receivers and between the key's two central spring prongs. Remove loose strings/burrs only; do not file away the hook shoulders or thin the prongs to force a fit. Keep the second key untouched as a comparison. Record filament, temperature and any cleanup needed.

## 2. Assemble a straight joint

Place both rails smooth-face down with their side branches pointing the same direction. Align one end of a key with an end receiver. Slide it along the rail axis: its two broad outside runners guide it while the two narrow central prongs flex inward. Keep it flat; do not insert downward from above. Hold close to the joint and press until both hook shoulders have passed the receiver shoulders and returned outward. Check engagement visually; a loud click is not required.

Slide the second rail onto the other half of the key in the same way. The assembled length is 286.63 mm. Both paper faces should share the same plane. Apply a gentle axial hand pull and check that the rails remain latched. Check for obvious looseness and small bending movement while supporting the parts near the joint. Stop if you see whitening or cracking; this is a fit test, not a destructive strength test.

## 3. Release and rebuild as a T

From the open rear of the receiver, press both central hook tips toward the center and slide the rail straight off that end of the key. Release the other end the same way. Do not twist the rail, pry the key upward or bend the whole rail as a lever. If the tips cannot be reached and released comfortably by hand, record that as a design failure rather than forcing the joint.

Insert the same key into one rail's projecting side socket. Connect an end of the other rail to the exposed key at 90 degrees. Keep both smooth faces coplanar. This tests the full gate's actual crossmember interface, although the short test uses a second branch rail in place of a full crossmember. Repeat the pull, play and release checks.

## 4. Repeat and report

Aim for 20 assembly/release cycles in each configuration as an initial screening test. Try the spare key too. Check that both hooks spring back and latch, hand release remains practical, and no new cracks, permanent bending, whitening or increasing play appear. Twenty cycles is a workshop screen, not a fatigue rating. Record which receiver (end or side) is tight/loose, whether one key differs, and photographs of the latch if it fails. Do not scale the whole part to tune clearance; revise the interface after the physical test if needed.

## Optional magnet comparison

Add two 6 x 2 mm magnets and an offcut of the intended paper. Seat one rear magnet in a rail's 6.3 mm pocket, with compatible retaining adhesive if required, observing its cure time. Check attraction before fixing either magnet. The two alternatives are:

- No pad: rear magnet -> unchanged 0.4 mm frame plastic -> paper -> bare front magnet.
- Optional pad: rear magnet -> unchanged 0.4 mm frame plastic -> paper -> 0.4 mm pad plastic -> front magnet in pad.

Use the same front magnet for successive comparisons before bonding it into the optional pad, or use a third magnet to keep both options ready. Compare sliding, peeling, paper marking and ease of removal. The pad spreads contact across a larger area and is easier to handle, but adds a plastic gap. The small plate only tests local grip, not retention of a full paper border.

## After the click test passes

Next print one production RUNG_SLEEVE to test actual PVC fit, then the 609.6 mm-wide braced bay in the [full gate guide](../sleeve_paper_gate/README.md). The four pieces here can be reused; deduct them from the later queue. This plate demonstrates joinery at 1:1 scale; it is not a complete two-foot-wide frame or a wind test. Physical fit, strength and durability remain unverified until you print it.

The current gate BOM and queue label PAPER_PAD as optional: 424 pieces / seven types without pads, or 560 / eight with all 136 pads fitted. All frame-side magnet holders and the peaked sleeve roof remain unchanged.

Rebuild in the repository with scripts/build_first_frame_print.py, scripts/slice_first_frame_print.py, then scripts/package_first_frame_print.py. The build imports the existing production geometry and asserts that its STL exports match the full gate byte-for-byte.
'''
(O/'README.md').write_text(readme)
styles=getSampleStyleSheet();styles.add(ParagraphStyle(name='Body',fontName='Helvetica',fontSize=10,leading=14,spaceAfter=9,textColor=HexColor('#17374c')))
story=[]
def para(s,style='Body'):story.append(Paragraph(s,styles[style]))
def pic(name):story.append(Image(str(O/'renders'/f'{name}.png'),width=510,height=340))
def section(title,body):para(title,'Heading2');para(body)
para('First frame print / A1 Mini','Title');pic('01_FIRST_PLATE')
para(f'<b>Recommended: FIRST_FRAME_TEST_A1Mini_PETG.3mf</b><br/>Two identical EDGE_BRANCH rails + two identical CLICK_KEYs.<br/>{a["grams"]:.2f} g PETG / about {duration(a["minutes"])} / one plate / four pieces.')
para(f'Optional alternative: FIRST_FRAME_TEST_WITH_PAD_A1Mini_PETG.3mf adds one PAPER_PAD. Five pieces / {p["grams"]:.2f} g / {duration(p["minutes"])}. Print one file, not both.')
para('A1 Mini, 0.4 mm nozzle, PETG, 0.20 mm layers, 4 walls, 20% infill, no supports/brim, print by layer. Open as a project; use 100% scale and the supplied flat orientation. Render colors are illustrative; one filament prints everything. Select your actual PETG preset and re-slice if it differs.')
para('5 mm minimum bed margin; 29 mm maximum height. All meshes match the production parts. The second key is a spare/comparison. No extra hardware is needed for this click test.')
story.append(PageBreak());para('1 / Connect the rails end-to-end','Title');pic('02_STRAIGHT_JOINT')
section('Prepare','Cool and remove the print. Clear loose strings and first-layer burrs from the receiver and the two central spring prongs. Preserve the hook shoulders. Keep the spare key untouched for comparison.')
section('Slide and latch','Keep smooth paper faces coplanar and both side branches facing the same direction. Insert the key along the rail axis. The wide outside runners guide it; the central fork flexes inward and springs outward behind the receiver shoulders. Check both hooks at each end. Support close to the joint when pressing.')
section('Check','The straight assembly is 286.63 mm long. Apply a gentle axial hand pull and check for unintended release or obvious play. Check slight bending near the joint. Stop if cracking or whitening appears. Do not use the full rail length as a bending lever.')
story.append(PageBreak());para('2 / Release, then build the T joint','Title');pic('03_PERPENDICULAR_JOINT')
section('Release','Access the central fork from the open back. Press both hook tips inward toward the center and withdraw straight. Repeat at the other end. Do not twist or pry upward. If comfortable hand release is not possible, record the problem instead of forcing it.')
section('Reconfigure','Move the same key into the projecting side receiver of one rail. Attach an end of the second rail at 90 degrees, with both paper faces in the same plane. This is the actual gate crossmember interface. The two configurations are tested successively, not assembled simultaneously.')
section('Repeat','Perform 20 assembly/release cycles in each configuration, then compare the spare key. Record receiver tightness, release access, increasing play, whitening, cracking or permanent prong bending. Success means both hooks latch reliably and release by hand without damage. This is an initial screen, not a strength or fatigue rating.')
story.append(PageBreak());para('3 / Alignment and optional magnet test','Title');pic('04_JOINT_EXPLODED')
para('Slide the guides along the rail axis; do not push the key down from above. Test results should identify whether an end receiver, side receiver or particular key needs adjustment. Keep all parts at 100% scale.')
section('Paper pads are optional','For a local paper-grip comparison, add two 6 x 2 mm magnets and paper. Check polarity before fixing magnets with compatible adhesive. Without a pad: rear magnet / <b>unchanged 0.4 mm frame skin</b> / paper / bare front magnet. With a pad: rear magnet / frame skin / paper / 0.4 mm pad skin / front magnet. The pad offers a larger contact area and a handle; compare grip, marking and removal. Reuse the front magnet between tests before bonding, or use a third magnet.')
section('Next stage','After click fit passes, test one RUNG_SLEEVE with actual PVC, then the 609.6 mm-wide braced bay in the full gate guide. The peaked sleeve roof is unchanged. These parts are reusable in the gate. This first plate tests joinery, not full-width rigidity or wind performance. No physical prototype has been tested here.')
def foot(c,d):c.setFont('Helvetica',8);c.drawString(51,22,'FPV gate / first frame interface test / production scale 1:1');c.drawRightString(560,22,str(d.page))
SimpleDocTemplate(str(O/'First_Frame_Test.pdf'),pagesize=(612,792),leftMargin=51,rightMargin=51,topMargin=32,bottomMargin=40).build(story,onFirstPage=foot,onLaterPages=foot)
figs=''.join(f'<figure><img src="renders/{n}.png" alt="{html.escape(t)}"><figcaption>{t}</figcaption></figure>' for n,t in [('01_FIRST_PLATE','Four-piece plate; spare key included.'),('02_STRAIGHT_JOINT','Straight connection, 286.63 mm overall.'),('03_PERPENDICULAR_JOINT','Reconfigure the same rails and key as a T.'),('04_JOINT_EXPLODED','Slide the guides along the rail axis. Pinch both hook tips to release.')])
(O/'index.html').write_text(f'''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>First frame print</title><style>body{{font:17px/1.6 system-ui;max-width:1100px;margin:35px auto;padding:0 24px;color:#17374c;background:#f3f6f8}}img{{width:100%}}figure{{margin:24px 0}}a{{color:#006d92}}aside{{padding:20px;background:#deecf2}}h1{{line-height:1.2}}</style><h1>One A1 Mini plate / test the click joints</h1><aside><b><a href="{a['prepared_3mf']}">Print the four-piece test</a></b> — {a['grams']:.2f} g PETG / {duration(a['minutes'])}. Two identical EDGE_BRANCH rails and two CLICK_KEYs. One key joins the rails; the second is a spare. Test straight, release, then rebuild as a T.</aside><p><a href="{p['prepared_3mf']}">Optional five-piece version with one paper pad</a> — {p['grams']:.2f} g / {duration(p['minutes'])}. Choose one file, not both.</p><p><a href="First_Frame_Test.pdf">Assembly and test PDF</a> · <a href="First_Frame_Print.blend">Blender scenes</a> · <a href="README.md">Detailed guide</a> · <a href="First_Frame_Print_Kit.zip">Download kit</a></p><p>PETG, 0.4 mm nozzle, 0.20 mm layers, four walls, 20% infill, no supports or brim, print by layer. Supplied flat orientations, 100% scale. All pieces fit with at least 5 mm bed margin and slice without warnings. No printer job has been submitted.</p>{figs}<p>All three part meshes match the current production geometry. Frame-side magnet holders retain the 0.4 mm plastic skin; front PAPER_PAD parts are optional. The peaked sleeve remains unchanged. Physical fit and durability are awaiting this test.</p><p><a href="print_checks.json">Print checks</a> · <a href="geometry_checks.json">Geometry checks</a> · <a href="../sleeve_paper_gate/index.html">Full gate and later tests</a></p></html>''')
with zipfile.ZipFile(O/'First_Frame_Print_Kit.zip','w',zipfile.ZIP_DEFLATED) as z:
 for f in O.rglob('*'):
  if not f.is_file() or f.suffix in ['.zip','.log','.gcode','.blend1']:continue
  if 'sliced' in f.parts and f.suffix!='.3mf':continue
  z.write(f,Path('first_frame_print')/f.relative_to(O))
print('FIRST FRAME PRINT VALIDATED AND PACKAGED',json.dumps(report['plates']))

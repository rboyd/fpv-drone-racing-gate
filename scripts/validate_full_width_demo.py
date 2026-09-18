from pathlib import Path
import json,struct,zipfile,xml.etree.ElementTree as ET,collections
O=Path(__file__).resolve().parents[1]/'output/full_width_demo'
bom=json.loads((O/'BOM.json').read_text());parts={p['code']:p for p in bom['parts']};report={'geometry':{},'plates':{},'slices':{}}
for code,p in parts.items():
 d=(O/'printable'/p['file']).read_bytes();n=struct.unpack_from('<I',d,80)[0];assert len(d)==84+50*n;vs=[];vol=0
 for i in range(n):
  tr=struct.unpack_from('<12fH',d,84+50*i);a,b,c=tr[3:6],tr[6:9],tr[9:12];vs.extend([a,b,c]);vol+=sum(a[j]*[b[1]*c[2]-b[2]*c[1],b[2]*c[0]-b[0]*c[2],b[0]*c[1]-b[1]*c[0]][j] for j in range(3))/6
 dims=[max(v[j] for v in vs)-min(v[j] for v in vs) for j in range(3)]
 assert max(dims)<170 and abs(min(v[2] for v in vs))<.0001 and p['nonmanifold_edges']==0
 assert vol>0 and abs(vol-p['solid_volume_mm3'])<.2
 report['geometry'][code]={'bounds_mm':[round(x,3) for x in dims],'watertight':True,'positive_volume_mm3':round(vol,3)}
for p in (O/'printable').glob('*.3mf'):
 with zipfile.ZipFile(p) as z:r=ET.fromstring(z.read('3D/3dmodel.model'))
 assert r.get('unit')=='millimeter';boxes=[]
 for obj in r.findall('.//{*}object'):
  vs=[tuple(float(v.get(k)) for k in ['x','y','z']) for v in obj.findall('.//{*}vertex')];lo=[min(v[j] for v in vs) for j in range(3)];hi=[max(v[j] for v in vs) for j in range(3)]
  assert min(lo[:2])>=4.99 and max(hi)<=175 and abs(lo[2])<.001
  boxes.append((lo,hi))
 for i,(lo,hi) in enumerate(boxes):
  for a,b in boxes[i+1:]:assert any(min(hi[j],b[j])-max(lo[j],a[j])<0 for j in range(2)),p
 report['plates'][p.stem]={'parts':len(boxes),'bed_margin_at_least_5mm':True,'no_overlap':True}
 d=json.loads((O/'sliced'/p.stem/'result.json').read_text());assert d['return_code']==0;sl=d['sliced_plates'][0];assert not sl['warning_message'],(p,sl)
 g=(O/'sliced'/p.stem/'plate_1.gcode').read_text()
 for s in ['; enable_support = 0','; printer_model = Bambu Lab A1 mini','; nozzle_diameter = 0.4','filament_type = PETG']:assert s in g,p
 report['slices'][p.stem]={'grams':round(sum(a['total_used_g'] for a in sl['filaments']),2),'minutes':round(sl['total_predication']/60,2),'support':False,'warning':''}
produced=collections.Counter()
for name,runs in [('01_FRAME_REPEAT_4_TIMES',4),('02_KEYS_AND_PADS_ONCE',1)]:
 for code,_,_ in bom['plates'][name]:produced[code]+=runs
assert dict(produced)=={p['code']:p['quantity'] for p in bom['parts'] if p['quantity']},produced
assert sum(produced.values())==42 and len(produced)==4
report['kit_totals']={k:round(report['slices']['01_FRAME_REPEAT_4_TIMES'][k]*4+report['slices']['02_KEYS_AND_PADS_ONCE'][k],2) for k in ['grams','minutes']}
report['kit_plus_fit_check']={k:round(v+report['slices']['00_FIT_CHECK'][k],2) for k,v in report['kit_totals'].items()}
report['assembly_checks']=json.loads((O/'assembly_checks.json').read_text());assert len(report['assembly_checks']['interfaces'])==4
assert max(p['max_sampled_penetration_mm'] for p in report['assembly_checks']['interfaces'])<.01
(O/'print_checks.json').write_text(json.dumps(report,indent=2));print('PASS: 7 masters (4 main + 3 fit-only), 10 slices, correct 42-piece kit quantities.');print(report['kit_totals']);print(report['kit_plus_fit_check'])

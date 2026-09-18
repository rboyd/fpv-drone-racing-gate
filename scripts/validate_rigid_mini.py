from pathlib import Path
import json,math,struct,zipfile,xml.etree.ElementTree as ET
O=Path(__file__).resolve().parents[1]/'output/rigid_whole_sheet'
report={}
data=json.loads((O/'validation.json').read_text())
assert abs(data['print_models']['mini_tabletop_foot_PRINT_2.stl']['solid_volume_mm3']-4500)<.1
L,W=143.04,37.52
expected=L*W*.8+(L*W-(L-12)*(W-12))*1.8+2*1.2*(W-12)*1.4-4*(16*1.8**2*math.sin(2*math.pi/32))*2.6
assert abs(data['print_models']['mini_1to15_border_PRINT_4.stl']['solid_volume_mm3']-expected)<.1
for p in (O/'printable').glob('*.stl'):
 d=p.read_bytes();n=struct.unpack_from('<I',d,80)[0];assert len(d)==84+50*n;verts=[];bad=0
 for i in range(n):
  t=struct.unpack_from('<12fH',d,84+50*i);a,b,c=t[3:6],t[6:9],t[9:12];verts.extend([a,b,c]);u=[b[j]-a[j] for j in range(3)];v=[c[j]-a[j] for j in range(3)];cross=[u[1]*v[2]-u[2]*v[1],u[2]*v[0]-u[0]*v[2],u[0]*v[1]-u[1]*v[0]];area=math.sqrt(sum(x*x for x in cross))/2
  if area>1e-5 and t[2]<-.72 and min(a[2],b[2],c[2])>.02:bad+=1
 bounds=[max(v[j] for v in verts)-min(v[j] for v in verts) for j in range(3)]
 assert max(bounds)<171 and abs(min(v[2] for v in verts))<.0001 and bad==0,(p,bounds,bad)
 report[p.name]={'bounds_mm':bounds,'unsupported_downward_faces':bad}
for p in (O/'printable').glob('*.3mf'):
 with zipfile.ZipFile(p) as z:root=ET.fromstring(z.read('3D/3dmodel.model'))
 objects=root.findall('.//{*}object');boxes=[]
 for ob in objects:
  vs=[tuple(float(v.attrib[k]) for k in ['x','y','z']) for v in ob.findall('.//{*}vertex')]
  lo=[min(v[j] for v in vs) for j in range(3)];hi=[max(v[j] for v in vs) for j in range(3)]
  assert lo[0]>=0 and lo[1]>=0 and abs(lo[2])<.001 and max(hi[:2])<=180,(p,lo,hi)
  boxes.append((lo,hi))
 for i,(lo,hi) in enumerate(boxes):
  for low,high in boxes[i+1:]:assert not all(min(hi[j],high[j])-max(lo[j],low[j])>0 for j in [0,1]),p
 report[p.name]={'parts':len(objects),'within_180mm_plate':True,'no_part_overlap':True}
for p in (O/'sliced').glob('*/result.json'):
 d=json.loads(p.read_text());assert d['return_code']==0;plate=d['sliced_plates'][0];g=(p.parent/'plate_1.gcode').read_text();assert '; enable_support = 0' in g and '; printer_model = Bambu Lab A1 mini' in g and '; filament_density: 1.24' in g and '; nozzle_diameter = 0.4' in g and 'A1' in g
 assert not plate['warning_message'],plate['warning_message']
 report[p.parent.name]={'sliced_successfully':True,'supports':False,'PLA_g':sum(x['total_used_g'] for x in plate['filaments']),'estimated_minutes':plate['total_predication']/60}
(O/'print_checks.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))

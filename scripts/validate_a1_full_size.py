"""Build a 1:1 interface fit kit and check exported STL/3MF bounds and real slices."""
from pathlib import Path
import json, math, struct, zipfile, xml.etree.ElementTree as ET
O=Path(__file__).resolve().parents[1]/'output/a1_full_size'
NS='http://schemas.microsoft.com/3dmanufacturing/core/2015/02'
ET.register_namespace('',NS)
placements=[('CHANNEL_LONG',5,5),('CHANNEL_SHORT',5,25),('SPLINT',5,45),('SNAP_BRIDGE',50,45),('DOCK_CAP',92,45),('DOCK_CAP',121,45),('PIPE_33',5,75),('RIB_CROSS',75,75),('FIELD_RECEIVER',130,75),('CORNER_NODE',136,105),('RIB_H_LOW',5,135),('DOCK_PEDESTAL',145,145)]
root=ET.Element('{'+NS+'}model',unit='millimeter');res=ET.SubElement(root,'resources');build=ET.SubElement(root,'build')
for i,(code,x,y) in enumerate(placements,1):
 with zipfile.ZipFile(O/'printable'/f'{code}.3mf') as z:r=ET.fromstring(z.read('3D/3dmodel.model'))
 obj=r.find('.//{*}object');obj.set('id',str(i));obj.set('name',code)
 for v in obj.findall('.//{*}vertex'):
  v.set('x',str(float(v.get('x'))-5+x));v.set('y',str(float(v.get('y'))-5+y))
 res.append(obj);ET.SubElement(build,'item',objectid=str(i))
with zipfile.ZipFile(O/'printable'/'Fit_Kit_1to1_LAYOUT.3mf','w',zipfile.ZIP_DEFLATED) as z:
 z.writestr('[Content_Types].xml','<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/></Types>')
 z.writestr('_rels/.rels','<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Target="/3D/3dmodel.model" Id="rel0" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/></Relationships>')
 z.writestr('3D/3dmodel.model',ET.tostring(root,encoding='utf-8',xml_declaration=True))
report={'geometry':{},'layouts':{},'slices':{}}
bom=json.loads((O/'BOM.json').read_text());bycode={p['code']:p for p in bom['parts']}
assert {k for k in bycode if k.startswith('CHANNEL_')}=={'CHANNEL_LONG','CHANNEL_SHORT'}
assert bycode['CHANNEL_LONG']['quantity']==120 and bycode['CHANNEL_SHORT']['quantity']==96
for p in (O/'printable').glob('*.stl'):
 d=p.read_bytes();n=struct.unpack_from('<I',d,80)[0];assert len(d)==84+50*n;verts=[];bad=[];volume=0
 for i in range(n):
  t=struct.unpack_from('<12fH',d,84+50*i);a,b,c=t[3:6],t[6:9],t[9:12];verts.extend([a,b,c]);u=[b[j]-a[j] for j in range(3)];v=[c[j]-a[j] for j in range(3)];cross=[u[1]*v[2]-u[2]*v[1],u[2]*v[0]-u[0]*v[2],u[0]*v[1]-u[1]*v[0]];area=math.sqrt(sum(x*x for x in cross))/2
  volume+=sum(a[j]*[b[1]*c[2]-b[2]*c[1],b[2]*c[0]-b[0]*c[2],b[0]*c[1]-b[1]*c[0]][j] for j in range(3))/6
  if area>1e-4 and t[2]<-.72 and min(a[2],b[2],c[2])>.02:bad.append({'triangle':i,'area_mm2':area,'normal_z':t[2]})
 bounds=[max(v[j] for v in verts)-min(v[j] for v in verts) for j in range(3)]
 assert max(bounds)<170 and abs(min(v[2] for v in verts))<.0001,(p,bounds)
 assert abs(volume-bycode[p.stem]['solid_volume_mm3'])<.15,(p,volume)
 assert not bad,(p,bad)
 report['geometry'][p.stem]={'bounds_mm':[round(x,3) for x in bounds],'volume_mm3':round(volume,2),'downward_faces_steeper_than_45deg_above_bed':len(bad),'source_nonmanifold_edges':bycode[p.stem]['nonmanifold_edges']}
for p in (O/'printable').glob('*.3mf'):
 with zipfile.ZipFile(p) as z:r=ET.fromstring(z.read('3D/3dmodel.model'))
 assert r.get('unit')=='millimeter';boxes=[]
 for ob in r.findall('.//{*}object'):
  vs=[tuple(float(v.attrib[k]) for k in ['x','y','z']) for v in ob.findall('.//{*}vertex')];lo=[min(v[j] for v in vs) for j in range(3)];hi=[max(v[j] for v in vs) for j in range(3)]
  assert lo[0]>=0 and lo[1]>=0 and abs(lo[2])<.001 and max(hi)<=175,(p,lo,hi)
  boxes.append((lo,hi))
 for i,(lo,hi) in enumerate(boxes):
  for low,high in boxes[i+1:]:assert not all(min(hi[j],high[j])-max(lo[j],low[j])>0 for j in [0,1]),p
 report['layouts'][p.stem]={'parts':len(boxes),'inside_180mm_volume':True,'no_xy_overlap':True}
weighted_g=weighted_seconds=weighted_main_seconds=0
for p in (O/'sliced').glob('*/result.json'):
 d=json.loads(p.read_text());assert d['return_code']==0;plate=d['sliced_plates'][0];g=(p.parent/'plate_1.gcode').read_text()
 assert '; enable_support = 0' in g and '; printer_model = Bambu Lab A1 mini' in g and '; nozzle_diameter = 0.4' in g
 assert 'filament_type = PETG' in g and 'filament_density: 0' not in g
 assert not plate['warning_message'],(p,plate['warning_message'])
 grams=sum(x['total_used_g'] for x in plate['filaments']);sec=plate['total_predication']
 main_g=sum(x.get('main_used_g',x['total_used_g']) for x in plate['filaments'])
 report['slices'][p.parent.name]={'success':True,'support':False,'PETG_g':grams,'main_PETG_g':main_g,'minutes':sec/60}
 if p.parent.name in bycode:weighted_g+=main_g*bycode[p.parent.name]['quantity'];weighted_seconds+=sec*bycode[p.parent.name]['quantity'];weighted_main_seconds+=plate['main_predication']*bycode[p.parent.name]['quantity']
report['gate_estimate']={'PETG_model_g':round(weighted_g,1),'PETG_with_10percent_reserve_g':round(weighted_g*1.1,1),'one_kg_spools_with_reserve':math.ceil(weighted_g*1.1/1000),'sum_of_single_part_slices_hours':round(weighted_seconds/3600,1),'sum_of_model_print_time_hours':round(weighted_main_seconds/3600,1),'note':'Single-part timing includes repeated startup; batch plates will differ. Reserve excludes PVC, posterboard and ties.'}
report['complete_slice_coverage']=set(bycode)<=set(report['slices'])
if not report['complete_slice_coverage']:report['gate_estimate']={'status':'pending complete slice coverage'}
(O/'print_checks.json').write_text(json.dumps(report,indent=2))
print('Geometry checked:',len(report['geometry']),'unique STLs. Layouts:',len(report['layouts']),'Slices:',len(report['slices']))
print(json.dumps(report['gate_estimate'],indent=2))

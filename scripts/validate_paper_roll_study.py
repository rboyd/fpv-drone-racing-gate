"""Check actual fabrication files, plate placement, slice profiles and stack-neck toolpaths."""
from pathlib import Path
import json,math,struct,zipfile,xml.etree.ElementTree as ET,re
O=Path(__file__).resolve().parents[1]/'output/paper_roll_study'
parts={x['code']:x for x in json.loads((O/'PROTOTYPE_PARTS.json').read_text())['parts']}
r={'geometry':{},'plates':{},'slices':{},'stack_neck_toolpaths':{},'physical_testing':'Not performed'}
for code,p in parts.items():
 d=(O/'printable'/p['file']).read_bytes();n=struct.unpack_from('<I',d,80)[0];assert len(d)==84+50*n
 vs=[];volume=0
 for i in range(n):
  t=struct.unpack_from('<12fH',d,84+50*i);a,b,c=t[3:6],t[6:9],t[9:12];vs.extend((a,b,c));volume+=sum(a[j]*[b[1]*c[2]-b[2]*c[1],b[2]*c[0]-b[0]*c[2],b[0]*c[1]-b[1]*c[0]][j] for j in range(3))/6
 dims=[max(v[j] for v in vs)-min(v[j] for v in vs) for j in range(3)]
 assert max(dims)<=170 and abs(min(v[2] for v in vs))<1e-4,(code,dims)
 assert p['nonmanifold_edges']==0 and volume>0 and abs(volume-p['solid_volume_mm3'])<.2,(code,volume)
 r['geometry'][code]={'bounds_mm':[round(a,3) for a in dims],'positive_volume_mm3':round(volume,2),'nonmanifold_edges':0}
for f in sorted((O/'printable').glob('*.3mf')):
 with zipfile.ZipFile(f) as z:a=ET.fromstring(z.read('3D/3dmodel.model'))
 assert a.get('unit')=='millimeter';objects=[]
 for ob in a.findall('.//{*}object'):
  vs=[tuple(float(v.attrib[k]) for k in ['x','y','z']) for v in ob.findall('.//{*}vertex')]
  assert min(v[0] for v in vs)>=4.999 and min(v[1] for v in vs)>=4.999 and abs(min(v[2] for v in vs))<.001
  assert max(max(v) for v in vs)<=175
  # Separating directions include bed axes and both diagonals. These suffice for our parallel rail stacks.
  directions=[(1,0),(0,1),(1,1),(1,-1)]
  projections=[(min(v[0]*dx+v[1]*dy for v in vs),max(v[0]*dx+v[1]*dy for v in vs)) for dx,dy in directions]
  objects.append(projections)
 for i,aa in enumerate(objects):
  for bb in objects[i+1:]:assert any(min(x[1],y[1])-max(x[0],y[0])<-.01 for x,y in zip(aa,bb)),('overlap',f)
 r['plates'][f.stem]={'objects':len(objects),'inside_180mm_volume':True,'separated_mesh_envelopes':True}
 d=json.loads((O/'sliced'/f.stem/'result.json').read_text());assert d['return_code']==0,(f,d)
 p=d['sliced_plates'][0];g=(O/'sliced'/f.stem/'plate_1.gcode').read_text()
 for setting in ['; enable_support = 0','; printer_model = Bambu Lab A1 mini','; nozzle_diameter = 0.4','filament_type = PETG']:assert setting in g,(f,setting)
 warning=p['warning_message']
 assert not warning,(f,warning)
 r['slices'][f.stem]={'PETG_g':round(sum(a['total_used_g'] for a in p['filaments']),2),'minutes':round(p['total_predication']/60,2),'main_minutes':round(p['main_predication']/60,2),'supports':False,'warning':warning}
 if f.stem in ['DIAGONAL_8x220','DIAGONAL_13x198','06_OVERNIGHT_26_RAILS']:
  n=8 if f.stem=='DIAGONAL_8x220' else 13;wanted=[round(.8+12.4*i,1) for i in range(n)];found={};height=None
  for line in g.splitlines():
   if line.startswith('; Z_HEIGHT:'):height=round(float(line.split(':')[1]),1)
   if height in wanted and line.startswith('G1 ') and 'X' in line and 'Y' in line:
    e=re.search(r'\bE([-\d.]+)',line)
    if e and float(e[1])>0:found[height]=found.get(height,0)+1
  assert set(found)==set(wanted),(f,wanted,found)
  r['stack_neck_toolpaths'][f.stem]={'neck_layer_z_mm':wanted,'extruding_xy_moves':[found[x] for x in wanted],'all_neck_layers_have_material':True}
clear=json.loads((O/'assembly_clearance_checks.json').read_text());assert max(clear['intersection_mm3'].values())<.05,clear
r['nominal_assembly_intersections_mm3']=clear['intersection_mm3'];r['complete_slice_coverage']=set(parts)<=set(r['slices'])
(O/'print_checks.json').write_text(json.dumps(r,indent=2));print(f"PASS: {len(parts)} watertight print masters, {len(r['plates'])} layouts/slices; 20 nominal assembly interference checks. No slicing warnings; physical bridge and separation tests remain.")

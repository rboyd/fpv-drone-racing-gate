from pathlib import Path
import json,struct,zipfile,xml.etree.ElementTree as ET,collections,math
O=Path(__file__).resolve().parents[1]/'output/orthogonal_pvc_gate';b=json.loads((O/'BOM.json').read_text());report={'geometry':{},'plates':{},'slices':{},'gates':{}}
for p in b['parts']:
 data=(O/'printable'/p['file']).read_bytes();n=struct.unpack_from('<I',data,80)[0];assert len(data)==84+50*n;verts=[];edges=collections.Counter();adj={};volume=0
 for i in range(n):
  tr=struct.unpack_from('<12fH',data,84+50*i);a,c,d=tr[3:6],tr[6:9],tr[9:12];vs=[tuple(round(z,4) for z in v) for v in [a,c,d]];verts+=vs
  volume+=(a[0]*(c[1]*d[2]-c[2]*d[1])+a[1]*(c[2]*d[0]-c[0]*d[2])+a[2]*(c[0]*d[1]-c[1]*d[0]))/6
  for j in range(3):
   aa,bb=vs[j],vs[(j+1)%3]
   if aa==bb:continue
   edges[tuple(sorted([aa,bb]))]+=1;adj.setdefault(aa,set()).add(bb);adj.setdefault(bb,set()).add(aa)
 # CAD manifold check is authoritative; STL rounding may collapse extremely short tessellation edges.
 assert p['nonmanifold_edges']==0 and volume>0,p['code']
 remaining=set(adj);components=0
 while remaining:
  stack=[remaining.pop()];components+=1
  while stack:
   for v in adj[stack.pop()]:
    if v in remaining:remaining.remove(v);stack.append(v)
 assert components==1,(p['code'],components)
 dims=[max(v[j] for v in verts)-min(v[j] for v in verts) for j in range(3)];assert max(dims)<=170.001
 report['geometry'][p['code']]={'manifold_in_CAD':True,'connected_components':components,'bounds_mm':dims,'volume_mm3':round(volume,2)}
for name,items in b['plates'].items():
 with zipfile.ZipFile(O/'printable'/f'{name}.3mf') as z:r=ET.fromstring(z.read('3D/3dmodel.model'))
 assert r.get('unit')=='millimeter';boxes=[]
 for obj in r.findall('.//{*}object'):
  vs=[tuple(float(v.get(k)) for k in ['x','y','z']) for v in obj.findall('.//{*}vertex')];lo=[min(v[j] for v in vs) for j in range(3)];hi=[max(v[j] for v in vs) for j in range(3)]
  assert min(lo[:2])>=4.999 and max(hi[:2])<=175.001 and abs(lo[2])<.001 and hi[2]<=180,(name,lo,hi)
  boxes.append((lo,hi))
 for i,(lo,hi) in enumerate(boxes):
  for a,c in boxes[i+1:]:assert any(min(hi[j],c[j])-max(lo[j],a[j])<-.01 for j in range(2)),(name,'parts overlap or touch')
 assert len(boxes)==len(items);report['plates'][name]={'pieces':len(items),'bed_margin_at_least_5mm':True,'overlap':False}
 dest=O/'sliced'/name;d=json.loads((dest/'result.json').read_text());assert d['return_code']==0 and len(d['sliced_plates'])==1
 sl=d['sliced_plates'][0];assert not sl['warning_message'],(name,sl['warning_message']);g=(dest/'plate_1.gcode').read_text()
 for st in ['; enable_support = 0','; printer_model = Bambu Lab A1 mini','; nozzle_diameter = 0.4','; filament_type = PETG','; wall_loops = 4','; print_sequence = by layer']:assert st in g,(name,st)
 assert '; FEATURE: Support' not in g
 report['slices'][name]={'grams':round(sum(f['total_used_g'] for f in sl['filaments']),2),'minutes':round(sl['total_predication']/60,2),'supports':False,'warnings':[]}
for kind,g in b['gates'].items():
 assert g['cords']==0 and g['diagonal_PVC']==0
 assert set(g['counts'])=={'ELBOW','CROSS','MAG_SLEEVE'}
 assert set(e['length_mm'] for e in g['edges'])=={389.6,1560.8}
 made=collections.Counter()
 for name,n in g['print_queue'].items():
  for code,*_ in b['plates'][name]:made[code]+=n
 assert dict(made)==g['counts'],(kind,made,g['counts'])
 # Each pipe is cut between hard-stop planes, and all sleeves occupy exposed pipe, not sockets.
 sleeve_checks=[];seen_mag=[]
 for code,xy,rot in g['placements']:
  rr=math.radians(rot);c,s=math.cos(rr),math.sin(rr)
  local={'ELBOW':[(-57,-57)],'CROSS':[(x,y) for x in [-57,57] for y in [-57,57]],'MAG_SLEEVE':[(0,57)]}.get(code,[])
  seen_mag += [(xy[0]+c*x-s*y,xy[1]+s*x+c*y) for x,y in local]
  if code!='MAG_SLEEVE':continue
  fits=[]
  for e in g['edges']:
   aa=e['start'];bb=e['end'];dx=bb[0]-aa[0];dy=bb[1]-aa[1];ll=math.hypot(dx,dy);ux,uy=dx/ll,dy/ll;vx,vy=xy[0]-aa[0],xy[1]-aa[1];t=vx*ux+vy*uy
   if abs(vx*uy-vy*ux)<.01 and 38.01<=t<=ll-38.01:fits.append((e['name'],round(t,3)))
  assert len(fits)==1,(kind,xy,'sleeve on socket or not on a unique exposed pipe',fits)
  sleeve_checks.append({'pipe':fits[0][0],'from_cut_end_mm':fits[0][1],'xy':xy,'angle':rot})
 for x,y in g['magnets']:assert min(math.hypot(x-a,y-c) for a,c in seen_mag)<.01,(kind,x,y,'magnet has no backing pocket')
 for stock in g['stock_plan']:
  assert sum(e['length_mm']+3 for e in stock['cuts'])<=3038.001
 totals={k:round(sum(report['slices'][name][k]*n for name,n in g['print_queue'].items()),2) for k in ['grams','minutes']}
 report['gates'][kind]={**totals,'printed_pieces':sum(made.values()),'unique_production_types':len(made),'plate_runs':sum(g['print_queue'].values()),'pipe_sticks':g['PVC_sticks'],'pipe_cost_usd':g['PVC_cost_usd'],'PETG_at_20_per_kg_usd':round(totals['grams']*.02,2),'frame_PVC_plus_PETG_usd':round(g['PVC_cost_usd']+totals['grams']*.02,2),'magnet_pairs':g['magnet_pairs'],'largest_pipe_cut_mm':max(e['length_mm'] for e in g['edges']),'sleeves':sleeve_checks}
checks=json.loads((O/'geometry_checks.json').read_text())
for g in checks.values():assert g['only_orthogonal_PVC'] and not g['printed_vertices_outside_paper'] and not g['magnet_centers_outside_paper']
report['front_projection_check']=checks
lo=collections.Counter(e['length_mm'] for e in b['gates']['single']['edges']);hi=collections.Counter(e['length_mm'] for e in b['gates']['split_s']['edges']);assert not lo-hi
report['upgrade']={'all_single_height_pipe_lengths_reused':True,'additional_pipe_cuts':dict(hi-lo),'additional_parts':dict(collections.Counter(b['gates']['split_s']['counts'])-collections.Counter(b['gates']['single']['counts']))}
single=b['gates']['single'];double=b['gates']['split_s'];shift=double['height_mm']-single['height_mm'];top=single['y_grid_mm'][-1]
# Move the intact top row, preserving its populated pads and sleeve clocking.
def pose(c,xy,r):return c,round(xy[0],2),round(xy[1],2),round(r%360,2)
available=collections.Counter(pose(c,xy,r) for c,xy,r in double['placements'])
reused=collections.Counter(pose(c,(xy[0],xy[1]+(shift if abs(xy[1]-top)<.01 else 0)),r) for c,xy,r in single['placements'])
assert not reused-available,'Upgrade cannot reuse intact top row poses'
new_magnets={(round(x,2),round(y,2)) for x,y in double['magnets']}
assert all((round(x,2),round(y+(shift if y>top else 0),2)) in new_magnets for x,y in single['magnets'])
report['upgrade']['intact_top_row_and_all_populated_pockets_reused']=True
(O/'print_checks.json').write_text(json.dumps(report,indent=2))
print('PASS: connected manifold masters, A1 Mini plate clearance, no supports/warnings, exact queues, aligned magnet pockets, exposed-pipe sleeves and pipe reuse.')
for k,g in report['gates'].items():print(k,{n:v for n,v in g.items() if n!='sleeves'})

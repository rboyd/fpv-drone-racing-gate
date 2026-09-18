"""Read the full-size Blender scene; do not confuse samples/miniature with a BOM."""
import bpy,json,struct,collections
from pathlib import Path
O=Path(__file__).resolve().parents[1]/'output/rigid_whole_sheet'
SC=bpy.data.scenes['01_RIGID_GATE'];bpy.context.window.scene=SC;bpy.context.view_layer.update()
prefixes=[('Slide-in U channel','Channel segment','rail'),('Workshop node / stays assembled','Workshop corner-node marker','schematic'),('Rear rib / 10 mm2','Long rear rib','rib'),('Rear cross rib / 10 mm2','Short rear rib','rib'),('Light paper keeper','Paper keeper','schematic'),('PVC docking receiver','Face docking receiver','schematic'),('Permanent straight splice','Rigid border splice','schematic'),('FIELD / removable corner bridge','Gate corner bridge','schematic'),('PVC dock / adjustable','Pipe-side docking assembly','schematic'),('Brace-end clamp','Brace-end clamp assembly','schematic')]
rows={};node_positions=collections.Counter()
for ob in SC.objects:
 if ob.type!='MESH':continue
 for pre,label,status in prefixes:
  if ob.name.startswith(pre):
   bounds=[]
   for j in range(3):bounds.append((max(v.co[j] for v in ob.data.vertices)-min(v.co[j] for v in ob.data.vertices))*abs(ob.scale[j])*1000)
   dims=tuple(sorted((round(x,3) for x in bounds),reverse=True));key=(label,dims)
   row=rows.setdefault(key,{'part':label,'envelope_mm':dims,'quantity':0,'status':status,'axis_aligned_volume_fit':max(dims)<=180})
   row['quantity']+=1
   if status=='rail':row['segment_mm']=ob.get('segment_mm')
   if pre.startswith('Workshop'):node_positions[tuple(round(x*1000,3) for x in ob.matrix_world.translation)]+=1
   break
coupons=[]
for p in sorted((O/'full_size_fit_samples').glob('*.stl')):
 data=p.read_bytes();vs=[]
 for i in range(struct.unpack_from('<I',data,80)[0]):
  t=struct.unpack_from('<12fH',data,84+50*i);vs.extend([t[3:6],t[6:9],t[9:12]])
 dims=[max(v[j] for v in vs)-min(v[j] for v in vs) for j in range(3)]
 coupons.append({'file':p.name,'print_bounds_mm':[round(x,3) for x in dims],'fits_180mm':all(x<=180 for x in dims)})
report={'scope':'Full-size scene 01_RIGID_GATE only; schematic assembly boxes are NOT finished printable parts. Coupons are test specimens, not production quantities.','modeled_geometry_variants':len(rows),'printed_candidate_object_count':sum(x['quantity'] for x in rows.values()),'parts':list(rows.values()),'node_marker_objects':sum(node_positions.values()),'unique_world_node_marker_centers':len(node_positions),'coincident_node_marker_locations':sum(n>1 for n in node_positions.values()),'full_size_STL_fit_samples':coupons,'not_a_manufacturing_BOM':True}
(O/'FULL_SIZE_PARTS_AUDIT.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))

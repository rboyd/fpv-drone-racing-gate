"""Create an unsliced native Bambu project with three unchanged crosses stacked vertically."""
from pathlib import Path
import json,math,copy,zipfile,xml.etree.ElementTree as E
R=Path(__file__).resolve().parents[1];O=R/'output/cross_stack';O.mkdir(parents=True,exist_ok=True)
S=R/'output/corner_guide_elbow/sliced/ONE_CROSS/ONE_CROSS_A1Mini_PETG.3mf'
CORE='http://schemas.microsoft.com/3dmanufacturing/core/2015/02';PROD='http://schemas.microsoft.com/3dmanufacturing/production/2015/06';N={'m':CORE}
E.register_namespace('',CORE);E.register_namespace('p',PROD);E.register_namespace('BambuStudio','http://schemas.bambulab.com/package/2021')
with zipfile.ZipFile(S) as z:
 original={n:z.read(n) for n in z.namelist()}
model=E.fromstring(original['3D/Objects/object_1.model']);mesh=model.find('.//m:mesh',N);vertices=mesh.find('m:vertices',N);triangles=mesh.find('m:triangles',N)
vs=[tuple(float(v.get(k)) for k in ['x','y','z']) for v in vertices];ts=[tuple(int(t.get(k)) for k in ['v1','v2','v3']) for t in triangles]
lo=[min(v[k] for v in vs) for k in range(3)];hi=[max(v[k] for v in vs) for k in range(3)];height=hi[2]-lo[2]
step=math.ceil((height+4)/.2)*.2;total=2*step+height;center=[(lo[k]+hi[k])/2 for k in range(3)]
vertices.clear();triangles.clear()
for level in range(3):
 for v in vs:
  xyz=(v[0]-center[0],v[1]-center[1],v[2]-lo[2]+level*step-total/2)
  E.SubElement(vertices,'{'+CORE+'}vertex',dict(zip(['x','y','z'],[f'{x:.8f}' for x in xyz])))
 for t in ts:E.SubElement(triangles,'{'+CORE+'}triangle',dict(zip(['v1','v2','v3'],[str(x+level*len(vs)) for x in t])))
main=E.fromstring(original['3D/3dmodel.model']);item=main.find('m:build/m:item',N);item.set('transform',f'1 0 0 0 1 0 0 0 1 90 90 {total/2:.8f}')
for meta in main.findall('m:metadata',N):
 if meta.get('name') in ['Title','Description']:meta.text='Three CROSS fittings / vertical stack / supports required / prototype'
settings=json.loads(original['Metadata/project_settings.config']);settings.update(enable_support='1',support_type='normal(auto)',support_style='default',support_on_build_plate_only='0',support_critical_regions_only='0',support_top_z_distance='0.2',support_bottom_z_distance='0.2',print_sequence='by layer',brim_type='outer_only',brim_width='5')
assert settings['printable_height']=='180' and settings['filament_type']==['PETG']
config=E.fromstring(original['Metadata/model_settings.config']);obj=config.find('object');part=obj.find('part')
for meta in obj.findall('metadata'):
 if meta.get('key')=='name':meta.set('value','CROSS x3 / vertical stack / do not split to objects')
 if 'face_count' in meta.attrib:meta.set('face_count',str(3*len(ts)))
for meta in part.findall('metadata'):
 key=meta.get('key')
 if key=='name':meta.set('value','Three separate cross solids / fixed vertical spacing')
 if key=='source_file':meta.set('value','THREE_CROSSES_STACK_A1Mini_PETG.3mf')
 if key=='source_offset_x' or key=='source_offset_y':meta.set('value','90')
 if key=='source_offset_z':meta.set('value',str(total/2))
part.find('mesh_stat').set('face_count',str(3*len(ts)))
plate=config.find('plate')
for meta in list(plate):
 if meta.get('key') in ['gcode_file','thumbnail_file','thumbnail_no_light_file','top_file','pick_file']:plate.remove(meta)
 if meta.get('key')=='plater_name':meta.set('value','3 CROSS / vertical support stack')
# Keep model/preset resources; discard single-cross previews and stale toolpaths.
keep=['[Content_Types].xml','_rels/.rels','3D/_rels/3dmodel.model.rels']
path=O/'THREE_CROSSES_STACK_A1Mini_PETG.3mf'
with zipfile.ZipFile(path,'w',zipfile.ZIP_DEFLATED) as z:
 for n in keep:z.writestr(n,original[n])
 z.writestr('3D/3dmodel.model',E.tostring(main,encoding='utf-8',xml_declaration=True))
 z.writestr('3D/Objects/object_1.model',E.tostring(model,encoding='utf-8',xml_declaration=True))
 z.writestr('Metadata/model_settings.config',E.tostring(config,encoding='utf-8',xml_declaration=True))
 z.writestr('Metadata/project_settings.config',json.dumps(settings,indent=2))
assert total<180 and 4*height>180
assert min(90-(hi[k]-lo[k])/2 for k in [0,1])>20
assert len(vertices)==3*len(vs) and len(triangles)==3*len(ts)
# Verify all three solids are exact translated copies with unchanged triangles.
for level in range(3):
 for i,v in enumerate(vs):
  new=vertices[level*len(vs)+i];expected=(v[0]-center[0],v[1]-center[1],v[2]-lo[2]+level*step-total/2)
  assert max(abs(float(new.get(k))-x) for k,x in zip(['x','y','z'],expected))<1e-7
report={'count':3,'part':'unchanged production CROSS','single_height_mm':height,'vertical_step_mm':step,'interpart_gap_mm':step-height,'bottom_Z_mm':[i*step for i in range(3)],'top_Z_mm':[i*step+height for i in range(3)],'total_height_mm':total,'bed_bounds_XY_mm':[[90-(hi[k]-lo[k])/2,90+(hi[k]-lo[k])/2] for k in [0,1]],'four_parts_without_gaps_height_mm':4*height,'preserved_geometry':True,'supports_enabled':True,'support_type':'normal(auto)','supports_build_plate_only':False,'print_sequence':'by layer','physical_stack_tested':False,'main_project_sliced':False}
(O/'layout_checks.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))

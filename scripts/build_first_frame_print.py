"""One A1 Mini plate: two production branch rails and two reusable click keys."""
from pathlib import Path
source=Path(__file__).with_name('build_sleeve_paper_gate.py').read_text().split('# One-piece sleeve rung.')[0]
source=source.replace("OUT=ROOT/'output/sleeve_paper_gate'", "OUT=ROOT/'output/first_frame_print'")
exec(compile(source,'<production frame geometry>','exec'),globals())
import hashlib
for code in list(PARTS):
 if code not in ['EDGE_BRANCH','CLICK_KEY','PAPER_PAD']:
  (OUT/'printable'/PARTS[code]['file']).unlink();PARTS.pop(code)
CORE=[('EDGE_BRANCH',5,5,0),('EDGE_BRANCH',5,84,0),('CLICK_KEY',143,5,90),('CLICK_KEY',143,75,90)]
PLATES={'FIRST_FRAME_TEST':CORE,'FIRST_FRAME_TEST_WITH_PAD':CORE+[('PAPER_PAD',148,146,0)]}
def bed_mesh(code,angle):
 pm=PARTS[code]['print_mesh'].copy();M=Rz(angle)
 for v in pm.vertices:v.co=M@v.co
 lo=Vector([min(v.co[j] for v in pm.vertices) for j in range(3)])
 for v in pm.vertices:v.co-=lo
 pm.calc_loop_triangles();return pm

def plate3mf(name,items):
 ns='http://schemas.microsoft.com/3dmanufacturing/core/2015/02';ET.register_namespace('',ns);root=ET.Element('{'+ns+'}model',unit='millimeter');res=ET.SubElement(root,'resources');build=ET.SubElement(root,'build')
 rects=[];min_gap=999
 for i,(code,x,y,a) in enumerate(items,1):
  pm=bed_mesh(code,a);lo=[min(v.co[j] for v in pm.vertices)*1000 for j in range(3)];hi=[max(v.co[j] for v in pm.vertices)*1000 for j in range(3)]
  assert x>=5-1e-5 and y>=5-1e-5 and x+hi[0]<=175.0001 and y+hi[1]<=175.0001 and hi[2]<=180,(code,lo,hi)
  for xx,yy,ww,hh in rects:
   dx=max(xx-(x+hi[0]),x-(xx+ww));dy=max(yy-(y+hi[1]),y-(yy+hh));assert dx>0 or dy>0,(name,'overlap')
   min_gap=min(min_gap,max(dx,dy))
  rects.append((x,y,hi[0],hi[1]))
  ob=ET.SubElement(res,'object',id=str(i),type='model',name=f'{i:02d}_{code}'+('_OPTIONAL' if code=='PAPER_PAD' else ''));me=ET.SubElement(ob,'mesh');vs=ET.SubElement(me,'vertices');ts=ET.SubElement(me,'triangles')
  for v in pm.vertices:ET.SubElement(vs,'vertex',x=str(v.co.x*1000+x),y=str(v.co.y*1000+y),z=str(v.co.z*1000))
  for tr in pm.loop_triangles:ET.SubElement(ts,'triangle',v1=str(tr.vertices[0]),v2=str(tr.vertices[1]),v3=str(tr.vertices[2]))
  ET.SubElement(build,'item',objectid=str(i))
 with zipfile.ZipFile(OUT/'printable'/f'{name}.3mf','w',zipfile.ZIP_DEFLATED) as z:
  z.writestr('[Content_Types].xml','<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/></Types>')
  z.writestr('_rels/.rels','<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Target="/3D/3dmodel.model" Id="rel0" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/></Relationships>');z.writestr('3D/3dmodel.model',ET.tostring(root,encoding='utf-8',xml_declaration=True))
 return {'parts':len(items),'minimum_part_gap_mm':min_gap,'bed_margin_mm':5,'maximum_height_mm':max(PARTS[c]['print_bounds_mm'][2] for c,*_ in items)}
checks={'plates':{n:plate3mf(n,p) for n,p in PLATES.items()},'production_meshes':{}}
for c,p in PARTS.items():
 a=(OUT/'printable'/p['file']).read_bytes();b=(ROOT/'output/sleeve_paper_gate/printable'/p['file']).read_bytes()
 assert a==b,('production geometry changed',c)
 checks['production_meshes'][c]={'identical_to_current_gate_STL':True,'sha256':hashlib.sha256(a).hexdigest(),'print_bounds_mm':p['print_bounds_mm'],'manifold':p['nonmanifold_edges']==0}
# The same actual source interface used in the full gate; screen both configurations.
for node in ast.parse(Path(__file__).with_name('build_full_width_demo.py').read_text()).body:
 if isinstance(node,ast.FunctionDef) and node.name=='intersection':exec(compile(ast.Module(body=[node],type_ignores=[]),'<intersection>','exec'),globals())
STRAIGHT=[('EDGE_BRANCH',Matrix.Identity(4)),('CLICK_KEY',T(L+7,0,0)),('EDGE_BRANCH',T(L+14,0,0))]
TEE=[('EDGE_BRANCH',Matrix.Identity(4)),('CLICK_KEY',T(L/2,63,0)@Rz(90)),('EDGE_BRANCH',T(L/2,70,0)@Rz(90))]
checks['interfaces']=[]
for name,parts in [('straight',STRAIGHT),('perpendicular',TEE)]:
 for ia,ib in [(0,1),(1,2)]:
  ca,A=parts[ia];cb,B=parts[ib];depth=intersection(ca,A,cb,B);assert depth<.01
  checks['interfaces'].append({'configuration':name,'parts':[ca,cb],'max_sampled_penetration_mm':depth})
checks['interface_method']='0.25 mm XY grid at Z .5/1/1.5/2.5/3.5/4.5 mm; sampled screen, not exhaustive collision proof or physical test.'
checks['magnet_holder']='Unchanged: 6.3 mm rear-loaded bore with .4 mm plastic between rear magnet and paper.'
(OUT/'geometry_checks.json').write_text(json.dumps(checks,indent=2))
(OUT/'BOM.json').write_text(json.dumps({'core':{'EDGE_BRANCH':2,'CLICK_KEY':2},'optional':{'PAPER_PAD':1},'plates':PLATES,'production_scale':1,'straight_length_mm':2*L+14,'first_run_only':True,'parts':[{k:v for k,v in p.items() if k not in ['object','print_mesh']}|{'code':c} for c,p in PARTS.items()]},indent=2))
def inst(code,M=Matrix.Identity(4)):
 o=bpy.data.objects.new(code,PARTS[code]['object'].data);COL.objects.link(o);o.matrix_world=M;return o
setup('01_FIRST_PLATE',(.26,-.28,.36),(.09,.09,.006),.35,False);coll('01 / exact print placement')
box('A1 Mini 180 mm bed',(90,90,-1),(180,180,2),GROUND)
for code,x,y,a in CORE:
 o=bpy.data.objects.new(code,bed_mesh(code,a));COL.objects.link(o);o.location=(x/1000,y/1000,0)
header('01','One plate / four useful test pieces','Two identical branch rails and two click keys. The keys print flat, rotated 90 degrees in the narrow strip beside the rails.')
footer('Choose FIRST_FRAME_TEST. All four pieces are production geometry; no magnets, PVC or additional supplies are needed for the click test.')
setup('02_STRAIGHT_JOINT',(.25,-.40,.37),(.143,.01,.008),.43,False);coll('01 / straight assembled')
for c,M in STRAIGHT:inst(c,M)
header('02','Test the straight rail connection','Use one key to join the two rails end-to-end. Keep their smooth paper faces coplanar and both side branches facing the same way.')
footer('Seat both rigid guide runners and inspect both catches at each end. The second key is a spare / comparison part.')
setup('03_PERPENDICULAR_JOINT',(.31,-.33,.40),(.065,.087,.01),.43,False);coll('01 / T joint assembled')
for c,M in TEE:inst(c,M)
header('03','Release it / rebuild as a T joint','Move the same key into the projecting side socket. Connect an end of the second rail at 90 degrees; use the same flat orientation.')
footer('This tests the actual crossmember interface, even though both test rails have branches. Pinch the two spring tips to release each key end.')
setup('04_JOINT_EXPLODED',(.26,-.40,.34),(.145,.015,.008),.45,False);coll('01 / alignment and release')
inst('EDGE_BRANCH');inst('CLICK_KEY',T(L+25,0,0));inst('EDGE_BRANCH',T(L+50,0,0))
header('04','Slide the guides straight into the receiver','The wide outside runners guide the joint. The two narrow central prongs flex inward and their hooks catch the receiver shoulders.')
footer('Do not push the key down from above or twist it out. Pinch both accessible hook tips toward the center, then slide the joint apart.')
for name in ['01_ASSEMBLED','00_MASTERS']:
 if bpy.data.scenes.get(name):bpy.data.scenes.remove(bpy.data.scenes[name])
bpy.context.window.scene=bpy.data.scenes['01_FIRST_PLATE'];bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'First_Frame_Print.blend'))
for sc in bpy.data.scenes:
 bpy.context.window.scene=sc;sc.render.filepath=str(OUT/'renders'/f'{sc.name}.png');bpy.ops.render.render(write_still=True,scene=sc.name)
print('FIRST PRINT BUILT',json.dumps(checks['plates']),flush=True)

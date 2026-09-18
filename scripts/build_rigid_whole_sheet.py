"""Rigid whole-stock gate and an adapted, printable 1:15 assembly model."""
from pathlib import Path
exec(Path(__file__).with_name('build_gate.py').read_text().split('# Print master:')[0],globals())
import ast,bmesh,zipfile
OUT=ROOT/'output/rigid_whole_sheet'
for d in ['printable','renders']:(OUT/d).mkdir(parents=True,exist_ok=True)
# Direct mesh boxes avoid operator/dependency-graph work for thousands of scene parts.
def cube(name,loc,size,material,bevel=0):
 vs=[(x*size[0]/2,y*size[1]/2,z*size[2]/2) for x,y,z in [(-1,-1,-1),(-1,-1,1),(-1,1,-1),(-1,1,1),(1,-1,-1),(1,-1,1),(1,1,-1),(1,1,1)]]
 fs=[(0,4,6,2),(1,3,7,5),(0,1,5,4),(2,6,7,3),(0,2,3,1),(4,5,7,6)]
 fs=[tuple(reversed(f)) for f in fs]
 me=bpy.data.meshes.new(name);me.from_pydata(vs,[],fs);me.update();ob=bpy.data.objects.new(name,me);COL.objects.link(ob);ob.location=loc;ob.data.materials.append(material)
 if bevel:
  m=ob.modifiers.new('Soft edges','BEVEL');m.width=bevel;m.segments=2
 return ob
PAPER=mat('Posterboard / ivory',(.86,.89,.90));PAPERS=[PAPER,mat('Posterboard / blue',(.40,.63,.87)),mat('Posterboard / mint',(.37,.73,.63)),mat('Posterboard / warm',(.86,.64,.32))]
STEELBLUE=mat('Rigid workshop nodes',(.035,.13,.25))
PROFILE=[(0,0),(6,0),(6,1.2),(1.2,1.2),(1.2,2),(6,2),(6,3.2),(1.2,3.2),(1.2,10),(0,10)]
RAIL_CACHE={}
source=ast.parse(Path(__file__).with_name('build_posterboard_concepts.py').read_text())
needed={'clean_mesh','prism_xy','profile_x','boolean','bake','mmcube','instance','rail_mesh','rail','leaf_geometry','move_objects','gate'}
for node in source.body:
 if isinstance(node,ast.FunctionDef) and node.name in needed:exec(compile(ast.Module(body=[node],type_ignores=[]),'<shared geometry>','exec'),globals())
_boolean=boolean
def boolean(ob,cutter,op='DIFFERENCE'):
 bpy.context.view_layer.update()
 _boolean(ob,cutter,op)
def move_objects(objs,M):
 bpy.context.view_layer.update()
 for x in objs:x.matrix_world=M@x.matrix_world
from posterboard_options import OPTIONS
O=dict(OPTIONS[2]);O['fold_columns']=[];L,W=O['cassette'];S=O['outer'];I=O['opening']
REPORT={'full_scale':{'outside_mm':S,'opening_mm':I,'border_mm':[L,W],'stock_sheet_mm':O['card'],'stock_sheets':12,'paper_cuts':0,'hinges':0,'fold_locks':0,'corner_keys':8,'PVC_docks':16,'channel_segments':216}}
old=O['PETG_kg'];new=old-.48*1.1
REPORT['cost']={'prior_foldable_PETG_kg':old,'rigid_PETG_kg':new,'removed_allowance_kg':old-new,'whole_kg_spools':math.ceil(new),'paper_USD':11.88,'consumed_USD_at_20_per_kg':new*20+11.88,'whole_spool_cash_USD':math.ceil(new)*20+11.88,'basis':'Same channel, dock, corner-key and workshop-joint allowances; remove 8 x 60g fold assemblies, then 10% waste. Planning estimate, not full-gate slicing.'}
def cassette(o,color=PAPER,transport=False):
 parts=leaf_geometry(o,0,3,color)
 for f in [1,2]:
  for z in [.04,W/1000-.04]:cube('Permanent straight splice / no hinge',(f*o['pitch'][0]/1000,.014,z),(.070,.008,.022),STEELBLUE,.001)
 return parts
setup('01_RIGID_GATE',(-3.5,-7.8,4.2),(.65,0,1.50),6.6);coll('01 / rigid whole-sheet cassettes');gate(O,pvc=True)
header('01','Whole sheets. Four rigid borders.','Twelve uncut 22 x 28 in inserts. Permanent internal splices. Release only the four gate corners and the PVC docks.')
overlay('NO HINGES / NO FOLD LOCKS',.71,.31,.017,True)
overlay('4 borders: 2146 x 563 mm\n8 removable corner bridge keys\nOne PVC backing + four braces',.71,.39,.015,color=MUTED)
overlay('2708 mm outside\n1583 mm clear opening',.71,.58,.017,True)
overlay(f'PETG planning: {new:.2f} kg\nAbout ${new*20+11.88:.0f} face materials\nPVC / anchoring additional',.71,.74,.015,color=MUTED)
footer('Long rigid borders require 2.15 m transport space. Cardstock stays installed. Permanent small rail splices are workshop assembly.')
setup('02_FOUR_RIGID_BORDERS',(2.7,-5.5,3.6),(.2,0,1.12),5.7,False);coll('01 / four separate rigid borders')
for k in range(4):
 before=set(COL.objects);cassette(O,PAPERS[k]);move_objects([x for x in COL.objects if x not in before],Matrix.Translation((-1.3,k*.17,.32+k*.12)))
header('02','Transport four long, flat sections','Each section keeps its three whole sheets, rear cross ribs and permanent rail joints. Nothing folds or creases.')
overlay('2145.6 x 562.8 mm',.70,.34,.021,True)
overlay('About 20-30 mm thick per border\nAllow pads between loaded faces',.70,.40,.014,color=MUTED)
overlay('REMOVED FROM OPTION C',.70,.57,.016,True)
overlay('16 hinges and their pins\n16 fold-lock bridges\nOffset mounts / folding clearance',.70,.63,.014,color=MUTED)
footer('Corner keys and PVC docks remain releasable. Stock paper is dry-weather material; retain the earlier anchored/ballasted PVC base design.')
setup('03_RIGID_SPLICES',(1.1,-1.8,1.1),(.55,0,.38),1.8,False);coll('01 / permanent workshop splice example')
# One whole-sheet bay plus adjacent bay edge; no hinge in the seam.
parts=leaf_geometry(O,0,1,PAPER)
for z in [.04,W/1000-.04]:cube('Permanent splice bridge',(O['pitch'][0]/1000,.014,z),(.070,.008,.022),STEELBLUE,.001)
header('03','The hinge becomes a fixed splice','Slide-in paper channels and rear ribs remain. Short printed rails still need rigid workshop nodes and removable paper end caps.')
overlay('216 short rail pieces per gate',.68,.35,.017,True)
overlay('Removing folding does not remove\nthe A1 Mini bed-size constraint',.68,.40,.014,color=MUTED)
overlay('Only eight field corner keys',.68,.65,.017,True)
footer('Full-size rail end nodes, twin-runner bridge adapters and PVC keeper remain design details to prototype; existing interface coupons are supplied.')
# ---- Print models: all local mesh coordinates in metres, export millimetres. ----
CHECKS={};MASTERS={}
def export(ob,filename):
 clean_mesh(ob);bm=bmesh.new();bm.from_mesh(ob.data);bad=sum(not e.is_manifold for e in bm.edges);volume=abs(bm.calc_volume())*1e9;bm.free();assert bad==0,(filename,bad)
 me=ob.data.copy();mins=Vector([min(v.co[j] for v in me.vertices) for j in range(3)])
 for v in me.vertices:v.co-=mins
 me.calc_loop_triangles();bounds=[max(v.co[j] for v in me.vertices)*1000 for j in range(3)];assert max(bounds)<171,(filename,bounds)
 with (OUT/'printable'/filename).open('wb') as f:
  f.write(b'FPV rigid gate; prototype; millimetres'.ljust(80,b' '));f.write(struct.pack('<I',len(me.loop_triangles)))
  for t in me.loop_triangles:
   a,b,c=[me.vertices[i].co*1000 for i in t.vertices];n=(b-a).cross(c-a).normalized();f.write(struct.pack('<12fH',*n,*a,*b,*c,0))
 bpy.data.meshes.remove(me);CHECKS[filename]={'bounds_mm':[round(v,3) for v in bounds],'solid_volume_mm3':round(volume,2),'solid_PLA_g':round(volume*.00124,2),'nonmanifold_edges':bad};MASTERS[filename]=ob
# 1:15 preserves in-plane dimensions, but makes printed thicknesses and keys usable.
scale=15;ml=L/scale;mw=W/scale;ms=S/scale;mi=I/scale
setup('05_A1_MINI_PRINT_LAYOUT',(.11,-.17,.28),(.085,.085,0),.36,False);coll('01 / printable miniature masters')
BORDER=mmcube('MINI / one rigid border / print four',(ml/2,mw/2,.4),(ml,mw,.8),PAPER);bake(BORDER)
# Continuous rear perimeter, cross ribs at paper boundaries, all built upward from bed.
for xyz,dims in [((ml/2,3,1.3),(ml,6,2.6)),((ml/2,mw-3,1.3),(ml,6,2.6)),((3,mw/2,1.3),(6,mw,2.6)),((ml-3,mw/2,1.3),(6,mw,2.6))]:boolean(BORDER,mmcube('Reinforced miniature rim',xyz,dims,STEELBLUE),'UNION')
for x in [ml/3,2*ml/3]:boolean(BORDER,mmcube('Visible whole-sheet boundary',(x,mw/2,1.1),(1.2,mw,2.2),ORANGE),'UNION')
# Four identical borders: right short-end holes mate with next border's lower long-edge holes.
HOLES=[(ml-4,8),(ml-4,mw-8),(8,4),(mw-8,4)]
for x,y in HOLES:boolean(BORDER,tube('3.6 mm bridge socket',(x/1000,y/1000,-.001),(x/1000,y/1000,.005),.0036,ORANGE))
export(BORDER,'mini_1to15_border_PRINT_4.stl')
def key(name,root,tip):
 pts=[(-4-root/2,0),(4+root/2,0),(4+root/2,2),(4+tip/2,7),(4-tip/2,7),(4-root/2,2),(-4+root/2,2),(-4+tip/2,7),(-4-tip/2,7),(-4-root/2,2)]
 return prism_xy(name,pts,2.4,ORANGE)
KEY=key('MINI / tapered bridge / print eight',3.2,2.2);export(KEY,'mini_bridge_standard_PRINT_8.stl')
LOOSE=key('MINI / alternate looser bridge',3.0,2.0);export(LOOSE,'mini_bridge_looser_OPTIONAL.stl')
FIT=mmcube('MINI / hole gauge 3.4 3.6 3.8',(9,18,1.3),(18,36,2.6),STEELBLUE);bake(FIT)
for row,d in enumerate([3.4,3.6,3.8]):
 for x in [5,13]:boolean(FIT,tube('Gauge hole',(x/1000,(6+row*12)/1000,-.001),(x/1000,(6+row*12)/1000,.005),d/1000,ORANGE))
export(FIT,'mini_bridge_fit_gauge_FIRST.stl')
STAND=mmcube('MINI / optional tabletop foot',(10,15,4),(20,30,8),STEELBLUE);bake(STAND)
boolean(STAND,mmcube('3 mm open vertical slot',(10,15,6),(22,3,6)))
export(STAND,'mini_tabletop_foot_PRINT_2.stl')
assert abs(CHECKS['mini_tabletop_foot_PRINT_2.stl']['solid_volume_mm3']-4500)<.1, 'Stand slot must remove 300 mm3'
# Show an actual feasible 180 mm bed arrangement: four borders plus 8 bridges.
for ob in MASTERS.values():ob.hide_render=True;ob.hide_set(True)
plate=[]
for k in range(4):
 ob=instance(BORDER,f'PLATE / border {k+1}',Matrix.Translation((.006,(6+k*(mw+4))/1000,0)));plate.append(ob)
for k in range(8):plate.append(instance(KEY,f'PLATE / key {k+1}',Matrix.Translation((.164,(8+k*11)/1000,0))))
cube('A1 Mini / 180 x 180 bed',(.09,.09,-.004),(.18,.18,.006),GROUND)
header('05','One plate for the four-part model','1:15 / four 143 x 38 mm borders plus eight miniature press-fit bridge keys. Print all parts at 100% file size.')
footer('Feet and fit gauge are separate small prints. No supports intended. Miniature keys demonstrate assembly; they are not scaled production snaps.')
# 3MF geometry-only multi-object plate, millimetres. Printer settings added by slicer later.
def write_3mf(objs,path):
 import xml.etree.ElementTree as ET
 ns='http://schemas.microsoft.com/3dmanufacturing/core/2015/02';ET.register_namespace('',ns)
 model=ET.Element('{'+ns+'}model',unit='millimeter',attrib={'xml:lang':'en-US'});res=ET.SubElement(model,'resources');build=ET.SubElement(model,'build')
 for i,ob in enumerate(objs,1):
  mesh=ob.data;mesh.calc_loop_triangles();obj=ET.SubElement(res,'object',id=str(i),type='model',name=ob.name);m=ET.SubElement(obj,'mesh');vs=ET.SubElement(m,'vertices');ts=ET.SubElement(m,'triangles')
  for v in mesh.vertices:
   a=ob.matrix_world@v.co*1000;ET.SubElement(vs,'vertex',x=f'{a.x:.6f}',y=f'{a.y:.6f}',z=f'{a.z:.6f}')
  for t in mesh.loop_triangles:ET.SubElement(ts,'triangle',v1=str(t.vertices[0]),v2=str(t.vertices[1]),v3=str(t.vertices[2]))
  ET.SubElement(build,'item',objectid=str(i))
 with zipfile.ZipFile(path,'w',zipfile.ZIP_DEFLATED) as z:
  z.writestr('[Content_Types].xml','<?xml version="1.0"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/></Types>')
  z.writestr('_rels/.rels','<?xml version="1.0"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Target="/3D/3dmodel.model" Id="rel0" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/></Relationships>')
  z.writestr('3D/3dmodel.model',ET.tostring(model,encoding='utf-8',xml_declaration=True))
write_3mf(plate,OUT/'printable/Mini_1to15_Four_Borders_LAYOUT.3mf')
fitplate=[]
for src,xy in [(FIT,(.006,.006)),(KEY,(.037,.008)),(LOOSE,(.037,.022)),(STAND,(.055,.006)),(STAND,(.080,.006))]:
 ob=instance(src,'Fit plate temporary',Matrix.Translation((*xy,0)));fitplate.append(ob)
write_3mf(fitplate,OUT/'printable/Mini_Fit_Test_and_Feet_LAYOUT.3mf')
for ob in fitplate:bpy.data.objects.remove(ob,do_unlink=True)
setup('04_MINI_ASSEMBLY',(.24,-.43,.31),(.03,0,.10),.46,False);coll('01 / assembled 1 to 15 miniature')
# Native miniature geometry is XY; stand the complete pinwheel vertically in XZ.
standup=Matrix(((1,0,0,-ms/2000),(0,0,1,0),(0,1,0,.003),(0,0,0,1)))
miniTransforms=[]
for k in range(4):
 M=Matrix.Translation((ms/2000,ms/2000,0))@Matrix.Rotation(-k*math.pi/2,4,'Z')@Matrix.Translation((-ms/2000,(ml-ms/2)/1000,0))
 miniTransforms.append(M);ob=instance(BORDER,f'MINI / assembled rigid border {k+1}',standup@M)
 ob.data=ob.data.copy();ob.data.materials.clear();ob.data.materials.append(PAPERS[k])
 for y in [8,mw-8]:
  # Key posts span each seam, 4 mm into each neighboring border.
  P=Matrix(((1,0,0,ml/1000),(0,0,1,(y-1.2)/1000),(0,-1,0,.007),(0,0,0,1)))
  instance(KEY,'MINI / removable bridge',standup@M@P)
for x in [-.055,.055]:instance(STAND,'MINI / tabletop stand',Matrix.Translation((x-.010,-.015,0)))
header('04','Print a four-part 1:15 assembly model','The complete miniature is 180.6 mm square with a 105.5 mm opening. Four long borders join with eight removable press-fit keys.')
overlay('143.04 x 37.52 mm / border',.70,.33,.017,True)
overlay('Print 4 borders + 8 keys\nOptional: 2 tabletop feet',.70,.40,.015,color=MUTED)
overlay('WHAT IT TESTS',.70,.59,.017,True)
overlay('Proportions and corner assembly\nHandling four rigid sections\nNot wind strength or full-size snap fit',.70,.66,.014,color=MUTED)
footer('Model faces are printed plastic. Thicknesses, sockets and miniature keys are intentionally enlarged; test real paper channels with the 1:1 coupons.')
# Exploded miniature key and gauge at a useful camera scale.
setup('06_MINI_KEY_AND_TEST',(.10,-.12,.15),(.035,.01,.015),.19,False);coll('01 / miniature fit gauge and press-fit key')
instance(FIT,'Gauge / print before full model',Matrix.Translation((-.015,0,0)))
instance(KEY,'Bridge / print flat',Matrix.Translation((.035,0,0)))
instance(LOOSE,'Looser bridge / alternative',Matrix.Translation((.035,.020,0)))
instance(STAND,'Optional display foot',Matrix.Translation((.065,.033,0)))
header('06','Check the miniature connector first','A tapered two-peg bridge presses into paired holes. Pull it out to separate the sections. No miniature hinge or fragile scaled latch.')
overlay('GAUGE ROWS',.12,.68,.017,True)
overlay('From Y=0 end: 3.4 / 3.6 / 3.8 mm\nModel sockets are 3.6 mm',.12,.74,.014,color=MUTED)
overlay('TWO KEY FITS',.56,.68,.017,True)
overlay('Standard + looser alternative\nUse the gentlest secure fit',.56,.74,.014,color=MUTED)
footer('Print flat as supplied. 0.4 mm nozzle / 0.20 mm layers / supports off. Do not resize the files; fit clearance is not scale invariant.')
# Verify transformed socket centers really match all 16 miniature bridge pegs.
allholes=[M@Vector((x/1000,y/1000,0)) for M in miniTransforms for x,y in HOLES]
errs=[]
for M in miniTransforms:
 for y in [8,mw-8]:
  for x in [ml-4,ml+4]:
   p=M@Vector((x/1000,y/1000,0));errs.append(min((p-h).length for h in allholes)*1000)
assert max(errs)<.001,errs
REPORT['miniature']={'scale':'1:15 in plane; practical unscaled thicknesses/joinery','outside_mm':ms,'opening_mm':mi,'border_mm':[ml,mw,2.6],'border_quantity':4,'bridge_quantity':8,'optional_feet':2,'socket_diameter_mm':3.6,'max_peg_to_socket_center_error_mm':max(errs),'assembly_model_only':True,'PLA_solid_estimate_g':4*CHECKS['mini_1to15_border_PRINT_4.stl']['solid_PLA_g']+8*CHECKS['mini_bridge_standard_PRINT_8.stl']['solid_PLA_g']}
REPORT['print_models']=CHECKS
(OUT/'validation.json').write_text(json.dumps(REPORT,indent=2))
for name,body in [('START_HERE.txt','RIGID WHOLE-SHEET ITERATION\nScenes 01-03: full-size rigid concept. Scenes 04-06: printable 1:15 assembly model.\nMiniature 3MF contains four borders and eight keys already at print size: import at 100%.\nRead DESIGN_AND_PRINT_GUIDE.md for fit-test-first workflow and limitations.\n')]:
 t=bpy.data.texts.new(name);t.write(body)
if (OUT/'DESIGN_AND_PRINT_GUIDE.md').exists():
 t=bpy.data.texts.new('DESIGN_AND_PRINT_GUIDE.md');t.write((OUT/'DESIGN_AND_PRINT_GUIDE.md').read_text())
empty=bpy.data.scenes.get('01_ASSEMBLED')
if empty and len(empty.objects)==0:bpy.data.scenes.remove(empty)
bpy.context.window.scene=bpy.data.scenes['01_RIGID_GATE']
for screen in bpy.data.screens:
 for area in screen.areas:
  if area.type=='VIEW_3D':area.spaces.active.region_3d.view_perspective='CAMERA';area.spaces.active.shading.type='MATERIAL'
bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'Rigid_Whole_Sheet_Gate.blend'))
for name in sorted(s.name for s in bpy.data.scenes):
 s=bpy.data.scenes[name];bpy.context.window.scene=s;s.render.filepath=str(OUT/'renders'/f'{name}.png');bpy.ops.render.render(write_still=True,scene=name)
print('RIGID BUILD COMPLETE',json.dumps(REPORT))

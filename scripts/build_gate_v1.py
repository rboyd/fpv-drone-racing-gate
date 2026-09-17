"""FPV gate: reproducible Blender model. Units: metres; STL export: millimetres."""
import bpy, math, os, json, struct
from mathutils import Vector, Matrix
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'output'
for d in ['renders','printable','cut-layouts']: (OUT/d).mkdir(parents=True,exist_ok=True)
bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False)
for s in list(bpy.data.scenes)[1:]: bpy.data.scenes.remove(s)
SC=bpy.context.scene; SC.name='01_ASSEMBLED'
FONT=bpy.data.fonts.load('/System/Library/Fonts/Supplemental/Arial.ttf')
BOLD=bpy.data.fonts.load('/System/Library/Fonts/Supplemental/Arial Bold.ttf')
def mat(name,c,metal=0,rough=.5,emit=False):
 m=bpy.data.materials.new(name); m.diffuse_color=(*c,1); m.use_nodes=True
 n=m.node_tree.nodes.get('Principled BSDF'); n.inputs['Base Color'].default_value=(*c,1); n.inputs['Roughness'].default_value=rough; n.inputs['Metallic'].default_value=metal
 if emit:
  ns=m.node_tree.nodes; ns.clear(); out=ns.new('ShaderNodeOutputMaterial'); em=ns.new('ShaderNodeEmission'); em.inputs['Color'].default_value=(*c,1); em.inputs['Strength'].default_value=1; m.node_tree.links.new(em.outputs[0],out.inputs[0])
 return m
BLUE=mat('Face / cobalt blue',(.018,.065,.55)); BLUE2=mat('Face extension / blue',(.028,.12,.7)); WHITE=mat('PVC / warm white',(.83,.86,.83)); RETURN=mat('Coroplast / white returns',(.7,.8,.85)); ORANGE=mat('Printed PETG / orange',(.95,.21,.025)); INK=mat('Typography / navy',(.015,.033,.068),emit=True); MUTED=mat('Typography / slate',(.055,.08,.105),emit=True); CORD=mat('Guy lines / amber',(.95,.46,.025)); DARK=mat('Ties / graphite',(.022,.033,.048)); GROUND=mat('Ground / warm gray',(.78,.81,.81)); PATCH=mat('Scrap backers / pale blue',(.31,.53,.74)); METAL=mat('Stakes / steel',(.25,.3,.32),.75); GREEN=mat('Sheet spare',(.65,.78,.68)); LIGHTTEXT=mat('White lettering',(.95,.98,1),emit=True)
COL=None

def coll(name):
 global COL
 COL=bpy.data.collections.new(name); SC.collection.children.link(COL); return COL

def link(o):
 for c in list(o.users_collection): c.objects.unlink(o)
 (COL or SC.collection).objects.link(o); return o

def cube(name,loc,size,material,bevel=0):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc); o=link(bpy.context.object); o.name=name; o.dimensions=size
 bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
 o.data.materials.append(material)
 if bevel:
  m=o.modifiers.new('Soft edges','BEVEL'); m.width=bevel; m.segments=2
  o.modifiers.new('Weighted normals','WEIGHTED_NORMAL')
 return o

def tube(name,a,b,od,material,wall=0):
 a,b=Vector(a),Vector(b); length=(b-a).length; n=32; ro=od/2; ri=max(ro-wall,0)
 if wall:
  verts=[]
  for z,r in [(-length/2,ro),(length/2,ro),(-length/2,ri),(length/2,ri)]:
   verts += [(r*math.cos(i*2*math.pi/n),r*math.sin(i*2*math.pi/n),z) for i in range(n)]
  faces=[]
  for i in range(n):
   j=(i+1)%n; faces.extend([(i,j,n+j,n+i),(2*n+j,2*n+i,3*n+i,3*n+j),(j,i,2*n+i,2*n+j),(n+i,n+j,3*n+j,3*n+i)])
  mesh=bpy.data.meshes.new(name); mesh.from_pydata(verts,[],faces); mesh.update(); o=bpy.data.objects.new(name,mesh); (COL or SC.collection).objects.link(o); o.location=(a+b)/2
 else:
  bpy.ops.mesh.primitive_cylinder_add(vertices=n,radius=ro,depth=length,location=(a+b)/2); o=link(bpy.context.object); o.name=name
 o.rotation_euler=(b-a).to_track_quat('Z','Y').to_euler(); o.data.materials.append(material)
 for p in o.data.polygons: p.use_smooth=True
 return o

def line(name,pts,r,material,closed=False):
 cv=bpy.data.curves.new(name,'CURVE'); cv.dimensions='3D'; cv.bevel_depth=r; cv.resolution_u=1; cv.bevel_resolution=2
 sp=cv.splines.new('POLY'); sp.points.add(len(pts)-1)
 for p,co in zip(sp.points,pts): p.co=(*co,1)
 sp.use_cyclic_u=closed; o=bpy.data.objects.new(name,cv); (COL or SC.collection).objects.link(o); o.data.materials.append(material); return o

def text(name,body,loc,size=.06,material=INK,rot=(math.pi/2,0,0),bold=False,align='LEFT'):
 cv=bpy.data.curves.new(name,'FONT'); cv.body=body; cv.font=BOLD if bold else FONT; cv.size=size; cv.align_x=align; cv.space_line=1.2
 o=bpy.data.objects.new(name,cv); (COL or SC.collection).objects.link(o); o.location=loc; o.rotation_euler=rot; o.data.materials.append(material); return o

def camera(loc,target,scale):
 bpy.ops.object.camera_add(location=loc); cam=link(bpy.context.object); cam.name='Camera / presentation'; cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler(); cam.data.type='ORTHO'; cam.data.clip_start=.001; cam.data.ortho_scale=scale; SC.camera=cam; return cam

def overlay(body,x,y,size=.022,bold=False,color=INK):
 cam=SC.camera; w=cam.data.ortho_scale; h=w*SC.render.resolution_y/SC.render.resolution_x
 o=text('Caption / '+body[:25],body,(0,0,0),w*size,color,(0,0,0),bold)
 o.parent=cam; o.location=(-w/2+x*w,h/2-y*h,-.01); return o

def setup(name,loc,target,scale,ground=True):
 global SC,COL
 SC=bpy.data.scenes.get(name) if name=='01_ASSEMBLED' else bpy.data.scenes.new(name)
 bpy.context.window.scene=SC; COL=None
 SC.unit_settings.system='METRIC'; SC.unit_settings.length_unit='MILLIMETERS'; SC.unit_settings.scale_length=1
 SC.render.engine='CYCLES'; SC.cycles.samples=24; SC.cycles.use_denoising=True
 SC.render.resolution_x=1800; SC.render.resolution_y=1200; SC.render.resolution_percentage=100
 SC.world=bpy.data.worlds.new(name+' / world'); SC.world.use_nodes=True; SC.world.node_tree.nodes['Background'].inputs[0].default_value=(.79,.84,.9,1); SC.world.node_tree.nodes['Background'].inputs[1].default_value=.35
 SC.view_settings.view_transform='AgX'; SC.render.image_settings.file_format='PNG'
 coll('90 / presentation'); camera(loc,target,scale)
 if ground: cube('Ground',(0,0,-.075),(200,200,.05),GROUND)
 for p,power,size in [((-3,-4,7),550,5),((4,3,6),650,4)]:
  bpy.ops.object.light_add(type='AREA',location=p); o=link(bpy.context.object); o.data.energy=power; o.data.shape='DISK'; o.data.size=size; o.rotation_euler=(Vector((0,0,1))-o.location).to_track_quat('-Z','Y').to_euler()
 return SC

def header(num,title,sub):
 coll('91 / page annotations')
 overlay('FIELDWORK  /  FPV RACING GATE',.045,.054,.014,True,MUTED)
 overlay(num,.93,.057,.018,True,MUTED)
 overlay(title,.044,.124,.042,True)
 overlay(sub,.046,.163,.014,color=MUTED)

def footer(t): overlay(t,.046,.956,.012,color=MUTED)

# Print master: broad saddle; no snap latch or threaded inserts.
def boolean_slot(o,x,y):
 cutter=cube('slot cutter',(x,y,.01),(.0032,.006,.06),ORANGE)
 bpy.context.view_layer.objects.active=o; m=o.modifiers.new('Tie slot','BOOLEAN'); m.operation='DIFFERENCE'; m.solver='EXACT'; m.object=cutter; bpy.ops.object.modifier_apply(modifier=m.name); bpy.data.objects.remove(cutter,do_unlink=True)

def saddle(name,od):
 r=od/2+.0002; center=.007+r; edge=math.sqrt(r*r-(center-.018)**2)
 xs=[-.030,-edge]+[-edge+2*edge*i/40 for i in range(1,40)]+[edge,.030]
 profile=[(-.030,0),(.030,0),(.030,.005),(.020,.005),(.020,.018)]+[(x,min(.018,center-math.sqrt(max(0,r*r-x*x)))) for x in reversed(xs[1:-1])]+[(-.020,.018),(-.020,.005),(-.030,.005)]
 n=len(profile); verts=[(x,y,z) for y in [-.02,.02] for x,z in profile]; faces=[]
 faces.extend([tuple(reversed(range(n))),tuple(range(n,2*n))])
 for i in range(n): j=(i+1)%n; faces.append((i,j,j+n,i+n))
 mesh=bpy.data.meshes.new(name); mesh.from_pydata(verts,[],faces); mesh.update(); o=bpy.data.objects.new(name,mesh); COL.objects.link(o); o.data.materials.append(ORANGE)
 for x in [-.023,.023]:
  for y in [-.01,.01]: boolean_slot(o,x,y)
 # Normals made consistent before export.
 bpy.context.view_layer.objects.active=o; o.select_set(True)
 import bmesh
 bm=bmesh.new(); bm.from_mesh(o.data); bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces)); bm.to_mesh(o.data); bm.free()
 o['pipe_OD_mm']=od*1000; o['diametral_clearance_mm']=.4; o['print_orientation']='Flat face on bed; no supports'; return o

def export_stl(o,name):
 mesh=o.data.copy(); mesh.calc_loop_triangles()
 with open(OUT/'printable'/name,'wb') as f:
  f.write(b'FPV gate; coordinates in mm'.ljust(80,b' ')); f.write(struct.pack('<I',len(mesh.loop_triangles)))
  for t in mesh.loop_triangles:
   vs=[mesh.vertices[i].co*1000 for i in t.vertices]; normal=(vs[1]-vs[0]).cross(vs[2]-vs[0]).normalized()
   f.write(struct.pack('<12fH',*normal,*vs[0],*vs[1],*vs[2],0))
 bpy.data.meshes.remove(mesh)

setup('05_CLIP_DETAIL',(.14,-.24,.19),(0,0,.06),.44,False); coll('01 / printable masters')
SADDLE=saddle('PRINT / saddle 1 inch / 60 x 40 x 18 mm',.033401); export_stl(SADDLE,'saddle_1in_OD33p40_mm.stl')
SADDLE34=saddle('PRINT / optional saddle 3-4 inch / 60 x 40 x 18 mm',.02667); export_stl(SADDLE34,'optional_saddle_3_4in_OD26p67_mm.stl'); SADDLE34.hide_render=True; SADDLE34.hide_set(True)
WASH=cube('PRINT / front load washer / 60 x 40 x 2.5 mm',(0,0,.00125),(.06,.04,.0025),BLUE)
# Bake washer location so both printable masters have origin at bed level.
bpy.context.view_layer.objects.active=WASH; bpy.ops.object.transform_apply(location=True,rotation=False,scale=False)
for x in [-.023,.023]:
 for y in [-.01,.01]: boolean_slot(WASH,x,y)
export_stl(WASH,'front_load_washer_mm.stl')
# Clip assembly exploded, flat bed orientation also demonstrates no supports.
SADDLE.location=(-.045,0,.06); WASH.location=(-.045,0,0)
cube('DEMO / 4 mm sheet',(-.045,0,.025),(.092,.075,.004),BLUE)
cube('DEMO / 4 mm scrap reinforcing pad',(-.045,0,.039),(.07,.05,.004),PATCH)
tube('DEMO / 1 inch PVC',(-.045,-.065,.112),(-.045,.065,.112),.033401,WHITE,.003378)
# Assembled smaller companion for a clear path of the two zip ties.
def copy_obj(src,name,loc,rot=None):
 o=src.copy(); o.data=src.data; o.name=name; COL.objects.link(o); o.hide_render=False; o.hide_set(False); o.location=loc
 if rot is not None: o.rotation_euler=rot
 return o
cp=copy_obj(SADDLE,'DEMO / assembled saddle',(.072,0,.02),(0,0,0)); wp=copy_obj(WASH,'DEMO / assembled washer',(.072,0,.0095),(0,0,0))
cube('DEMO / assembled sheet',(.072,0,.014),(.068,.048,.004),BLUE); cube('DEMO / assembled pad',(.072,0,.018),(.068,.048,.004),PATCH)
cy=.02+.0239005
tube('DEMO / assembled pipe',(.072,-.057,cy),(.072,.057,cy),.033401,WHITE,.003378)
for yy in [-.01,.01]:
 pts=[(.072-.023,yy,.0095),(.072+.023,yy,.0095),(.072+.023,yy,cy)]
 pts += [(.072+.023*math.cos(a),yy,cy+.020*math.sin(a)) for a in [i*math.pi/16 for i in range(17)]]
 pts +=[(.072-.023,yy,.0095)]; line('DEMO / zip tie path',pts,.0012,DARK)
header('05','Tie-retained saddle','Two ties per attachment. Broad contact. No snap-fit dependency.')
overlay('EXPLODED',.15,.31,.018,True); overlay('ASSEMBLED',.69,.55,.018,True)
overlay('1 in PVC / OD 33.40 mm',.57,.26,.014)
overlay('PETG saddle / 60 x 40 x 18',.57,.30,.014)
overlay('4 mm scrap pad + 4 mm face',.57,.34,.014)
overlay('Front washer / 2.5 mm',.57,.38,.014)
footer('20 saddles + 20 washers per gate. STL units: mm. Print one fit sample first. Optional 3/4 in saddle is not in the BOM.')

# Gate parts grouped for assembly and exploded views.
setup('01_ASSEMBLED',(-3.6,-7,3.7),(.6,0,1.48),6.4)
coll('01 / face panels / 4 mm'); FACE=[]
def panel(name,x,z,w,h,material=BLUE):
 o=cube(name,(x,.002,z),(w,.004,h),material); FACE.append(o); o['thickness_mm']=4; return o
panel('F1 / top main / 2400 x 600',-.15,2.4,2.4,.6)
panel('F2 / bottom main / 2400 x 600',.15,.3,2.4,.6)
panel('F3 / left stile / 1500 x 600',-1.05,1.35,.6,1.5)
panel('F4 / right stile / 1500 x 600',1.05,1.35,.6,1.5)
panel('F5 / top cap / 300 x 600',1.2,2.4,.3,.6,BLUE2)
panel('F6 / bottom cap / 300 x 600',-1.2,.3,.3,.6,BLUE2)
coll('02 / scrap seam backers'); BACK=[]
for x,z in [(1.05,2.4),(-1.05,.3)]: BACK.append(cube('B1 / extension backer / 180 x 525',(x,.006,z+(.0375 if z>1 else -.0375)),(.18,.004,.525),PATCH))
for x in [-1.05,1.05]:
 for z in [.6,2.1]: BACK.append(cube('B2 / stile seam backer / 560 x 150',(x+math.copysign(.020,x),.006,z),(.56,.004,.15),PATCH))
coll('03 / 260 mm opening returns'); RET=[]
for x in [-.752,.752]:
 RET.append(cube('R1 / side wall / 1500 x 256',(x,.132,1.35),(.004,.256,1.5),RETURN))
 RET.append(cube('R1 / outward folded 30 mm flange',(math.copysign(.769,x),.006,1.35),(.03,.004,1.5),RETURN))
for z in [.598,2.102]:
 RET.append(cube('R2 / top-bottom wall / 1508 x 256',(0,.132,z),(1.508,.256,.004),RETURN))
 RET.append(cube('R2 / outward folded 30 mm flange',(0,.006,z+(-.017 if z<1 else .017)),(1.508,.004,.03),RETURN))
# Mechanically stitched return corners and flanges. Cord loops schematic at true connection positions.
for x in [-.752,.752]:
 for z in [.598,2.102]:
  for y in [.055,.14,.225]:
   sx=1 if x>0 else -1; sz=1 if z>1 else -1
   line('Return corner / zip-tie stitch',[(x-sx*.018,y,z),(x,y,z+sz*.018),(x+sx*.006,y,z+sz*.006)],.0013,DARK,True)
for x in [-.769,.769]:
 for z in [.7,.95,1.2,1.45,1.7,1.95,2.03]: line('Flange tie / side',[(x-.004,-.001,z),(x+.004,-.001,z),(x+.004,.009,z),(x-.004,.009,z)],.0009,DARK,True)
for z in [.58,2.12]:
 for x in [-.68,-.43,-.18,.07,.32,.57,.68]: line('Flange tie / top-bottom',[(x,-.001,z-.004),(x,-.001,z+.004),(x,.009,z+.004),(x,.009,z-.004)],.0009,DARK,True)
coll('04 / 1 inch PVC frame and feet'); FRAME=[]
P=.0319005; G=.0174625; H=.04048; OD=.033401
# Four long pipes use manufacturer fitting stop offsets, not socket depth subtraction.
def pipe(name,a,b,od=OD):
 o=tube(name,a,b,od,WHITE,.003378 if od==OD else .00287); o['cut_length_mm']=round((Vector(b)-Vector(a)).length*1000,3); FRAME.append(o); return o
for z in [.3,2.4]: pipe('P1 / rail / 2065.075 mm',(-1.05+G,P,z),(1.05-G,P,z))
for x in [-1.05,1.05]:
 pipe('P2 / upright / 2065.075 mm',(x,P,.3+G),(x,P,2.4-G))
 pipe('P3 / leg / 290.075 mm',(x,P,-.025+G),(x,P,.3-G))
 for s in [-1,1]: pipe('P4 / foot / 582.538 mm',(x,P+s*G,-.025),(x,P+s*.6,-.025))
# Fittings are simplified envelopes with socket collars, not printable parts.
def fitting(name,center,dirs):
 c=Vector(center)
 body=cube(name+' / hub',c,(.040,.040,.040),WHITE,.008); FRAME.append(body); body['visual_only']='Purchased fitting envelope; verify actual dimensions'
 for d in dirs:
  d=Vector(d); o=tube(name+' / socket',c+d*.009,c+d*H,.046,WHITE,.0063); FRAME.append(o)
for x in [-1.05,1.05]:
 inward=1 if x<0 else -1
 fitting('E1 / bought 1 in elbow',(x,P,2.4),[(inward,0,0),(0,0,-1)])
 fitting('T1 / bought 1 in tee',(x,P,.3),[(0,0,1),(0,0,-1),(inward,0,0)])
 fitting('T2 / bought 1 in foot tee',(x,P,-.025),[(0,1,0),(0,-1,0),(0,0,1)])
 for s in [-1,1]:
  FRAME.append(tube('C1 / bought end cap',(x,P+s*.588,-.025),(x,P+s*.608,-.025),.041,WHITE))
# Small screws retain sockets; these joints are not pressure service.
for x in [-1.05,1.05]:
 for z in [.07,.26,.34,2.36]: tube('Retaining screw / schematic',(x,P+.02,z),(x,P+.028,z),.007,METAL)
coll('05 / 3-4 inch corner braces'); BRACE=[]
for sx in [-1,1]:
 for top in [False,True]:
  z=2.4 if top else .3; dz=-1 if top else 1
  a=Vector((sx*1.05,P+.031,z+dz*.4)); b=Vector((sx*.65,P+.031,z)); v=(b-a).normalized()
  o=tube('P5 / corner brace / 646 mm',a-v*.040,b+v*.040,.02667,WHITE,.00287); BRACE.append(o); o['cut_length_mm']=646
  for pt in [a,b]:
   for off in [-.009,.009]:
    line('Brace / crossed zip tie',[(pt.x-.024,pt.y-.044,pt.z+off-.02),(pt.x+.024,pt.y-.044,pt.z+off+.02),(pt.x+.024,pt.y+.017,pt.z+off+.02),(pt.x-.024,pt.y+.017,pt.z+off-.02)],.0015,DARK,True)
coll('06 / printed attachments and zip ties'); ATT=[]
Rvert=Matrix(((1,0,0),(0,0,1),(0,-1,0))).to_4x4()
Rhor=Matrix(((0,1,0),(0,0,1),(1,0,0))).to_4x4()
positions=[(x,z,False) for z in [.3,2.4] for x in [-.84,-.42,0,.42,.84]]+[(x,z,True) for x in [-1.05,1.05] for z in [.45,.9,1.35,1.8,2.25]]
for i,(x,z,vert) in enumerate(positions):
 R=Rvert if vert else Rhor
 # Local z points toward the rear of the gate, local y follows the pipe.
 M=Matrix.Translation((x,.008,z))@R
 o=copy_obj(SADDLE,f'A{i+1:02} / 1 inch saddle',(0,0,0)); o.matrix_world=M; ATT.append(o)
 w=copy_obj(WASH,f'A{i+1:02} / front washer',(0,0,0)); w.matrix_world=Matrix.Translation((x,-.0025,z))@R; ATT.append(w)
 if not (vert and ((x<0 and z==.45) or (x>0 and z==2.25))):
  pad=cube(f'A{i+1:02} / scrap pad',(x,.006,z),(.07 if vert else .05,.004,.05 if vert else .07),PATCH); ATT.append(pad)
 for yy in [-.01,.01]:
  pts=[(-.023,yy,-.0105),(.023,yy,-.0105),(.023,yy,.024)]
  pts +=[(.023*math.cos(a),yy,.024+.020*math.sin(a)) for a in [j*math.pi/16 for j in range(17)]]
  pts +=[(-.023,yy,-.0105)]
  line('4.8 mm UV zip tie / attachment',[M@Vector(p) for p in pts],.0013,DARK)
# Fasten long and horizontal seams with stitched pairs, independent of adhesive.
for x,z in [(1.05,2.4),(-1.05,.3)]:
 for dz in [-.24,-.08,.08,.24]:
  line('Extension seam / tie bridge',[(x-.06,-.001,z+dz),(x+.06,-.001,z+dz),(x+.06,.009,z+dz),(x-.06,.009,z+dz)],.0011,DARK,True)
for x in [-1.05,1.05]:
 for z in [.6,2.1]:
  for dx in [-.23,0,.23]: line('Stile seam / tie bridge',[(x+dx,-.001,z-.04),(x+dx,-.001,z+.04),(x+dx,.009,z+.04),(x+dx,.009,z-.04)],.0011,DARK,True)
coll('07 / guy lines and ground anchors'); ANCHOR=[]
for sx in [-1,1]:
 for sy in [-1,1]:
  a=(sx*1.05,P,2.4); b=(sx*1.6,P+sy*1.2,-.025)
  o=line('4 mm guy cord / outside flight opening',[a,b],.002,CORD); ANCHOR.append(o)
  o=tube('450 mm ground anchor / indicative',(b[0],b[1],-.45),(b[0],b[1],0),.012,METAL); ANCHOR.append(o)
  cube('Bright anchor marker',(b[0],b[1],-.025),(.08,.06,.045),ORANGE,.008)
# Presentation dimensions, visible front.
coll('80 / dimensions')
def dim(a,b,label,offset=(0,0,0),ts=.055):
 a,b=Vector(a),Vector(b); line('Dimension / '+label,[a,b],.002,MUTED)
 d=(b-a).normalized(); tick=Vector((0,0,.035)) if abs(d.x)>.5 else Vector((.035,0,0))
 for p in [a,b]: line('Dimension tick',[p-tick,p+tick],.002,MUTED)
 text('Dimension text',label,(a+b)/2+Vector(offset),ts,MUTED,align='CENTER')
dim((-1.35,-.06,2.86),(1.35,-.06,2.86),'2700 mm',(0,0,.055))
dim((-.75,-.065,1.33),(.75,-.065,1.33),'1500 mm clear',(0,0,.075))
dim((-1.52,-.04,0),(-1.52,-.04,2.7),'2700',(-.08,0,0))
header('01','FPV / 2700','A single face. A braced PVC frame. Replaceable, tie-fastened parts.')
overlay('2700 x 2700',.735,.31,.025,True); overlay('Face / 600 mm border',.735,.355,.015,color=MUTED)
overlay('1500 x 1500',.735,.45,.025,True); overlay('Clear opening / 260 mm deep',.735,.495,.015,color=MUTED)
overlay('3 sheets + 5 pipes',.735,.59,.023,True); overlay('4 x 1 in + 1 x 3/4 in\nAll pipe stock: 10 ft',.735,.635,.015,color=MUTED)
overlay('Stake in both directions',.735,.76,.017,True); overlay('Feet and anchors extend\nbeyond the 260 mm body.',.735,.80,.014,color=MUTED)
footer('DESIGN PROTOTYPE  /  4 mm Coroplast assumed  /  Grass stakes shown  /  Verify wind response before racing')
ASSEMBLY=SC
# Additional rear and exploded scenes link original geometry, retaining native part names.
def dup_collection(src,delta=(0,0,0),prefix=''):
 c=bpy.data.collections.new(prefix+src.name); SC.collection.children.link(c)
 for old in src.objects:
  o=old.copy(); o.data=old.data; c.objects.link(o); o.location=old.location+Vector(delta)
 return c
setup('02_REAR_STRUCTURE',(4,7,4.4),(-.4,0,1.50),6.3)
for c in ASSEMBLY.collection.children:
 if c.name[:2] in ['01','02','03','04','05','06','07']: dup_collection(c)
header('02','The structure behind it','One frame, four corner braces, four guy lines. All hardware stays outside the opening.')
overlay('01 / MAIN FRAME',.725,.31,.017,True); overlay('1 in Schedule 40 PVC\n2100 x 2100 mm centerlines',.725,.35,.014,color=MUTED)
overlay('02 / CORNER BRACES',.725,.47,.017,True); overlay('3/4 in PVC / 4 x 646 mm\nCross-lashed at each end',.725,.51,.014,color=MUTED)
overlay('03 / OPENING WALLS',.725,.63,.017,True); overlay('Folded 30 mm fixing flanges\nStitched corners / no rear face',.725,.67,.014,color=MUTED)
overlay('04 / BASE',.725,.79,.017,True); overlay('1200 mm fore-aft pipe feet\nFour anchors resist reversal',.725,.83,.014,color=MUTED)
footer('Purchased elbows and tees are simplified envelopes. Pin/screw removable sockets. Tape alone is not a structural attachment.')
setup('03_EXPLODED',(5,-7,4.8),(.5,.1,1.55),7.6)
for c in ASSEMBLY.collection.children:
 key=c.name[:2]
 if key in ['01','02','03','04','05','06']:
  delta={'01':(-.65,-.9,0),'02':(-.25,-.45,0),'03':(.85,1.1,0),'04':(.3,.25,0),'05':(.3,.25,0),'06':(0,-.15,0)}[key]
  dup_collection(c,delta)
header('03','Assembly / layer by layer','Front face -> scrap backers -> saddles -> PVC -> folded opening walls')
overlay('1  CUT + SPLICE',.75,.30,.017,True); overlay('2400 + 300 = 2700 mm\nBackers bridge every seam',.75,.34,.014,color=MUTED)
overlay('2  BUILD THE FRAME',.75,.47,.017,True); overlay('Standard tees and elbows\nAdd braces and broad feet',.75,.51,.014,color=MUTED)
overlay('3  TIE ON THE FACE',.75,.64,.017,True); overlay('20 saddles / two ties each\nUse washers + scrap pads',.75,.68,.014,color=MUTED)
overlay('4  CLOSE THE TUNNEL',.75,.81,.017,True); overlay('Fold, stitch, square, anchor',.75,.85,.014,color=MUTED)
footer('Exploded spacing is for instruction only. Assembled body depth is 260 mm; full support footprint is larger.')
# Sheet layout in native Blender. Exact stock and part dimensions, knife cuts.
setup('04_SHEET_LAYOUT',(0,-8,2.35),(0,0,2.35),7.9,False)
coll('01 / sheet nesting'); layout=[]
def sheet_rect(sheet,x,y,w,h,name,color):
 # Three side-by-side sheets, longest edge vertical for readable presentation.
 ox=(sheet-1)*2.55-2.55; oz=.52
 o=cube(name,(ox+x/1000+w/2000-1.2192/2,.001,oz+y/1000+h/2000),(w/1000,.004,h/1000),color)
 layout.append(dict(sheet=sheet,x=x,y=y,w=w,h=h,name=name))
 return o
for s in [1,2,3]:
 ox=(s-1)*2.55-2.55
 cube('Stock / 2438.4 x 1219.2',(ox,.008,.52+2.4384/2),(1.2192,.006,2.4384),GREEN)
 text('Sheet number',f'SHEET {s:02}',(ox-.61,-.012,3.13),.1,INK,bold=True)
 text('Stock size','1219.2 x 2438.4 mm',(ox-.61,-.012,3.00),.055,MUTED)
 if s==1:
  for x in [0,600]:
   sheet_rect(s,x,0,600,2400,'Face main / 2400 x 600',BLUE)
   text('Part label','2400\nx 600',(ox+x/1000-.6096+.3,-.008,1.67),.095,LIGHTTEXT,align='CENTER',bold=True)
 elif s==2:
  for x in [0,600]:
   y=0
   for h,name,color in [(1500,'Stile',BLUE),(300,'Cap',BLUE2),(180,'Splice',PATCH),(150,'Joint',PATCH),(150,'Joint',PATCH)]:
    sheet_rect(s,x,y,600,h,name,color)
    text('Cut label',f'{name}\n{h} x 600' if h>=300 else f'{h} x 600',(ox+x/1000-.6096+.3,-.008,.52+y/1000+h/2000-.035),.06 if h>=300 else .048,LIGHTTEXT if h>=300 else INK,align='CENTER')
    y+=h
 elif s==3:
  for i in range(4):
   h=1500 if i<2 else 1508
   sheet_rect(s,i*286,0,286,h,'Return blank / '+str(h)+' x 286',RETURN)
   xx=ox-.6096+i*.286
   line('30 mm flange fold',[(xx+.03,-.008,.52),(xx+.03,-.008,.52+h/1000)],.0015,ORANGE)
   text('Return label',f'{h}\nx 286',(xx+.16,-.009,1.2),.062,INK,align='CENTER')
  text('Spare material','SPARE / repairs\n+ reinforcement pads',(ox-.50,-.012,2.60),.065,INK)
header('04','Every cut has a place','Three 8 x 4 ft sheets. Face on sheets 1-2; opening walls on sheet 3.')
overlay('2400 + 300 mm',.062,.865,.019,True); overlay('Seam sits over an upright',.062,.905,.013,color=MUTED)
overlay('Backers from offcuts',.389,.865,.019,True); overlay('600 x 150 blanks: trim to 560 wide',.389,.905,.013,color=MUTED)
overlay('286 = 256 + 30 mm',.711,.865,.019,True); overlay('Wall depth + fixing flange',.711,.905,.013,color=MUTED)
footer('Knife layout / no saw kerf assumed. Green = spare. Orange = fold. Return blanks need a bend test and corner relief trimming.')
# Front dimensional elevation, useful separately from hero.
setup('06_DIMENSIONS',(0,-8,1.60),(0,0,1.60),6.2,False)
for c in ASSEMBLY.collection.children:
 if c.name[:2] in ['01','03','80']: dup_collection(c)
header('06','Dimensions / front elevation','All dimensions in millimetres. Clear flight envelope: 1500 x 1500 x 260.')
coll('02 / supplementary dimensions')
dim((-.75,-.07,.46),(.75,-.07,.46),'1500',(0,0,.06),.06)
dim((1.50,-.07,.6),(1.50,-.07,2.1),'1500',(.15,0,0),.06)
text('Border dimension','600',(1.06,-.07,1.35),.07,LIGHTTEXT,align='CENTER')
footer('Face: x = -1350..1350, z = 0..2700. Opening: x = -750..750, z = 600..2100. Front y = 0; rear wall edge y = 260.')
# Hard-surface configuration: longer self-contained feet, ballasted at guy attachment points.
setup('07_HARD_SURFACE',(4.8,6.4,4.4),(-.4,0,1.45),6.5)
for c in ASSEMBLY.collection.children:
 if c.name[:2] in ['01','02','03','04','05','06']:
  nc=dup_collection(c,prefix='Hard / ')
  if c.name[:2]=='04':
   for o in list(nc.objects):
    if o.name.startswith(('P4 / foot','C1 / bought end cap')): bpy.data.objects.remove(o,do_unlink=True)
coll('07 / hard floor extended feet and ballast')
BAG=mat('Ballast / olive fabric',(.19,.27,.17),rough=.92)
for sx in [-1,1]:
 for sy in [-1,1]:
  x=sx*1.05
  pipe('H1 / extended foot / 1182.538 mm',(x,P+sy*G,-.025),(x,P+sy*1.2,-.025))
  tube('H2 / end cap',(x,P+sy*1.188,-.025),(x,P+sy*1.208,-.025),.041,WHITE)
  by=P+sy*1.10
  cube('H3 / anti-slip rubber under ballast',(x,by,-.048),(.46,.40,.004),DARK,.002)
  cube('H4 / 15 kg filled ballast bag',(x,by,.035),(.42,.34,.16),BAG,.042)
  # Straps tie the flexible bag to the actual foot, preventing separation.
  for dy in [-.08,.08]:
   line('H5 / ballast retaining strap',[(x-.20,by+dy,-.035),(x-.20,by+dy,.12),(x+.20,by+dy,.12),(x+.20,by+dy,-.035)],.006,DARK,True)
  line('H6 / guy to ballasted foot end',[(x,P,2.4),(x,P+sy*1.15,-.015)],.002,CORD)
header('07','Hard ground / contained base','Longer feet carry the guy anchors. Ballast is strapped to the feet, over anti-slip mats.')
overlay('2400 mm FOOT SPAN',.73,.31,.018,True)
overlay('4 x 1182.5 mm half-feet\nTwo extra 10 ft / 1 in pipes',.73,.35,.014,color=MUTED)
overlay('4 x 15 kg BALLAST',.73,.49,.018,True)
overlay('60 kg total / weighed fill\nBags retained to the pipe ends',.73,.53,.014,color=MUTED)
overlay('FOUR INTERNAL GUYS',.73,.67,.017,True)
overlay('Upper corners to foot ends\nNo loose freestanding anchors',.73,.71,.014,color=MUTED)
overlay('PROTOTYPE LOAD CHECK',.73,.83,.015,True)
overlay('Verify sliding, lift and pipe joints',.73,.87,.013,color=MUTED)
footer('Baseline for testing in slight wind, not a wind rating. Read BUILD_GUIDE.md for load assumptions and ballast/friction checks.')

# Embed practical guide and scene index.
t=bpy.data.texts.new('START_HERE.txt'); t.write('FPV GATE / 2700\n\nScenes:\n01_ASSEMBLED: complete staked gate\n02_REAR_STRUCTURE: rear construction\n03_EXPLODED: separated assembly layers\n04_SHEET_LAYOUT: exact 8x4 ft stock nesting\n05_CLIP_DETAIL: printable saddle and load washer\n06_DIMENSIONS: orthographic front elevation\n07_HARD_SURFACE: long feet, integrated guys, four 15 kg bags\n\nModel uses meters; display is millimeters. Exported STL files use millimeters.\nRead BUILD_GUIDE.md for cut lengths, socket measurement, assembly, wind assumptions, cost and WIP review.\nPurchased fittings and zip tie paths are simplified. Printed STL parts are actual watertight solids, pending physical fit/load testing.\n')
guide=bpy.data.texts.new('BUILD_GUIDE.md'); guide.write((OUT/'BUILD_GUIDE.md').read_text())
# Verification of dimensional/nesting and printable topology.
import bmesh
checks={}
for o in [SADDLE,SADDLE34,WASH]:
 bm=bmesh.new(); bm.from_mesh(o.data); checks[o.name]={'nonmanifold_edges':sum(not e.is_manifold for e in bm.edges),'volume_mm3':round(abs(bm.calc_volume())*1e9,2),'bounds_mm':[round(d*1000,3) for d in o.dimensions]}; bm.free()
 assert checks[o.name]['nonmanifold_edges']==0, checks[o.name]
for r in layout:
 assert r['x']>=0 and r['y']>=0 and r['x']+r['w']<=1219.2 and r['y']+r['h']<=2438.4
for i,a in enumerate(layout):
 for b in layout[i+1:]:
  if a['sheet']==b['sheet']:
   assert not (a['x']<b['x']+b['w'] and a['x']+a['w']>b['x'] and a['y']<b['y']+b['h'] and a['y']+a['h']>b['y']), (a,b)
checks['hard_surface']={'extra_1in_stock_count':2,'extended_foot_qty':4,'cut_mm':1182.5375,'stock_use_two_cuts_with_kerf_mm':2*1182.5375+6,'ballast_kg':60,'feet_span_mm':2400}
checks['dimensions']={'outer_mm':[2700,2700],'clear_opening_mm':[1500,1500],'body_depth_mm':260,'face_area_m2':5.04,'saddle_count':len(positions),'sheet_nesting':'no overlaps; all pieces within 1219.2 x 2438.4 mm','pipe_stock_1in_mm':3048,'long_cut_mm':2065.075,'leg_cut_mm':290.075,'foot_cut_mm':582.5375,'stock_worst_used_with_3mm_kerf':2065.075+290.075+582.5375+9}
(OUT/'validation.json').write_text(json.dumps(checks,indent=2)); (OUT/'cut-layouts'/'nesting.json').write_text(json.dumps(layout,indent=2))
# Save with assembled scene and camera view, useful material shading in the viewport.
bpy.context.window.scene=ASSEMBLY
for screen in bpy.data.screens:
 for area in screen.areas:
  if area.type=='VIEW_3D':
   area.spaces.active.region_3d.view_perspective='CAMERA'; area.spaces.active.shading.type='MATERIAL'
bpy.ops.file.pack_all()
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'FPV_Gate_2700.blend'))
for name in ['01_ASSEMBLED','02_REAR_STRUCTURE','03_EXPLODED','04_SHEET_LAYOUT','05_CLIP_DETAIL','06_DIMENSIONS','07_HARD_SURFACE']:
 s=bpy.data.scenes[name]; bpy.context.window.scene=s; s.render.filepath=str(OUT/'renders'/f'{name}.png'); bpy.ops.render.render(write_still=True,scene=name)
print('BUILD COMPLETE',json.dumps(checks))

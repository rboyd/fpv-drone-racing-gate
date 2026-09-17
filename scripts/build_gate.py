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

def polygon_panel(name,points,y,thick,material):
 n=len(points); verts=[(x,yy,z) for yy in [y,y+thick] for x,z in points]
 faces=[tuple(range(n)),tuple(reversed(range(n,2*n)))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
 mesh=bpy.data.meshes.new(name); mesh.from_pydata(verts,[],faces); mesh.update()
 o=bpy.data.objects.new(name,mesh); (COL or SC.collection).objects.link(o); o.data.materials.append(material)
 import bmesh
 bm=bmesh.new(); bm.from_mesh(mesh); bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces)); bm.to_mesh(mesh); bm.free()
 return o

def rotate_face(points,k):
 result=[]
 for x,z in points:
  a,b=x,z-1.35
  for j in range(k): a,b=b,-a
  result.append((a,b+1.35))
 return result

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
 mesh=o.data.copy()
 if name.startswith('brace_joint'):
  for v in mesh.vertices: v.co=Vector((v.co.x,-v.co.z,v.co.y+.030))
 mesh.calc_loop_triangles()
 with open(OUT/'printable'/name,'wb') as f:
  f.write(b'FPV gate; coordinates in mm'.ljust(80,b' ')); f.write(struct.pack('<I',len(mesh.loop_triangles)))
  for t in mesh.loop_triangles:
   vs=[mesh.vertices[i].co*1000 for i in t.vertices]; normal=(vs[1]-vs[0]).cross(vs[2]-vs[0]).normalized()
   f.write(struct.pack('<12fH',*normal,*vs[0],*vs[1],*vs[2],0))
 bpy.data.meshes.remove(mesh)

def brace_joint(name,angle):
 o=cube(name,(0,0,.012),(.060,.060,.024),ORANGE)
 bpy.context.view_layer.objects.active=o; bpy.ops.object.transform_apply(location=True,rotation=False,scale=False)
 def subtract(c):
  bpy.context.view_layer.objects.active=o; m=o.modifiers.new('Pipe seat / slot','BOOLEAN'); m.operation='DIFFERENCE'; m.solver='EXACT'; m.object=c
  bpy.ops.object.modifier_apply(modifier=m.name); bpy.data.objects.remove(c,do_unlink=True)
 subtract(tube('cutter main',(0,-.06,-.0089005),(0,.06,-.0089005),.033801,ORANGE))
 u=Vector((-math.sin(angle),math.cos(angle),0)); v=Vector((math.cos(angle),math.sin(angle),0))
 c=Vector((0,0,.031535)); subtract(tube('cutter brace',c-u*.07,c+u*.07,.02707,ORANGE))
 for x in [-.025,.025]:
  for y in [-.021,.021]: boolean_slot(o,x,y)
 for a in [-.023,.023]:
  for b in [-.012,.012]:
   q=v*a+u*b; c=cube('brace tie slot',(q.x,q.y,.009),(.0032,.006,.06),ORANGE); c.rotation_euler.z=angle; subtract(c)
 # Enclosed transverse tunnels keep both tie return runs clear of both pipes.
 for y in [-.021,.021]: subtract(cube('main tie tunnel',(0,y,.013),(.064,.006,.0028),ORANGE))
 for along in [-.012,.012]:
  q=u*along;c=cube('brace tie tunnel',(q.x,q.y,.013),(.090,.006,.0028),ORANGE);c.rotation_euler.z=angle;subtract(c)
 import bmesh
 bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(o.data);bm.free()
 o['main_OD_mm']=33.401;o['brace_OD_mm']=26.67;o['angle_degrees']=round(math.degrees(angle));o['minimum_web_before_channels_mm']=10; o['tie_tunnel_mm']='6 wide x 2.8 high at z=13; permits two crossing tie straps'
 o['print_orientation']='Print on 60 x 24 edge with brim; support groove overhangs as needed. Physical fit test required.'
 return o

setup('05_CLIP_DETAIL',(.14,-.24,.19),(0,0,.06),.44,False); coll('01 / printable masters')
SADDLE=saddle('PRINT / saddle 1 inch / 60 x 40 x 18 mm',.033401); export_stl(SADDLE,'saddle_1in_OD33p40_mm.stl')
SADDLE34=saddle('PRINT / optional saddle 3-4 inch / 60 x 40 x 18 mm',.02667); export_stl(SADDLE34,'optional_saddle_3_4in_OD26p67_mm.stl'); SADDLE34.hide_render=True; SADDLE34.hide_set(True)
WASH=cube('PRINT / front load washer / 60 x 40 x 2.5 mm',(0,0,.00125),(.06,.04,.0025),BLUE)
# Bake washer location so both printable masters have origin at bed level.
bpy.context.view_layer.objects.active=WASH; bpy.ops.object.transform_apply(location=True,rotation=False,scale=False)
for x in [-.023,.023]:
 for y in [-.01,.01]: boolean_slot(WASH,x,y)
export_stl(WASH,'front_load_washer_mm.stl')
JPLUS=brace_joint('PRINT / brace joint +45',math.pi/4); export_stl(JPLUS,'brace_joint_plus45_mm.stl'); JPLUS.hide_render=True; JPLUS.hide_set(True)
JMINUS=brace_joint('PRINT / brace joint -45',-math.pi/4); export_stl(JMINUS,'brace_joint_minus45_mm.stl'); JMINUS.hide_render=True; JMINUS.hide_set(True)

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
footer('24 saddles + 24 washers per gate. STL units: mm. Print one fit sample first. Optional 3/4 in saddle is not in the BOM.')

# Gate parts grouped for assembly and exploded views.
setup('01_ASSEMBLED',(-3.6,-7,3.7),(.6,0,1.48),6.4)
coll('01 / four identical pentagons and four corner triangles'); FACE=[]
PENTA=[(-1.35,2.7),(1.05,2.7),(1.05,2.4),(.75,2.1),(-.75,2.1)]
TRI=[(1.05,2.7),(1.35,2.7),(1.05,2.4)]
for k in range(4):
 FACE.append(polygon_panel(f'F{k+1} / identical pentagon / 2400 x 600 blank',rotate_face(PENTA,k),0,.004,BLUE))
 FACE.append(polygon_panel(f'C{k+1} / corner triangle / 300 mm legs',rotate_face(TRI,k),0,.004,BLUE2))
coll('02 / scrap backers / no stacked intersections'); BACK=[]
# A 600 x 100 strip crosses the long diagonal seam; 140 x 100 plate crosses the short seam.
for k in range(4):
 center=Vector((1.05,2.4)); u=Vector((1,1)).normalized(); v=Vector((-1,1)).normalized()
 pts=[tuple(center+u*a+v*b) for a,b in [(-.3,-.05),(.3,-.05),(.3,.05),(-.3,.05)]]
 BACK.append(polygon_panel('B1 / diagonal scrap backer / 600 x 100',rotate_face(pts,k),.004,.004,PATCH))
 pts=[(.98,2.57),(1.12,2.57),(1.12,2.67),(.98,2.67)]
 BACK.append(polygon_panel('B2 / short-seam scrap backer / 140 x 100',rotate_face(pts,k),.004,.004,PATCH))
# No solid Coroplast tunnel walls: shared corner sheet stays available for other gates.
RET=[]
coll('04 / 1 inch PVC frame and feet'); FRAME=[]
P=.0319005; G=.0174625; H=.04048; OD=.033401
# Four long pipes use manufacturer fitting stop offsets, not socket depth subtraction.
def pipe(name,a,b,od=OD):
 o=tube(name,a,b,od,WHITE,.003378 if od==OD else .00287); o['cut_length_mm']=round((Vector(b)-Vector(a)).length*1000,3); FRAME.append(o); return o
for z in [.3,2.4]:
 pipe('P1 / rail / 2065.075 mm',(-1.05+G,P,z),(1.05-G,P,z))
for x in [-1.05,1.05]:
 pipe('P2 / upright / 2065.075 mm',(x,P,.3+G),(x,P,2.4-G))
 pipe('P3 / leg / 290.075 mm',(x,P,-.025+G),(x,P,.3-G))
 for sg in [-1,1]: pipe('P4 / foot / 582.538 mm',(x,P+sg*G,-.025),(x,P+sg*.6,-.025))
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
coll('05 / corner braces with printed end joints'); BRACE=[]; JOINTS=[]
Rvert=Matrix(((1,0,0),(0,0,1),(0,-1,0))).to_4x4()
Rhor=Matrix(((0,1,0),(0,0,1),(1,0,0))).to_4x4()
BRACEY=P+.0404355
for sx in [-1,1]:
 for top in [False,True]:
  z=2.4 if top else .3; dz=-1 if top else 1
  a=Vector((sx*1.05,BRACEY,z+dz*.4)); b=Vector((sx*.65,BRACEY,z)); v=(b-a).normalized()
  o=tube('P5 / brace / 646 mm',a-v*.040,b+v*.040,.02667,WHITE,.00287); BRACE.append(o)
  for pt,R in [(a,Rvert),(b,Rhor)]:
   direction=R.to_3x3().inverted()@v; angle=math.atan2(-direction.x,direction.y)
   while angle>math.pi/2: angle-=math.pi
   while angle<-math.pi/2: angle+=math.pi
   src=JPLUS if angle>0 else JMINUS
   M=Matrix.Translation((pt.x,P+.0089005,pt.z))@R
   o=copy_obj(src,'J / printed brace end '+('plus45' if angle>0 else 'minus45'),(0,0,0));o.matrix_world=M;JOINTS.append(o)
   # Two loops around main pipe through main-side slots.
   for yy in [-.021,.021]:
    ps=[(-.025,yy,.013),(.025,yy,.013),(.025,yy,-.0089005)]
    ps +=[(.025*math.cos(t),yy,-.0089005-.020*math.sin(t)) for t in [j*math.pi/16 for j in range(17)]]
    ps +=[(-.025,yy,.013)]; line('J / main pipe retention tie',[M@Vector(q) for q in ps],.0012,DARK)
   u=Vector((-math.sin(angle),math.cos(angle),0)); vv=Vector((math.cos(angle),math.sin(angle),0))
   for aa in [-.012,.012]:
    ps=[vv*(-.023)+u*aa+Vector((0,0,.013)), vv*.023+u*aa+Vector((0,0,.013))]
    ps +=[vv*(.023*math.cos(t))+u*aa+Vector((0,0,.031535+.016*math.sin(t))) for t in [j*math.pi/16 for j in range(17)]]
    ps +=[vv*(-.023)+u*aa+Vector((0,0,.013))]; line('J / brace retention tie',[M@q for q in ps],.0012,DARK)
coll('06 / printed attachments and zip ties'); ATT=[]
Rvert=Matrix(((1,0,0),(0,0,1),(0,-1,0))).to_4x4()
Rhor=Matrix(((0,1,0),(0,0,1),(1,0,0))).to_4x4()
positions=[(x,z,False) for z in [.3,2.4] for x in [-.84,-.5,-.16,.16,.5,.84]]+[(x,z,True) for x in [-1.05,1.05] for z in [.45,.85,1.15,1.55,1.85,2.25]]
for i,(x,z,vert) in enumerate(positions):
 R=Rvert if vert else Rhor
 # Local z points toward the rear of the gate, local y follows the pipe.
 M=Matrix.Translation((x,.008,z))@R
 o=copy_obj(SADDLE,f'A{i+1:02} / 1 inch saddle',(0,0,0)); o.matrix_world=M; ATT.append(o)
 w=copy_obj(WASH,f'A{i+1:02} / front washer',(0,0,0)); w.matrix_world=Matrix.Translation((x,-.0025,z))@R; ATT.append(w)
 if True:
  pad=cube(f'A{i+1:02} / scrap pad',(x,.006,z),(.07 if vert else .05,.004,.05 if vert else .07),PATCH); ATT.append(pad)
 for yy in [-.01,.01]:
  pts=[(-.023,yy,-.0105),(.023,yy,-.0105),(.023,yy,.024)]
  pts +=[(.023*math.cos(a),yy,.024+.020*math.sin(a)) for a in [j*math.pi/16 for j in range(17)]]
  pts +=[(-.023,yy,-.0105)]
  line('4.8 mm UV zip tie / attachment',[M@Vector(p) for p in pts],.0013,DARK)
# Mechanically stitch diagonal and short seams at every corner, with scrap spreaders.
for k in range(4):
 for t in [-.23,0,.23]:
  cen=Vector((1.05,2.4))+Vector((1,1)).normalized()*t
  v=Vector((-1,1)).normalized()*.035
  endpoints=rotate_face([tuple(cen-v),tuple(cen+v)],k)
  (xa,za),(xb,zb)=endpoints
  line('Corner diagonal / tie bridge',[(xa,-.001,za),(xb,-.001,zb),(xb,.009,zb),(xa,.009,za)],.0012,DARK,True)
 for dz in [-.025,.025]:
  (xa,za),(xb,zb)=rotate_face([(1.00,2.62+dz),(1.10,2.62+dz)],k)
  line('Corner short seam / tie bridge',[(xa,-.001,za),(xb,-.001,zb),(xb,.009,zb),(xa,.009,za)],.0012,DARK,True)
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
header('01','FPV / 2700','Four identical pentagons. Four small corners. One braced PVC backing frame.')
overlay('2700 x 2700',.735,.31,.025,True); overlay('Face / 600 mm border',.735,.355,.015,color=MUTED)
overlay('1500 x 1500',.735,.45,.025,True); overlay('Clear opening / shallow backing',.735,.495,.015,color=MUTED)
overlay('2 sheets per face',.735,.59,.023,True); overlay('Shared corner sheet: 16 gates\nOne frame + four corner braces',.735,.635,.015,color=MUTED)
overlay('Stake in both directions',.735,.76,.017,True); overlay('Feet and anchors extend\nbeyond the shallow gate body.',.735,.80,.014,color=MUTED)
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
header('02','The structure behind it','One 1 in backing frame, four 3/4 in braces and eight printed brace-end joints.')
overlay('01 / MAIN FRAME',.725,.31,.017,True); overlay('1 in Schedule 40 PVC\n2100 x 2100 mm centerlines',.725,.35,.014,color=MUTED)
overlay('02 / CORNER BRACES',.725,.47,.017,True); overlay('3/4 in PVC / 4 x 646 mm\nPrinted 45-degree joints',.725,.51,.014,color=MUTED)
overlay('03 / PRINTED JOINTS',.725,.63,.017,True); overlay('Eight positive-angle connectors\nTwo tie pairs per connector',.725,.67,.014,color=MUTED)
overlay('04 / BASE',.725,.79,.017,True); overlay('1200 mm fore-aft pipe feet\nFour anchors resist reversal',.725,.83,.014,color=MUTED)
footer('Purchased elbows and tees are simplified envelopes. Pin/screw removable sockets. Tape alone is not a structural attachment.')
setup('03_EXPLODED',(5,-7,4.8),(.5,.1,1.55),7.6)
for c in ASSEMBLY.collection.children:
 key=c.name[:2]
 if key in ['01','02','03','04','05','06']:
  delta={'01':(-.65,-.9,0),'02':(-.25,-.45,0),'03':(.85,1.1,0),'04':(.3,.25,0),'05':(.3,.25,0),'06':(0,-.15,0)}[key]
  dup_collection(c,delta)
header('03','Assembly / layer by layer','Pentagons + corners -> scrap backers -> saddles -> one backing frame with corner braces')
overlay('1  CUT + SPLICE',.75,.30,.017,True); overlay('Four identical 2400 x 600 blanks\nFour 300 mm corner triangles',.75,.34,.014,color=MUTED)
overlay('2  BUILD THE FRAME',.75,.47,.017,True); overlay('Standard tees and elbows\nAdd braces and broad feet',.75,.51,.014,color=MUTED)
overlay('3  TIE ON THE FACE',.75,.64,.017,True); overlay('24 saddles / two ties each\nUse washers + scrap pads',.75,.68,.014,color=MUTED)
overlay('4  STAND + ANCHOR',.75,.81,.017,True); overlay('Fit the selected feet and guy lines',.75,.85,.014,color=MUTED)
footer('Exploded spacing is for instruction only. Body is about 94 mm thick; feet and guys extend beyond it.')
# Sheet layouts use exact local cut polygons; third stock yields 64 triangles / 16 gates.
setup('04_SHEET_LAYOUT',(0,-8,2.35),(0,0,2.35),7.9,False)
coll('01 / polygon sheet nesting'); layout=[]
LOCAL_PENTA=[(0,600),(2400,600),(2400,300),(2100,0),(600,0)]
for sh in [1,2,3]:
 ox=(sh-2)*2.55; oz=.52
 cube('Stock / 2438.4 x 1219.2',(ox,.008,oz+2.4384/2),(1.2192,.006,2.4384),GREEN)
 text('Sheet label',f'SHEET {sh:02}',(ox-.61,-.012,3.13),.1,INK,bold=True)
 text('Stock size','1219.2 x 2438.4 mm',(ox-.61,-.012,3),.055,MUTED)
 if sh<3:
  for row in range(2):
   poly=[(x,y+600*row) for x,y in LOCAL_PENTA]
   pts=[(ox-.6096+y/1000,oz+x/1000) for x,y in poly]
   polygon_panel('F / pentagon / identical',pts,-.004,.004,BLUE)
   layout.append({'sheet':sh,'type':'pentagon','polygon_mm':poly})
   text('Part label','2400\nx 600',(ox-.3096+.6*row,-.009,1.65),.10,LIGHTTEXT,align='CENTER',bold=True)
  text('Scrap label','OFFCUTS -> BACKERS',(ox-.60,-.02,.61),.045,INK)
 else:
  for i in range(8):
   for j in range(4):
    for half in range(2):
     x=i*300;y=j*300
     poly=[(x,y),(x+300,y),(x,y+300)] if half==0 else [(x+300,y),(x+300,y+300),(x,y+300)]
     pts=[(ox-.6096+v/1000,oz+u/1000) for u,v in poly]
     polygon_panel('C / shared corner / 300 legs',pts,-.004,.004,BLUE2 if half else BLUE)
     layout.append({'sheet':sh,'type':'corner','polygon_mm':poly})
     line('Triangle cut line',[(pts[0][0],-.009,pts[0][1]),(pts[-1][0],-.009,pts[-1][1])],.001,RETURN)
header('04','Two identical cuts per sheet','Sheets 1 and 2 make four identical pentagons. Share sheet 3 across the fleet.')
overlay('4 MAIN PANELS / GATE',.062,.865,.018,True);overlay('2400 x 600 mm bounding blanks',.062,.905,.013,color=MUTED)
overlay('BACKERS FROM OFFCUTS',.389,.865,.018,True);overlay('4 diagonal strips + 4 short tabs',.389,.905,.013,color=MUTED)
overlay('64 CORNERS / SHEET',.711,.865,.018,True);overlay('300 mm right triangles = 16 gates',.711,.905,.013,color=MUTED)
footer('Knife cuts / no saw kerf. Face sheets: 2 per gate. Shared corner allocation: 1/16 sheet per gate. See SVG for backer nesting.')
# Front dimensional elevation, useful separately from hero.
setup('06_DIMENSIONS',(0,-8,1.60),(0,0,1.60),6.2,False)
for c in ASSEMBLY.collection.children:
 if c.name[:2] in ['01','03','80']: dup_collection(c)
header('06','Dimensions / front elevation','All dimensions in millimetres. Clear opening: 1500 x 1500. Shallow single-frame construction.')
coll('02 / supplementary dimensions')
dim((-.75,-.07,.46),(.75,-.07,.46),'1500',(0,0,.06),.06)
dim((1.50,-.07,.6),(1.50,-.07,2.1),'1500',(.15,0,0),.06)
text('Border dimension','600',(1.06,-.07,1.35),.07,LIGHTTEXT,align='CENTER')
footer('Face: x = -1350..1350, z = 0..2700. Opening: x = -750..750, z = 600..2100. Body thickness: about 94 mm including ties; excludes feet and guys.')
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

setup('08_BRACE_JOINT',(.17,-.28,.21),(.005,0,.038),.40,False)
coll('01 / actual printed joint demonstration')
jo=copy_obj(JPLUS,'J / +45 prototype joint',(-.060,0,.018),(0,0,0))
tube('Main 1 in pipe',(-.060,-.06,.018-.0089005),(-.060,.06,.018-.0089005),.033401,WHITE,.003378)
u=Vector((-math.sqrt(.5),math.sqrt(.5),0));c=Vector((-.060,0,.018+.031535))
tube('Brace 3-4 in pipe',c-u*.06,c+u*.06,.02667,WHITE,.00287)
cut=copy_obj(JPLUS,'J / cutaway showing tie tunnels',(.035,-.05,.015),(0,0,0)); cut.data=cut.data.copy()
cutter=cube('Cutaway removal',(.065,-.05,.027),(.060,.090,.090),ORANGE)
bpy.context.view_layer.objects.active=cut;mod=cut.modifiers.new('Section for instruction only','BOOLEAN');mod.operation='DIFFERENCE';mod.object=cutter;bpy.ops.object.modifier_apply(modifier=mod.name);bpy.data.objects.remove(cutter,do_unlink=True)
copy_obj(JMINUS,'J / isolated minus45',(.035,.03,.015),(0,0,0))
# Retaining ties on the detail assembly, including the internal return runs.
M=Matrix.Translation((-.060,0,.018))
for yy in [-.021,.021]:
 ps=[(-.025,yy,.013),(.025,yy,.013),(.025,yy,-.0089005)]
 ps +=[(.025*math.cos(t),yy,-.0089005-.020*math.sin(t)) for t in [j*math.pi/16 for j in range(17)]]
 ps +=[(-.025,yy,.013)];line('Detail / main-pipe tie',[M@Vector(q) for q in ps],.0012,DARK)
u=Vector((-math.sqrt(.5),math.sqrt(.5),0));vv=Vector((math.sqrt(.5),math.sqrt(.5),0))
for aa in [-.012,.012]:
 ps=[vv*(-.023)+u*aa+Vector((0,0,.013)),vv*.023+u*aa+Vector((0,0,.013))]
 ps +=[vv*(.023*math.cos(t))+u*aa+Vector((0,0,.031535+.016*math.sin(t))) for t in [j*math.pi/16 for j in range(17)]]
 ps +=[vv*(-.023)+u*aa+Vector((0,0,.013))];line('Detail / brace-pipe tie',[M@q for q in ps],.0012,DARK)
header('08','A positive seat at both ends','Two modeled pipe cradles fix the crossing angle; four ties retain each printed joint.')
overlay('1 in main / OD 33.40',.735,.28,.015,True)
overlay('3/4 in brace / OD 26.67',.735,.33,.015,True)
overlay('8 JOINTS / GATE',.735,.40,.018,True)
overlay('4 x +45 and 4 x -45\n60 x 60 x 24 mm body\nInternal tie-return tunnels',.735,.45,.014,color=MUTED)
overlay('TIE RETENTION',.735,.71,.017,True)
overlay('Two ties around each pipe\nPrint a fit sample first',.735,.76,.014,color=MUTED)
footer('Grooves on opposite faces. Print on an edge with a brim; support overhangs as needed. STLs are in mm, closed and manifold.')
setup('09_FACE_PARTS',(0,-8,1.55),(0,0,1.55),7.2,False)
coll('01 / face explosion')
for k in range(4):
 off=rotate_face([(0,1.65)],k)[0]; offset=Vector((off[0],off[1]-1.35))
 pts=[tuple(Vector(q)+offset) for q in rotate_face(PENTA,k)]
 polygon_panel('Pentagon / identical',pts,0,.004,BLUE)
 p2=rotate_face(TRI,k); c=Vector((sum(q[0] for q in p2)/3,sum(q[1] for q in p2)/3));delta=(c-Vector((0,1.35))).normalized()*.43
 polygon_panel('Corner infill', [tuple(Vector(q)+delta) for q in p2],0,.004,BLUE2)
header('09','Four pentagons. Four corners.','Identical border pieces rotate through 90 degrees. All long midspans stay continuous.')
footer('Assembled face: 2700 x 2700 mm / opening: 1500 x 1500 mm. Each corner infill is a right triangle with 300 mm legs.')
# Embed practical guide and scene index.
t=bpy.data.texts.new('START_HERE.txt'); t.write('FPV GATE / 2700\n\nScenes:\n01_ASSEMBLED: complete staked gate\n02_REAR_STRUCTURE: rear construction\n03_EXPLODED: separated assembly layers\n04_SHEET_LAYOUT: exact 8x4 ft stock nesting\n05_CLIP_DETAIL: printable saddle and load washer\n06_DIMENSIONS: orthographic front elevation\n07_HARD_SURFACE: long feet, integrated guys, four 15 kg bags\n08_BRACE_JOINT: handed printed joints, tie routes and cutaway\n09_FACE_PARTS: four pentagons and corner triangles\n\nModel uses meters; display is millimeters. Exported STL files use millimeters.\nRead BUILD_GUIDE.md for cut lengths, socket measurement, assembly, wind assumptions, cost and WIP review.\nPurchased fittings and zip tie paths are simplified. Printed STL parts are actual watertight solids, pending physical fit/load testing.\n')
guide=bpy.data.texts.new('BUILD_GUIDE.md'); guide.write((OUT/'BUILD_GUIDE.md').read_text())
# Verification of dimensional/nesting and printable topology.
import bmesh
checks={}
for o in [SADDLE,SADDLE34,WASH,JPLUS,JMINUS]:
 bm=bmesh.new(); bm.from_mesh(o.data); checks[o.name]={'nonmanifold_edges':sum(not e.is_manifold for e in bm.edges),'volume_mm3':round(abs(bm.calc_volume())*1e9,2),'bounds_mm':[round(d*1000,3) for d in o.dimensions]}; bm.free()
 assert checks[o.name]['nonmanifold_edges']==0, checks[o.name]
def area2(poly):
 return abs(sum(poly[i][0]*poly[(i+1)%len(poly)][1]-poly[(i+1)%len(poly)][0]*poly[i][1] for i in range(len(poly))))/2
for r in layout:
 assert all(0<=x<=2438.4 and 0<=y<=1219.2 for x,y in r['polygon_mm'])
assert len([r for r in layout if r['type']=='corner'])==64
assert abs(area2(LOCAL_PENTA)*4+45000*4-5040000)<.001
assert len(JOINTS)==8
checks['face']={'pentagon_area_mm2':area2(LOCAL_PENTA),'corner_area_mm2':45000,'total_face_area_mm2':5040000,'shared_corners_per_sheet':64,'gates_per_corner_sheet':16,'panels_per_main_sheet':2}
checks['hard_surface']={'extra_1in_stock_count':2,'extended_foot_qty':4,'cut_mm':1182.5375,'stock_use_two_cuts_with_kerf_mm':2*1182.5375+6,'ballast_kg':60,'feet_span_mm':2400}
# Verify removal, continuity of four main members, and actual evaluated body bounds.
bpy.context.window.scene=ASSEMBLY; bpy.context.view_layer.update()
assert not any(o.name.startswith(('P6 /','P7 /','T3 /','T4 /','E2 /')) for o in ASSEMBLY.objects)
assert len([o for o in ASSEMBLY.objects if o.name.startswith(('P1 /','P2 /'))])==4
assert len(JOINTS)==8 and len(BRACE)==4
ys=[]; depsgraph=bpy.context.evaluated_depsgraph_get()
for c in ASSEMBLY.collection.children:
 if c.name[:2] in ['01','02','04','05','06']:
  for o in c.objects:
   if o.type in ['MESH','CURVE'] and not o.name.startswith(('P4 /','T2 /','C1 /')):
    ev=o.evaluated_get(depsgraph)
    if o.type=='CURVE':
     # Curve bounding boxes can be unavailable; measure evaluated geometry.
     mesh=ev.to_mesh()
     oy=[(ev.matrix_world@v.co).y for v in mesh.vertices]
     ev.to_mesh_clear()
    else:
     oy=[(ev.matrix_world@Vector(co)).y for co in ev.bound_box]
    ys.extend(oy)
body_depth_mm=(max(ys)-min(ys))*1000
assert 90<body_depth_mm<100,body_depth_mm
checks['single_frame']={'rear_square_absent':True,'depth_links_absent':True,'midpoint_tees_absent':True,'continuous_main_members':4,'body_y_bounds_mm':[round(min(ys)*1000,3),round(max(ys)*1000,3)],'pipe_stock_1in':4,'pipe_stock_3_4in':1,'brace_stock_used_with_kerf_mm':4*646+12}
checks['dimensions']={'outer_mm':[2700,2700],'clear_opening_mm':[1500,1500],'body_depth_mm':round(body_depth_mm,3),'face_area_m2':5.04,'saddle_count':len(positions),'sheet_nesting':'main panels and shared triangles within stock; polygon union verified separately','pipe_stock_1in_mm':3048,'main_rail_cut_mm':2065.075,'square_frame_count':1,'brace_count':4,'brace_joint_count':len(JOINTS),'leg_cut_mm':290.075,'foot_cut_mm':582.5375,'stock_worst_used_with_3mm_kerf':2065.075+290.075+582.5375+9}
(OUT/'validation.json').write_text(json.dumps(checks,indent=2)); (OUT/'cut-layouts'/'nesting.json').write_text(json.dumps(layout,indent=2))
# Save with assembled scene and camera view, useful material shading in the viewport.
bpy.context.window.scene=ASSEMBLY
for screen in bpy.data.screens:
 for area in screen.areas:
  if area.type=='VIEW_3D':
   area.spaces.active.region_3d.view_perspective='CAMERA'; area.spaces.active.shading.type='MATERIAL'
bpy.ops.file.pack_all()
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'FPV_Gate_2700.blend'))
render_names=os.environ.get('RENDER_SCENES','01_ASSEMBLED,02_REAR_STRUCTURE,03_EXPLODED,04_SHEET_LAYOUT,05_CLIP_DETAIL,06_DIMENSIONS,07_HARD_SURFACE,08_BRACE_JOINT,09_FACE_PARTS').split(',')
for name in render_names:
 s=bpy.data.scenes[name]; bpy.context.window.scene=s; s.render.filepath=str(OUT/'renders'/f'{name}.png'); bpy.ops.render.render(write_still=True,scene=name)
print('BUILD COMPLETE',json.dumps(checks))

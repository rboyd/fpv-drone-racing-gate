"""Four uniform-insert, folding gate concepts in native Blender. Not production certified."""
from pathlib import Path
# Reuse only scene/primitive helpers; do not execute the existing gate generator.
base=Path(__file__).with_name('build_gate.py').read_text().split('# Print master:')[0]
exec(base,globals())
import sys,struct,bmesh
sys.path.insert(0,str(ROOT/'scripts'))
from posterboard_options import OPTIONS
OUT=ROOT/'output/posterboard_concepts'
for d in ['renders','prototype_coupons']:(OUT/d).mkdir(parents=True,exist_ok=True)
PAPER=mat('Cardstock / ivory',(.82,.87,.90)); PAPERS=[PAPER,mat('Cardstock / pale blue',(.44,.66,.9)),mat('Cardstock / mint',(.40,.72,.65)),mat('Cardstock / warm cream',(.86,.68,.39))]
STEELBLUE=mat('Permanent assembly / dark blue',(.045,.15,.28))
PROFILE=[(0,0),(6,0),(6,1.2),(1.2,1.2),(1.2,2),(6,2),(6,3.2),(1.2,3.2),(1.2,10),(0,10)]
MASTERS=[]; PRINT_CHECKS={}

def clean_mesh(o):
 bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-7);bmesh.ops.dissolve_degenerate(bm,edges=list(bm.edges),dist=1e-8);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(o.data);bm.free()

def prism_xy(name,pts,height,material=ORANGE):
 n=len(pts);vs=[(x/1000,y/1000,z/1000) for z in [0,height] for x,y in pts]
 fs=[tuple(reversed(range(n))),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
 me=bpy.data.meshes.new(name);me.from_pydata(vs,[],fs);me.update();o=bpy.data.objects.new(name,me);COL.objects.link(o);o.data.materials.append(material);clean_mesh(o);return o

def profile_x(name,profile,length,material=ORANGE):
 n=len(profile);vs=[(x/1000,y/1000,z/1000) for x in [0,length] for y,z in profile]
 fs=[tuple(reversed(range(n))),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
 me=bpy.data.meshes.new(name);me.from_pydata(vs,[],fs);me.update();o=bpy.data.objects.new(name,me);COL.objects.link(o);o.data.materials.append(material);clean_mesh(o);return o

def boolean(o,c,op='DIFFERENCE'):
 for target in [o,c]:
  bm=bmesh.new();bm.from_mesh(target.data);bmesh.ops.triangulate(bm,faces=list(bm.faces));bm.to_mesh(target.data);bm.free()
 bpy.context.view_layer.objects.active=o;m=o.modifiers.new('Prototype geometry','BOOLEAN');m.operation=op;m.solver='EXACT';m.object=c
 bpy.ops.object.modifier_apply(modifier=m.name);bpy.data.objects.remove(c,do_unlink=True)

def bake(o):
 bpy.context.view_layer.objects.active=o
 for x in bpy.context.selected_objects:x.select_set(False)
 o.select_set(True);bpy.ops.object.transform_apply(location=True,rotation=True,scale=True)

def mmcube(name,xyz,whd,material=ORANGE):return cube(name,tuple(x/1000 for x in xyz),tuple(x/1000 for x in whd),material)

def instance(src,name,matrix):
 o=bpy.data.objects.new(name,src.data);COL.objects.link(o);o.matrix_world=matrix;return o

def save_coupon(o,name,orientation,overhang='None: constant extrusion / open features'):
 clean_mesh(o);bm=bmesh.new();bm.from_mesh(o.data)
 bad=sum(not e.is_manifold for e in bm.edges);volume=abs(bm.calc_volume())*1e9;bm.free()
 assert bad==0,(name,bad)
 vs=[v.co*1000 for v in o.data.vertices];mins=[min(v[i] for v in vs) for i in range(3)];maxs=[max(v[i] for v in vs) for i in range(3)]
 bounds=[maxs[i]-mins[i] for i in range(3)]
 assert all(d<=170 for d in bounds),(name,bounds)
 me=o.data.copy()
 for v in me.vertices:v.co-=Vector(mins)/1000
 me.calc_loop_triangles()
 with (OUT/'prototype_coupons'/name).open('wb') as f:
  f.write(b'FPV concept prototype; mm; fit test first'.ljust(80,b' '));f.write(struct.pack('<I',len(me.loop_triangles)))
  for t in me.loop_triangles:
   a,b,c=[me.vertices[i].co*1000 for i in t.vertices];normal=(b-a).cross(c-a).normalized();f.write(struct.pack('<12fH',*normal,*a,*b,*c,0))
 bpy.data.meshes.remove(me)
 PRINT_CHECKS[name]={'bounds_mm':[round(d,3) for d in bounds],'solid_volume_mm3':round(volume,2),'nonmanifold_edges':bad,'orientation':orientation,'overhang_design':overhang,'status':'Prototype coupon; not physically fit/cycle tested'}
 MASTERS.append(o)

setup('10_PRINT_ORIENTATIONS',(.075,-.50,1.3),(.075,.07,0),1.12,False);coll('01 / actual coupon solids')
RAIL=profile_x('U channel / natural assembly coordinates',PROFILE,150)
# A separate mesh in actual print orientation, bed on the full 150 x 10 mm spine.
RPRINT=RAIL.copy();RPRINT.data=RAIL.data.copy();COL.objects.link(RPRINT)
for v in RPRINT.data.vertices:v.co=Vector((v.co.x,.010-v.co.z,v.co.y))
save_coupon(RPRINT,'channel_150_on_spine_mm.stl','150 x 10 mm spine on bed; slot faces UP')
RAIL.hide_render=True;RAIL.hide_set(True)
# Open-ended female track: 45-degree inward walls require no support.
TRACK=mmcube('Female dovetail / 50 mm',(25,0,2.1),(50,20,4.2),STEELBLUE);bake(TRACK)
boolean(TRACK,mmcube('Latch foot',(37.5,-11.7,.7),(15,7.4,1.4),STEELBLUE),'UNION')
boolean(TRACK,mmcube('Latch rail',(37.5,-14.35,3.5),(15,2.1,7),STEELBLUE),'UNION')
cavity=profile_x('Dovetail open cutter',[(-6,1.2),(6,1.2),(3,4.2),(3,9),(-3,9),(-3,4.2)],49)
cavity.location.x=-.001;boolean(TRACK,cavity)
boolean(TRACK,mmcube('Open catch notch',(37,-14.4,5),(8,3.2,6)))
save_coupon(TRACK,'dovetail_receiver_50_mm.stl','Flat base on bed; groove and release notch face UP','45-degree inward groove walls; notch is open on top')
# Male shoe prints upside-down: its wide retaining foot grows at 45 degrees.
SHOE=mmcube('Male shoe / replaceable in-plane spring',(22.5,-1.75,1.2),(45,24.5,2.4));bake(SHOE)
boolean(SHOE,mmcube('Spring root',(4,12,1.2),(8,3,2.4)),'UNION')
boolean(SHOE,mmcube('Spring beam',(23,13,1.2),(30,1.2,2.4)),'UNION')
hook=prism_xy('Ramped latch hook',[(32,13.6),(32,15.2),(35,15.2),(38,13.6)],2.4);boolean(SHOE,hook,'UNION')
neck=profile_x('Runner neck',[(-2.7,2.4),(2.7,2.4),(2.7,2.6),(-2.7,2.6)],42);neck.location.x=.0015;boolean(SHOE,neck,'UNION')
runner=profile_x('45 degree runner',[(-2.7,2.6),(2.7,2.6),(5.7,5.6),(-5.7,5.6)],42);runner.location.x=.0015;boolean(SHOE,runner,'UNION')
save_coupon(SHOE,'dovetail_shoe_release_spring_mm.stl','Broad plate on bed; trapezoid foot points UP; spring flexes in XY','45-degree widening runner; cantilever lies flat')
# Separate planar knuckles: no horizontal barrel roofs or floating hinge loops.
pts=[(6*math.cos(t),6*math.sin(t)) for t in [2*math.pi*i/64 for i in range(64)]]
HINGE=prism_xy('Hinge knuckle / two identical tags per hinge',pts,6,STEELBLUE)
boolean(HINGE,mmcube('Hinge tag',(15,0,3),(22,10,6),STEELBLUE),'UNION')
boolean(HINGE,tube('Vertical eye cutter',(0,0,-.001),(0,0,.008),.0055,ORANGE))
save_coupon(HINGE,'hinge_knuckle_flat_mm.stl','Eye axis vertical on bed; two separate knuckles stack along the pin')
PIN=prism_xy('Removable flat split pin',[(-4,0),(4,0),(4,2),(2,2),(2,15),(2.8,15),(2.8,16),(2,17),(2,19),(-2,19),(-2,17),(-2.8,16),(-2.8,15),(-2,15),(-2,2),(-4,2)],3)
boolean(PIN,mmcube('Fork split',(0,12,1.5),(1.2,16,5)))
save_coupon(PIN,'hinge_split_pin_flat_mm.stl','Flat fork on bed; flex legs in XY; pinch tips to remove')
# A pipe clip printed along its pipe axis, with completely vertical hole walls.
r=16.95;ro=20.15;angles=[math.radians(75+210*i/64) for i in range(65)]
outline=[(ro*math.cos(t),ro*math.sin(t)) for t in angles]+[(r*math.cos(t),r*math.sin(t)) for t in reversed(angles)]
PVC=prism_xy('PVC click saddle / OD 33.4 target',outline,8)
boolean(PVC,mmcube('Dock mounting lug',(-25,0,4),(14,14,8)),'UNION')
for yy in [-4,4]:boolean(PVC,mmcube('Backup keeper passage',(-25,yy,4),(4,2,12)))
save_coupon(PVC,'PVC_C_saddle_OD33p4_mm.stl','Pipe axis vertical; ring profile flat on bed','None; open C profile. Positive keeper still to be detailed.')
# Plain support rib coupon, also prints flat.
RIB=mmcube('Rear support rib coupon',(75,2.5,1),(150,5,2));bake(RIB)
save_coupon(RIB,'support_rib_150_mm.stl','150 x 5 mm side on bed')
# Arrange actual coupon solids on separate miniature A1 Mini bed tiles.
for i,o in enumerate(MASTERS):
 col=i%4;row=i//4
 center=Vector((-.225+col*.20,-.05+row*.20,0))
 mins=Vector(tuple(min(v.co[j] for v in o.data.vertices) for j in range(3)));maxs=Vector(tuple(max(v.co[j] for v in o.data.vertices) for j in range(3)))
 o.location=center-Vector(((mins.x+maxs.x)/2,(mins.y+maxs.y)/2,mins.z))
 cube('180 mm print bed / orientation reference',(center.x,center.y,-.004),(.18,.18,.005),GROUND)
 label=text('Coupon bed label',['CHANNEL','RECEIVER','RELEASE SHOE','HINGE EYE','SPLIT PIN','PVC SADDLE','REAR RIB'][i],(center.x-.075,center.y-.075,.001),.009,INK)
 label.rotation_euler=(0,0,0)
header('10','Support-free print orientations','Seven fit coupons. Largest footprint 150 x 10 mm. No support structures modeled or required by the intended geometry.')
footer('Design coupons only: slice and test slot clearance, snap force, fatigue and PVC retention before producing gate quantities.')

# Mesh cache: every rail segment remains an individual selectable native object.
RAIL_CACHE={}
def rail_mesh(length):
 key=round(length,5)
 if key not in RAIL_CACHE:
  o=profile_x('Rail mesh source',PROFILE,length);RAIL_CACHE[key]=o.data;bpy.data.objects.remove(o,do_unlink=True)
 return RAIL_CACHE[key]

def rail(a,b,inward,name='Slide-in U channel'):
 a,b=Vector(a),Vector(b);d=(b-a).normalized();length=(b-a).length*1000;n=math.ceil(length/150)
 for i in range(n):
  p=a+(b-a)*i/n;seg=length/n-.20
  # Natural local X along rail; Y points into paper bay; Z points behind face.
  m=Matrix(((d.x,inward[0],0,p.x),(0,0,1,p.y),(d.z,inward[1],0,p.z),(0,0,0,1)))
  o=bpy.data.objects.new(name,rail_mesh(seg));COL.objects.link(o);o.matrix_world=m
  o['print']='On spine; slot up';o['segment_mm']=round(seg,3)

def leaf_geometry(o,start_col,end_col,color=PAPER,offset=(0,0,0),rib=True):
 px,py=[v/1000 for v in o['pitch']];a,b=[v/1000 for v in o['card']];nx,ny=o['grid'];L,W=[v/1000 for v in o['cassette']]
 ox,oy,oz=offset
 before=set(COL.objects)
 for i in range(start_col,end_col):
  for j in range(ny):
   u=i*px+ox;v=j*py+oz
   cube(f"{o['id']} / cardstock / {o['card'][0]} x {o['card'][1]}",(u+.002+a/2,oy+.0014,v+.002+b/2),(a,.0004,b),color)
   rail((u,oy,v),(u+px,oy,v),(0,1))
   rail((u+px,oy,v+py),(u,oy,v+py),(0,-1))
   rail((u,oy,v+py),(u,oy,v),(1,0))
   rail((u+px,oy,v),(u+px,oy,v+py),(-1,0))
   # Orange splice nodes identify permanent workshop joints; details are in scene 07.
   for du,dv in [(0,0),(px,0),(0,py),(px,py)]:cube('Workshop node / stays assembled',(u+du,oy+.010,v+dv),(.010,.004,.010),STEELBLUE)
   if o['rib'] and rib:
    cube('Rear rib / 10 mm2 section',(u+px/2,oy+.004,v+py/2),(px,.005,.002),ORANGE)
    if o['id']=='C':cube('Rear cross rib / 10 mm2',(u+px/2,oy+.004,v+py/2),(.002,.005,py),ORANGE)
    for f in [.25,.75]:cube('Light paper keeper / rounded concept',(u+px*f,oy+.0006,v+py/2),(.016,.0012,.006),ORANGE)
 # Low receivers stay on each leaf and follow its fold transform.
 for frac in [.16,.39,.61,.84]:
  u=L*frac
  if start_col*px<=u<end_col*px:
   cube('PVC docking receiver / release from rear',(u+ox,oy+.013,W/2+oz),(.055,.006,.032),STEELBLUE,.001)
 return [x for x in COL.objects if x not in before]

def move_objects(objs,M):
 for x in objs:x.matrix_world=M@x.matrix_world

def cassette(o,color=PAPER,transport=False):
 ends=[0]+o['fold_columns']+[o['grid'][0]];L,W=[v/1000 for v in o['cassette']];allparts=[]
 for idx,(a,b) in enumerate(zip(ends,ends[1:])):
  parts=leaf_geometry(o,a,b,color)
  if transport:
   if len(ends)==3 and idx==1:
    # Front-to-front book fold, pin axis outside front of paper.
    x=ends[1]*o['pitch'][0]/1000;M=Matrix.Translation((x,-.004,0))@Matrix.Rotation(math.pi,4,'Z')@Matrix.Translation((-x,.004,0));move_objects(parts,M)
   elif len(ends)==4 and idx==0:
    x=ends[1]*o['pitch'][0]/1000;M=Matrix.Translation((x,-.004,0))@Matrix.Rotation(math.pi,4,'Z')@Matrix.Translation((-x,.004,0));move_objects(parts,M)
   elif len(ends)==4 and idx==2:
    x=ends[2]*o['pitch'][0]/1000;M=Matrix.Translation((x,.018,0))@Matrix.Rotation(math.pi,4,'Z')@Matrix.Translation((-x,-.018,0));move_objects(parts,M)
  allparts+=parts
 if not transport:
  for f in o['fold_columns']:
   x=f*o['pitch'][0]/1000;axis=.018 if o['id']=='C' and f==2 else -.004
   for z in [.028,W-.028]:
    cube('Two-knuckle hinge / axis along border',(x,axis,z),(.025,.014,.014),STEELBLUE,.002)
    tube('Flat-print pin / assembled schematic',(x,axis,z-.011),(x,axis,z+.011),.005,ORANGE)
   for z in [.085,W-.085]:cube('Fold lock / removable dovetail bridge',(x,.015,z),(.075,.007,.030),ORANGE,.001)
 return allparts

def gate(o,offset=(0,0,0),scale=1,pvc=False):
 L,W=[v/1000 for v in o['cassette']];S=L+W
 allobjects=[]
 for k in range(4):
  before=set(COL.objects);cassette(o,PAPERS[k]);parts=[x for x in COL.objects if x not in before]
  M=Matrix.Translation(offset)@Matrix.Diagonal((scale,scale,scale,1))@Matrix.Translation((0,0,S/2))@Matrix.Rotation(-k*math.pi/2,4,'Y')@Matrix.Translation((-S/2,0,L-S/2))
  move_objects(parts,M);allobjects+=parts
 # Two radial slide-on keys per corner seam, accessible from its two open ends.
 for k in range(4):
  for dz in [.070,W-.070]:
   x=L-S/2;z=L+dz
   v=Vector((x,0,z-S/2));v=Matrix.Rotation(-k*math.pi/2,4,'Y')@v;v.z+=S/2
   p=Vector(offset)+v*scale
   q=cube('FIELD / removable corner bridge / 8 total',(p.x,p.y+.016*scale,p.z),(.065*scale,.009*scale,.040*scale),ORANGE,.001)
   q.rotation_euler.y=-k*math.pi/2
 if pvc:
  cy=S/2;P=.055;half=1.05
  for z in [cy-half,cy+half]:
   for sign in [-1,1]:tube('PVC / removable half rail',(0,P,z),(sign*half,P,z),.033401,WHITE,.003378)
   tube('PVC / midpoint coupling / separate transport',( -.035,P,z),(.035,P,z),.044,WHITE)
  for x in [-half,half]:
   for sign in [-1,1]:tube('PVC / removable half upright',(x,P,cy),(x,P,cy+sign*half),.033401,WHITE,.003378)
   tube('PVC / midpoint coupling / separate transport',(x,P,cy-.035),(x,P,cy+.035),.044,WHITE)
   for sg in [-1,1]:
    z=cy+sg*half;direction=-sg
    tube('PVC / 3-4 corner brace',(x,P+.035,z+direction*.4),(x-math.copysign(.4,x),P+.035,z),.02667,WHITE,.00287)
    cube('Brace-end clamp / split flat parts concept',(x,P+.02,z+direction*.4),(.040,.025,.030),ORANGE,.002)
    cube('Brace-end clamp / split flat parts concept',(x-math.copysign(.4,x),P+.02,z),(.040,.025,.030),ORANGE,.002)
  for x in [-half,half]:
   tube('Leg / schematic',(x,P,cy-half),(x,P,-.025),.033401,WHITE,.003378)
   tube('Short base foot / schematic',(x,P-.6,-.025),(x,P+.6,-.025),.033401,WHITE,.003378)
  for k in range(4):
   for t in [L*f-S/2 for f in [.16,.39,.61,.84]]:
    a=Vector((t,.055,cy+(half+L/2)/2));a=Matrix.Translation((0,0,cy))@Matrix.Rotation(-k*math.pi/2,4,'Y')@Matrix.Translation((0,0,-cy))@a
    dock=cube('PVC dock / adjustable offset +/-30 mm',(a.x,.037,a.z),(.040,.025,.034+abs(L/2-half)),ORANGE,.002)
    dock.rotation_euler.y=-k*math.pi/2
 return allobjects

setup('01_OPTIONS',(0,-12,2.55),(0,0,2.55),8.1,False);coll('01 / four complete face concepts')
for i,o in enumerate(OPTIONS):
 ox=-2.15 if i%2==0 else 1.35;oz=2.65 if i<2 else .65
 gate(o,(ox,0,oz),.52)
 text('Option label',f"{o['id']} / {o['name']}",(ox-.9,-.025,oz-.15),.105,INK,bold=True)
 text('Option summary',f"{o['inserts']} inserts | {o['cuts']} cuts | pack {o['pack'][0]:.0f} mm",(ox-.9,-.025,oz-.30),.065,MUTED)
header('01','Four uniform-insert options','All travel as four folding cassettes. Cardstock stays loaded. Quarter / half / whole sheets versus exact metric sizing.')
footer('Small dimensional changes include 4 mm pitch allowance for channels and paper clearance. Color shows the four identical pinwheel cassettes.')

for i,o in enumerate(OPTIONS):
 setup(f"0{i+2}_{o['id']}_ASSEMBLED",(-3.5,-7.8,4.2),(.65,0,1.50),6.6)
 coll('01 / uniform inserts and folding exoskeleton');gate(o,pvc=True)
 header(str(i+2).zfill(2),f"{o['id']} / {o['name']}",o['note'])
 overlay(f"{o['card'][0]:g} x {o['card'][1]:g} mm",.735,.30,.022,True)
 overlay('ONE INSERT SIZE',.735,.345,.014,color=MUTED)
 overlay(f"{o['inserts']} inserts / {o['sheets']} sheets\n{o['cuts']} straight cuts total",.735,.43,.017,True)
 overlay(f"Outer: {o['outer']:.1f} mm\nOpening: {o['opening']:.1f} mm",.735,.55,.015,color=MUTED)
 overlay(f"4 folded bundles\n{o['pack'][0]:.0f} x {o['pack'][1]:.0f} mm",.735,.68,.018,True)
 overlay(f"PETG planning: {o['PETG_kg']:.1f} kg\nFace materials: ~${o['consumed_USD']:.0f}",.735,.81,.014,color=MUTED)
 footer('Same single PVC backing concept; pipe splits at four midpoints for transport. Base/guys must follow the existing anchored or ballasted design.')

# Scene 06: actual paper channels plus insertion and removable cap.
setup('06_SLIDE_IN',(1.15,-1.75,1.20),(.38,0,.45),1.95,False);coll('01 / half-sheet insertion sequence')
o=OPTIONS[1];px,py=[v/1000 for v in o['pitch']]
# Build one cell; move the entire end cap away, then draw paper partly withdrawn.
parts=leaf_geometry(o,0,1,PAPER,offset=(0,0,0))
for part in list(parts):
 if part.name.startswith('B / cardstock'):part.location.z+=.22
 if part.name.startswith('Slide-in'):
  loc=part.matrix_world.translation
  # Top cap has longitudinal rail direction -X.
  if part.matrix_world.col[0].x<-.9 and loc.z>py-.01:
   part.location.y-=.12;part.location.x+=.08;part.location.z+=.06
# Large labels and insertion arrow alongside actual rail channels.
line('Slide direction',[(.43,-.012,.74),(.43,-.012,.31)],.003,CORD)
line('Slide arrow',[(.40,-.012,.35),(.43,-.012,.31),(.46,-.012,.35)],.003,CORD)
# A greatly magnified end section demonstrates open slot and paper engagement.
coll('02 / magnified rail section')
sec=profile_x('Channel cutaway / 6x scale',PROFILE,22)
sec.matrix_world=Matrix(((6,0,0,.68),(0,0,6,0),(0,6,0,.20),(0,0,0,1)))
cube('Paper / magnified 0.4 mm',(.746,.0084,.257),(.10,.0024,.09),PAPER)
header('06','Slide in. Click the cap back.','Remove the outer end-cap rail only. Feed the card through parallel side channels; stop against the fixed bottom channel.')
overlay('0.8 mm slot',.69,.31,.019,True)
overlay('For nominal 0.4 mm card\nMeasure the actual stock first',.69,.355,.014,color=MUTED)
overlay('1.2 mm lips + rear spine',.69,.52,.017,True)
overlay('One channel prints on its spine\nOpposed channels share a node',.69,.56,.013,color=MUTED)
overlay('Printed joints stay assembled',.64,.78,.018,True)
footer('Slot tolerance is a starting point. Stop cap prevents card migration. Rear ribs and keepers support both pressure directions.')

# Scene 07: meaningful prototype parts and assembly motion, all mesh geometry.
setup('07_CLICK_JOINERY',(.17,-.25,.25),(.04,.005,.015),.43,False);coll('01 / sliding dovetail and release spring')
track=instance(TRACK,'ASSEMBLED / dovetail receiver',Matrix.Translation((-.06,0,0)))
shoeM=Matrix.Translation((-.058,0,.007))@Matrix.Rotation(math.pi,4,'X')
instance(SHOE,'ASSEMBLED / release shoe',shoeM)
instance(TRACK,'EXPLODED / receiver',Matrix.Translation((.035,0,0)))
instance(SHOE,'EXPLODED / shoe / withdraw parallel to track',Matrix.Translation((.037,0,.035))@Matrix.Rotation(math.pi,4,'X'))
line('Withdrawal arrow',[(.012,-.033,.012),(-.033,-.033,.012)],.0008,CORD)
line('Withdrawal arrowhead',[(-.025,-.038,.012),(-.033,-.033,.012),(-.025,-.028,.012)],.0008,CORD)
header('07','Let the dovetail carry the load','The replaceable spring only retains the slide. Press it sideways to clear the notch, then withdraw the shoe.')
overlay('ASSEMBLED',.12,.70,.018,True);overlay('EXPLODED',.54,.70,.018,True)
overlay('Spring lies in print XY plane',.10,.78,.016,color=MUTED)
overlay('45-degree dovetail walls',.55,.78,.016,color=MUTED)
footer('For field corners: two tracks joined by a bridge shoe, inserted along the open seam ends. Eight release keys close the four-panel ring.')

# Scene 08: half-sheet cassette, actual book fold and four packed bundles.
setup('08_FOUR_PACKS',(2.9,-5.8,3.7),(.2,0,1.1),5.8,False);coll('01 / unfolded half-sheet cassette')
o=OPTIONS[1];before=set(COL.objects);cassette(o,PAPER)
parts=[x for x in COL.objects if x not in before];move_objects(parts,Matrix.Translation((-1.7,0,1.55)))
coll('02 / four book-fold bundles')
for k in range(4):
 before=set(COL.objects);cassette(o,PAPERS[k],transport=True)
 parts=[x for x in COL.objects if x not in before]
 # Folded range is [0, L/2]. Offset each bundle with a small rear gap.
 move_objects(parts,Matrix.Translation((-.9,.12*k,.15)))
header('08','Four bundles. No loose paper.','B / Half sheets: unfold each book, engage two fold locks, then join the four cassettes at their corners.')
overlay('UNFOLDED',.70,.30,.018,True)
overlay('2158 x 563 mm per cassette\nSix half-sheet inserts remain in place',.70,.35,.014,color=MUTED)
overlay('TRANSPORT',.70,.60,.018,True)
overlay('About 1079 x 563 x 40 mm each\nFour face bundles + a PVC parts bag',.70,.65,.014,color=MUTED)
footer('PVC saddles stay on the separate frame. Low docking receivers stay on the face. PVC rails split into sub-1.2 m sections at four couplers.')

# Scene 09: whole-sheet trifold uses opposite fold offsets and no paper bending.
setup('09_TRIFOLD_AND_HINGE',(2.5,-4.0,3.2),(.25,0,1.0),5.0,False);coll('01 / whole-sheet open cassette')
o=OPTIONS[2];before=set(COL.objects);cassette(o,PAPER);move_objects([x for x in COL.objects if x not in before],Matrix.Translation((-1.5,0,1.15)))
coll('02 / trifold bundle');before=set(COL.objects);cassette(o,PAPER,True);move_objects([x for x in COL.objects if x not in before],Matrix.Translation((-1.4,0,.10)))
# Enlarged printable hinge components, separated so the axis and split pin are visible.
coll('03 / planar hinge construction')
instance(HINGE,'Hinge leaf one / magnified',Matrix.Translation((1.20,0,.20))@Matrix.Scale(5,4))
instance(HINGE,'Hinge leaf two / magnified',Matrix.Translation((1.20,0,.245))@Matrix.Rotation(math.pi,4,'Z')@Matrix.Scale(5,4))
instance(PIN,'Flat split pin / magnified',Matrix.Translation((1.34,0,.20))@Matrix.Scale(5,4))
header('09','Uncut sheets need a third leaf','C / Two offset hinges fold the three rigid leaves into a roughly 715 x 563 mm bundle. Cardstock never folds.')
overlay('HINGE PARTS',.71,.68,.018,True)
overlay('Two flat knuckles + removable pin\nA separate bridge locks the leaf straight',.71,.73,.013,color=MUTED)
footer('Quarter and half sheets need one fold per cassette. Whole sheets need two: no hidden crease, slit or paper cutting is required.')

# Scene 11: stock yield visualized using exact equal cuts.
setup('11_STOCK_CUTS',(0,-8,1.1),(0,0,1.1),4.8,False);coll('01 / exact stock patterns')
for i,o in enumerate(OPTIONS):
 ox=-2.1+i*1.08;oz=.75
 cube('22 x 28 stock',(ox+.2794,.007,oz+.3556),(.5588,.004,.7112),GREEN)
 for j,(x,y,w,h) in enumerate(o['stock_pattern']):cube('Uniform insert cut',(ox+(x+w/2)/1000,0,oz+(y+h/2)/1000),(w/1000,.004,h/1000),PAPERS[j%4])
 text('Stock option',o['id']+' / '+o['name'],(ox,-.015,1.60),.070,INK,bold=True)
 text('Cut quantity',f"{o['cuts_per_sheet']} cuts / sheet\n{o['sheets']} sheets / gate\n{o['cuts']} cuts total",(ox,-.015,.60),.065,MUTED)
header('11','Uniform inserts change the equation','Quarter: split both ways. Half: one crosscut. Whole: use as purchased. Metric: two trims, then split both ways.')
footer('Cut counts are separate straight cuts without stacked cutting; repeated knife passes are not counted. Stock size and squareness must be checked.')

# Scene 12: rear side demonstrates single PVC backing, removable saddles and accessible releases.
setup('12_REAR_DOCKING',(4,7,4.3),(-.35,0,1.5),6.3);coll('01 / complete rear half-sheet concept');gate(OPTIONS[1],pvc=True)
header('12','Click the face onto one PVC frame','Sixteen docking positions. Saddles stay with the pipes; the four folded face bundles keep their low-profile receivers.')
overlay('PVC / 33.4 mm OD',.73,.32,.017,True)
overlay('C-saddles print with pipe axis vertical\nProvide a positive mouth keeper',.73,.37,.013,color=MUTED)
overlay('RELEASE FROM THE REAR',.73,.53,.017,True)
overlay('Press latch, slide dock free\nFold only after detaching from PVC',.73,.58,.013,color=MUTED)
overlay('FOUR CORNER BRACES',.73,.74,.017,True)
overlay('Retain the established anchoring\nClamps need support-free split bodies',.73,.79,.013,color=MUTED)
footer('PVC fitting envelopes and dock positions are schematic. Keeper and brace clamp interfaces need the next fit-prototype pass; no structural rating.')

# Save all design data and print-validation results with the model.
(OUT/'options.json').write_text(json.dumps(OPTIONS,indent=2));(OUT/'prototype_validation.json').write_text(json.dumps(PRINT_CHECKS,indent=2))
t=bpy.data.texts.new('START_HERE.txt');t.write('UNIFORM POSTERBOARD GATE CONCEPTS\n\n01: compare four options\n02-05: full assembled alternatives\n06: slide-in cardstock and removable end cap\n07: releasable load-bearing dovetail concept\n08: half-sheet book folds / four bundles\n09: whole-sheet trifold and planar hinge parts\n10: actual support-free prototype coupon print orientations\n11: equal stock cuts\n12: PVC rear docking\n\nRead CONCEPT_GUIDE.md. This file compares concepts; seven coupon STLs are for fit testing, not a complete gate manufacturing kit. No cycle/load validation has been performed.\n')
if (OUT/'CONCEPT_GUIDE.md').exists():
 t=bpy.data.texts.new('CONCEPT_GUIDE.md');t.write((OUT/'CONCEPT_GUIDE.md').read_text())
# Remove only the empty helper startup scene.
empty=bpy.data.scenes.get('01_ASSEMBLED')
if empty and len(empty.objects)==0:bpy.data.scenes.remove(empty)
bpy.context.window.scene=bpy.data.scenes['01_OPTIONS']
for screen in bpy.data.screens:
 for area in screen.areas:
  if area.type=='VIEW_3D':area.spaces.active.region_3d.view_perspective='CAMERA';area.spaces.active.shading.type='MATERIAL'
bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'Posterboard_Gate_Options.blend'))
names=os.environ.get('RENDER_SCENES',','.join(s.name for s in bpy.data.scenes)).split(',')
for name in names:
 if not name:continue
 s=bpy.data.scenes[name];bpy.context.window.scene=s;s.render.filepath=str(OUT/'renders'/f'{name}.png');bpy.ops.render.render(write_still=True,scene=name)
print('CONCEPT BUILD COMPLETE',json.dumps(PRINT_CHECKS))

"""Clearance study using the user-supplied GEPRC assembly; original helper code: scripts/LICENSE.
Imported drone geometry retains its separate CC BY-NC 4.0 reference terms.
"""
from pathlib import Path
exec(Path(__file__).with_name('build_a1_full_size.py').read_text().split('# Registered channel splice:')[0],globals())
import numpy as np,csv
OUT=ROOT/'output/drone_clearance_study';(OUT/'renders').mkdir(parents=True,exist_ok=True)
REF=Path(os.environ.get('GEPRC_REFERENCE_DIR','/tmp/fpv-geprc-reference'))
with bpy.data.libraries.load(str(ROOT/'output/corner_guide_elbow/Corner_Guide_Elbow.blend')) as (src,dst):dst.scenes=['11_ALL_PRODUCTION_PARTS']
lib=dst.scenes[0];gate_meshes={}
for code in ['ELBOW','DUAL_GUY_ELBOW','TEE','CROSS','MAG_SLEEVE']:
 gate_meshes[code]=next(o.data for o in lib.objects if o.type=='MESH' and o.name.startswith(code))
bpy.data.scenes.remove(lib)
bpy.context.window.scene=SC
bpy.ops.import_scene.gltf(filepath=str(REF/'geprc.glb'))
imported=[o for o in SC.objects if o.type=='MESH'];Rx=lambda a:Matrix.Rotation(math.radians(a),4,'X');Ry=lambda a:Matrix.Rotation(math.radians(a),4,'Y')
NORMALIZE=Rx(90);drone=[];points=[];prop_arrays=[]
for o in imported:
 M=NORMALIZE@o.matrix_world
 a=np.empty((len(o.data.vertices),3),np.float32);o.data.vertices.foreach_get('co',a.ravel());mm=np.array(M)
 a=a@mm[:3,:3].T+mm[:3,3];points.append(a)
 if o.name.startswith('HQ V1S'):prop_arrays.append(a)
 drone.append((o.name,o.data,M));o.hide_render=True;o.hide_set(True)
allpoints=np.concatenate(points)
source_rows=json.loads((REF/'assembly_bounds.json').read_text())
nuts=[r for r in source_rows if r['name'].startswith('AS 1285')]
MOTORS=[((r['bounds'][0]+r['bounds'][3])/2000,-(r['bounds'][1]+r['bounds'][4])/2000) for r in nuts];assert len(MOTORS)==4
radii=[];propz=[]
for a in prop_arrays:
 cx,cy=min(MOTORS,key=lambda p:np.linalg.norm(a[:,:2].mean(axis=0)-p))
 radii.append(float(np.sqrt((a[:,0]-cx)**2+(a[:,1]-cy)**2).max()));propz.extend([float(a[:,2].min()),float(a[:,2].max())])
RADIUS=max(.0889,*radii);ZLO=min(propz);ZHI=max(propz)
# A clearly labeled provisional flight battery, absent from the downloaded assembly.
# 110 x 40 x 45 mm, top mounted on the 30 mm-high deck. It is not the user's measured battery.
BAT_CENTER=Vector((0,0,.053));BAT_SIZE=Vector((.040,.110,.045))
batpoints=np.array([BAT_CENTER+Vector((sx*BAT_SIZE.x/2,sy*BAT_SIZE.y/2,sz*BAT_SIZE.z/2)) for sx in [-1,1] for sy in [-1,1] for sz in [-1,1]])
allpoints=np.concatenate([allpoints,batpoints])
CARBON=mat('Study / dark battery',(.025,.030,.04));STRAP=mat('Study / orange battery straps',(.9,.26,.025));PAPER_STUDY=mat('Study / paper',(.98,.29,.045));MAG=mat('Study / magnets',(.35,.40,.45),.7)
SWEEP=mat('Swept prop boundary / cyan',(.02,.55,.65),emit=True)
BATTERY=box('Assumed 110 x 40 x 45 mm battery',tuple(BAT_CENTER*1000),tuple(BAT_SIZE*1000),CARBON);BATTERY.hide_render=True;BATTERY.hide_set(True)
drone.append((BATTERY.name,BATTERY.data,Matrix.Identity(4)))
# Two straps identify the explicitly assumed battery in the illustration.
for yy in [-30,30]:
 o=box('Assumed battery strap',(0,yy,76),(42,12,1.6),STRAP);o.hide_render=True;o.hide_set(True);drone.append((o.name,o.data,Matrix.Identity(4)))
# Include strap bounds in the geometric envelope too.
allpoints=np.concatenate([allpoints,np.array([(x,y,z) for x in [-.021,.021] for y in [-.036,.036] for z in [.0752,.0768]])])

def bounds(rotation):
 R=np.array(rotation)[:3,:3];a=allpoints@R.T;lo=a.min(axis=0);hi=a.max(axis=0)
 for x,y in MOTORS:
  for zz in [ZLO,ZHI]:
   center=R@np.array([x,y,zz]);rad=RADIUS*np.sqrt(R[:,0]**2+R[:,1]**2)
   lo=np.minimum(lo,center-rad);hi=np.maximum(hi,center+rad)
 return lo,hi

def drone_at(center,pitch=20,yaw=0,roll=0,sweep=True,animate=False):
 rot=Rz(yaw)@Ry(roll)@Rx(pitch);lo,hi=bounds(rot);mid=Vector((lo+hi)/2);origin=Vector(center)-mid
 coll('20 / imported reference drone and assumed battery')
 parent=bpy.data.objects.new('Flight path / center crossing at frame 40',None);COL.objects.link(parent);parent.location=origin
 for name,data,M in drone:
  o=bpy.data.objects.new('Drone / '+name,data);COL.objects.link(o);o.parent=parent;o.matrix_parent_inverse=Matrix.Identity(4);o.matrix_basis=rot@M
 if sweep:
  coll('21 / swept propeller boundaries')
  for x,y in MOTORS:
   pts=[rot@Vector((x+RADIUS*math.cos(t*math.tau/128),y+RADIUS*math.sin(t*math.tau/128),(ZLO+ZHI)/2)) for t in range(128)]
   ring=line('Swept prop disc / envelope, not a physical guard',pts,.0018,SWEEP,True);ring.parent=parent
 if animate:
  for frame,offset in [(1,.8),(40,0),(80,-.8)]:
   parent.location=origin+Vector((0,offset,0));parent.keyframe_insert(data_path='location',frame=frame)
  SC.frame_start=1;SC.frame_end=80;SC.frame_set(40)
 return {'width_mm':float((hi[0]-lo[0])*1000),'height_mm':float((hi[2]-lo[2])*1000),'depth_mm':float((hi[1]-lo[1])*1000)}

BOM=json.loads((ROOT/'output/corner_guide_elbow/BOM.json').read_text());base=BOM['gates']['single'];W=609.6
# Use exactly the existing fittings at adjusted grid positions. Four sleeves per long
# member are retained even on smaller study gates; all have exposed pipe room.
def render_gate(opening,center=(0,0,0),paper=True):
 outer=opening+2*W;oldxs=base['x_grid_mm'];oldys=base['y_grid_mm'];new=[75,W-75,outer-W+75,outer-75]
 def coord(q,old):
  for i in range(3):
   if old[i]-.001<=q<=old[i+1]+.001:return new[i]+(q-old[i])/(old[i+1]-old[i])*(new[i+1]-new[i])
  raise ValueError(q)
 M=basis((1,0,0),(0,0,1),(0,1,0),(center[0]*1000-outer/2,center[1]*1000,center[2]*1000-outer/2))
 coll('10 / unchanged printed fittings')
 magnets=set()
 for code,xy,angle in base['placements']:
  pos=(coord(xy[0],oldxs),coord(xy[1],oldys));matr=M@T(*pos,0)@Rz(angle)
  o=bpy.data.objects.new('Gate / '+code,gate_meshes[code]);COL.objects.link(o);o.matrix_world=matr
  if code=='MAG_SLEEVE' or code in ['ELBOW','DUAL_GUY_ELBOW']:
   locals=BOM['magnet_pockets_local_mm'][code]
  else:
   # Keep only the populated positions from the real gate's magnet ledger.
   locals=[]
   for x,y in BOM['magnet_pockets_local_mm'][code]:
    a=math.radians(angle);px=xy[0]+x*math.cos(a)-y*math.sin(a);py=xy[1]+x*math.sin(a)+y*math.cos(a)
    if min(math.hypot(px-u,py-v) for u,v in base['magnets'])<.01:locals.append((x,y))
  for x,y in locals:magnets.add(tuple(matr@Vector((x/1000,y/1000,-.0012))))
 coll('11 / actual PVC diameters')
 for e in base['edges']:
  aa=base['nodes'][e['a']]['xy'];zz=base['nodes'][e['b']]['xy'];a=Vector((coord(aa[0],oldxs),coord(aa[1],oldys),24));z=Vector((coord(zz[0],oldxs),coord(zz[1],oldys),24));u=(z-a).normalized()
  tube('PVC '+e['name'],M@((a+35*u)/1000),M@((z-35*u)/1000),.0334,WHITE,.00338)
 coll('12 / paper and magnets')
 if paper:
  rects=[(0,0,outer,W),(0,outer-W,outer,W),(0,W-36,W,opening+72),(outer-W,W-36,W,opening+72)]
  for i,(x,y,w,h) in enumerate(rects):
   o=box('Paper',(x+w/2,y+h/2,-.2 if i<2 else -.5),(w,h,.2),PAPER_STUDY);raw_transform(o,M)
 for p in magnets:tube('Front 6 mm magnet',Vector(p)+Vector((0,-.002,0)),p,.006,MAG)
 return outer

def dimension(a,b,label,offset=(0,0,.03),size=.05):
 a,b=Vector(a),Vector(b);line('Dimension / '+label,[a,b],.002,INK)
 t=Vector((0,0,.025)) if abs(a.x-b.x)>.01 else Vector((.025,0,0))
 for p in [a,b]:line('Witness',[p-t,p+t],.002,INK)
 text('Dimension / '+label,label,(a+b)/2+Vector(offset),size,INK,align='CENTER')

pitch=20;lo,hi=bounds(Rx(pitch));width=(hi[0]-lo[0])*1000;height=(hi[2]-lo[2])*1000
motor_width=(max(p[0] for p in MOTORS)-min(p[0] for p in MOTORS))*1000
motor_length=(max(p[1] for p in MOTORS)-min(p[1] for p in MOTORS))*1000
wheelbase=math.hypot(motor_width,motor_length)
assert len(prop_arrays)==4 and 290<wheelbase<300 and .085<RADIUS<.095
assert np.linalg.norm(allpoints[:,:2],axis=1).max()<=wheelbase/2000+RADIUS
yawmax=wheelbase+RADIUS*2000
LEVEL=bounds(Matrix.Identity(4));ANGLED=bounds(Rz(45)@Ry(30)@Rx(20))
report={'source':'Dendy / Printables 1515387, user supplied ZIP; STEP assembly includes third-party frame','motor_width_mm':motor_width,'motor_length_mm':motor_length,'motor_diagonal_mm':wheelbase,'nominal_prop_diameter_mm':177.8,'measured_prop_radii_mm':[r*1000 for r in radii],'used_prop_radius_mm':RADIUS*1000,'battery_assumption_mm':[110,40,45],'battery_measured':False,'render_pitch_degrees':20,'main_envelope_axis_order':['width_x','height_z','depth_y'],'other_envelopes_axis_order':['x','y','z'],'main_envelope_mm':[width,height,float((hi[1]-lo[1])*1000)],'level_envelope_mm':list((LEVEL[1]-LEVEL[0])*1000),'banked_envelope_mm':list((ANGLED[1]-ANGLED[0])*1000),'level_worst_yaw_prop_width_mm':yawmax,'variants':[]}
for opening in [1480.8,1200,1000,800]:
 report['variants'].append({'opening_mm':opening,'outer_mm':opening+2*W,'left_right_clearance_mm':(opening-width)/2,'top_bottom_clearance_mm':(opening-height)/2,'level_worst_yaw_side_clearance_mm':(opening-yawmax)/2,'width_ratio':opening/width,'opening_area_relative':(opening/1480.8)**2,'short_pvc_cut_mm':389.6,'long_pvc_cut_mm':opening+80})
(OUT/'clearance.json').write_text(json.dumps(report,indent=2))
with (OUT/'Clearance_Comparison.csv').open('w') as f:
 writer=csv.DictWriter(f,fieldnames=list(report['variants'][0]));writer.writeheader();writer.writerows(report['variants'])

# Faithful full-size gate with centered drone, moving toward the camera.
setup('01_CURRENT_GATE_PASS',(3.7,-6.0,2.6),(0,0,.2),6.8,False)
render_gate(1480.8);drone_at((0,0,0),animate=True)
header('01','Your 7-inch quad / current gate','Imported MK4 assembly, centered at the crossing plane. 20-degree forward pitch; full swept propeller envelope.')
footer('Reference: Dendy / Printables 1515387 (CC BY-NC 4.0). Battery is assumed 110 x 40 x 45 mm; verify your own build.')
setup('02_CURRENT_CLEARANCE',(0,-6,.15),(0,0,.15),6.3,False)
render_gate(1480.8);drone_at((0,0,0))
coll('30 / dimensions');gap=(1480.8-width)/2
for sign in [-1,1]:dimension((sign*.7404,-.29,0),(sign*width/2000,-.29,0),f'{gap:.0f} mm',size=.062)
dimension((-.7404,-.29,.85),(.7404,-.29,.85),'1480.8 mm clear',size=.068)
dimension((width/2000+.11,-.29,height/2000),(width/2000+.11,-.29,.7404),f'{(1480.8-height)/2:.0f} mm',(0.20,0,0),.058)
dimension((width/2000+.11,-.29,-.7404),(width/2000+.11,-.29,-height/2000),f'{(1480.8-height)/2:.0f} mm',(0.20,0,0),.058)
header('02','Current opening / centered clearances',f'Swept width {width:.1f} mm; projected height {height:.1f} mm at 20-degree pitch. The reference envelope is centered in the opening.')
footer('Static geometric clearance to the paper edges, not an allowance for tracking error, wind or paper movement. Cyan outlines = swept props.')
# Same image scale and drone size in every cell.
setup('03_FOUR_OPENINGS',(0,-8,0),(0,0,0),9.2,False);SC.render.resolution_x=2400;SC.render.resolution_y=2000
for row,center in zip(report['variants'],[(-1.85,0,1.10),(1.85,0,1.10),(-1.85,0,-2.10),(1.85,0,-2.10)]):
 render_gate(row['opening_mm'],center);drone_at(center)
 # Labels are camera-space for readability across four physical examples.
 x=.09 if center[0]<0 else .55;y=.555 if center[2]>0 else .955
 overlay(f'{row["opening_mm"]:.0f} mm opening  |  {row["left_right_clearance_mm"]:.0f} mm each side',x,y,.015,True)
header('03','Four openings / same drone / same scale','24-inch paper bands and existing fittings retained. Compare the clear opening, not the overall gate size.')
# Side-by-side opening-only close-ups make differences legible without wide paper bands.
setup('04_OPENING_DETAIL',(0,-6,0),(0,0,0),4.6,False);SC.render.resolution_x=2400;SC.render.resolution_y=2100
for row,center in zip(report['variants'],[(-1.05,0,.52),(1.05,0,.52),(-1.05,0,-1.13),(1.05,0,-1.13)]):
 h=row['opening_mm']/2000;band=.045;cx,cy,cz=center
 coll('10 / inner-edge crop, actual dimensions')
 for xx,zz,ww,hh in [(cx-h-band/2,cz,band,2*h+2*band),(cx+h+band/2,cz,band,2*h+2*band),(cx,cz+h+band/2,2*h,band),(cx,cz-h-band/2,2*h,band)]:
  box('Paper inner edge crop',(xx*1000,0,zz*1000),(ww*1000,.3,hh*1000),PAPER_STUDY)
 drone_at(center);x=.095 if cx<0 else .555;y=.585 if cz>0 else .938
 overlay(f'{row["opening_mm"]:.0f} mm  /  side gap {row["left_right_clearance_mm"]:.0f} mm',x,y,.016,True)
header('04','Opening close-ups / equal scale','Only a narrow strip of each paper edge is shown. Drones remain the same size; pose is 20-degree forward pitch.')
# Enlarged reference, including clear identification of its illustrative battery.
setup('05_DRONE_REFERENCE',(.55,-.70,.45),(0,0,0),.80,False);drone_at((0,0,0),pitch=0)
header('05','Imported MK4 / swept propeller envelope',f'Motor diagonal {wheelbase:.1f} mm. CAD prop sweep diameter {RADIUS*2000:.1f} mm; nominal seven inches = 177.8 mm.')
footer('Actual supplied assembly, reoriented upright. Cyan = prop sweep. Dark top battery with orange straps is an assumed addition.')
setup('06_SMALLER_GATE_PASS',(2.8,-4.8,2.18),(0,0,.18),5.6,False);render_gate(1000);drone_at((0,0,0),animate=True)
header('06','1000 mm opening / suggested next trial',f'Outer size 2219.2 mm with full-width paper. Centered side clearance: {(1000-width)/2:.0f} mm per side at this pose.')
footer('A sizing study, not a newly validated production kit. Existing printed types retained; long PVC cuts become 1080 mm.')
# Attitude comparison at 1 m opening, using actual swept model supports.
setup('07_ATTITUDE_COMPARISON',(0,-6,0),(0,0,0),3.8,False);SC.render.resolution_x=2400;SC.render.resolution_y=1400
for center,yaw,roll in [((-.84,0,-.15),0,0),((.84,0,-.15),45,30)]:
 h=.5;cx,cy,cz=center;coll('10 / opening border')
 for xx,zz,ww,hh in [(cx-h-.025,cz,.05,1.1),(cx+h+.025,cz,.05,1.1),(cx,cz+h+.025,1,.05),(cx,cz-h-.025,1,.05)]:box('1 m opening crop',(xx*1000,0,zz*1000),(ww*1000,.3,hh*1000),PAPER_STUDY)
 q=drone_at(center,yaw=yaw,roll=roll);x=.12 if yaw==0 else .565
 overlay(f'Yaw {yaw} / roll {roll} / pitch 20 degrees',x,.835,.017,True)
 overlay(f'{q["width_mm"]:.0f} x {q["height_mm"]:.0f} mm projected envelope',x,.876,.014)
header('07','Attitude matters / both openings are 1 metre','The drone is re-centered by its projected swept envelope in each view. A turn or bank changes both clearances.')
footer('No flight-control error margin is included. Measure your actual props, battery and antennas before choosing an opening.')
for name in ['00_MASTERS','01_ASSEMBLED']:
 if bpy.data.scenes.get(name):bpy.data.scenes.remove(bpy.data.scenes[name])
bpy.context.window.scene=bpy.data.scenes['01_CURRENT_GATE_PASS'];bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'Drone_Clearance_Study.blend'),compress=True)
if '--no-render' not in sys.argv:
 for sc in bpy.data.scenes:
  selected=os.environ.get('RENDER_SCENES','')
  if selected and sc.name not in selected.split(','):continue
  bpy.context.window.scene=sc;sc.render.filepath=str(OUT/'renders'/f'{sc.name}.png');bpy.ops.render.render(write_still=True,scene=sc.name)
print('CLEARANCE STUDY',json.dumps(report),flush=True)

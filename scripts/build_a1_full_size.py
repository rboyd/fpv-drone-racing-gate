"""Full-size rigid whole-sheet gate: all printed components represented by STL masters.
Units in calculations: mm; Blender: m. Permanent workshop joints use ties.
"""
from pathlib import Path
exec(Path(__file__).with_name('build_gate.py').read_text().split('# Print master:')[0],globals())
import bmesh,collections,hashlib,zipfile,xml.etree.ElementTree as ET
OUT=ROOT/'output/a1_full_size'
for d in ['printable','renders']:(OUT/d).mkdir(parents=True,exist_ok=True)
PX,PY=717.2,564.8;L=3*PX;S=L+PY;OPEN=L-PY
PARTS={};COUNTS=collections.Counter();STOCK=collections.Counter();PLACEMENTS=[];BAY0=[]
PAPER=mat('Posterboard / warm white',(.84,.88,.9));STEEL=mat('Workshop PETG / blue',(.035,.16,.30))
PROFILE=[(0,0),(6,0),(6,1.2),(1.8,1.2),(1.8,2),(6,2),(6,3.2),(1.8,3.2),(1.8,7),(2.4,7),(2.4,14),(0,14)]
# All raw CAD geometry uses mm coordinates, converted to m immediately.
def mesh(name,vs,fs,material=ORANGE):
 m=bpy.data.meshes.new(name);m.from_pydata([[a/1000 for a in v] for v in vs],[],fs);m.update();o=bpy.data.objects.new(name,m);COL.objects.link(o);o.data.materials.append(material);clean(o);return o
def clean(o):
 b=bmesh.new();b.from_mesh(o.data);bmesh.ops.remove_doubles(b,verts=list(b.verts),dist=1e-7);bmesh.ops.dissolve_degenerate(b,edges=list(b.edges),dist=1e-8);bmesh.ops.recalc_face_normals(b,faces=list(b.faces));b.to_mesh(o.data);b.free()
def box(name,c,d,material=ORANGE):
 vs=[(c[0]+x*d[0]/2,c[1]+y*d[1]/2,c[2]+z*d[2]/2) for x,y,z in [(-1,-1,-1),(1,-1,-1),(1,1,-1),(-1,1,-1),(-1,-1,1),(1,-1,1),(1,1,1),(-1,1,1)]]
 return mesh(name,vs,[(3,2,1,0),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],material)
def prism(name,pts,h,z=0,material=ORANGE):
 n=len(pts);vs=[(x,y,zz) for zz in [z,z+h] for x,y in pts];fs=[tuple(reversed(range(n))),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)];return mesh(name,vs,fs,material)
def extrude_x(name,profile,length,x0=0,material=ORANGE):
 n=len(profile);vs=[(x,y,z) for x in [x0,x0+length] for y,z in profile];fs=[tuple(reversed(range(n))),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)];return mesh(name,vs,fs,material)
def boolean(o,c,op='DIFFERENCE'):
 bpy.context.view_layer.update()
 for t in [o,c]:
  b=bmesh.new();b.from_mesh(t.data);bmesh.ops.triangulate(b,faces=list(b.faces));b.to_mesh(t.data);b.free()
 bpy.context.view_layer.objects.active=o;m=o.modifiers.new('CAD','BOOLEAN');m.operation=op;m.solver='EXACT';m.object=c;bpy.ops.object.modifier_apply(modifier=m.name);bpy.data.objects.remove(c,do_unlink=True);clean(o)
def add(o,c):boolean(o,c,'UNION')
def diamond(o,x,y,d,z0=-5,h=40):boolean(o,prism('Diamond clearance',[(x-d/2,y),(x,y-d/2),(x+d/2,y),(x,y+d/2)],h,z0))
def raw_transform(o,M):
 for v in o.data.vertices:v.co=M@v.co
 clean(o)
def T(x=0,y=0,z=0):return Matrix.Translation((x/1000,y/1000,z/1000))
def Rz(a):return Matrix.Rotation(math.radians(a),4,'Z')
def basis(ex,ey,ez,origin):
 return Matrix(((ex[0],ey[0],ez[0],origin[0]/1000),(ex[1],ey[1],ez[1],origin[1]/1000),(ex[2],ey[2],ez[2],origin[2]/1000),(0,0,0,1)))
PRINT_RAIL=Matrix(((1,0,0,0),(0,0,-1,0),(0,1,0,0),(0,0,0,1)))
PRINT_RIB=Matrix(((1,0,0,0),(0,0,1,0),(0,-1,0,0),(0,0,0,1)))
PRINT_AXIAL=Matrix(((0,1,0,0),(0,0,1,0),(1,0,0,0),(0,0,0,1)))
def master(code,o,description,print_matrix=Matrix.Identity(4)):
 clean(o);b=bmesh.new();b.from_mesh(o.data);bad=sum(not e.is_manifold for e in b.edges);vol=abs(b.calc_volume())*1e9;b.free();assert bad==0,(code,bad)
 pm=o.data.copy()
 for v in pm.vertices:v.co=print_matrix@v.co
 lo=Vector([min(v.co[j] for v in pm.vertices) for j in range(3)])
 for v in pm.vertices:v.co-=lo
 bm=bmesh.new();bm.from_mesh(pm);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(pm);bm.free();pm.calc_loop_triangles()
 bounds=[max(v.co[j] for v in pm.vertices)*1000 for j in range(3)];assert max(bounds)<=170,(code,bounds)
 fn=code+'.stl'
 with (OUT/'printable'/fn).open('wb') as f:
  f.write(('A1 full-size prototype '+code+'; mm').encode().ljust(80,b' ')[:80]);f.write(struct.pack('<I',len(pm.loop_triangles)))
  for tr in pm.loop_triangles:
   a,b,c=[pm.vertices[j].co*1000 for j in tr.vertices];n=(b-a).cross(c-a).normalized();f.write(struct.pack('<12fH',*n,*a,*b,*c,0))
 PARTS[code]={'object':o,'print_mesh':pm,'description':description,'file':fn,'print_bounds_mm':[round(x,3) for x in bounds],'solid_volume_mm3':round(vol,2),'nonmanifold_edges':bad}
 o.hide_render=True;o.hide_set(True);return code
setup('00_MASTERS',(1,-2,1),(0,0,0),2,False);coll('00 / CAD masters hidden in presentation')
# Registered channel splice: four hollow locating bosses carry shear; two ties retain it.
o=box('Registered channel splint',(0,0,1.2),(40,8,2.4),STEEL)
for x in [-16.1,-8.1,8.1,16.1]:
 add(o,box('Hollow locating boss',(x,0,3.4),(5.6,4.6,2)))
 boolean(o,box('Tie passage',(x,0,2.4),(3.6,2.6,8)))
master('SPLINT',o,'40 mm registered channel splint; two ties per joint')
# Corner nodes occupy the INSIDE quadrant, so adjacent cells do not overlap.
o=prism('Inside-quadrant L node',[(0,0),(34,0),(34,14),(14,14),(14,34),(0,34)],3,material=STEEL)
for c,d in [((18,3.45,5),(24,1.5,4)),((3.45,18,5),(1.5,24,4))]:add(o,box('Locating fence',c,d))
for x,y in [(14.1,6),(6,14.1),(18,10),(26,10),(10,18),(10,26)]:diamond(o,x,y,4.4)
master('CORNER_NODE',o,'Inside L node; two rail ties; spare paired holes for border bridges')
o=box('Rib endpoint anchor',(0,13,1.5),(40,26,3),STEEL);add(o,box('Rail locating fence',(0,3.45,5),(36,1.5,4)))
for x,y in [(-8.1,6),(8.1,6),(0,12),(0,20)]:diamond(o,x,y,4.4)
master('RIB_ANCHOR',o,'Rib endpoint saddle; two rail ties and one rib tie')
o=box('Stepped rib cross',(0,0,1.5),(48,16,3),STEEL);add(o,box('Cross arm',(0,0,1.5),(16,48,3)))
for y in [-13.5,13.5]:add(o,box('Raised vertical-rib seat',(0,y,4.5),(16,21,3)))
for x,y in [(-14,0),(-6,0),(6,0),(14,0),(0,-14),(0,-6),(0,6),(0,14)]:diamond(o,x,y,4.4)
master('RIB_CROSS',o,'Cross node: horizontal ribs on 3 mm seat, vertical ribs on 6 mm seat')
o=box('Permanent cell-to-cell bridge',(0,0,1.5),(60,12,3),STEEL)
for x in [-26,-18,18,26]:diamond(o,x,0,4.4)
master('BORDER_BRIDGE',o,'Fixed bridge between neighboring whole-sheet cells; two ties')
o=box('Field corner receiver',(0,12,1.2),(40,24,2.4),STEEL);add(o,box('Rail locating fence',(0,3.45,4.4),(36,1.5,4)))
for x in [-8.1,8.1]:diamond(o,x,6,4.4)
diamond(o,0,12,7.2)
master('FIELD_RECEIVER',o,'Gate corner socket cap; diamond hole; two rail ties')
# A two-fork bridge prints in the layer plane. Stops, not the flexible beams, seat on the receivers.
o=box('Releasable two-fork bridge',(0,1.5,1.5),(36,3,3))
for cx in [-12,12]:
 for dx in [-4.4,4.4]:add(o,box('Rigid stop',(cx+dx,7,1.5),(1.4,8,3)))
 pts=[(cx-1.7,2.8),(cx+1.7,2.8),(cx+1.7,13.8),(cx+2.7,13.8),(cx+2.7,14.5),(cx+1.7,16.8),(cx-1.7,16.8),(cx-2.7,14.5),(cx-2.7,13.8),(cx-1.7,13.8)]
 add(o,prism('Spring fork',pts,3))
 # Rounded end of split reduces the sharp-root notch.
 boolean(o,box('Fork split',(cx,11.5,1.5),(1.6,12.4,6)))
 boolean(o,prism('Rounded split root',[(cx+.8*math.cos(t*math.tau/32),5.3+.8*math.sin(t*math.tau/32)) for t in range(32)],6,-1))
master('SNAP_BRIDGE',o,'Two reusable fork latches, 24 mm socket pitch; 2.4 mm receiver thickness')
# Rib profiles contain their paper-contact standoffs: no floating keepers or loose spacer buttons.
LONG_P=(PX/2-26)/3;SHORT_P=(PY/2-26)/2
for axis,pitch in [('H',LONG_P),('V',SHORT_P)]:
 for high in [False,True]:
  for dock in ([False,True] if axis=='H' and not high else [False]):
   length=pitch+16;h=17.8 if high else 14.8;width=16 if dock else 12
   o=box('Rib beam',(length/2,0,1.5),(length,width,3))
   add(o,box('Integral paper-contact post',(length/2,0,-h/2),(8,width,h+.05)))
   add(o,box('Paper-contact shoe',(length/2,0,-h+.6),(16,width,1.2)))
   for x in [4,12,length-12,length-4]:diamond(o,x,0,4.4,z0=-1,h=6)
   if dock:
    for x in [length/2-8,length/2+8]:
     for y in [-4.5,4.5]:diamond(o,x,y,4.4,z0=-1,h=6)
   code=f'RIB_{axis}_{"HIGH" if high else "LOW"}'+('_DOCK' if dock else '')
   master(code,o,f'{axis} rib, {length:.3f} mm, {"raised" if high else "lower"} layer, integrated paper support'+('; dock mounting holes' if dock else ''),PRINT_RIB)
# Pipe C saddles share a flat front foot; the 1-inch saddle also contains the dock socket.
for code,inner,outer,footmin,footmax,socket in [('PIPE_33',33.9,42.5,-25,36,True),('PIPE_27',27.2,34.4,-22,22,False)]:
 r=inner/2;ro=outer/2;aa=[math.radians(75+210*i/72) for i in range(73)];profile=[(ro*math.cos(t),ro*math.sin(t)) for t in aa]+[(r*math.cos(t),r*math.sin(t)) for t in reversed(aa)]
 o=extrude_x('Axial-print pipe C saddle',profile,16,-8)
 add(o,box('Flat front foot',(0,(footmin+footmax)/2,-ro-.2),(16,footmax-footmin,2.4)))
 if socket:diamond(o,0,25.8,7.2,z0=-ro-5,h=10)
 master(code,o,f'C saddle for {(33.4 if code=="PIPE_33" else 26.67):.2f} mm target OD; {inner} mm bore; mandatory 250 mm keeper tie',PRINT_AXIAL)
# Same cap thickness and latch geometry as field corners. Rib-side pedestal clears the fork tips.
o=box('Rib dock socket cap',(0,0,1.2),(24,18,2.4),STEEL);diamond(o,0,0,7.2)
for x in [-8,8]:
 for y in [-5.5,5.5]:diamond(o,x,y,4.4)
master('DOCK_CAP',o,'Rib-side docking socket; two ties through matching rib holes')
H=12.35
profile=[(-3.5,0),(3.5,0),(3.5,H),(2,H),(2,2.4),(-2,2.4),(-2,H),(-3.5,H)]
o=extrude_x('Side-print open pedestal',profile,22,-11,STEEL);master('DOCK_PEDESTAL',o,'12.35 mm dock stand-off with open clearance beneath snap fork',PRINT_AXIAL)
# Brace link: planar and reversible; two pipe feet sit on its same face.
o=box('45 degree brace link main pad',(0,0,1.5),(26,74,3),STEEL)
c=box('Brace pad',(0,0,1.5),(26,50,3),STEEL);raw_transform(c,T(90/math.sqrt(2),90/math.sqrt(2),0)@Rz(45));add(o,c)
c=box('Diagonal web',(0,0,1.5),(94,18,3),STEEL);raw_transform(c,T(45/math.sqrt(2),45/math.sqrt(2),0)@Rz(45));add(o,c)
for center,rot in [((0,0),0),((90/math.sqrt(2),90/math.sqrt(2)),45)]:
 for x in [-10,10]:
  for y in [-16,16]:
   p=Rz(rot)@Vector((x/1000,y/1000,0));diamond(o,center[0]+p.x*1000,center[1]+p.y*1000,4.8)
master('BRACE_LINK_45',o,'Flat reversible 90 mm brace-end link; two pipe saddles and four heavy ties')
# Only two universal channels. Collect actual mounting requirements, mirror them,
# and merge close windows instead of exporting a new SKU for every hole pattern.
EDGE_PLANS={};CHANNEL_FEATURES={};REQUIREMENTS=[]
for bay in range(3):
 for side,length,n in [('bottom',PX,5),('right',PY,4),('top',PX,5),('left',PY,4)]:
  pitch=(length-12)/n;body=round(pitch-.2,4);code='CHANNEL_LONG' if n==5 else 'CHANNEL_SHORT'
  f=CHANNEL_FEATURES.setdefault(code,{'length':body,'holes':set(),'grooves':set()})
  extra=[length/2-8.1,length/2+8.1]
  if (bay==0 and side=='bottom') or (bay==2 and side=='right'):
   for a in [64,PY-64]:extra.extend([a-8.1,a+8.1])
  plans=[]
  for i in range(n):
   start=6.1+i*pitch;holes=[8,16,body-16,body-8]
   holes += [a-start for a in extra if .01<a-start<body-.01]
   groove=length/2-start;grooves=[groove] if -1.21<groove<body+1.21 else []
   for x in holes:f['holes'].update([round(x,4),round(body-x,4)])
   for x in grooves:f['grooves'].update([round(x,4),round(body-x,4)])
   REQUIREMENTS.append((code,holes,grooves));plans.append((code,start,body))
  EDGE_PLANS[(bay,side)]=(length,n,pitch,plans)
for code,f in CHANNEL_FEATURES.items():
 intervals=[]
 for x in sorted(f.pop('holes')):
  lo,hi=round(x-3,4),round(x+3,4)
  if intervals and lo-intervals[-1][1]<2-1e-4:intervals[-1][1]=max(hi,intervals[-1][1])
  else:intervals.append([lo,hi])
 f['windows']=intervals;f['grooves']=sorted(f['grooves']);body=f['length']
 assert all(b[0]-a[1]>=2-1e-4 for a,b in zip(intervals,intervals[1:])),(code,intervals)
 assert all(any(abs(body-hi-lo2)<1e-4 and abs(body-lo-hi2)<1e-4 for lo2,hi2 in intervals) for lo,hi in intervals)
 o=extrude_x(code,PROFILE,body)
 for lo,hi in intervals:boolean(o,box('Universal rear-spine window',((lo+hi)/2,1.2,10),(hi-lo,8,5)))
 for x in f['grooves']:boolean(o,prism('Universal cord groove',[(x-1.2,-.1),(x+1.2,-.1),(x,1.2)],15,-.5))
 master(code,o,f'{body:.2f} mm universal slide channel; symmetric mounting windows and cord notches; use on every '+('long' if code=='CHANNEL_LONG' else 'short')+' edge',PRINT_RAIL)
# Every former attachment window remains fully available. Registered end windows
# stay 6 mm wide; enlarged accessory windows do not alter the splice bosses.
for code,holes,grooves in REQUIREMENTS:
 f=CHANNEL_FEATURES[code]
 assert all(any(lo<=x-3+1e-4 and hi>=x+3-1e-4 for lo,hi in f['windows']) for x in holes)
 assert all(any(abs(x-g)<1e-4 for g in f['grooves']) for x in grooves)
 for x in [8,16,f['length']-16,f['length']-8]:assert any(abs(lo-(x-3))<1e-4 and abs(hi-(x+3))<1e-4 for lo,hi in f['windows'])
(OUT/'CHANNEL_FEATURES.json').write_text(json.dumps(CHANNEL_FEATURES,indent=2))
# Parts are now immutable. Instances in the actual full-size assembly drive the BOM.
STANDUP=Matrix(((1,0,0,-S/2000),(0,0,1,0),(0,1,0,0),(0,0,0,1)))
def put(code,M,label='',count=True):
 p=PARTS[code];o=bpy.data.objects.new(code+' / '+label,p['object'].data);COL.objects.link(o);o.matrix_world=STANDUP@M;o['part_code']=code
 if count:COUNTS[code]+=1;PLACEMENTS.append((code,M.copy(),o))
 return o
def tie(kind,n=1):STOCK[kind]+=n
ZFLIP=Matrix.Diagonal((1,1,-1,1))
def edge_matrix(side):
 return {'bottom':Matrix.Identity(4),'right':T(PX,0)@Rz(90),'top':T(PX,PY)@Rz(180),'left':T(0,PY)@Rz(270)}[side]
def snap(M,x,y,socket_rear):
 # Print Y is peg axis; print Z maps to the 3 mm lateral peg thickness.
 P=Matrix(((1,0,0,x/1000),(0,0,1,(y-1.5)/1000),(0,-1,0,(socket_rear+11)/1000),(0,0,0,1)))
 return put('SNAP_BRIDGE',M@P,'field release')
setup('01_FULL_GATE',(-3.5,-7.8,4.2),(.65,0,1.50),6.6);coll('01 / every full-size printed component')
BORDER_M=[]
for k in range(4):
 BM=T(S/2,S/2)@Rz(-90*k)@T(-S/2,L-S/2);BORDER_M.append(BM)
 for bay in range(3):
  BMcell=BM@T(bay*PX,0);before=len(PLACEMENTS)
  # Whole paper insert; no cutting or punched holes.
  ob=box('Whole 22 x 28 posterboard',(0,0,0),(711.2,558.8,.4),PAPER);ob.matrix_world=STANDUP@BMcell@T(PX/2,PY/2,1.4);STOCK['posterboard_22x28']+=1
  for side in ['bottom','right','top','left']:
   E=BMcell@edge_matrix(side);length,n,pitch,plans=EDGE_PLANS[(bay,side)]
   for code,start,body in plans:put(code,E@T(start),side+' channel')
   for i in range(1,n):
    # Native splint plane XY maps to the rail XZ plane; bosses enter the spine holes.
    a=6+i*pitch;M=basis((1,0,0),(0,0,1),(0,-1,0),(a,4.8,10));put('SPLINT',E@M,'channel splice');tie('tie_2p5_standard',2)
   put('RIB_ANCHOR',E@T(length/2,0,17)@ZFLIP,'rib end')
   tie('tie_2p5_releasable' if side=='top' else 'tie_2p5_standard',2)
  for x,y,a in [(0,0,0),(PX,0,90),(PX,PY,180),(0,PY,270)]:
   put('CORNER_NODE',BMcell@T(x,y,17)@Rz(a)@ZFLIP,'whole-sheet corner')
   if y==PY:tie('tie_2p5_standard');tie('tie_2p5_releasable')
   else:tie('tie_2p5_standard',2)
  put('RIB_CROSS',BMcell@T(PX/2,PY/2,14),'rear cross')
  for axis,n,pitch in [('H',3,LONG_P),('V',2,SHORT_P)]:
   for half in [0,1]:
    if axis=='H':base=(16 if half==0 else PX-16,PY/2);angle=0 if half==0 else 180
    else:base=(PX/2,16 if half==0 else PY-16);angle=90 if half==0 else 270
    A=T(*base)@Rz(angle)
    for j in range(n):
     high=bool(j%2);dock=axis=='H' and (bay,half,j) in [(0,1,2),(1,0,0),(1,1,0),(2,0,2)]
     code=f'RIB_{axis}_{"HIGH" if high else "LOW"}'+('_DOCK' if dock else '')
     M=BMcell@A@T(j*pitch-8,0,20 if high else 17);put(code,M,'paper-supported rear rib')
     if dock:
      c=(A@Vector(((j+.5)*pitch/1000,0,0)))*1000;u=bay*PX+c.x
      put('DOCK_PEDESTAL',BM@T(u,PY/2,20),'rib dock stand-off')
      put('DOCK_CAP',BM@T(u,PY/2,32.35),'rib dock socket');tie('tie_2p5_standard',2)
      put('PIPE_33',BM@T(u-24,PY/2-25.8,55),'frame pipe dock');tie('tie_3p6_keeper_250')
      snap(BM,u-12,PY/2,34.75)
    # One tie per intermediate lap, plus one at the endpoint and one at the cross node.
    tie('tie_2p5_standard',n+1)
  # Two front monofilament runs complement the rear contact shoes. No paper holes.
  for pts in [[(3,PY/2,-.6),(PX-3,PY/2,-.6)],[(PX/2,3,-.6),(PX/2,PY-3,-.6)]]:
   pp=[STANDUP@BMcell@Vector(tuple(a/1000 for a in p)) for p in pts];line('Front retention line / 0.8 mm',pp,.0004,DARK)
  STOCK['front_cord_runs']+=2
  if k==0 and bay==0:BAY0=list(PLACEMENTS[before:])
 for a in [PX,2*PX]:
  for y,rot in [(10,0),(PY-10,180)]:put('BORDER_BRIDGE',BM@T(a,y,17)@Rz(rot),'fixed cell seam');tie('tie_2p5_standard',2)
 for bay,side in [(0,'bottom'),(2,'right')]:
  E=BM@T(bay*PX)@edge_matrix(side)
  for a in [64,PY-64]:put('FIELD_RECEIVER',E@T(a,0,16.4)@ZFLIP,'field corner socket');tie('tie_2p5_standard',2)
 for a in [64,PY-64]:snap(BM,L,a,16.4)
# PVC frame and actual brace-end printed assemblies. Pipe geometry is purchased stock.
coll('02 / one PVC frame and four shorter braces')
def pipe(name,a,b,diam):
 tube(name,STANDUP@Vector(tuple(v/1000 for v in a)),STANDUP@Vector(tuple(v/1000 for v in b)),diam/1000,WHITE,3/1000)
c=S/2;h=1050
for y in [c-h,c+h]:pipe('Purchased 1-inch PVC frame',(c-h,y,55),(c+h,y,55),33.4)
for x in [c-h,c+h]:pipe('Purchased 1-inch PVC frame',(x,c-h,55),(x,c+h,55),33.4)
for sx in [-1,1]:
 for sy in [-1,1]:
  corner=Vector((c+sx*h,c+sy*h,0));a=corner+Vector((-sx*400,0,0));b=corner+Vector((0,-sy*400,0));u=(b-a).normalized()
  aa=a+u*70;bb=b-u*70;pipe('Purchased 3/4-inch brace',(aa.x,aa.y,50.95),(bb.x,bb.y,50.95),26.67)
  for origin,direction,horizontal in [(a,u,True),(b,-u,False)]:
   ex=Vector((math.copysign(1,direction.x),0,0)) if horizontal else Vector((0,math.copysign(1,direction.y),0))
   ey=Vector((0,math.copysign(1,direction.y),0)) if horizontal else Vector((math.copysign(1,direction.x),0,0))
   M=basis(ex,ey,(0,0,1),(origin.x,origin.y,0))
   put('BRACE_LINK_45',M@T(0,0,29.35),'brace-end link')
   put('PIPE_33',M@T(0,0,55),'brace main-pipe clamp')
   put('PIPE_27',M@T(90/math.sqrt(2),90/math.sqrt(2),50.95)@Rz(45),'brace tube clamp')
   tie('tie_3p6_brace_150',4);tie('tie_3p6_keeper_250',2)
STOCK['PVC_main_square_sides']=4;STOCK['PVC_upper_elbows']=2;STOCK['PVC_lower_tees']=2;STOCK['PVC_foot_tees']=2;STOCK['PVC_foot_caps']=4;STOCK['PVC_legs']=2;STOCK['PVC_grass_half_feet']=4;STOCK['PVC_hard_surface_half_feet_alternative']=4;STOCK['PVC_brace_tubes_425p685mm']=4
header('01','Full-size parts sized for the A1 Mini','Twelve uncut posterboard sheets. Four rigid borders. Printed snap releases at gate corners and PVC docks; tied workshop joints.')
overlay(f'{S:.1f} mm outside\n{OPEN:.1f} mm opening',.73,.32,.017,True)
overlay('No hinges\nNo oversized printed ribs\nEvery printed part has an STL',.73,.49,.014,color=MUTED)
overlay('Four rigid 2152 x 565 mm borders',.69,.72,.016,True)
footer('Prototype geometry, not a wind-rated kit. Keep the established anchored/ballasted base; ground feet and ballast omitted in this component audit view.')
# Full BOM generated from physical master instances, not presentation counts.
assert COUNTS['SPLINT']==168 and COUNTS['CORNER_NODE']==48 and COUNTS['RIB_ANCHOR']==48
assert sum(v for k,v in COUNTS.items() if k.startswith('CHANNEL'))==216
assert sum(v for k,v in COUNTS.items() if k.startswith('RIB_') and k not in ['RIB_ANCHOR','RIB_CROSS'])==120
assert COUNTS['SNAP_BRIDGE']==24 and COUNTS['PIPE_33']==24 and COUNTS['PIPE_27']==8
# Rear view links the complete actual assembly, including the single PVC backing frame.
full=bpy.data.scenes['01_FULL_GATE']
setup('06_REAR_FRAME',(3.5,7.8,4.2),(-.40,0,1.50),6.3);coll('01 / complete rear assembly view')
for ob in full.objects:
 if ob.type in ['MESH','CURVE'] and ob.name!='Ground' and not any(c.name.startswith(('90 /','91 /')) for c in ob.users_collection):COL.objects.link(ob)
header('06','One backing frame, four diagonal braces','Sixteen removable docks attach the four rigid borders. Every brace has a printed link and two pipe saddles at each end.')
footer('Purchased pipe is shown at its target centerline. Add elbows and the retained anchored or ballasted base; tube cut lengths depend on fitting take-up.')
# Catalogue pages show the exact STL meshes in their supplied print orientations.
ordered=sorted(PARTS,key=lambda x:(not x.startswith('CHANNEL'),not x.startswith('RIB_'),x))
for page in range(math.ceil(len(ordered)/8)):
 setup(f'{page+2:02d}_PRINT_PARTS_{page+1}',(.15,-.55,1.5),(.36,.17,0),1.14,False);coll('01 / actual print-oriented solids')
 for j,code in enumerate(ordered[page*8:(page+1)*8]):
  p=PARTS[code];x=(j%4)*.23;y=(j//4)*.25
  ob=bpy.data.objects.new(code,p['print_mesh']);COL.objects.link(ob);ob.location=(x,y,.001)
  label=text('Part label',f'{code}\nQty {COUNTS[code]} | '+ ' x '.join(f'{a:g}' for a in p['print_bounds_mm'])+' mm',(x,y-.018,.001),.010,INK,rot=(0,0,0),bold=True)
 header(str(page+2).zfill(2),f'Printable components / {page+1}','Actual STL orientations. All dimensions in mm. Quantity is per full-size gate; purchased pipes and ties are separate.')
 footer('Support-free intent: flat extrusions, upright channels and 45-degree diamond openings. Slice checks and a physical fit print come before production.')
# Show the two standard channel masters together at a useful inspection scale.
setup('05_TWO_CHANNELS',(.07,-.20,.25),(.07,.025,.01),.245,False);coll('01 / two channel lengths only')
for code,y in [('CHANNEL_LONG',.06),('CHANNEL_SHORT',0)]:
 p=PARTS[code];ob=bpy.data.objects.new('Universal / '+code,p['print_mesh']);COL.objects.link(ob);ob.location=(0,y,0)
 text('Universal channel label',f'{code} | {COUNTS[code]} per gate | {p["print_bounds_mm"][0]:g} mm',(0,y-.014,.001),.005,INK,rot=(0,0,0),bold=True)
header('05','Two channel types','One long and one short. Common symmetric mounting windows and cord notches replace nine position-specific variants.')
footer('Five long pieces per long edge; four short pieces per short edge. All sheets, corner positions, splice bosses and gate dimensions stay the same.')
# Detailed rail joint, exact masters, exploded for inspection.
setup('07_CHANNEL_JOINT',(.15,-.32,.21),(.141,0,.025),.40,False);coll('01 / registered rail joint')
basecode=next(k for k in PARTS if k.startswith('CHANNEL'))
for shift in [0,PARTS[basecode]['object'].dimensions.x*1000+.2]:
 ob=bpy.data.objects.new('Detail / channel',PARTS[basecode]['object'].data);COL.objects.link(ob);ob.location=(shift/1000,0,0)
# Detail uses native XYZ; the splint is separated in Y to expose four hollow registration bosses.
length=PARTS[basecode]['object'].dimensions.x*1000
ob=bpy.data.objects.new('Detail / splint',PARTS['SPLINT']['object'].data);COL.objects.link(ob);ob.matrix_world=basis((1,0,0),(0,0,1),(0,-1,0),(length+.1,22,10))
header('07','Registered splice, two retaining ties','Four hollow bosses locate the two channel ends. The ties pass through those bosses; the solid shoulders carry sliding loads.')
footer('The 0.2 mm joint gap is intentional. These permanent workshop joints stay assembled when the four borders are transported.')
setup('08_SNAP_RELEASE',(.08,-.16,.19),(.015,0,.018),.22,False);coll('01 / reusable field snap geometry')
for cx in [-12,12]:
 ob=bpy.data.objects.new('Detail / socket',PARTS['DOCK_CAP']['object'].data);COL.objects.link(ob);ob.matrix_world=T(cx,0,0)
ob=bpy.data.objects.new('Detail / released bridge',PARTS['SNAP_BRIDGE']['object'].data);COL.objects.link(ob);ob.matrix_world=basis((1,0,0),(0,0,-1),(0,1,0),(0,-1.5,25))
header('08','One snap bridge for corners and docks','Two independent fork latches. Pinch and release one end, lift it slightly, then release the other. Print the bridge flat in PETG.')
footer('A 7.2 mm diamond socket clears the 3.4 x 3 mm shaft; wider hooks retain a 2.4 mm socket plate. Validate force and repeated release with the fit kit.')
# Assembly detail views use exact native meshes, with explicitly illustrative tie routing.
def detail(code,M,label=''):
 ob=bpy.data.objects.new('Detail / '+code+' / '+label,PARTS[code]['object'].data);COL.objects.link(ob);ob.matrix_world=M;return ob
setup('09_REAR_BAY',(.95,.95,.85),(.36,.28,.025),1.50,False);coll('01 / one complete sheet rear exoskeleton')
inv=BORDER_M[0].inverted()
for code,M,ob in BAY0:detail(code,inv@M)
ob=box('Whole sheet / detail',(PX/2,PY/2,1.4),(711.2,558.8,.4),PAPER)
header('09','One whole sheet, supported from both sides','Segmented rear ribs use alternating lap layers and integrated paper-contact shoes. The stepped central node separates the crossing ribs.')
footer('120 short rib pieces per gate replace the unprintable long ribs. Lightly tensioned front cord crosses each sheet; keep all twelve sheets uncut.')
setup('10_DOCK_AND_BRACE',(.24,-.40,.36),(.07,.01,.028),.38,False);coll('01 / exact dock assembly')
for code,M in [('RIB_H_LOW_DOCK',T(-LONG_P/2-8,0,17)),('DOCK_PEDESTAL',T(0,0,20)),('DOCK_CAP',T(0,0,32.35)),('PIPE_33',T(-24,-25.8,55))]:detail(code,M)
P=basis((1,0,0),(0,0,-1),(0,1,0),(-12,-1.5,45.75));detail('SNAP_BRIDGE',P)
tube('Frame pipe / dock detail',(-.060,-.0258,.055),(.055,-.0258,.055),.0334,WHITE,.003)
# Second detail: one brace endpoint; both C saddles are tied onto the same flat printed link.
B=T(110,15)
for code,M in [('BRACE_LINK_45',T(0,0,29.35)),('PIPE_33',T(0,0,55)),('PIPE_27',T(90/math.sqrt(2),90/math.sqrt(2),50.95)@Rz(45))]:detail(code,B@M)
for cx in [-8,8]:
 pts=[(cx/1000,-.0055,.0355),(cx/1000,-.0055,.018),(cx/1000,.0055,.018),(cx/1000,.0055,.0355)]
 line('Illustrative dock cap tie',pts,.0006,DARK,True)
header('10','PVC docks and printed brace-end links','Left: snap bridge couples a rib pedestal to the frame saddle. Right: two tied C saddles connect a diagonal brace to the same backing frame.')
footer('Every C saddle needs a keeper tie around pipe and saddle. The brace link uses four additional heavy ties. No cross-lashed pipe-to-pipe joint remains.')
# Machine-readable BOM, plus lightweight unit-aware 3MF for each unique part.
def write_3mf(code):
 ns='http://schemas.microsoft.com/3dmanufacturing/core/2015/02';ET.register_namespace('',ns);root=ET.Element('{'+ns+'}model',unit='millimeter');res=ET.SubElement(root,'resources');ob=ET.SubElement(res,'object',id='1',type='model',name=code);me=ET.SubElement(ob,'mesh');vs=ET.SubElement(me,'vertices');ts=ET.SubElement(me,'triangles');pm=PARTS[code]['print_mesh'];pm.calc_loop_triangles()
 for v in pm.vertices:ET.SubElement(vs,'vertex',x=str(v.co.x*1000+5),y=str(v.co.y*1000+5),z=str(v.co.z*1000))
 for tr in pm.loop_triangles:ET.SubElement(ts,'triangle',v1=str(tr.vertices[0]),v2=str(tr.vertices[1]),v3=str(tr.vertices[2]))
 build=ET.SubElement(root,'build');ET.SubElement(build,'item',objectid='1')
 with zipfile.ZipFile(OUT/'printable'/f'{code}.3mf','w',zipfile.ZIP_DEFLATED) as z:
  z.writestr('[Content_Types].xml','<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/></Types>')
  z.writestr('_rels/.rels','<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Target="/3D/3dmodel.model" Id="rel0" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/></Relationships>')
  z.writestr('3D/3dmodel.model',ET.tostring(root,encoding='utf-8',xml_declaration=True))
rows=[]
for code,p in PARTS.items():
 write_3mf(code);rows.append(dict(code=code,quantity=COUNTS[code],**{k:v for k,v in p.items() if k not in ['object','print_mesh']}))
(OUT/'CHANNEL_ASSEMBLY_MAP.json').write_text(json.dumps({f'bay_{bay+1}_{side}':{'edge_length_mm':v[0],'segments':[{'code':code,'start_mm':start,'length_mm':length} for code,start,length in v[3]]} for (bay,side),v in EDGE_PLANS.items()},indent=2))
report={'gate_mm':{'outside':S,'opening':OPEN,'border':[L,PY],'paper':[711.2,558.8]},'unique_printed_parts':len(rows),'printed_piece_count':sum(COUNTS.values()),'parts':rows,'purchased_quantities':dict(STOCK),'front_cord_purchase_m':20,'geometry_only':True,'physical_validation':'Required: paper slot, splice registration, snap cycle, pipe retention, one complete bay and anchored outdoor test.'}
(OUT/'BOM.json').write_text(json.dumps(report,indent=2))
import csv
with (OUT/'BOM.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=['code','quantity','description','print_bounds_mm','solid_volume_mm3','file'],extrasaction='ignore');w.writeheader();w.writerows(rows)
start=bpy.data.texts.new('START_HERE.txt');start.write('FULL-SIZE A1 MINI ITERATION\nEvery printed component in scene 01 references an exported STL master.\nRead BUILD_AND_PRINT_GUIDE.md and BOM.csv. This is a fabrication prototype, not a physically validated product.\nWorkshop ties are deliberately retained to reduce separate printed latch parts. Field corners and PVC docks use the common SNAP_BRIDGE.\n')
if (OUT/'BUILD_AND_PRINT_GUIDE.md').exists():t=bpy.data.texts.new('BUILD_AND_PRINT_GUIDE.md');t.write((OUT/'BUILD_AND_PRINT_GUIDE.md').read_text())
for name in ['01_ASSEMBLED','00_MASTERS']:
 s=bpy.data.scenes.get(name)
 if s:bpy.data.scenes.remove(s)
bpy.context.window.scene=bpy.data.scenes['01_FULL_GATE']
for screen in bpy.data.screens:
 for a in screen.areas:
  if a.type=='VIEW_3D':a.spaces.active.region_3d.view_perspective='CAMERA';a.spaces.active.shading.type='MATERIAL'
bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'A1_Full_Size_Gate.blend'))
for name in os.environ.get('RENDER_SCENES',','.join(s.name for s in bpy.data.scenes)).split(','):
 if name:
  s=bpy.data.scenes[name];bpy.context.window.scene=s;s.render.filepath=str(OUT/'renders'/f'{name}.png');bpy.ops.render.render(write_still=True,scene=name)
print('BUILD COMPLETE',len(rows),'types',sum(COUNTS.values()),'printed pieces',dict(STOCK))

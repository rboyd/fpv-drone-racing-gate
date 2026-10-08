"""One-piece 84.8 mm end-stop cap and marking tongue; existing 33.5 mm bore."""
from pathlib import Path
exec(Path(__file__).with_name('build_a1_full_size.py').read_text().split('# Registered channel splice:')[0],globals())
import ast
from mathutils.bvhtree import BVHTree
OUT=ROOT/'output/short_pipe_gauge'
for folder in ['printable','renders']:(OUT/folder).mkdir(parents=True,exist_ok=True)
for node in ast.parse(Path(__file__).with_name('build_paper_roll_study.py').read_text()).body:
 if isinstance(node,ast.FunctionDef) and node.name=='export3mf':exec(compile(ast.Module(body=[node],type_ignores=[]),'<export>','exec'),globals())
PARTS={};LENGTH=84.8;BORE=33.5;OD=33.4;AXIS=24.;WALL=4.;BACK=3.;GRIP=16.;HALF_WIDTH=12.;TRAY_R=16.95
r=BORE/2+WALL
outer=[(-r,0),(r,0),(r,AXIS),(r/2**.5,AXIS+r/2**.5),(0,AXIS+r*2**.5),(-r/2**.5,AXIS+r/2**.5),(-r,AXIS)]
inner=[(BORE/2*math.cos(math.radians(135+270*i/72)),AXIS+BORE/2*math.sin(math.radians(135+270*i/72))) for i in range(73)]+[(0,AXIS+BORE/2*2**.5)]
o=extrude_x('Stop cap',outer,GRIP+BACK,-BACK,STEEL)
boolean(o,extrude_x('Accepted 33.5 mm bore; stop at X=0',inner,GRIP+1,0,STEEL))
# A solid, concave tongue stays close to the pipe without clamping it along its length.
ys=[HALF_WIDTH-2*HALF_WIDTH*i/64 for i in range(65)]
profile=[(-HALF_WIDTH,0),(HALF_WIDTH,0)]+[(y,AXIS-math.sqrt(TRAY_R**2-y*y)) for y in ys]
add(o,extrude_x('Rigid concave measuring tongue',profile,LENGTH,0,STEEL))
# Engraved seven-segment 84.8 identification: simple recessed strokes print cleanly.
segments={'a':(0,8,2.3,.5),'b':(1.5,6.75,.5,1.9),'c':(1.5,4.25,.5,1.9),'d':(0,3,2.3,.5),'e':(-1.5,4.25,.5,1.9),'f':(-1.5,6.75,.5,1.9),'g':(0,5.5,2.3,.5)}
for x,digit in [(31,'8'),(36,'4'),(43,'8')]:
 for seg in ('abcdefg' if digit=='8' else 'bcfg'):
  dx,z,w,h=segments[seg];boolean(o,box('Engraved '+digit+' / '+seg,(x+dx,-11.9,z),(w,1.2,h),STEEL))
boolean(o,box('Decimal point',(39.5,-11.9,3),(.65,1.2,.65),STEEL))
code='END_CAP_GAUGE_84_8';master(code,o,'Single stop cap and concave marking tongue. Pipe-end stop X=0; far marking edge X=84.8 mm. Accepted 33.5 mm bore, 16 mm grip, 3 mm closed back. Mark only, then remove before cutting.')
export3mf('ONE_'+code,[(code,5,5)])
# Measure the actual CAD faces, not just input parameters.
bm=bmesh.new();bm.from_mesh(o.data);tree=BVHTree.FromBMesh(bm);bm.free()
hit=tree.ray_cast(Vector((.010,0,AXIS/1000)),Vector((-1,0,0)))
assert hit[0] is not None and abs(hit[0].x)<1e-7,hit
xmax=max(v.co.x for v in o.data.vertices)*1000;xmin=min(v.co.x for v in o.data.vertices)*1000
assert abs(xmax-LENGTH)<1e-4 and abs(xmin+BACK)<1e-4
assert abs((xmax-hit[0].x*1000)-84.8)<1e-4
# At the pipe-end contact annulus, the datum remains flat all around.
for k in range(24):
 a=k*math.tau/24;start=Vector((.010,.015*math.cos(a),(AXIS+15*math.sin(a))/1000));p=tree.ray_cast(start,Vector((-1,0,0)))[0]
 assert p is not None and abs(p.x)<1e-7,(k,p)
# Connectivity and bed footprint; the STL uses the same unchanged print orientation.
adj={v.index:set() for v in o.data.vertices}
for e in o.data.edges:
 a,b=e.vertices;adj[a].add(b);adj[b].add(a)
seen=set();todo=[0]
while todo:
 i=todo.pop()
 if i in seen:continue
 seen.add(i);todo.extend(adj[i]-seen)
assert len(seen)==len(adj)
report={'part':code,'nominal_mark_distance_mm':84.8,'measured_mesh_stop_to_edge_mm':xmax-hit[0].x*1000,'PVC_bore_mm':33.5,'PVC_OD_mm':33.4,'cap_grip_mm':16,'back_thickness_mm':3,'overall_length_mm':xmax-xmin,'tongue_width_mm':24,'tongue_min_thickness_mm':AXIS-TRAY_R,'tongue_nominal_radial_clearance_mm':TRAY_R-OD/2,'print_bounds_mm':PARTS[code]['print_bounds_mm'],'solid_volume_mm3':PARTS[code]['solid_volume_mm3'],'nonmanifold_edges':PARTS[code]['nonmanifold_edges'],'connected_components':1,'stop_face_annulus_samples':24,'stop_face_samples_pass':True,'print_orientation':'Flat tongue and cap foot on bed; same horizontal peaked bore as accepted sleeve','use':'Mark, remove jig, cut; not a blade guide','calibration':'Nominal CAD dimension only. Measure first print and trial cut before batch work.'}
(OUT/'geometry_checks.json').write_text(json.dumps(report,indent=2))

def show_jig():
 ob=bpy.data.objects.new('84.8 mm end cap gauge',o.data);COL.objects.link(ob);return ob
MARK=mat('Orange marking line',(.95,.3,.03),emit=True)
def dim(a,b,label,z=-.010):
 line('84.8 mm dimension',[(a,-.027,z),(b,-.027,z)],.00035,INK)
 for x in [a,b]:line('Dimension witness',[(x,-.027,z-.002),(x,-.027,z+.002)],.00035,INK)
 text('Dimension label',label,((a+b)/2,-.028,z-.006),.004,INK,align='CENTER')
setup('01_PRINTABLE_GAUGE',(.19,-.27,.15),(.039,0,.018),.205,False);coll('01 / one-piece printed gauge');show_jig()
header('01','84.8 mm / cap-and-tab cut marker','One PETG part. Seat the pipe against the internal stop; the far end of the tongue is the marking datum.')
footer('Accepted 33.5 mm bore. Flat foot on the A1 Mini bed. Nominal dimension: verify the printed jig before making all 16 short pipes.')
setup('02_SEATED_ON_PIPE',(.11,-.34,.14),(.047,0,.017),.225,False);coll('01 / cap and rigid tab');show_jig()
coll('02 / PVC seated at internal zero stop');tube('PVC end at X=0',(.000,0,.024),(.127,0,.024),.0334,WHITE,.00338)
pts=[(.0848,.01685*math.cos(a*math.tau/128),.024+.01685*math.sin(a*math.tau/128)) for a in range(128)]
line('Illustrative pencil line at 84.8 mm',pts,.00035,MARK,True)
coll('03 / dimensions');dim(0,.0848,'84.8 mm: pipe end to mark')
header('02','Seat / mark / remove / cut','Rotate the seated cap to extend the mark around the pipe if needed. Remove the jig before using the ratcheting cutter.')
footer('Orange ring illustrates the intended cut mark; it is not another printed part. Keep the finished piece on the cap side of the line.')
setup('03_STOP_SECTION',(.15,-.29,.10),(.037,0,.019),.205,False);coll('01 / cutaway for explanation only')
q=show_jig();q.data=q.data.copy();boolean(q,box('Cutaway negative Y',(.04*1000,-50,40),(200,100,130),STEEL))
p=tube('Half PVC / square end seated',(.000,0,.024),(.108,0,.024),.0334,WHITE,.00338)
boolean(p,box('Cutaway pipe negative Y',(40,-50,40),(200,100,130),STEEL))
line('Zero datum',[(0,-.001,0),(0,-.001,.048)],.0004,MARK)
coll('03 / dimension');dim(0,.0848,'Internal stop to far edge = 84.8 mm')
header('03','The inside stop is zero','The 3 mm back is behind the pipe end. Overall printed length is 87.8 mm; useful measuring length is 84.8 mm.')
footer('Cutaway view only. Print the complete cap. A square, deburred pipe end must contact the stop; cap-mouth insertion is 16 mm.')
for name in ['00_MASTERS','01_ASSEMBLED']:
 if bpy.data.scenes.get(name):bpy.data.scenes.remove(bpy.data.scenes[name])
bpy.context.window.scene=bpy.data.scenes['02_SEATED_ON_PIPE'];bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'Short_Pipe_Gauge.blend'),compress=True)
if '--no-render' not in sys.argv:
 for sc in bpy.data.scenes:
  bpy.context.window.scene=sc;sc.render.filepath=str(OUT/'renders'/f'{sc.name}.png');bpy.ops.render.render(write_still=True,scene=sc.name)
print('PASS',json.dumps(report))

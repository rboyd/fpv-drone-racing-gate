"""Six compact layouts using unchanged production meshes and the imported MK4 reference."""
from pathlib import Path
exec(Path(__file__).with_name('build_a1_full_size.py').read_text().split('# Registered channel splice:')[0],globals())
from mathutils.bvhtree import BVHTree
import numpy as np
OUT=ROOT/'output/compact_gate_study';(OUT/'renders').mkdir(parents=True,exist_ok=True)
D=json.loads((OUT/'layouts.json').read_text());G=D['gates'];PROD=ROOT/'output/corner_guide_elbow'
with bpy.data.libraries.load(str(PROD/'Corner_Guide_Elbow.blend')) as (src,dst):dst.scenes=['11_ALL_PRODUCTION_PARTS']
lib=dst.scenes[0];meshes={c:next(o.data for o in lib.objects if o.type=='MESH' and o.name.startswith(c)) for c in ['ELBOW','DUAL_GUY_ELBOW','TEE','CROSS','MAG_SLEEVE']};bpy.data.scenes.remove(lib)
# Only sleeve color changes for identification. Geometry and print files are identical.
meshes['MAG_SLEEVE']=meshes['MAG_SLEEVE'].copy();meshes['MAG_SLEEVE'].materials.clear();meshes['MAG_SLEEVE'].materials.append(ORANGE)
with bpy.data.libraries.load(str(ROOT/'output/drone_clearance_study/Drone_Clearance_Study.blend')) as (src,dst):dst.scenes=['01_CURRENT_GATE_PASS']
ref=dst.scenes[0];bpy.context.window.scene=ref;ref.frame_set(40);bpy.context.view_layer.update()
drone=[(o.name,o.data,o.matrix_world.copy()) for o in ref.objects if o.name.startswith(('Drone /','Swept prop disc /'))]
assert len(drone)>100;bpy.data.scenes.remove(ref)
PAPER_COMPACT=mat('Compact / orange paper',(.98,.29,.045));MAG=mat('Compact / magnets',(.4,.44,.47),.75)

def show_drone(center):
 coll('20 / MK4 imported reference, battery assumed')
 for name,data,m in drone:
  o=bpy.data.objects.new(name,data);COL.objects.link(o);o.matrix_world=Matrix.Translation(center)@m

def render_gate(g,center=(0,0,0),paper=True):
 S=g['outer_mm'];M=basis((1,0,0),(0,0,1),(0,1,0),(center[0]*1000-S/2,center[1]*1000,center[2]*1000-S/2))
 coll('10 / '+g['id']+' / exact printed fittings')
 for code,xy,r in g['placements']:
  o=bpy.data.objects.new(code,meshes[code]);COL.objects.link(o);o.matrix_world=M@T(*xy,0)@Rz(r)
 coll('11 / PVC cut to stop planes')
 for e in g['edges']:
  a=Vector((*g['nodes'][e['a']]['xy'],24));z=Vector((*g['nodes'][e['b']]['xy'],24));u=(z-a).normalized()
  tube(e['name'],M@((a+35*u)/1000),M@((z-35*u)/1000),.0334,WHITE,.00338)
 coll('12 / paper and actual 6 mm magnets')
 if paper:
  for i,(x,y,w,h) in enumerate(g['paper_rectangles']):
   o=box('Paper / '+str(i+1),(x+w/2,y+h/2,-.2 if i<2 else -.5),(w,h,.2),PAPER_COMPACT);raw_transform(o,M)
 for x,y in g['magnets']:tube('Front 6 mm magnet',M@Vector((x/1000,y/1000,-.0028)),M@Vector((x/1000,y/1000,-.0008)),.006,MAG)
 return M

# Validate the actual fitting meshes at every candidate position, including 12-inch corners.
checks={}
for g in G:
 trees=[];bounds=[];unexpected=0
 for code,xy,r in g['placements']:
  M=T(*xy,0)@Rz(r);vs=[M@v.co for v in meshes[code].vertices];lo=Vector([min(v[j] for v in vs) for j in range(3)]);hi=Vector([max(v[j] for v in vs) for j in range(3)])
  trees.append(BVHTree.FromPolygons(vs,[list(p.vertices) for p in meshes[code].polygons]));bounds.append((lo,hi))
  for v,local in zip(vs,meshes[code].vertices):
   covered=any(x-.02<=v.x*1000<=x+w+.02 and y-.02<=v.y*1000<=y+h+.02 for x,y,w,h in g['paper_rectangles'])
   if not covered and not(code=='DUAL_GUY_ELBOW' and local.co.x<-.04 and local.co.y<-.04):unexpected+=1
 hits=[]
 for i,(lo,hi) in enumerate(bounds):
  for j in range(i):
   a,b=bounds[j]
   if all(min(hi[k],b[k])-max(lo[k],a[k])>0 for k in range(3)) and trees[i].overlap(trees[j]):hits.append((i,j))
 assert not hits,(g['id'],hits)
 assert unexpected==0,(g['id'],unexpected)
 # Every populated magnet remains on a paper rectangle.
 assert all(any(x<=mx<=x+w and y<=my<=y+h for x,y,w,h in g['paper_rectangles']) for mx,my in g['magnets'])
 checks[g['id']]={'intersecting_printed_part_pairs':hits,'unexpected_vertices_outside_paper':unexpected,'magnets_on_paper':True,'maximum_edge_gap_mm':g['maximum_magnet_gap_mm'],'short_pipe_exposed_between_socket_mouths_mm':round(g['short_cut_mm']-60,3)}
(OUT/'geometry_checks.json').write_text(json.dumps(checks,indent=2))

setup('01_SIX_PAPER_LAYOUTS',(0,-9,0),(0,0,0),8.5,False);SC.render.resolution_x=3000;SC.render.resolution_y=2300
for i,g in enumerate(G):
 row,col=divmod(i,3);center=(-2.65+col*2.65,0,.95-row*2.65);render_gate(g,center);show_drone(center)
 x=.061+col*.313;y=.556 if row==0 else .966
 overlay(f'{g["opening_mm"]} mm / {g["band_inches"]}-inch paper',x,y,.018,True)
 overlay(f'{g["outer_mm"]:.1f} mm outside / {g["counts"]["MAG_SLEEVE"]} sleeves',x,y+.025,.012)
header('01','Smaller openings. Narrower paper. Fewer sleeves.','All six gates and drones use the same scale. 1000 mm openings above; 800 mm below. Bands: 24 / 18 / 12 inches.')
# Two clear views of the underlying orthogonal frames, no paper occlusion.
for opening,scene in [(1000,'02_FRAME_1000'),(800,'03_FRAME_800')]:
 setup(scene,(0,-8,0),(0,0,0),8.3,False);SC.render.resolution_x=3000;SC.render.resolution_y=1500
 for col,g in enumerate([q for q in G if q['opening_mm']==opening]):
  render_gate(g,(-2.65+col*2.65,0,-.15),False);x=.061+col*.313
  overlay(f'{g["band_inches"]}-inch paper / {g["printed_pieces"]} printed parts',x,.845,.018,True)
  overlay(f'{g["counts"]["MAG_SLEEVE"]} orange sleeves / {g["PVC_sticks"]} PVC sticks',x,.894,.014)
 header(scene[:2],f'{opening} mm opening / frame with paper removed','Blue: 16 unchanged structural fittings. Orange: reduced sleeve count. White: 1-inch PVC, accepted 33.5 mm sockets.')
 footer('350 mm maximum magnet-gap trial. No internal cords, diagonals or additional fittings. Footings and external guys omitted.')
setup('04_TWELVE_INCH_GATE_PAIR',(0,-7,0),(0,0,0),4.4,False);SC.render.resolution_x=2400;SC.render.resolution_y=1800
for g,cx in [(G[2],-1.05),(G[5],1.05)]:
 render_gate(g,(cx,0,-.1));show_drone((cx,0,-.1));x=.065 if cx<0 else .555
 overlay(f'{g["opening_mm"]} mm opening / {g["outer_mm"]:.1f} mm outside',x,.85,.018,True)
 overlay(f'16 sleeves + 16 fittings / {g["PVC_sticks"]} PVC sticks',x,.898,.016)
header('04','12-inch paper / the leanest compatible pair','Same drone scale. 1000 mm opening: 299 mm centered side gap. 800 mm opening: 199 mm side gap.')
footer('Dendy / Printables 1515387 (CC BY-NC 4.0). Battery assumed. Cyan rings show propeller sweep, not physical guards.')
setup('05_NARROW_CORNER_DETAIL',(.52,-1.0,.57),(0,0,0),.82,False)
g=dict(G[2]);corner_nodes={'N00','N10','N01','N11'}
g['placements']=[p for p in g['placements'] if p[1][0]<305 and p[1][1]<305]
g['edges']=[e for e in g['edges'] if e['a'] in corner_nodes and e['b'] in corner_nodes]
g['magnets']=[p for p in g['magnets'] if p[0]<305 and p[1]<305]
center=(g['outer_mm']/2000-.16,0,g['outer_mm']/2000-.16);render_gate(g,center,False)
header('05','12-inch corner / no short-pipe sleeves','Four existing fittings are joined by 84.8 mm pipe cuts. 30 mm insertion per end leaves 24.8 mm of exposed pipe.')
footer('No new part geometry. Fitting-mounted magnets cover short edges and paper overlap seams; long rails still use sleeves.')
# Clip this close-up to its lower-left corner; avoid the rest of the full gate in the camera view.
SC.camera.data.clip_end=2.0
for name in ['00_MASTERS','01_ASSEMBLED']:
 if bpy.data.scenes.get(name):bpy.data.scenes.remove(bpy.data.scenes[name])
bpy.context.window.scene=bpy.data.scenes['04_TWELVE_INCH_GATE_PAIR'];bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'Compact_Gate_Study.blend'),compress=True)
if '--no-render' not in sys.argv:
 for sc in bpy.data.scenes:
  selected=os.environ.get('RENDER_SCENES','')
  if selected and sc.name not in selected.split(','):continue
  bpy.context.window.scene=sc;sc.render.filepath=str(OUT/'renders'/f'{sc.name}.png');bpy.ops.render.render(write_still=True,scene=sc.name)
print('PASS: six exact layouts, no fitting collisions; paper coverage and magnet positions validated.')

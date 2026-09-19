"""Three-magnet dual-guy elbow with recessed paper corner alignment guides."""
from pathlib import Path
exec(Path(__file__).with_name('build_a1_full_size.py').read_text().split('# Registered channel splice:')[0],globals())
import ast,csv
OUT=ROOT/'output/corner_guide_elbow'
for d in ['printable','renders']:(OUT/d).mkdir(parents=True,exist_ok=True)
PARTS={}
COSTS=json.loads((ROOT/'docs/material_costs.json').read_text())
for node in ast.parse(Path(__file__).with_name('build_paper_roll_study.py').read_text()).body:
 if isinstance(node,ast.FunctionDef) and node.name in ['cyl','window','roundplate','export3mf']:exec(compile(ast.Module(body=[node],type_ignores=[]),'<helpers>','exec'),globals())
PAPER_ORANGE=mat('Orange roll paper',(.96,.255,.028));MAGNET=mat('6 x 2 mm magnets',(.43,.47,.50),.82)
S=2700.;W=609.6;A=75.;B=W-A;C=S-B;D=S-A;H2=2*S-W;AXIS=24.;STOP=35.;MOUTH=65.;OFFSET=A-18
BORE=33.5;WALL=4.;OD=33.4 # User accepted sleeve fit, 2026-09-18.
assert 33.1<=BORE<=34.3

def tear(r):return [(r*math.cos(math.radians(135+270*i/72)),r*math.sin(math.radians(135+270*i/72))) for i in range(73)]+[(0,r*2**.5)]
def axprof(name,prof,length,start,angle=0):
 o=extrude_x(name,prof,length,start,STEEL);raw_transform(o,Rz(angle));return o

def shell(length,start,bore=BORE):
 r=bore/2+WALL
 return axprof('Flat-foot peaked socket',[(-r,0),(r,0),(r,AXIS),(r/2**.5,AXIS+r/2**.5),(0,AXIS+r*2**.5),(-r/2**.5,AXIS+r/2**.5),(-r,AXIS)],length,start)
def boretool(length,start,diam=BORE):return axprof('Trial friction bore',[(y,z+AXIS) for y,z in tear(diam/2)],length,start)
def pocket(o,xy):window(o,xy,3.15,.4)
def magnet_arm(o,x,y):
 # A broad diagonal root supports a small 3 mm face pad; no full square backing plate.
 a=math.degrees(math.atan2(y,x));r=math.hypot(x,y)
 q=box('Magnet arm front flange',(r/2,0,1.5),(r+12,20,3),STEEL);raw_transform(q,Rz(a));add(o,q)
 q=prism('Magnet pad',[(x-9,y-9),(x+9,y-9),(x+9,y+9),(x-9,y+9)],3,material=STEEL);add(o,q)
 q=extrude_x('Tapered magnet arm rib',[(-6,2.8),(6,2.8),(6,8),(-6,8)],max(1,r-23),0,STEEL);raw_transform(q,Rz(a));add(o,q)
 # The final 23 mm is a continuous 3 mm flange; only the local magnet window thins to .4.
 pocket(o,(x,y))


PRODUCTION=['ELBOW','DUAL_GUY_ELBOW','TEE','CROSS','MAG_SLEEVE']
PORTS={'ELBOW':[0,90],'DUAL_GUY_ELBOW':[0,90],'TEE':[0,90,180],'CROSS':[0,90,180,270]}
MAGS={'ELBOW':[(-OFFSET,-OFFSET)],'DUAL_GUY_ELBOW':[(-OFFSET,15),(15,-OFFSET),(-OFFSET,-OFFSET)],'TEE':[(-OFFSET,-OFFSET),(OFFSET,-OFFSET)],'CROSS':[(sx*OFFSET,sy*OFFSET) for sx in [-1,1] for sy in [-1,1]],'MAG_SLEEVE':[(0,OFFSET)]}
EYE_CENTER=(-84.,-84.);EYE_SPACING=18.;EYE_RADIUS=5.25;EAR_RADIUS=13.25;EAR_THICKNESS=14.
EYES=[(-84-9/2**.5,-84+9/2**.5),(-84+9/2**.5,-84-9/2**.5)]
for code,angles in PORTS.items():
 o=box('Wide fitting core',(0,0,6),(44,44,12),STEEL)
 for ang in angles:
  add(o,axprof('Continuous socket root',[(-16,0),(16,0),(16,12),(-16,12)],STOP,0,ang))
  q=shell(MOUTH-STOP+5,STOP-5);raw_transform(q,Rz(ang));add(o,q)
 for x,y in MAGS[code]:
  if code=='DUAL_GUY_ELBOW' and (x,y)==(-OFFSET,-OFFSET):continue # pocket is cut into the existing diagonal load arm below
  magnet_arm(o,x,y)
 if code=='DUAL_GUY_ELBOW':
  # Flat diagonal ear with two front/back through-eyes. Broad base plus sloped root rib.
  reach=math.hypot(*EYE_CENTER)
  ear=box('Continuous 32 x 14 mm diagonal load arm',(reach/2,0,7),(reach+8,32,14),STEEL);raw_transform(ear,Rz(225));add(o,ear)
  pts=[(9+EAR_RADIUS*math.cos(math.radians(a)),EAR_RADIUS*math.sin(math.radians(a))) for a in [-90+180*i/48 for i in range(49)]]
  pts += [(-9+EAR_RADIUS*math.cos(math.radians(a)),EAR_RADIUS*math.sin(math.radians(a))) for a in [90+180*i/48 for i in range(49)]]
  head=prism('One continuous rounded twin-eye head',pts,14,material=STEEL);raw_transform(head,T(*EYE_CENTER,0)@Rz(-45));add(o,head)
  rib=extrude_x('Sloped diagonal root rib',[(0,12),(0,28),(90,14),(90,12)],24,-12,STEEL);raw_transform(rib,Rz(135));add(o,rib)
  # One watertight loft per hole includes both chamfers, avoiding tangent Boolean cuts.
  for x,y in EYES:
   n=96;rings=[(-1,6.05),(0,6.05),(.8,5.25),(13.2,5.25),(14,6.05),(15,6.05)]
   vs=[(x+r*math.cos(t*math.tau/n),y+r*math.sin(t*math.tau/n),z) for z,r in rings for t in range(n)]
   fs=[tuple(reversed(range(n))),tuple(range((len(rings)-1)*n,len(rings)*n))]
   fs += [(j*n+i,j*n+(i+1)%n,(j+1)*n+(i+1)%n,(j+1)*n+i) for j in range(len(rings)-1) for i in range(n)]
   boolean(o,mesh('10.5 mm through-eye with 0.8 mm chamfer',vs,fs,STEEL))
  # Third magnet uses the existing broad diagonal arm, without a new projecting pad.
  # A 6.3 mm seat retains the 0.4 mm paper-side skin; 10 mm rear access well
  # makes it possible to push the 6 x 2 mm magnet down into its deep seat.
  window(o,(-OFFSET,-OFFSET),3.15,.4,40)
  window(o,(-OFFSET,-OFFSET),5.,2.6,40)
  # Recessed L on paper-facing Z=0; align edges to its centerlines.
  # Lines stop inside the solid arm, clear of magnet skins and guy eyes.
  boolean(o,box('Paper X edge / 0.8 wide x 0.4 deep',(-75,-64,.1),(.8,22.8,.6),STEEL))
  boolean(o,box('Paper Y edge / 0.8 wide x 0.4 deep',(-64,-75,.1),(22.8,.8,.6),STEEL))
 for ang in angles:
  q=boretool(MOUTH-STOP+1,STOP);raw_transform(q,Rz(ang));boolean(o,q)
 desc={'ELBOW':'Two-port elbow for bottom outside corners','DUAL_GUY_ELBOW':'Top elbow with reinforced diagonal ear, two independent 10.5 mm front/back through-eyes and top/side/corner magnetic seats and recessed paper alignment L','TEE':'Three-way tee, native ports +X, +Y, -X; two magnetic pads on missing-port side','CROSS':'Four-way cross for the inner grid intersections'}[code]
 master(code,o,desc+'; accepted 33.5 mm PVC bore; 30 mm engagement and 35 mm center-to-stop')
# One plain friction sleeve supplies intermediate magnets, including the straight seam crossbars.
o=shell(16,-8);boolean(o,boretool(18,-9))
add(o,box('Sleeve front arm',(0,OFFSET/2,1.5),(20,OFFSET+18,3),STEEL))
add(o,extrude_x('Sleeve arm root gusset',[(16,2.8),(16,9),(OFFSET-12,3)],12,-6,STEEL));pocket(o,(0,OFFSET))
master('MAG_SLEEVE',o,f'Universal friction sleeve with {OFFSET:.1f} mm offset magnetic face; no cleat, pin or cord eye; 16 mm pipe engagement')

# Fully orthogonal lattice: the same short/long pipe cuts serve every level.
def gate(levels):
 H=S+(levels-1)*(S-W);xs=[A,B,C,D];ys=[A]
 for j in range(levels):ys += [j*(S-W)+B,j*(S-W)+C]
 ys += [H-A]
 nodes={};placements=[];edges=[];magset=set()
 def putmag(x,y):magset.add((round(x,4),round(y,4)))
 for j,y in enumerate(ys):
  for i,x in enumerate(xs):
   name=f'N{i}{j}';outsidecorner=i in [0,3] and j in [0,len(ys)-1]
   angle=0 if (i,j)==(0,0) else 90 if (i,j)==(3,0) else 180 if (i,j)==(3,len(ys)-1) else 270 if (i,j)==(0,len(ys)-1) else 0
   if outsidecorner:code='DUAL_GUY_ELBOW' if j==len(ys)-1 else 'ELBOW'
   elif i in [0,3] or j in [0,len(ys)-1]:
    code='TEE';angle=0 if j==0 else 180 if j==len(ys)-1 else 270 if i==0 else 90
   else:code='CROSS';angle=0
   nodes[name]={'xy':(x,y),'code':code,'angle':angle};placements.append((code,(x,y),angle))
   if outsidecorner:
    rr=math.radians(angle)
    for mx,my in MAGS[code]:putmag(x+mx*math.cos(rr)-my*math.sin(rr),y+mx*math.sin(rr)+my*math.cos(rr))
   elif j in [0,len(ys)-1]:
    for sx in [-1,1]:putmag(x+sx*OFFSET,18 if j==0 else H-18)
   elif i in [0,3]:
    for sy in [-1,1]:putmag(18 if i==0 else S-18,y+sy*OFFSET)
   else:
    # Opening-side corner: lower boundary faces upward, upper boundary downward.
    putmag(x+(OFFSET if i==1 else -OFFSET),y+(OFFSET if j%2==1 else -OFFSET))
 def connect(a,bb,side):
  aa=Vector((*nodes[a]['xy'],0));zz=Vector((*nodes[bb]['xy'],0));u=(zz-aa).normalized();dist=(zz-aa).length;cut=dist-2*STOP;start=aa+STOP*u;end=zz-STOP*u;angle=math.degrees(math.atan2(u.y,u.x))+(0 if side==1 else 180)
  name=a+'_'+bb;clips=4 if dist>1000 else 1;positions=[]
  for k in range(1,clips+1):
   p=aa+(zz-aa)*(k/(clips+1));placements.append(('MAG_SLEEVE',tuple(p[:2]),angle));v=Rz(angle)@Vector((0,OFFSET/1000,0));putmag(p.x+v.x*1000,p.y+v.y*1000);positions.append(round((p-start).length,3))
  edges.append({'name':name,'a':a,'b':bb,'length_mm':round(cut,3),'start':list(start[:2]),'end':list(end[:2]),'sleeves_from_cut_start_mm':positions,'sleeve_angle':angle})
 for j,y in enumerate(ys):
  side=-1 if j==0 else 1 if j==len(ys)-1 else (1 if j%2 else -1)
  for i in range(3):connect(f'N{i}{j}',f'N{i+1}{j}',side)
 for i,x in enumerate(xs):
  side=1 if i in [0,2] else -1
  for j in range(len(ys)-1):connect(f'N{i}{j}',f'N{i}{j+1}',side)
 paper=[(0,j*(S-W),S,W) for j in range(levels+1)]
 for j in range(levels):
  for x in [0,S-W]:paper.append((x,j*(S-W)+W-36,W,S-2*W+72))
 return {'levels':levels,'height_mm':H,'x_grid_mm':xs,'y_grid_mm':ys,'nodes':nodes,'edges':edges,'placements':placements,'magnets':sorted(magset),'paper_rectangles':paper,'counts':dict(collections.Counter(p[0] for p in placements)),'retention':'Friction only, as requested; 33.5 mm sleeve physically accepted; socket engagement and frame load tests pending','internal_cords':0,'guy_eyes':4,'guy_lines':4,'diagonal_PVC':0}
GATES={'single':gate(1),'split_s':gate(2)}
def nesting(edges):
 bins=[]
 for e in sorted(edges,key=lambda e:-e['length_mm']):
  need=e['length_mm']+3;options=[(p['remaining_mm']-need,i) for i,p in enumerate(bins) if p['remaining_mm']>=need]
  if options:i=min(options)[1]
  else:i=len(bins);bins.append({'stock':i+1,'remaining_mm':3038.,'cuts':[]})
  bins[i]['cuts'].append({'name':e['name'],'length_mm':e['length_mm']});bins[i]['remaining_mm']-=need
 return bins
for g in GATES.values():
 g['stock_plan']=nesting(g['edges']);g['PVC_sticks']=len(g['stock_plan']);g['PVC_cost_usd']=round(COSTS['pvc_10ft_stick_usd']*g['PVC_sticks'],2);g['PVC_total_m']=sum(e['length_mm'] for e in g['edges'])/1000;g['magnet_pairs']=len(g['magnets']);g['printed_pieces']=sum(g['counts'].values())

PLATES={}
for c in PRODUCTION:
 PLATES['ONE_'+c]=[(c,5,5)];export3mf('ONE_'+c,PLATES['ONE_'+c])
w,h,_=PARTS['MAG_SLEEVE']['print_bounds_mm'];nx=int(173//(w+3));ny=int(173//(h+3))
PLATES['BATCH_MAG_SLEEVE']=[('MAG_SLEEVE',5+i*(w+3),5+j*(h+3)) for j in range(ny) for i in range(nx)]
export3mf('BATCH_MAG_SLEEVE',PLATES['BATCH_MAG_SLEEVE'])
for g in GATES.values():
 g['print_queue']={}
 for c,n in g['counts'].items():
  recipe='BATCH_MAG_SLEEVE' if c=='MAG_SLEEVE' else 'ONE_'+c;cap=len(PLATES[recipe]);full,tail=divmod(n,cap)
  if full:g['print_queue'][recipe]=full
  if tail:
   name='TAIL_'+c+'_'+str(tail)
   if name not in PLATES:PLATES[name]=PLATES[recipe][:tail];export3mf(name,PLATES[name])
   g['print_queue'][name]=1
rows=[{'code':c,**{k:v for k,v in p.items() if k not in ['object','print_mesh']}} for c,p in PARTS.items()]
BOM={'outside_width_mm':S,'paper_band_width_mm':W,'opening_mm':S-2*W,'PVC_bore_mm':BORE,'sleeve_fit_status':'User confirmed perfect fit on purchased PVC, 2026-09-18','pipe_OD_mm':OD,'pipe_axis_behind_paper_mm':AXIS,'pipe_inset_mm':A,'socket_engagement_mm':30,'socket_stop_mm':STOP,'magnet_offset_mm':OFFSET,'parts':rows,'gates':GATES,'plates':PLATES,'production_types':5,'production_codes':PRODUCTION,'magnet_pockets_local_mm':MAGS,'ports_local_degrees':PORTS,'no_internal_cords':True,'no_diagonal_PVC':True,'source_price_PVC_10ft_USD':COSTS['pvc_10ft_stick_usd'],'guy_eye':{'count_per_elbow':2,'hole_nominal_diameter_mm':10.5,'eye_centers_local_mm':EYES,'eye_spacing_mm':18,'ear_thickness_mm':14,'mouth_chamfer_mm':.8,'minimum_outer_ligament_at_mouth_mm':7.2,'minimum_outer_ligament_mm':8,'inter_eye_ligament_mm':7.5,'root_rib_height_mm':28,'magnet_centers_local_mm':MAGS['DUAL_GUY_ELBOW'],'magnet_edge_inset_mm':18,'edge_magnets_from_corner_mm':90,'corner_magnet_inset_mm':[18,18],'corner_access_well_diameter_mm':10,'corner_seat_diameter_mm':6.3,'corner_seat_floor_mm':.4,'alignment':{'paper_corner_local_mm':[-75,-75],'groove_width_mm':.8,'groove_depth_mm':.4,'arm_length_mm':22,'reference':'groove centerlines'},'load_rating':None},'baseline_commit':'6a7fb47','baseline_folder':'tee_pvc_gate'}
(OUT/'BOM.json').write_text(json.dumps(BOM,indent=2))
def covered(x,y,g):return any(xx-.01<=x<=xx+w+.01 and yy-.01<=y<=yy+h+.01 for xx,yy,w,h in g['paper_rectangles'])
CHECKS={}
for kind,g in GATES.items():
 bad=[];exposed=[];hole_checks=[]
 for c,xy,r in g['placements']:
  M=T(*xy,0)@Rz(r)
  for v in PARTS[c]['object'].data.vertices:
   p=M@v.co
   if not covered(p.x*1000,p.y*1000,g):
    # The exposed diagonal ear is intentional. No socket or magnetic pad may protrude.
    if c=='DUAL_GUY_ELBOW' and v.co.x*1000 < -40 and v.co.y*1000 < -40:
     exposed.append([c,xy,list(p)])
    else:bad.append([c,xy,list(p)])
  if c=='DUAL_GUY_ELBOW':
   for ex,ey in EYES:
    p=M@Vector((ex/1000,ey/1000,0));x,y=p.x*1000,p.y*1000
    clear=(x+6.05<0 or x-6.05>S or y-6.05>g['height_mm'] or y+6.05<0)
    hole_checks.append({'center_xy_mm':[x,y],'entire_hole_outside_paper_outline':clear})
 CHECKS[kind]={'unexpected_printed_vertices_outside_paper':bad,'exposed_diagonal_ear_vertex_count':len(exposed),'magnet_centers_outside_paper':[(x,y) for x,y in g['magnets'] if not covered(x,y,g)],'eye_clearance':hole_checks,'only_orthogonal_PVC':all(abs(e['start'][0]-e['end'][0])<.001 or abs(e['start'][1]-e['end'][1])<.001 for e in g['edges'])}
(OUT/'geometry_checks.json').write_text(json.dumps(CHECKS,indent=2))
# Native part instance helpers. Front view paper on X/Z plane, depth along +Y.
FRONT=basis((1,0,0),(0,0,1),(0,1,0),(-1350,0,50))
def instance(c,xy=(0,0),angle=0,M=Matrix.Identity(4)):
 o=bpy.data.objects.new(c,PARTS[c]['object'].data);COL.objects.link(o);o.matrix_world=M@T(*xy,0)@Rz(angle);return o

def render_gate(g,paper=True):
 coll('01 / actual five production meshes')
 for c,xy,r in g['placements']:instance(c,xy,r,FRONT)
 coll('02 / only horizontal and vertical 1 inch PVC')
 for e in g['edges']:
  aa=FRONT@Vector((e['start'][0]/1000,e['start'][1]/1000,AXIS/1000));bb=FRONT@Vector((e['end'][0]/1000,e['end'][1]/1000,AXIS/1000));tube(e['name'],aa,bb,OD/1000,WHITE,.00338)
 coll('03 / paper and edge magnets')
 if paper:
  for i,(x,y,w,h) in enumerate(g['paper_rectangles']):
   o=box('Paper '+str(i+1),(x+w/2,y+h/2,-.18-i*.01),(w,h,.18),PAPER_ORANGE);raw_transform(o,FRONT)
 for x,y in g['magnets']:
  o=cyl('Front magnet',(x,y,-2.5),3,2,MAGNET,n=32);raw_transform(o,FRONT)


FRONT_LINE=mat('Front guy / orange',(.95,.23,.025));REAR_LINE=mat('Rear guy / teal',(.025,.52,.47))
# Two independent illustrative eye loops; knot details are not simulated.
LOOPS=[];TAILS=[]
for idx,(x,y) in enumerate(EYES):
 dx,dy=(-1,1) if idx==0 else (1,-1)
 loop=[(x,y,17),(x,y,-3),(x+8*dx,y+8*dy,-8),(x+16*dx,y+16*dy,-3),(x+16*dx,y+16*dy,17),(x+7*dx,y+7*dy,21),(x,y,17)]
 start=loop[2] if idx==0 else loop[5]
 tail=[start,(-150+idx*15,-150-idx*15,-145 if idx==0 else 160)]
 LOOPS.append(loop);TAILS.append(tail)
# Coordinate conversion with translation must happen after mm-to-m conversion.
def rope_mm(path,M,material,label):
 for j,(a,z) in enumerate(zip(path,path[1:])):tube(label+' '+str(j),M@(Vector(a)/1000),M@(Vector(z)/1000),.003,material)
def ropes(M=Matrix.Identity(4),tails=True):
 for i in range(2):
  material=FRONT_LINE if i==0 else REAR_LINE
  rope_mm(LOOPS[i],M,material,'Front loop' if i==0 else 'Rear loop')
  if tails:rope_mm(TAILS[i],M,material,'Front tail' if i==0 else 'Rear tail')
def corner(paper=False,cords=True):
 coll('01 / actual printable dual guy elbow');instance('DUAL_GUY_ELBOW')
 coll('02 / 1 inch PVC')
 tube('PVC X',(.035,0,.024),(.13,0,.024),.0334,WHITE,.00338);tube('PVC Y',(0,.035,.024),(0,.13,.024),.0334,WHITE,.00338)
 if paper:
  coll('03 / paper corner and magnets');box('Paper corner / no cutout',(27.5,27.5,-.2),(205,205,.2),PAPER_ORANGE)
  for x,y in MAGS['DUAL_GUY_ELBOW']:cyl('Bare front magnet',(x,y,-2.3),3,2,MAGNET,n=32);cyl('Rear magnet',(x,y,.4),3,2,MAGNET,n=32)
 if cords:coll('04 / independent front and rear loops');ropes()
# Validate the sample routing against the real printed mesh, not just its bounding box.
from mathutils.bvhtree import BVHTree
bm=bmesh.new();bm.from_mesh(PARTS['DUAL_GUY_ELBOW']['object'].data);tree=BVHTree.FromBMesh(bm);bm.free()
guide_checks=[]
for x,y,z_expected in [(-75,-75,.4),(-75,-65,.4),(-65,-75,.4),(-73,-65,0),(-65,-73,0),(-57,-57,0)]:
 hit=tree.ray_cast(Vector((x/1000,y/1000,-.01)),Vector((0,0,1)))
 assert hit[0] is not None and abs(hit[0].z*1000-z_expected)<.002,('Bad paper guide depth',x,y,hit[0])
 guide_checks.append({'xy_mm':[x,y],'face_z_mm':round(hit[0].z*1000,4)})
for x,y,z_expected in [(-57,-57,.4),(-53,-57,2.6)]:
 hit=tree.ray_cast(Vector((x/1000,y/1000,.06)),Vector((0,0,-1)))
 assert hit[0] is not None and abs(hit[0].z*1000-z_expected)<.002,('Bad magnet seat floor',x,y,hit[0])
 guide_checks.append({'xy_mm':[x,y],'rear_seat_z_mm':round(hit[0].z*1000,4)})
CHECKS['paper_guide_and_magnet_seat_probes']=guide_checks
minimum=1000.;samples=0
for path in LOOPS+TAILS:
 for a,z in zip(path,path[1:]):
  aa,zz=Vector(a)/1000,Vector(z)/1000;n=max(2,math.ceil((zz-aa).length*1000/.5))
  for i in range(n+1):
   point=aa+(zz-aa)*i/n;hit=tree.find_nearest(point);minimum=min(minimum,hit[3]*1000);samples+=1
   assert hit[3]*1000>=1.49,('3 mm cord intersects printed elbow',list(point),hit[3]*1000)
# Paper spans the +X/+Y quadrant from (-75,-75); crossing the plane must occur beyond it.
for path in LOOPS+TAILS:
 for a,z in zip(path,path[1:]):
  for i in range(101):
   q=Vector(a)+(Vector(z)-Vector(a))*i/100
   if -.3-1.5<=q.z<=-.1+1.5:assert q.x+1.5 < -75 or q.y+1.5 < -75,('Cord intersects paper',list(q))
CHECKS['local_cord_routing']={'samples':samples,'cord_diameter_mm':3,'minimum_centerline_distance_to_mesh_mm':round(minimum,3),'no_mesh_or_paper_intersection':True,'knots_not_simulated':True}
(OUT/'geometry_checks.json').write_text(json.dumps(CHECKS,indent=2))
setup('01_DUAL_GUY_PART',(.26,-.36,.32),(-.02,-.02,.025),.50,False);coll('01 / printable master');instance('DUAL_GUY_ELBOW')
header('01','Two independent guys / one diagonal ear','Two 10.5 mm through-eyes in a 14 mm-thick ear. The load arm is 32 mm wide with a sloped root rib.')
footer('Three magnets: top edge, side edge and corner. Recessed L marks the paper corner. PVC bore stays 33.5 mm, with the same 30 mm engagement.')
setup('02_FRONT_AND_REAR',(.27,-.38,.25),(-.035,-.035,.02),.69,False);corner(paper=False)
header('02','Orange to the front / teal to the rear','Separate eyes keep the two lines independently attachable. Both have 0.8 mm entry chamfers.')
footer('Loops illustrate threading only; use tested knots or suitable soft loops. No eye load or wind rating is assigned.')
setup('03_PAPER_FRONT',(.20,-.24,-.35),(-.03,-.03,.005),.64,False);corner(paper=True)
header('03','Front guy access without puncturing paper','The diagonal ear projects beyond the paper corner. Corner magnet sits 18 mm inside both edges; top/side pads remain 90 mm along each edge.')
footer('Only the small tie-down ear is exposed beyond the paper. The accepted PVC interfaces and all cut lengths remain unchanged.')
setup('04_PAPER_REAR',(.28,-.32,.36),(-.02,-.02,.025),.66,False);corner(paper=True)
header('04','Both lines can stay installed together','The two eye loops clear the printed elbow and paper in the sampled 3 mm cord routing shown here.')
footer('This is a routing check, not a strength test. Apply opposing lines without pulling the friction sockets off their seating marks.')
setup('05_SINGLE_FRONT',(0,-6,1.67),(0,0,1.67),5.9,False);render_gate(GATES['single'])
header('05','Single gate / magnetic paper face','2700 mm square, 1480.8 mm opening, 609.6 mm bands. Magnet total is now 76 pairs / 152 individual magnets.')
footer('Blender assembly render. Five printed part types and 64 pieces; PVC structure concealed behind the paper face.')
setup('06_STACKED_REAR',(4,7,4.8),(0,0,2.80),10.2,False);render_gate(GATES['split_s'],False)
header('06','The same top corners extend to Split-S','2700 x 4790.4 mm paper outline. Two dual-guy elbows, 120 magnet pairs, and unchanged pipe and fitting quantities.')
footer('The complete top row moves upward. Guy lengths, ground anchors and base sizing remain installation-specific.')
setup('07_A1_MINI_PLATE',(.30,-.30,.37),(.09,.09,.024),.40,False);coll('01 / real print orientation')
box('180 mm A1 Mini bed',(90,90,-1),(180,180,2),GROUND)
for c,x,y in PLATES['ONE_DUAL_GUY_ELBOW']:
 o=bpy.data.objects.new(c,PARTS[c]['print_mesh']);COL.objects.link(o);o.location=(x/1000,y/1000,0)
header('07','One support-free PETG print','Flat paper face and ear on the bed. Vertical tie-down holes need no roofs; PVC sockets retain their peaked roofs.')
footer('Print one, test both PVC sockets and both guy loops, then repeat for the second top corner.')
setup('08_TOP_CORNER_ROUTING',(-1.70,-.8,3.05),(-1.32,.01,2.72),.72,False);coll('01 / installed upper left corner')
g=GATES['single'];xy=(75,2625);rot=270;M=FRONT@T(*xy,0)@Rz(rot)
instance('DUAL_GUY_ELBOW',xy,rot,FRONT)
for aa,zz in [((35,0,24),(180,0,24)),((0,35,24),(0,180,24))]:tube('Corner PVC',M@(Vector(aa)/1000),M@(Vector(zz)/1000),.0334,WHITE,.00338)
p=box('Upper-left paper corner',(-18,-18,-.2),(114,114,.2),PAPER_ORANGE);raw_transform(p,M)
for x,y in MAGS['DUAL_GUY_ELBOW']:
 p=cyl('Front magnet',(x,y,-2.3),3,2,MAGNET,n=32);raw_transform(p,M)
for i in range(2):
 material=FRONT_LINE if i==0 else REAR_LINE;rope_mm(LOOPS[i],M,material,'Eye loop')
 start=M@(Vector(TAILS[i][0])/1000);end=start+Vector((-.13,-.13 if i==0 else .13,-.16));tube('Front guy' if i==0 else 'Rear guy',start,end,.003,material)
header('08','Installed corner / front and rear support','One eye for each guy at each top corner. Both lines leave the face without a paper hole or conflict with a magnet.')
footer('Orange = toward the front. Teal = toward the rear. Ground endpoints are not shown or specified in this close-up.')
# Face-up view exposes the physical relief, with exact corner and edge references.
setup('09_PAPER_GUIDES',(-.02,-.02001,-.42),(-.02,-.02,0),.46,False)
coll('90 / paper-face lighting');bpy.ops.object.light_add(type='AREA',location=(-.15,-.1,-.3));lamp=link(bpy.context.object);lamp.data.energy=.65;lamp.data.shape='DISK';lamp.data.size=.3;lamp.rotation_euler=(Vector((-.04,-.04,0))-lamp.location).to_track_quat('-Z','Y').to_euler()
coll('01 / actual recessed paper-facing surface');view=instance('DUAL_GUY_ELBOW');view.data=view.data.copy()
# Presentation only: optional contrasting marker on actual groove floors.
view.data.materials.append(PAPER_ORANGE);marker_index=len(view.data.materials)-1
for face in view.data.polygons:
 vs=[view.data.vertices[i].co*1000 for i in face.vertices]
 if all(abs(v.z-.4)<.002 for v in vs) and all(-75.41<=v.x<=-52.59 and -75.41<=v.y<=-52.59 for v in vs):face.material_index=marker_index
header('09','Paper corner / recessed alignment L','Align both paper edges to the centers of the 0.8 mm-wide grooves. Their intersection is the exact corner.')
footer('Orange illustrates optional marker in the 0.4 mm-deep grooves. One PETG part; no raised ridge or multicolor print required.')
setup('10_CORNER_MAGNET_SEAT',(.12,-.24,.29),(-.054,-.054,.006),.30,False)
coll('01 / actual three-magnet elbow');instance('DUAL_GUY_ELBOW')
coll('02 / exploded corner magnet');cyl('6 x 2 mm corner magnet shown lifted',(-57,-57,28),3,2,MAGNET,n=64)
header('10','Corner magnet / rear access well','Push one 6 x 2 mm magnet down the 10 mm access well into the 6.3 mm seat; paper-side skin stays 0.4 mm.')
footer('The corner seat is cut into the existing 32 mm-wide arm. Both separate guy eyes and 33.5 mm PVC bores remain.')
# All five production meshes, shown at one scale in a labeled parts overview.
setup('11_ALL_PRODUCTION_PARTS',(0,0,1),(0,0,0),.94,False)
SC.render.resolution_x=2400;SC.render.resolution_y=1600
header('11','Five printed parts / current gate design','Actual production geometry at one scale. All PVC bores: 33.5 mm. Counts below: single gate / stacked Split-S.')
view_rotation=Matrix.Rotation(math.radians(35),4,'X')@Rz(-35)
for code,label,detail,cx,cy,ly in [
 ('ELBOW','BOTTOM ELBOW','2 / 2 pieces   |   one magnet seat',.18,.35,.53),
 ('DUAL_GUY_ELBOW','TOP GUY ELBOW','2 / 2 pieces   |   three magnet seats + two guy eyes',.50,.35,.53),
 ('TEE','THREE-WAY TEE','8 / 12 pieces   |   two magnet seats',.82,.35,.53),
 ('CROSS','FOUR-WAY CROSS','4 / 8 pieces   |   four magnet seats',.34,.74,.885),
 ('MAG_SLEEVE','MAGNETIC SLEEVE','48 / 80 pieces   |   one magnet seat',.66,.74,.885)]:
 coll('01 / '+label);o=instance(code)
 vv=[view_rotation@v.co for v in o.data.vertices]
 center=Vector([(max(v[j] for v in vv)+min(v[j] for v in vv))/2 for j in range(3)])
 pos=Vector(((cx-.5)*.94,(.5-cy)*.94*1600/2400,0))
 o.matrix_world=Matrix.Translation(pos-center)@view_rotation
 coll('91 / part labels');overlay(label,cx-.125,ly,.018,True);overlay(detail,cx-.125,ly+.031,.010)
footer('Five required types: 64 pieces single / 104 stacked. Top elbow includes the new corner magnet and recessed paper guides on its underside.')
setup('12_SPLIT_S_FRONT',(0,-8,2.8),(0,0,2.8),10.2,False);render_gate(GATES['split_s'],True)
header('12','Split-S / two stacked openings','2700 x 4790.4 mm paper face. Shared 609.6 mm middle band; two 1480.8 mm square openings.')
footer('Blender assembly render. Ground anchors and feet are not shown. 104 printed pieces, 120 magnet pairs and fourteen 10-ft PVC sticks.')
for name in ['01_ASSEMBLED','00_MASTERS']:
 if bpy.data.scenes.get(name):bpy.data.scenes.remove(bpy.data.scenes[name])
bpy.context.window.scene=bpy.data.scenes['11_ALL_PRODUCTION_PARTS'];bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'Corner_Guide_Elbow.blend'))
if '--no-render' not in sys.argv:
 for sc in bpy.data.scenes:
  selected=os.environ.get('RENDER_SCENES','')
  if selected and sc.name not in selected.split(','):continue
  bpy.context.window.scene=sc;sc.render.filepath=str(OUT/'renders'/f'{sc.name}.png');bpy.ops.render.render(write_still=True,scene=sc.name)
print('DUAL GUY BUILD',json.dumps({k:{'counts':g['counts'],'magnet_pairs':g['magnet_pairs']} for k,g in GATES.items()}),flush=True)
print('CORD ROUTING',CHECKS['local_cord_routing'],flush=True)

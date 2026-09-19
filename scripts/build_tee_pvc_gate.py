"""Cord-free orthogonal PVC gate: one elbow, one cross, one magnetic sleeve."""
from pathlib import Path
exec(Path(__file__).with_name('build_a1_full_size.py').read_text().split('# Registered channel splice:')[0],globals())
import ast,csv
OUT=ROOT/'output/tee_pvc_gate'
for d in ['printable','renders']:(OUT/d).mkdir(parents=True,exist_ok=True)
PARTS={}
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


PRODUCTION=['ELBOW','GUY_ELBOW','TEE','CROSS','MAG_SLEEVE']
PORTS={'ELBOW':[0,90],'GUY_ELBOW':[0,90],'TEE':[0,90,180],'CROSS':[0,90,180,270]}
MAGS={'ELBOW':[(-OFFSET,-OFFSET)],'GUY_ELBOW':[(-OFFSET,-OFFSET)],'TEE':[(-OFFSET,-OFFSET),(OFFSET,-OFFSET)],'CROSS':[(sx*OFFSET,sy*OFFSET) for sx in [-1,1] for sy in [-1,1]],'MAG_SLEEVE':[(0,OFFSET)]}
for code,angles in PORTS.items():
 o=box('Wide fitting core',(0,0,6),(44,44,12),STEEL)
 for ang in angles:
  add(o,axprof('Continuous socket root',[(-16,0),(16,0),(16,12),(-16,12)],STOP,0,ang))
  q=shell(MOUTH-STOP+5,STOP-5);raw_transform(q,Rz(ang));add(o,q)
 for x,y in MAGS[code]:magnet_arm(o,x,y)
 if code=='GUY_ELBOW':
  # A rear eye rising directly from the central core. Its 45-degree hole roof needs no support.
  profile=[(-18,8),(18,8),(18,30)]+[(18*math.cos(math.radians(t)),30+18*math.sin(math.radians(t))) for t in range(5,181,5)]
  eye=extrude_x('Integral guy eye / 14 mm thick',profile,14,-7,STEEL)
  hole=extrude_x('10.5 mm guy passage',[(y,z+31) for y,z in tear(5.25)],16,-8,STEEL);boolean(eye,hole)
  raw_transform(eye,Rz(45));add(o,eye)
 for ang in angles:
  q=boretool(MOUTH-STOP+1,STOP);raw_transform(q,Rz(ang));boolean(o,q)
 desc={'ELBOW':'Two-port elbow for bottom outside corners','GUY_ELBOW':'Top elbow with integral 10.5 mm peaked guy passage in 14 mm-thick rear eye; eye connects to central core','TEE':'Three-way tee, native ports +X, +Y, -X; two magnetic pads on missing-port side','CROSS':'Four-way cross for the inner grid intersections'}[code]
 master(code,o,desc+'; accepted 33.5 mm PVC bore; 30 mm engagement and 35 mm center-to-stop')
# One plain friction sleeve supplies intermediate magnets, including the straight seam crossbars.
o=shell(16,-8);boolean(o,boretool(18,-9))
add(o,box('Sleeve front arm',(0,OFFSET/2,1.5),(20,OFFSET+18,3),STEEL))
add(o,extrude_x('Sleeve arm root gusset',[(16,2.8),(16,9),(OFFSET-12,3)],12,-6,STEEL));pocket(o,(0,OFFSET))
master('MAG_SLEEVE',o,f'Universal friction sleeve with {OFFSET:.1f} mm offset magnetic face; no cleat, pin or cord eye; 16 mm pipe engagement')

# Two compact heads create a long story-pole jig on an uncut PVC reference rail.
# Both pipe axes are 24 mm above the table, 70 mm apart. All round bores remain 33.5.
JIG_SPACING=70.
for code in ['JIG_ZERO','JIG_MARK']:
 start=-16 if code=='JIG_ZERO' else 0
 o=shell(32,start)
 def tool_bore(length,x0):
  if code=='JIG_MARK':return axprof('Round marking-tool bore',[(BORE/2*math.cos(t*math.tau/96),AXIS+BORE/2*math.sin(t*math.tau/96)) for t in range(96)],length,x0)
  return boretool(length,x0)
 boolean(o,tool_bore(34,start-1))
 add(o,box('Flat linking foot',(start+16,35,2.5),(32,111.5,5),STEEL))
 if code=='JIG_ZERO':
  q=shell(28,0);raw_transform(q,T(0,JIG_SPACING,0))
  cut=boretool(30,-1);raw_transform(cut,T(0,JIG_SPACING,0));boolean(q,cut)
  boolean(q,box('Open loading saddle',(14,JIG_SPACING,65),(40,70,82),STEEL));add(o,q)
  add(o,box('End datum / right face is ZERO',(-3,JIG_SPACING,24),(6,41.5,48),STEEL))
  desc='Reference rail friction sleeve plus open work saddle and end stop. Workpiece end contacts X=0. All PVC bores 33.5 mm.'
 else:
  q=shell(12,0);raw_transform(q,T(0,JIG_SPACING,0));cut=tool_bore(14,-1);raw_transform(cut,T(0,JIG_SPACING,0));boolean(q,cut);add(o,q)
  desc='Reference rail sleeve plus closed 12 mm marking collar. Mark along X=0 end face. Slide workpiece through while holding head against its rail witness mark.'
 # Shallow transverse witness grooves on the connecting bridge identify the actual datum plane.
 if code=='JIG_ZERO':boolean(o,box('Zero witness groove',(0,36,4.75),(.8,22,1),STEEL))
 else:
  # Three notches are behind the marker datum, useful for distinguishing heads after printing.
  for x in [4,8,12]:boolean(o,box('Marker ID groove',(x,36,4.75),(.8,16,1),STEEL))
 master(code,o,desc+' Use as a measuring/marking jig only; remove stock for cutting.',PRINT_AXIAL if code=='JIG_MARK' else Matrix.Identity(4))
# Dedicated 30 mm insertion-depth marker, also tests the longer accepted bore.
o=shell(34,0);boolean(o,boretool(31,4));master('DEPTH_30',o,'Blind 33.5 mm gauge: pipe end at X=4; marking face X=34, exactly 30 mm engagement. Optional workshop tool.')
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
   if outsidecorner:code='GUY_ELBOW' if j==len(ys)-1 else 'ELBOW'
   elif i in [0,3] or j in [0,len(ys)-1]:
    code='TEE';angle=0 if j==0 else 180 if j==len(ys)-1 else 270 if i==0 else 90
   else:code='CROSS';angle=0
   nodes[name]={'xy':(x,y),'code':code,'angle':angle};placements.append((code,(x,y),angle))
   if outsidecorner:putmag(18 if i==0 else S-18,18 if j==0 else H-18)
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
 return {'levels':levels,'height_mm':H,'x_grid_mm':xs,'y_grid_mm':ys,'nodes':nodes,'edges':edges,'placements':placements,'magnets':sorted(magset),'paper_rectangles':paper,'counts':dict(collections.Counter(p[0] for p in placements)),'retention':'Friction only, as requested; 33.5 mm sleeve physically accepted; socket engagement and frame load tests pending','internal_cords':0,'guy_eyes':2,'diagonal_PVC':0}
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
 g['stock_plan']=nesting(g['edges']);g['PVC_sticks']=len(g['stock_plan']);g['PVC_cost_usd']=6*g['PVC_sticks'];g['PVC_total_m']=sum(e['length_mm'] for e in g['edges'])/1000;g['magnet_pairs']=len(g['magnets']);g['printed_pieces']=sum(g['counts'].values())

PLATES={}
for c in [*PRODUCTION,'JIG_ZERO','JIG_MARK','DEPTH_30']:
 PLATES['ONE_'+c]=[(c,5,5)];export3mf('ONE_'+c,PLATES['ONE_'+c])
w,h,_=PARTS['MAG_SLEEVE']['print_bounds_mm'];nx=int(173//(w+3));ny=int(173//(h+3))
PLATES['BATCH_MAG_SLEEVE']=[('MAG_SLEEVE',5+i*(w+3),5+j*(h+3)) for j in range(ny) for i in range(nx)]
PLATES['MEASURING_KIT']=[('JIG_ZERO',5,5),('JIG_MARK',54,5)]
PLATES['MEASURING_KIT_PLUS_DEPTH']=PLATES['MEASURING_KIT']+[('DEPTH_30',54,65)]
for name in ['BATCH_MAG_SLEEVE','MEASURING_KIT','MEASURING_KIT_PLUS_DEPTH']:export3mf(name,PLATES[name])
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
BOM={'outside_width_mm':S,'paper_band_width_mm':W,'opening_mm':S-2*W,'PVC_bore_mm':BORE,'sleeve_fit_status':'User confirmed perfect fit on purchased PVC, 2026-09-18','pipe_OD_mm':OD,'pipe_axis_behind_paper_mm':AXIS,'pipe_inset_mm':A,'socket_engagement_mm':30,'socket_stop_mm':STOP,'magnet_offset_mm':OFFSET,'parts':rows,'gates':GATES,'plates':PLATES,'production_types':5,'production_codes':PRODUCTION,'magnet_pockets_local_mm':MAGS,'ports_local_degrees':PORTS,'no_internal_cords':True,'no_diagonal_PVC':True,'source_price_PVC_10ft_USD':6,'guy_eye':{'hole_nominal_diameter_mm':10.5,'eye_plate_thickness_mm':14,'outer_width_mm':36,'center_height_behind_paper_mm':31,'load_rating':None},'measuring_jig':{'reference':'Straight uncut 1-inch PVC, 33.5 mm friction bore','axis_spacing_mm':70,'zero_datum_local_x_mm':0,'mark_datum_local_x_mm':0,'set_lengths_mm':[389.6,1560.8],'printed_absolute_scale':False,'initial_calibration':'Set datum face to datum face with a trusted metric tape; verify a trial cut','pipe_required_minimum_mm':1650,'tool_counts':{'JIG_ZERO':1,'JIG_MARK':1},'optional_tools':{'DEPTH_30':1},'marking_only':True,'cutter':'Husky 1-1/4 inch ratcheting PVC cutter','marking_collar':'33.5 mm round bore; printed axially so circular guide needs no supports'}}
(OUT/'BOM.json').write_text(json.dumps(BOM,indent=2))
def covered(x,y,g):return any(xx-.01<=x<=xx+w+.01 and yy-.01<=y<=yy+h+.01 for xx,yy,w,h in g['paper_rectangles'])
CHECKS={}
for kind,g in GATES.items():
 bad=[]
 for c,xy,r in g['placements']:
  M=T(*xy,0)@Rz(r)
  for v in PARTS[c]['object'].data.vertices:
   p=M@v.co
   if not covered(p.x*1000,p.y*1000,g):bad.append([c,xy,list(p)]);break
 CHECKS[kind]={'printed_vertices_outside_paper':bad,'magnet_centers_outside_paper':[(x,y) for x,y in g['magnets'] if not covered(x,y,g)],'only_orthogonal_PVC':all(abs(e['start'][0]-e['end'][0])<.001 or abs(e['start'][1]-e['end'][1])<.001 for e in g['edges'])}
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


setup('01_SINGLE_FRONT',(0,-6,1.67),(0,0,1.67),5.9,False);render_gate(GATES['single'])
header('01','Same face / fewer unused sockets','2700 mm outer square, 1480.8 mm opening and 609.6 mm paper bands. The accepted PVC bore remains 33.5 mm.')
footer('The sleeve you printed is unchanged. Tees and guy-eye top elbows keep the existing magnet positions and PVC cut lengths.')
setup('02_SINGLE_FRAME',(3.3,4.6,3.4),(0,0,1.67),5.9,False);render_gate(GATES['single'],False)
header('02','Use tees where only three pipes meet','Single: 2 bottom elbows, 2 guy-eye top elbows, 8 tees, 4 crosses and 48 magnetic sleeves.')
footer('Two PVC cuts: 389.6 and 1560.8 mm. Friction pipe joints; guy lines attach only at the two top elbows.')
setup('03_SPLIT_S_FRONT',(0,-8,2.80),(0,0,2.80),10.2,False);render_gate(GATES['split_s'])
header('03','Extend upward / retain the same borders','2700 x 4790.4 mm paper face. Two 1480.8 mm square openings and one shared 609.6 mm divider.')
footer('The two top guy-eye elbows move up with the complete top row. All existing pipes and sleeves are reused.')
setup('04_SPLIT_S_FRAME',(4,7,4.8),(0,0,2.80),10.2,False);render_gate(GATES['split_s'],False)
header('04','Five production types at either height','Stacked: 2 bottom elbows, 2 top guy elbows, 12 tees, 8 crosses and 80 magnetic sleeves.')
footer('Guy attachment geometry is supplied; base, anchors and allowable wind load still require validation.')
setup('05_PART_FAMILY',(.35,-.48,.42),(.08,.04,.025),.79,False);coll('01 / production parts')
for code,xy in [('ELBOW',(-130,100)),('GUY_ELBOW',(50,100)),('TEE',(-130,-85)),('CROSS',(50,-85)),('MAG_SLEEVE',(215,0))]:instance(code,xy)
header('05','A tee saves one socket and two unused pads','ELBOW bottom corners / GUY_ELBOW top corners / TEE outer three-way nodes / CROSS inner four-way nodes / MAG_SLEEVE edges.')
footer('Every PVC bore is 33.5 mm. Optional front pads remain in the previous kit; no new bore gauges are needed.')
setup('06_TEE_DETAIL',(.20,-.25,.22),(0,.00,.02),.37,False);coll('01 / new tee')
instance('TEE')
header('06','Three ports / two edge magnet pads','The missing branch faces the outside of the gate. Rotate this same tee at the top, bottom, left and right edges.')
footer('Socket engagement stays 30 mm. The two magnetic pads replace the two populated pads of the former cross at that position.')
setup('07_GUY_ELBOW',(-.22,-.28,.23),(.006,.005,.025),.36,False);coll('01 / integral rear eye')
instance('GUY_ELBOW')
# Short line is a threading illustration, not a knot or anchoring prescription.
q=Rz(45)@Vector((.035,0,.031));z=Rz(45)@Vector((-.045,0,.031));tube('Illustrative guy through rear eye',q,z,.003,ORANGE)
header('07','Tie down through the central body','A 10.5 mm peaked passage in a 14 mm-thick eye rises from the thick elbow core, behind the paper face.')
footer('Thread the eye; do not tie to the thin magnet arm. Printed eye strength and friction-joint loads are not yet measured.')
setup('08_MEASURING_HEADS',(.24,-.29,.26),(.035,.04,.020),.40,False);coll('01 / actual measuring heads')
instance('JIG_ZERO',(-25,0));instance('JIG_MARK',(55,0));instance('DEPTH_30',(112,0))
header('08','Small printed heads / full-length PVC reference rail','Left: end stop. Middle: round-bore marking collar. Right: optional 30 mm insertion-depth gauge. All use the accepted 33.5 mm bore.')
footer('Set the head spacing with a metric tape once, then repeat. This is a marking jig: remove the workpiece before cutting.')
setup('09_LONG_LENGTH_JIG',(.70,-1.50,1.10),(.78,.035,.023),2.50,False);coll('01 / long length measuring setup')
instance('JIG_ZERO');instance('JIG_MARK',(1560.8,0))
tube('Uncut reference PVC',(-.025,0,.024),(1.65,0,.024),.0334,WHITE,.00338)
tube('Workpiece end against zero datum',(0,.070,.024),(1.70,.070,.024),.0334,ORANGE,.00338)
tube('1560.8 mm datum distance',(0,.12,.055),(1.5608,.12,.055),.0018,MAGNET)
header('09','Measure once / repeat the long cut','Set ZERO contact face to MARK collar face = 1560.8 mm. The same two heads reset to 389.6 mm for the short cuts.')
footer('Hold the marking carriage while feeding pipe. Recheck witness marks and a trial cut; friction is not a calibrated positive clamp.')
setup('10_JIG_DATUM_DETAIL',(.20,-.28,.27),(.018,.060,.026),.36,False);coll('01 / zero contact surface')
instance('JIG_ZERO');tube('Reference rail',(-.07,0,.024),(.095,0,.024),.0334,WHITE,.00338)
tube('Work against end stop',(0,.070,.024),(.095,.070,.024),.0334,ORANGE,.00338)
header('10','Zero is the pipe-contact face','The pipe end meets the inner stop face, X = 0. Measure from that face to the near face of the marking collar, not between tool centers.')
footer('Keep the printed feet flat. Use a square pipe end, deburr it, and press gently against the end stop when marking.')
setup('11_MEASURING_KIT',(.29,-.31,.37),(.09,.08,.025),.39,False);coll('01 / bed layout')
box('A1 Mini bed',(90,90,-1),(180,180,2),GROUND)
for c,x,y in PLATES['MEASURING_KIT']:
 o=bpy.data.objects.new(c,PARTS[c]['print_mesh']);COL.objects.link(o);o.location=(x/1000,y/1000,0)
header('11','One A1 Mini plate / complete measuring kit','Two repeat-cut heads. The 30 mm insertion-depth gauge is available separately or on the optional expanded plate.')
footer('Use the supplied print orientations: marking head prints on its end face for a round, support-free pencil guide.')
for name in ['01_ASSEMBLED','00_MASTERS']:
 if bpy.data.scenes.get(name):bpy.data.scenes.remove(bpy.data.scenes[name])
bpy.context.window.scene=bpy.data.scenes['02_SINGLE_FRAME'];bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'Tee_PVC_Gate.blend'))
if '--no-render' not in sys.argv:
 for sc in bpy.data.scenes:
  selected=os.environ.get('RENDER_SCENES','')
  if selected and sc.name not in selected.split(','):continue
  bpy.context.window.scene=sc;sc.render.filepath=str(OUT/'renders'/f'{sc.name}.png');bpy.ops.render.render(write_still=True,scene=sc.name)
print('TEE BUILD',json.dumps({k:{'counts':g['counts'],'PVC_sticks':g['PVC_sticks'],'magnet_pairs':g['magnet_pairs']} for k,g in GATES.items()}),flush=True)
print('VISIBILITY',json.dumps(CHECKS),flush=True)

"""Cord-free orthogonal PVC gate: one elbow, one cross, one magnetic sleeve."""
from pathlib import Path
exec(Path(__file__).with_name('build_a1_full_size.py').read_text().split('# Registered channel splice:')[0],globals())
import ast,csv
OUT=ROOT/'output/orthogonal_pvc_gate'
for d in ['printable','renders']:(OUT/d).mkdir(parents=True,exist_ok=True)
PARTS={}
for node in ast.parse(Path(__file__).with_name('build_paper_roll_study.py').read_text()).body:
 if isinstance(node,ast.FunctionDef) and node.name in ['cyl','window','roundplate','export3mf']:exec(compile(ast.Module(body=[node],type_ignores=[]),'<helpers>','exec'),globals())
PAPER_ORANGE=mat('Orange roll paper',(.96,.255,.028));MAGNET=mat('6 x 2 mm magnets',(.43,.47,.50),.82)
S=2700.;W=609.6;A=75.;B=W-A;C=S-B;D=S-A;H2=2*S-W;AXIS=24.;STOP=35.;MOUTH=65.;OFFSET=A-18
BORE=float(os.environ.get('PVC_FIT_BORE','33.5'));WALL=4.;OD=33.4
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

for code,angles,mags in [('ELBOW',[0,90],[(-OFFSET,-OFFSET)]),('CROSS',[0,90,180,270],[(sx*OFFSET,sy*OFFSET) for sx in [-1,1] for sy in [-1,1]])]:
 o=box('Wide fitting core',(0,0,6),(44,44,12),STEEL)
 for ang in angles:
  q=axprof('Continuous socket root',[(-16,0),(16,0),(16,12),(-16,12)],STOP,0,ang);add(o,q)
  q=shell(MOUTH-STOP+5,STOP-5);raw_transform(q,Rz(ang));add(o,q)
 for x,y in mags:magnet_arm(o,x,y)
 for ang in angles:
  q=boretool(MOUTH-STOP+1,STOP);raw_transform(q,Rz(ang));boolean(o,q)
 master(code,o,('Universal outside elbow; two perpendicular sockets and one corner magnet pad' if code=='ELBOW' else 'Universal four-way cross; four identical sockets and four selectable corner magnet pads')+f'; {BORE:.1f} mm trial friction bore; 30 mm engagement; no fasteners or cord')
# One plain friction sleeve supplies intermediate magnets, including the straight seam crossbars.
o=shell(16,-8);boolean(o,boretool(18,-9))
add(o,box('Sleeve front arm',(0,OFFSET/2,1.5),(20,OFFSET+18,3),STEEL))
add(o,extrude_x('Sleeve arm root gusset',[(16,2.8),(16,9),(OFFSET-12,3)],12,-6,STEEL));pocket(o,(0,OFFSET))
master('MAG_SLEEVE',o,f'Universal friction sleeve with {OFFSET:.1f} mm offset magnetic face; no cleat, pin or cord eye; 16 mm pipe engagement')
# Three full-length coupons tune the real pipe/printer fit; these are tooling, not gate part types.
for d in [BORE-.2,BORE,BORE+.2]:
 o=shell(30,0,d);boolean(o,boretool(32,-1,d));master('FIT_'+str(round(d*10)),o,f'Thirty-mm-long friction fit coupon: {d:.1f} mm bore. Read labeled plate position; no scaling.')
o=roundplate('Optional front paper pad',24,24,3,r=6);window(o,(0,0),3.15,.4);master('PAPER_PAD',o,'Optional prior front magnet pad; .4 mm skin. Not part of the standard three-type gate BOM.')

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
   code='ELBOW' if outsidecorner else 'CROSS';nodes[name]={'xy':(x,y),'code':code,'angle':angle};placements.append((code,(x,y),angle))
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
 return {'levels':levels,'height_mm':H,'x_grid_mm':xs,'y_grid_mm':ys,'nodes':nodes,'edges':edges,'placements':placements,'magnets':sorted(magset),'paper_rectangles':paper,'counts':dict(collections.Counter(p[0] for p in placements)),'retention':'Friction only, as requested; physical pull-out/clocking/racking tests pending','cords':0,'diagonal_PVC':0}
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
# Source plate recipes and exact queues.
PLATES={}
for c in ['ELBOW','CROSS','MAG_SLEEVE']:
 PLATES['ONE_'+c]=[(c,5,5)];export3mf('ONE_'+c,PLATES['ONE_'+c])
w,h,_=PARTS['MAG_SLEEVE']['print_bounds_mm'];nx=int(173//(w+3));ny=int(173//(h+3));PLATES['BATCH_MAG_SLEEVE']=[('MAG_SLEEVE',5+i*(w+3),5+j*(h+3)) for j in range(ny) for i in range(nx)];export3mf('BATCH_MAG_SLEEVE',PLATES['BATCH_MAG_SLEEVE'])
FITC=['FIT_'+str(round(d*10)) for d in [BORE-.2,BORE,BORE+.2]]
PLATES['FIRST_FRICTION_FIT']=[('ELBOW',5,5)]+[(c,142,5+50*i) for i,c in enumerate(FITC)]+[('PAPER_PAD',5,145)]
PLATES['CROSS_AND_SLEEVE']=[('CROSS',5,5),('MAG_SLEEVE',145,5)]
for n in ['FIRST_FRICTION_FIT','CROSS_AND_SLEEVE']:export3mf(n,PLATES[n])
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
BOM={'outside_width_mm':S,'paper_band_width_mm':W,'opening_mm':S-2*W,'bore_trial_mm':BORE,'pipe_OD_mm':OD,'pipe_axis_behind_paper_mm':AXIS,'pipe_inset_mm':A,'socket_engagement_mm':30,'socket_stop_mm':STOP,'magnet_offset_mm':OFFSET,'parts':rows,'gates':GATES,'plates':PLATES,'friction_fit_samples_mm':[BORE-.2,BORE,BORE+.2],'production_types':3,'optional_front_pads':True,'no_cords':True,'no_diagonal_PVC':True,'source_price_PVC_10ft_USD':6}
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
 coll('01 / actual three production meshes')
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
header('01','One elbow / one cross / one magnetic sleeve','2700 mm outer size, 1480.8 mm opening, and equal 609.6 mm paper bands. Pipework and fittings stay behind the paper.')
footer('Friction-fit prototype. No diagonal PVC, tension cord, pin, screw, drilled pipe or magnetic seam backer.')
setup('02_SINGLE_FRAME',(3.3,4.6,3.4),(0,0,1.67),5.9,False);render_gate(GATES['single'],False)
header('02','A symmetric rectangular PVC grid','Four identical elbows, twelve identical crosses, and straight links between the inner and outer edges.')
footer('All pipes use just two cut lengths: 389.6 mm and 1560.8 mm. Crosses also serve at T junctions; the unused socket stays empty.')
setup('03_SPLIT_S_FRONT',(0,-8,2.80),(0,0,2.80),10.2,False);render_gate(GATES['split_s'])
header('03','Two openings / the same two-foot borders','2700 x 4790.4 mm paper face. The shared middle band is also 609.6 mm wide.')
footer('The head-on face shows paper and magnets. This is the face frame; cord-free base/restraint sizing is separate and remains unqualified.')
setup('04_SPLIT_S_FRAME',(4,7,4.8),(0,0,2.80),10.2,False);render_gate(GATES['split_s'],False)
header('04','Extend the same grid upward','The two top elbows move up. Every existing pipe is reused; add crosses and the same short/long cuts.')
footer('No cord is present in this iteration, including external guy lines. Friction retention and racking resistance still need physical testing.')
setup('05_THREE_PART_TYPES',(.26,-.42,.34),(.09,.025,.025),.58,False);coll('01 / production part family')
instance('ELBOW',(-80,0));instance('CROSS',(90,0));instance('MAG_SLEEVE',(225,0))
header('05','Exactly three production part types','ELBOW at outside corners. CROSS at every other grid junction. MAG_SLEEVE for magnets between junctions.')
footer('The sleeve has no cord eye or cleat. Fit coupons and optional front pads are tooling/options, not additional required gate part types.')
setup('06_ELBOW_CROSS_DETAIL',(.30,-.45,.37),(.095,.10,.02),.69,False);coll('01 / real parts and straight links')
instance('ELBOW');instance('CROSS',(350,0))
tube('Horizontal PVC',(.035,0,.024),(.315,0,.024),.0334,WHITE,.00338)
for x in [0,.350]:tube('Vertical PVC',(x,.035,.024),(x,.22,.024),.0334,WHITE,.00338)
header('06','Straight sockets and broad magnet supports',f'Trial bore {BORE:.1f} mm for nominal 33.4 mm OD pipe. All sockets have a 35 mm center-to-stop offset and 30 mm engagement.')
footer('Choose the bore after printing the full-length fit samples. The peaked socket roof and 0.4 mm frame-side magnet skin are retained.')
setup('07_SLEEVE_AND_PAPER',(.18,.23,.19),(.0,.026,.023),.28,False);coll('01 / friction sleeve')
instance('MAG_SLEEVE');tube('PVC',(-.08,0,.024),(.08,0,.024),.0334,WHITE,.00338)
box('Paper cutaway / exploded 8 mm forward',(5,OFFSET,-8.18),(100,25,.18),PAPER_ORANGE)
cyl('Back magnet',(0,OFFSET,.4),3,2,MAGNET);cyl('Front magnet',(0,OFFSET,-10.27),3,2,MAGNET)
header('07','The same sleeve supports edges and paper seams','Rotate the sleeve on the pipe to put its flat face in the common paper plane. Its friction fit holds its location and rotation.')
footer('Paper is exploded 8 mm forward here. Assembled stack: rear magnet / 0.4 mm plastic / paper / front magnet.')
setup('08_FIRST_FRICTION_FIT',(.30,-.30,.37),(.09,.09,.024),.39,False);coll('01 / actual first-fit layout')
box('180 mm A1 Mini bed',(90,90,-1),(180,180,2),GROUND)
for c,x,y in PLATES['FIRST_FRICTION_FIT']:
 o=bpy.data.objects.new(c,PARTS[c]['print_mesh']);COL.objects.link(o);o.location=(x/1000,y/1000,0)
header('08','First print / select a reliable friction fit',f'One elbow, three 30 mm-long fit coupons, and an optional front pad. Coupons: {BORE-.2:.1f}, {BORE:.1f}, {BORE+.2:.1f} mm from front to rear.')
footer('Use actual pipe offcuts. Pick full hand seating plus firm pull-out and rotational resistance; do not choose a bore from the CAD number alone.')
setup('09_SHARED_MIDDLE',(1.5,4,3.2),(0,0,2.50),4.4,False);coll('01 / middle-band nodes and pipes')
g=GATES['split_s'];lo,hi=C,D
for c,xy,r in g['placements']:
 if lo-100<=xy[1]<=hi+100:instance(c,xy,r,FRONT)
for e in g['edges']:
 if not (lo-.01<=e['start'][1]<=hi+.01 and lo-.01<=e['end'][1]<=hi+.01):continue
 aa=FRONT@Vector((e['start'][0]/1000,e['start'][1]/1000,AXIS/1000));bb=FRONT@Vector((e['end'][0]/1000,e['end'][1]/1000,AXIS/1000));tube(e['name'],aa,bb,.0334,WHITE,.00338)
header('09','One shared divider / no special junction part','The same cross serves both opening corners, the outer verticals, and the straight links across the band.')
footer('Paper band width remains 609.6 mm. The centerline spacing is 459.6 mm because both rows of PVC are inset behind the paper.')
for name in ['01_ASSEMBLED','00_MASTERS']:
 if bpy.data.scenes.get(name):bpy.data.scenes.remove(bpy.data.scenes[name])
bpy.context.window.scene=bpy.data.scenes['02_SINGLE_FRAME'];bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'Orthogonal_PVC_Gate.blend'))
if '--no-render' not in sys.argv:
 for sc in bpy.data.scenes:
  selected=os.environ.get('RENDER_SCENES','')
  if selected and sc.name not in selected.split(','):continue
  bpy.context.window.scene=sc;sc.render.filepath=str(OUT/'renders'/f'{sc.name}.png');bpy.ops.render.render(write_still=True,scene=sc.name)
print('ORTHOGONAL BUILD',json.dumps({k:{'counts':g['counts'],'PVC_sticks':g['PVC_sticks'],'magnet_pairs':g['magnet_pairs']} for k,g in GATES.items()}),flush=True)
print('VISIBILITY',json.dumps(CHECKS),flush=True)

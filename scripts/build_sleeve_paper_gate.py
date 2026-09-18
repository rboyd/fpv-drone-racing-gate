"""Reinforced paper gate, exact production masters and assembly; dimensions mm."""
from pathlib import Path
exec(Path(__file__).with_name('build_a1_full_size.py').read_text().split('# Registered channel splice:')[0],globals())
import ast,csv
OUT=ROOT/'output/sleeve_paper_gate'
for d in ['printable','renders']:(OUT/d).mkdir(parents=True,exist_ok=True)
PARTS={};GUIDE=[(-3,0),(3,0),(1,2),(-1,2)]
src=Path(__file__).with_name('build_paper_roll_study.py').read_text()
for node in ast.parse(src).body:
 if isinstance(node,ast.FunctionDef) and node.name in ['cyl','roundplate','window','add_male','export3mf']:
  exec(compile(ast.Module(body=[node],type_ignores=[]),'<helpers>','exec'),globals())
PAPER_ORANGE=mat('Orange roll paper',(.95,.24,.035));MAGNET=mat('Neodymium magnets',(.45,.49,.53),.8)
LINE_A=mat('2.4 mm paracord / yellow',(.95,.66,.03));LINE_B=mat('Paracord wraps / teal',(.02,.6,.48))
S=2700.;W=609.6;BL=S-W;L=(BL-13*14)/14;P=L+14;RL=(W-152-56)/3
IDX=[0,2,5,8,11,13];XS=[L/2+i*P for i in IDX]
def cut_socket(o,origin=(0,0,0),angle=0,clear=.4):
 A=T(*origin)@Rz(angle)
 for c,d in [((10,0,14),(20.05,8+2*clear,32)),((24,0,14),(8,11.6,32))]:
  q=box('Open latch relief',c,d);raw_transform(q,A);boolean(o,q)
 for yy in [-11,11]:
  pr=[(-3-clear,-.1),(3+clear,-.1),(1+clear,2),(1+clear,31),(-1-clear,31),(-1-clear,2)]
  q=extrude_x('Guide groove',[(y+yy,z) for y,z in pr],15,-.1);raw_transform(q,A);boolean(o,q)
def cone(name,x,y,z,r0,r1,h,material=STEEL):
 n=48;vs=[(x+r*math.cos(i*math.tau/n),y+r*math.sin(i*math.tau/n),zz) for r,zz in [(r0,z),(r1,z+h)] for i in range(n)]
 return mesh(name,vs,[tuple(reversed(range(n))),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)],material)
def beam_master(length,branch=False,rung=False):
 o=box('Continuous front flange',(length/2,0,1),(length,40,2),STEEL)
 add(o,box('Continuous central spine',(length/2,0,6),(length-60,16,12),STEEL))
 for x in [17,length-17]:add(o,box('Thick receiver end',(x,0,4),(34,40,8),STEEL))
 mx=length/2 if rung else length/4
 pts=[(mx+10*math.cos(math.pi*i/48),19.95+10*math.sin(math.pi*i/48)) for i in range(49)]
 add(o,prism('D magnet holder',pts,3,material=STEEL));window(o,(mx,24.75),3.15,.4)
 cut_socket(o);cut_socket(o,(length,0,0),180)
 if branch:
  xc=length/2
  pts=[(xc-28,6),(xc+28,6),(xc+20,32),(xc+20,56),(xc-20,56),(xc-20,32)]
  add(o,prism('Gusseted projecting socket',pts,8,material=STEEL))
  add(o,extrude_x('Back root gusset',[(7,7.9),(7,16),(28,8)],40,xc-20,STEEL))
  cut_socket(o,(xc,56,0),270)
  for x in [xc-22,xc+22]:
   add(o,cyl('Cleat and fairlead post',(x,0,11.9),6,12.2,STEEL))
   add(o,cone('Support-free 45 degree horn',x,0,24,6,9,3))
   add(o,cyl('Horn cap',(x,0,26.9),9,2.1,STEEL))
   q=extrude_x('Support-free cord eye',[(0,16.5),(3.5,20),(0,23.5),(-3.5,20)],18,x-9);boolean(o,q)
 return o
for code,desc,br,ru,length in [('EDGE_PLAIN','Continuous 16 x 12 mm spine; two 8 mm deep receivers; integral magnet lug',False,False,L),('EDGE_BRANCH','Projecting crossmember receiver; uninterrupted main spine; integral two-horn cleat and cord eyes',True,False,L),('RUNG','Crossmember segment with magnet lug; no mounting hardware or bolt holes',False,True,RL)]:master(code,beam_master(length,br,ru),desc)
o=box('Double click key',(0,0,2.5),(14,32,5),ORANGE);add_male(o,(7,0,0),0);add_male(o,(-7,0,0),180);master('CLICK_KEY',o,'Replaceable double-ended click key; pinch both fork tips at each end to release')
o=roundplate('Paper pad',24,24,3,r=6);window(o,(0,0),3.15,.4);master('PAPER_PAD',o,'Optional front magnetic pad, 6.3 mm bore and .4 mm paper-facing skin')
# One-piece sleeve rung. Native Y is the PVC axis; paper remains on Z=0.
PIPE_AXIS=46.;BORE=34.2;WALL=6.;SLEEVE_DEPTH=24.
def tear(r):
 # Circular lower 270 degrees; tangent 45-degree roof clears the round pipe without supports.
 return [(r*math.cos(math.radians(135+270*i/108)),r*math.sin(math.radians(135+270*i/108))) for i in range(109)]+[(0,r*math.sqrt(2))]
def across_y(name,profile,depth,origin=(0,0,0)):
 q=prism(name,profile,depth,-depth/2,STEEL)
 raw_transform(q,basis((1,0,0),(0,0,1),(0,1,0),origin));return q
o=beam_master(RL,rung=True);xc=RL/2;ri=BORE/2;ro=ri+WALL
# Wide tapered root occupies the entire sleeve depth: no suspended lower rim or narrow neck.
add(o,across_y('Broad tapered sleeve root',[(-34,1.8),(34,1.8),(ro,PIPE_AXIS),(-ro,PIPE_AXIS)],SLEEVE_DEPTH,(xc,0,0)))
add(o,across_y('Integral closed PVC loop',tear(ro),SLEEVE_DEPTH,(xc,0,PIPE_AXIS)))
boolean(o,across_y('34.2 mm pipe clearance and peaked roof',tear(ri),SLEEVE_DEPTH+2,(xc,0,PIPE_AXIS)))
master('RUNG_SLEEVE',o,'One-piece frame rung + closed sleeve for 33.4 mm OD PVC; 34.2 mm nominal bore, 6 mm wall, 24 mm engagement, broad tapered root; no bolts')
# Short fit gauges share the actual bore orientation and roof geometry.
for diam in [34.,34.2,34.4]:
 r=diam/2;rr=r+5;z=rr
 prof=[(-rr,0),(rr,0),(rr,z),(rr/2**.5,z+rr/2**.5),(0,z+rr*2**.5),(-rr/2**.5,z+rr/2**.5),(-rr,z)]
 o=across_y('Pipe fit gauge',prof,8)
 boolean(o,across_y('Gauge bore',tear(r),10,(0,0,z)))
 master('GAUGE_'+str(round(diam*10)),o,f'Fit-only short horizontal bore gauge: {diam:.1f} mm; not a production part')
# Four identical V blocks plus one universal crossing plate per PVC brace end.
prof=[(-32,0),(32,0),(32,22),(16,22),(0,6),(-16,22),(-32,22)]
o=extrude_x('Universal PVC V clamp',prof,24,-12,STEEL)
for y in [-25,25]:window(o,(0,y),2.25,-1,h=30)
master('V_BLOCK',o,'Universal 90-degree V clamp half; four per brace crossing; M4 through-bolts')
o=roundplate('Brace crossing plate',70,70,6,r=5,material=ORANGE)
for x,y in [(0,-25),(0,25)]+[(sx*25/math.sqrt(2),sy*25/math.sqrt(2)) for sx in [-1,1] for sy in [-1,1]]:window(o,(x,y),2.25,-1,h=10)
master('CROSS_PLATE',o,'Universal +/-45 degree brace joint; use appropriate diagonal pair of M4 holes')
# Exact panel placement ledger, in panel XY; +Z points behind paper.
PANEL=[];MAGS=[];DOCKS=[];CORD_PATHS=[]
for i in range(14):
 code='EDGE_BRANCH' if i in IDX else 'EDGE_PLAIN';x=i*P
 PANEL.extend([(code,T(x,20,0)),(code,T(BL-x,W-20,0)@Rz(180))])
 MAGS.extend([(x+L/4,44.75),(BL-x-L/4,W-44.75)])
 if i<13:PANEL.extend([('CLICK_KEY',T(x+L+7,20,0)),('CLICK_KEY',T(x+L+7,W-20,0))])
# Symmetric index set guarantees branches line up after rotating upper rail.
for j,x in enumerate(XS):
 for k in range(3):PANEL.append(('RUNG_SLEEVE' if k==1 and j in [1,2,3,4] else 'RUNG',T(x,90+k*(RL+14),0)@Rz(90)))
 for y in [83,90+RL+7,90+2*RL+21,W-83]:PANEL.append(('CLICK_KEY',T(x,y,0)@Rz(90)))
 MAGS.append((x-24.75,W/2))
 if j in [1,2,3,4]:DOCKS.append(T(x,90+RL+14,0)@Rz(90))
for j in range(5):
 a,b=XS[j]+22,XS[j+1]-22
 # One cord, four spans: LL -> UR -> LR -> UL -> LL; independent adjustment per bay.
 pts=[(a-8,20,18.7),(a+8,20,18.7),(b-8,W-20,20),(b+8,W-20,20),(b+8,20,20),(b-8,20,20),((a+b)/2,W/2,23),(a+8,W-20,20),(a-8,W-20,20),(a-8,20,21.3),(a+8,20,21.3)]
 length=sum((Vector(v)-Vector(u)).length for u,v in zip(pts,pts[1:]))+600
 CORD_PATHS.append({'bay':j+1,'points':pts,'cut_mm':math.ceil(length/10)*10})
for x,y in MAGS:PANEL.append(('PAPER_PAD',T(x,y,-.18)@Matrix.Diagonal((1,1,-1,1))))
# Transform native panel XY to upright world XZ; rear points world +Y.
PM=[]
for k in range(4):
 rot=Matrix.Rotation(math.radians(-90*k),4,'Y')
 PM.append(T(0,0,1400)@rot@T(-1350,0,BL-1350)@basis((1,0,0),(0,0,1),(0,1,0),(0,0,0)))
QTY=collections.Counter(code for code,_ in PANEL)
QTY={c:4*n for c,n in QTY.items()};QTY.update(V_BLOCK=32,CROSS_PLATE=8)
assert QTY=={'EDGE_BRANCH':48,'EDGE_PLAIN':64,'CLICK_KEY':200,'RUNG':56,'RUNG_SLEEVE':16,'PAPER_PAD':136,'V_BLOCK':32,'CROSS_PLATE':8},QTY
# Each homogeneous plate fits a 170 mm square (5 mm border), simple reliable queue.
PLATES={};RUNS={};EXPANDED=[]
for code,p in PARTS.items():
 if not QTY.get(code,0):continue
 w,h,z=p['print_bounds_mm'];nx=int(173//(w+3));ny=int(173//(h+3));cap=nx*ny
 assert cap>=1,(code,w,h)
 items=[(code,5+i*(w+3),5+j*(h+3)) for j in range(ny) for i in range(nx)]
 full,tail=divmod(QTY[code],cap)
 for n,count,label in [(cap,full,'FULL'),(tail,1 if tail else 0,'TAIL')]:
  if not count:continue
  name=f'Q_{code}_{label}';PLATES[name]=items[:n];RUNS[name]=count;export3mf(name,items[:n]);EXPANDED.extend([name]*count)
# Start with a new reinforced junction/cleat test: actual production parts, not reduced scale.
TESTS={'T01_BRANCH':[('EDGE_BRANCH',5,5),('CLICK_KEY',5,85),('CLICK_KEY',75,85),('PAPER_PAD',5,123)],
       'T02_RUNG':[('RUNG',5,5),('RUNG',5,59),('RUNG',5,113)],
       'T03_BAY_SLEEVE':[('RUNG',5,5),('RUNG',5,59),('RUNG_SLEEVE',5,113)],
       'T00_SLEEVE_FIT':[('RUNG_SLEEVE',5,5),('GAUGE_340',5,66),('GAUGE_342',61,66),('GAUGE_344',117,66),('CLICK_KEY',5,88),('CLICK_KEY',75,88),('PAPER_PAD',5,130)],
       'T05_SINGLE_PLAIN':[('EDGE_PLAIN',5,5),('CLICK_KEY',5,63),('CLICK_KEY',75,63),('PAPER_PAD',5,103),('PAPER_PAD',35,103)],
       'T04_BRACE':[('V_BLOCK',5+27*i,5) for i in range(4)]+[('CROSS_PLATE',5,75)]}
for name,items in TESTS.items():export3mf(name,items)
rows=[dict(code=c,quantity=QTY.get(c,0),optional=(c=='PAPER_PAD'),**{k:v for k,v in p.items() if k not in ['object','print_mesh']}) for c,p in PARTS.items()]
BOM={'outside_mm':S,'opening_mm':S-2*W,'border_mm':[BL,W],'parts':rows,'printed_pieces':sum(QTY.values()),'unique_types':len(QTY),'totals_configuration':'With optional front paper pads','printed_pieces_without_optional_pads':sum(QTY.values())-QTY['PAPER_PAD'],'unique_types_without_optional_pads':len(QTY)-1,'paper_pads_optional':True,'sleeve':{'PVC_OD_mm':33.4,'bore_mm':BORE,'wall_mm':WALL,'engagement_mm':SLEEVE_DEPTH,'pipe_axis_behind_paper_mm':PIPE_AXIS,'extra_stays':0,'bolts_at_face_attachment':0},'magnets_6x2':len(MAGS)*8,'cords':CORD_PATHS,'cord_minimum_m':4*sum(p['cut_mm'] for p in CORD_PATHS)/1000,'cord_uniform_cut_mm':3300,'cord_total_m':66,'guy_cord_m':16,'plates':PLATES,'plate_runs':RUNS,'expanded_queue':EXPANDED,'test_plates':TESTS,'crossmember_x_mm':XS,'edge_length_mm':L,'rung_length_mm':RL,'status':'Digital fabrication prototype; not physically validated'}
(OUT/'BOM.json').write_text(json.dumps(BOM,indent=2))
with (OUT/'BOM.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=['code','quantity','optional','description','print_bounds_mm','file'],extrasaction='ignore');w.writeheader();w.writerows(rows)
# Scene helpers. Exported mesh instances are used throughout.
def inst(code,M=Matrix.Identity(4)):
 o=bpy.data.objects.new(code,PARTS[code]['object'].data);COL.objects.link(o);o.matrix_world=M;return o
def mmline(name,pts,r,matr=LINE_A,M=Matrix.Identity(4)):
 return line(name,[M@Vector(tuple(c/1000 for c in p)) for p in pts],r/1000,matr)
def bolt(name,M,x,y,z,length,d=3,flat=False,grip=None):
 # Purchased hardware envelope: shaft, head and hex nut. Threads not modeled.
 q=cyl(name+' shaft',(x,y,z),d/2,length,METAL,24);q.matrix_world=M
 q=cyl(name+' head',(x,y,z-2),d,2,METAL,6 if not flat else 24);q.matrix_world=M
 q=cyl(name+' nut',(x,y,z+(length-3 if grip is None else grip)),d,2.5,METAL,6);q.matrix_world=M

def panel(M,paper=True,cords=True,hardware=True):
 for c,Pm in PANEL:inst(c,M@Pm)
 if paper:
  q=box('2090.4 x 609.6 paper',(BL/2,W/2,-.09),(BL,W,.18),PAPER_ORANGE);q.matrix_world=M
 for x,y in MAGS:
  q=cyl('Rear 6 x 2 magnet',(x,y,.4),3,2,MAGNET,24);q.matrix_world=M
  q=cyl('Pad 6 x 2 magnet',(x,y,-2.58),3,2,MAGNET,24);q.matrix_world=M
 if cords:
  for cp in CORD_PATHS:
   mmline('Bay %s permanent X cord'%cp['bay'],cp['points'],1.2,LINE_A,M)
   j=cp['bay']-1;xc=XS[j]
   # Two figure-eight turns around paired posts; tail remains accessible on rear.
   pts=[]
   for turn in range(2):
    for i in range(81):
     t=i*math.tau/80;pts.append((xc+30*math.sin(t),20+8.5*math.sin(2*t),21.5+turn*2.5))
   mmline('Cleat figure-eight wraps (hitch shown in instructions)',pts,1.2,LINE_B,M)

HM=6+math.sqrt(2)*16.7;HB=6+math.sqrt(2)*(26.67/2);SEP=HM+6+HB;PY=PIPE_AXIS
FRAME_CORNERS=[Vector((x,PY,z)) for x,z in [(-1045.2,354.8),(1045.2,354.8),(1045.2,2445.2),(-1045.2,2445.2)]]
BRACES=[]
for j,c in enumerate(FRAME_CORNERS):
 prev=FRAME_CORNERS[(j-1)%4];nxt=FRAME_CORNERS[(j+1)%4]
 a=c+(prev-c).normalized()*400;b=c+(nxt-c).normalized()*400;v=(b-a).normalized()
 BRACES.append((a,b,v))
def brace_joint(c,main,v):
 ez=Vector((0,1,0));ey=ez.cross(main);theta=math.degrees(math.atan2(v.dot(ey),v.dot(main)))
 J=basis(main,ey,ez,c+ez*HM);F=Matrix.Rotation(math.pi,4,'Y')
 inst('CROSS_PLATE',J);inst('V_BLOCK',J@F);inst('V_BLOCK',J@T(0,0,-2*HM));inst('V_BLOCK',J@T(0,0,6)@Rz(theta));inst('V_BLOCK',J@T(0,0,6+2*HB)@Rz(theta)@F)
 for y in [-25,25]:bolt('M4 x 80 main V clamp',J,0,y,-2*HM-.8,80,4,grip=2*HM+7.6)
 for y in [-25,25]:bolt('M4 x 70 brace V clamp',J@Rz(theta),0,y,-.8,70,4,grip=2*HB+7.6)
 return J

def pipe(name,a,b,od=33.4):return tube(name,Vector(a)/1000,Vector(b)/1000,od/1000,WHITE,(3.38 if od==33.4 else 2.87)/1000)
def fitting(c,directions,name):
 # Purchased fitting envelopes, not printable geometry. Measure actual take-up before cutting.
 for d in directions:pipe(name,c,c+Vector(d)*43,43)

def backbone(hard=False):
 g=17.4625
 for j,a in enumerate(FRAME_CORNERS):
  b=FRAME_CORNERS[(j+1)%4];v=(b-a).normalized();pipe('1 inch PVC square / 2055.48 mm',a+v*g,b-v*g)
 for j,c in enumerate(FRAME_CORNERS):
  prev=(FRAME_CORNERS[(j-1)%4]-c).normalized();nxt=(FRAME_CORNERS[(j+1)%4]-c).normalized();dirs=[prev,nxt]
  dirs.append(Vector((0,0,-1 if j<2 else 1)))
  fitting(c,dirs,'Purchased main-frame tee')
  # Positive retention envelopes for each occupied fitting socket.
  for d in dirs:
   center=c+Vector(d)*31;pipe('M4 fitting retention bolt',center+Vector((0,-30,0)),center+Vector((0,30,0)),4)
 for a,b,v in BRACES:
  pipe('3/4 inch PVC corner brace / 645.69 mm',a+Vector((0,SEP,0))-v*40,b+Vector((0,SEP,0))+v*40,26.67)
  for c in [a,b]:
   main=Vector((1,0,0)) if c.z in [354.8,2445.2] else Vector((0,0,1));brace_joint(c,main,v)
 for x in [-1045.2,1045.2]:
  pipe('Upper guy mast / 637.34 mm',(x,PY,2445.2+g),(x,PY,3100))
  pipe('Upper mast end cap',(x,PY,3085),(x,PY,3105),43)
  pipe('M4 guy-loop stop bolt',(x-30,PY,3085),(x+30,PY,3085),4)
 footspan=1200 if hard else 600
 for x in [-1045.2,1045.2]:
  c=Vector((x,PY,25));pipe('Lower leg / 294.88 mm',c+Vector((0,0,g)),Vector((x,PY,354.8-g)))
  fitting(c,[(0,1,0),(0,-1,0),(0,0,1)],'Purchased foot tee')
  for d in [Vector((0,1,0)),Vector((0,-1,0)),Vector((0,0,1))]:
   cc=c+d*31;pipe('M4 foot retention bolt',cc+Vector((-30,0,0)),cc+Vector((30,0,0)),4)
  for sy in [-1,1]:
   end=c+Vector((0,sy*footspan,0));pipe('Detachable foot pipe',c+Vector((0,sy*g,0)),end)
   pipe('Purchased foot end cap',end-Vector((0,sy*15,0)),end+Vector((0,sy*5,0)),43)
   box('Rubber contact pad',(end.x,end.y,2),(60,60,4),DARK)
   anchor=Vector((x,PY+sy*(1150 if hard else 1500),25))
   mmline('Separate 2.4 mm guy cord',[(x,PY,3075),tuple(anchor)],1.2,CORD)
   if hard:
    box('15 kg weighed ballast bag',(x,anchor.y,75),(350,340,150),DARK)
    mmline('Purchased ballast retaining strap',[(x-170,anchor.y,30),(x-170,anchor.y,190),(x+170,anchor.y,190),(x+170,anchor.y,30)],8,DARK)
   else:pipe('Ground stake',anchor+Vector((0,0,20)),anchor-Vector((0,0,300)),10)

setup('01_ASSEMBLED_FRONT',(-4.5,-7,4.5),(0,.15,1.6),7.0);coll('01 / full gate')
for M in PM:panel(M)
backbone()
header('01','Paper gate / reinforced click frame','2700 mm outside | 1480.8 mm opening | Four permanent cord-braced borders | One braced PVC square')
footer('Digital prototype. The face frames stay assembled for transport. Prove joints, magnetic grip and stability before field use.')
setup('02_REAR_STRUCTURE',(4.8,7,4.8),(0,.10,1.6),7.1);coll('01 / exact parts, paper removed')
for M in PM:panel(M,False)
backbone()
header('02','The complete load path','Paper pads > reinforced rails > integral sleeves > PVC square > corner braces > feet and guys')
footer('With optional pads: 560 pieces / 8 types; without: 424 / 7. All visible blue/orange structural parts instantiate their actual exported fabrication meshes.')
setup('03_ONE_BORDER',(.9,-1.8,2.6),(BL/2000,W/2000,.02),2.65,False);coll('01 / permanent border')
panel(Matrix.Identity(4),False)
header('03','One transport section / 2090.4 x 609.6 mm','Two click rails, six crossmembers, five individually adjustable X cords and four integral closed PVC sleeves')
footer('Thread and tension on a flat bench. Keep the five cords installed; disconnect the PVC corner fittings to remove a border.')
setup('04_REINFORCED_JUNCTION',(.18,-.23,.24),(.071,.012,.006),.28,False);coll('01 / new junction')
inst('EDGE_BRANCH');inst('CLICK_KEY',T(L/2,63,0)@Rz(90));
header('04','Keep the structural spine intact','The crossmember socket projects off the rail. A 16 x 12 mm spine continues behind it; the old 4 x 5 mm neck is removed.')
footer('Raised posts double as cord eyes and a permanent two-horn cleat. All features grow from the flat paper-facing print surface.')
setup('05_CORD_THREADING',(.07,-.16,.18),(.07,.005,.012),.22,False);coll('01 / integral cleat')
inst('EDGE_BRANCH')
xc=L/2
pts=[]
for turn in range(2):
 for i in range(101):
  t=i*math.tau/100;pts.append((xc+30*math.sin(t),8.5*math.sin(2*t),21.5+turn*2.5))
mmline('Two figure-eight wraps',pts,1.2,LINE_A)
mmline('Pull tail then lock with half-hitch',[(xc+60,30,20),(xc+30,0,20),(xc+14,0,20),(xc+12,-22,20)],1.2,LINE_B)
header('05','Pull, wrap, lock / no tightening tool','Pull slack out by hand; add two figure-eight wraps and a locking half-hitch. Lift off the hitch and unwrap to release.')
footer('Knot path is explained in the assembly guide. Smooth the cord-contact edges; bench-test slip and wear with the actual 2.4 mm cord.')
setup('06_INTEGRAL_PVC_SLEEVE',(.20,-.25,.19),(.067,0,.025),.29,False);coll('01 / one printed part, no fasteners')
inst('RUNG_SLEEVE')
pipe('33.4 mm OD PVC threaded through sleeve',(RL/2,-80,PIPE_AXIS),(RL/2,80,PIPE_AXIS))
header('06','A single printed part / slide the PVC through','The rung and closed sleeve are one printed piece. Broad tapered root, 6 mm loop wall, 24 mm pipe engagement; no attachment bolts or nuts.')
footer('34.2 mm trial bore for 33.4 mm OD pipe. Peaked roof prints without support; check the fit with your actual PVC before repeating.')
setup('10_SLEEVE_PRINT_FACE',(.18,-.23,.21),(.067,0,.025),.27,False);coll('01 / printable loop and broad root')
inst('RUNG_SLEEVE')
header('10','Broad root and a closed load path','Paper face prints flat on the bed. The 45-degree bore roof clears round PVC while avoiding an unsupported circular ceiling.')
footer('The 68 mm wide root tapers into the sleeve. The pipe center sits 46 mm behind the paper, clear of the face-bracing cords.')
setup('07_BRACE_JOINT',(.17,.23,.14),(0,.02,.00),.27,False);coll('01 / universal brace crossing')
brace_joint(Vector((0,0,0)),Vector((1,0,0)),Vector((1,0,1)).normalized())
pipe('Main PVC',(-90,0,0),(90,0,0));pipe('Brace PVC',(-65,SEP,-65),(65,SEP,65),26.67)
header('07','One universal brace clamp / both pipe sizes','Four identical V blocks and one crossing plate per brace end. Eight crossings support the four PVC corner braces.')
footer('Two M4 x 80 bolts clamp the main pipe; two M4 x 70 clamp the brace. Printed parts have flat bases and support-free V seats.')
setup('08_HARD_SURFACE',(-4.5,-7.5,4.7),(0,.12,1.6),7.2);coll('01 / ballast and long feet')
for M in PM:panel(M)
backbone(True)
header('08','Hard surface / longer feet and attached ballast','2400 mm fore-aft stance, four 15 kg bags and four guy lines. Use rubber contact pads; keep the flying approach clear.')
footer('60 kg is a starting test configuration, not a wind rating. Real sliding, overturning, paper grip and joint stiffness require field verification.')
setup('09_FULL_WIDTH_TEST',(.8,-.9,1.1),(.22,.30,.025),1.05,False);coll('01 / reusable full-width test bay')
TEST_LENGTH=3*L+2*14
for code,M in PANEL:
 vs=[M@v.co for v in PARTS[code]['object'].data.vertices]
 if min(v.x for v in vs)>=-.00001 and max(v.x for v in vs)<=TEST_LENGTH/1000+.00001:inst(code,M)
mmline('Threaded X test bay',CORD_PATHS[0]['points'],1.2,LINE_A)
header('09','Prove one full-width bay first','436.94 x 609.6 mm. Four branch rails, two plain rails, five plain rungs, one sleeve rung, twelve keys and eight pads.')
footer('Print T01 four times, T02 once, T03 once and T05 twice. All 32 pieces can be reused in the full gate.')
setup('11_PIPE_THREADING',(.9,-1.8,2.4),(1.18,.31,.015),3.15,False);coll('01 / pipe through four closed loops')
panel(Matrix.Identity(4),False)
pipe('Loose straight PVC rail before corner fittings',(W/2+17.4625,W/2,PIPE_AXIS),(S-W/2-17.4625,W/2,PIPE_AXIS))
header('11','Thread the bare pipe first / then join the corners','Four closed loops share one straight PVC rail. Fit the PVC tees after threading; nothing bolts to the face frame.')
footer('Disassemble the corner fittings and brace clamps before removing a rail. There are no extra cord stays at the sleeves.')
# Placement audit and stronger-spine geometric evidence.
checks={'manifold_masters':all(p['nonmanifold_edges']==0 for p in PARTS.values()),'all_parts_within_170_mm':all(max(p['print_bounds_mm'])<=170 for p in PARTS.values()),'panel_counts':dict(collections.Counter(c for c,_ in PANEL)),'old_neck_nominal_mm':[4,5],'new_continuous_spine_mm':[16,12],'socket_nearest_y_mm':28,'spine_y_mm':[-8,8],'physical_testing':'Not yet performed','cord_bays_per_border':5,'magnet_pairs_per_border':len(MAGS)}
# Check every plate AABB fits and no boxes overlap. Source homogeneous queue has no duplicate/omitted pieces.
for name,items in {**PLATES,**TESTS}.items():
 rect=[]
 for code,x,y in items:
  w,h,z=PARTS[code]['print_bounds_mm'];assert x>=5 and y>=5 and x+w<=175.001 and y+h<=175.001,(name,code,x,y,w,h)
  for xx,yy,ww,hh in rect:assert x+w<=xx+.001 or xx+ww<=x+.001 or y+h<=yy+.001 or yy+hh<=y+.001,(name,code,'overlap')
  rect.append((x,y,w,h))
# Sample actual mating interiors with ray tests (not coplanar Boolean volumes).
for node in ast.parse(Path(__file__).with_name('build_full_width_demo.py').read_text()).body:
 if isinstance(node,ast.FunctionDef) and node.name=='intersection':
  exec(compile(ast.Module(body=[node],type_ignores=[]),'<intersection>', 'exec'),globals())
interfaces=[]
for ca,ma,cb,mb in [
 ('EDGE_BRANCH',Matrix.Identity(4),'CLICK_KEY',T(L+7,0,0)),
 ('EDGE_BRANCH',Matrix.Identity(4),'CLICK_KEY',T(L/2,63,0)@Rz(90)),
 ('RUNG',Matrix.Identity(4),'CLICK_KEY',T(-7,0,0)),
 ('RUNG_SLEEVE',Matrix.Identity(4),'CLICK_KEY',T(-7,0,0))]:
 penetration=intersection(ca,ma,cb,mb)
 interfaces.append({'a':ca,'b':cb,'sampled_penetration_mm':penetration});assert penetration<.01,interfaces
checks['interfaces']=interfaces
# Actual circular pipe points must remain inside the peaked bore with positive radial clearance.
profile=tear(BORE/2)
def segdist(p,a,b):
 d=Vector(b)-Vector(a);t=max(0,min(1,(Vector(p)-Vector(a)).dot(d)/d.length_squared));return (Vector(p)-(Vector(a)+t*d)).length
minimum=min(segdist((16.7*math.cos(i*math.tau/720),16.7*math.sin(i*math.tau/720)),a,b) for i in range(720) for a,b in zip(profile,profile[1:]+profile[:1]))
assert minimum>.39,minimum
checks['sampled_pipe_radial_clearance_mm']=minimum
checks['cord_to_pipe_front_clearance_mm']=PIPE_AXIS-16.7-24.2
checks['sleeve_wall_nominal_mm']=WALL
checks['no_face_attachment_fasteners']=True
me=PARTS['RUNG_SLEEVE']['object'].data
neighbors={i:set() for i in range(len(me.vertices))}
for edge in me.edges:
 a,b=edge.vertices;neighbors[a].add(b);neighbors[b].add(a)
remaining=set(neighbors);components=0
while remaining:
 components+=1;stack=[remaining.pop()]
 while stack:
  for n in neighbors[stack.pop()] & remaining:remaining.remove(n);stack.append(n)
assert components==1,components
checks['sleeve_connected_components']=components


checks['interface_method']='0.25 mm XY grid at Z 0.5/1/1.5/2.5/3.5/4.5 mm; ray inside classification, .01 mm tolerance. Sampled screen, not exhaustive proof.'
(OUT/'geometry_checks.json').write_text(json.dumps(checks,indent=2))
for name in ['01_ASSEMBLED','00_MASTERS']:
 if bpy.data.scenes.get(name):bpy.data.scenes.remove(bpy.data.scenes[name])
for sc in bpy.data.scenes:
 for ob in sc.objects:
  if ob.name.startswith('Ground'):ob.location.z=-.025
bpy.context.window.scene=bpy.data.scenes['06_INTEGRAL_PVC_SLEEVE'];bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'Sleeve_Paper_Gate.blend'))
print('BUILT',json.dumps({'pieces':sum(QTY.values()),'types':len(QTY),'plate_runs':len(EXPANDED),'cord_m':BOM['cord_total_m']}),flush=True)
if '--no-render' not in sys.argv:
 for s in bpy.data.scenes:
  bpy.context.window.scene=s;s.render.filepath=str(OUT/'renders'/f'{s.name}.png');bpy.ops.render.render(write_still=True,scene=s.name)

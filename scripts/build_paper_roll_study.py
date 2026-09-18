"""Paper-roll concept study: original no-tie joinery, magnetic clamps and stack samples.
Only explicitly exported coupons are fabrication geometry; whole-gate rails are schematics.
"""
from pathlib import Path
exec(Path(__file__).with_name('build_a1_full_size.py').read_text().split('# Registered channel splice:')[0],globals())
OUT=ROOT/'output/paper_roll_study'
for d in ['printable','renders']:(OUT/d).mkdir(parents=True,exist_ok=True)
import zipfile,xml.etree.ElementTree as ET,csv
PARTS={};PAPER_ORANGE=mat('Orange kraft paper',(.95,.24,.035));MAGNET=mat('6 x 2 neodymium',(.43,.47,.52),.8);BLUE_PRINT=STEEL
# Geometrically closed cylindrical cutters, in mm.
def cyl(name,c,r,h,material=ORANGE,n=64):return prism(name,[(c[0]+r*math.cos(t*math.tau/n),c[1]+r*math.sin(t*math.tau/n)) for t in range(n)],h,c[2],material)
def roundplate(name,L,W,h,z=0,r=3,material=ORANGE):
 pts=[]
 for cx,cy,a in [(L/2-r,W/2-r,0),(-L/2+r,W/2-r,90),(-L/2+r,-W/2+r,180),(L/2-r,-W/2+r,270)]:
  pts += [(cx+r*math.cos(math.radians(a+t*90/8)),cy+r*math.sin(math.radians(a+t*90/8))) for t in range(9)]
 return prism(name,pts,h,z,material)
def window(o,c,r,z,h=20):boolean(o,cyl('magnet pocket',(c[0],c[1],z),r,h))
# Replaceable track-style key: two in-plane forks and two rigid dovetail guide runners.
# Female samples have clearances 0.25 and 0.40 mm per side; guide geometry resists lift/shear.
GUIDE=[(-3,0),(3,0),(1,2),(-1,2)]
def add_male(o,origin,angle):
 A=T(*origin)@Rz(angle)
 for yy in [-11,11]:
  q=extrude_x('Rigid dovetail guide',[(y+yy,z) for y,z in GUIDE],14,-.1);raw_transform(q,A);add(o,q)
 for sy in [-1,1]:
  # Beam 20 mm from rounded relief root to catch; 1.6 mm nominal thickness.
  pts=[(-.15,sy*2.0),(2,sy*2.4),(24,sy*2.4),(26,sy*3.1),(24,sy*5.0),(20,sy*5.0),(20,sy*4.0),(0,sy*4.0)]
  q=prism('Cantilever fork',pts,5);raw_transform(q,A);add(o,q)
 # Round the two inner relief starts; practical root radius >=0.8 mm.
 for sy in [-1,1]:
  q=cyl('Rounded fork relief',(1,sy*1.9,-1),1.0,7);raw_transform(q,A);boolean(o,q)
o=box('Replaceable double key',(0,0,2.5),(14,32,5),ORANGE)
add_male(o,(7,0,0),0);add_male(o,(-7,0,0),180)
master('CLICK_KEY',o,'Replaceable double-ended key; XY flexures and 45-degree rigid guide runners')
for clear in [.25,.40]:
 o=box('Female track sample',(24,0,2.5),(48,32,5),STEEL)
 # Open-top center throat; catch shoulders at x=20, width grows for released hooks.
 boolean(o,box('Fork entry',(10,0,2.5),(20.05,8+2*clear,9)))
 boolean(o,box('Hook clearance',(24,0,2.5),(8,11.6,9)))
 for yy in [-11,11]:
  prof=[(-3-clear,-.1),(3+clear,-.1),(1+clear,2),(1+clear,6),(-1-clear,6),(-1-clear,2)]
  q=extrude_x('Open dovetail receiving channel',[(y+yy,z) for y,z in prof],15,-.1);boolean(o,q)
 master(f'CLICK_SOCKET_{int(clear*100):02d}',o,f'Track-style socket test; {clear:.2f} mm side clearance; press fork tips to release')
# Magnet-held alternative. Identical rail-end samples receive a removable keyed cap.
o=box('Magnetic rail-end sample',(25,0,2),(50,30,4),STEEL)
window(o,(12,0),3.15,1.8)
for y in [-9,9]:window(o,(12,y),1.8,1.0)
master('MAG_RAIL_END',o,'Rail-end coupon; one 6x2 magnet and two 3.6 mm locating holes')
o=roundplate('Magnetic keyed splice',44,28,3,material=ORANGE)
for x in [-12,12]:
 window(o,(x,0),3.15,.8)
 for y in [-9,9]:add(o,cyl('Locating pin',(x,y,2.98),1.5,2.5))
master('MAG_SPLICE_CAP',o,'Keyed magnetic bridge; two 6x2 magnets; pins carry in-plane load, magnets retain against lift')
# Literal magnet/frame/paper/magnet stack: locally thin frame windows, pressure-spreading top pad.
for skin in [.4,.8,1.2]:
 o=roundplate('Paper clamp frame coupon',70,28,4,material=STEEL)
 window(o,(0,0),3.15,skin)
 # A slot at each end permits hanging known test loads without piercing the paper.
 for x in [-27,27]:diamond(o,x,0,4,z0=-1,h=8)
 master(f'PAPER_WINDOW_{int(skin*10):02d}',o,f'Magnet behind {skin:.1f} mm local frame skin; 6.3 mm pocket; rear-load 6x2 disc')
o=roundplate('Paper pressure pad',24,24,3,r=6)
window(o,(0,0),3.15,.4)
master('PAPER_PAD',o,'Front magnet pad with 0.4 mm paper-facing skin; rear-loaded 6x2 disc')
# Pocket gauge: test actual magnets before gluing; depth is 2.2 mm from the opening.
o=box('Pocket gauge',(0,0,1.5),(52,20,3),STEEL)
for x,d in [(-17,6.1),(0,6.3),(17,6.5)]:window(o,(x,0),d/2,.8)
master('MAGNET_POCKET_GAUGE',o,'Left to right: 6.1 / 6.3 / 6.5 mm bores, 2.2 mm deep; measure supplied magnets')
# Magnet-free paper retention: end-printed rail and two snap-over batten clearances.
baseprof=[(-9,0),(9,0),(9,1),(11,1),(11,2),(10,3),(7,3),(7,2),(-7,2),(-7,3),(-10,3),(-11,2),(-11,1),(-9,1)]
o=extrude_x('Paper clamp base',baseprof,60)
master('PAPER_SNAP_BASE',o,'No-magnet paper clamp coupon; paper over the flat central face',PRINT_AXIAL)
for gap in [.15,.30]:
 # U-section with inward rounded/ramped catches; printed on an end so flex is in XY layers.
 prof=[(-12,.1),(-10.1,.1),(-10.1,.8),(-11.25,1.0),(-11.25,3.8+gap),(-6,3.8+gap),(-6,2+gap),(6,2+gap),(6,3.8+gap),(11.25,3.8+gap),(11.25,1.0),(10.1,.8),(10.1,.1),(12,.1),(12,5.2+gap),(-12,5.2+gap)]
 o=extrude_x('Snap-over batten',prof,60)
 master(f'PAPER_SNAP_CAP_{int(gap*100):02d}',o,f'End-printed paper batten, {gap:.2f} mm trial added clearance; paper slips/friction need test',PRINT_AXIAL)
# No-tie PVC clamp: two identical printed halves with two purchased M3 bolts/nuts.
for code,od in [('PVC_HALF_33',33.4),('PVC_HALF_27',26.67)]:
 ri=od/2+.2;ro=ri+4;aa=[math.pi*i/64 for i in range(65)];pts=[(ro*math.cos(a),ro*math.sin(a)) for a in aa]+[(ri*math.cos(a),ri*math.sin(a)) for a in reversed(aa)]
 o=prism('Split PVC collar half',pts,12,material=STEEL)
 ex=ro+5
 for x in [-ex,ex]:
  add(o,box('Bolt ear',(x,4,6),(14,8,12),STEEL))
  q=extrude_x('45-degree horizontal bolt passage',[(-2.4,0),(0,-2.4),(2.4,0),(0,2.4)],12,-2)
  raw_transform(q,basis((0,1,0),(1,0,0),(0,0,1),(x,0,6)));boolean(o,q)
 add(o,box('Mounting pad',(0,ro+5,6),(20,12,12),STEEL))
 for x in [-5,5]:window(o,(x,ro+6),1.7,-1,h=15)
 boolean(o,box('Clamp closing gap',(0,-30,6),(100,60.8,18)))
 master(code,o,f'Print two identical halves; {od:g} mm PVC; two M3 through-bolts/nuts; no zip ties; mounting pad for DOCK_SOCKET on the 33.4 mm version')
# Diagonal print strategy. All stacks include a removable starter foot.
def stack(name,length,count,neck=.4,tabbed=False):
 o=box(name,(length/2,0,.3),(length,20,.6),ORANGE);z=.6
 for i in range(count):
  if tabbed and i:
   for x in sorted(set(list(range(0,int(length)-1,10))+[length-2])):add(o,box('Breakaway tab',(x+1,0,z+.2),(2,neck,.44)))
  else:add(o,box('Continuous scoring neck',(length/2,0,z+.2),(length,neck,.44)))
  z+=.4
  prof=[(-neck/2,z-.02),(neck/2,z-.02),(6,z+6),(neck/2,z+12),(-neck/2,z+12),(-6,z+6)]
  add(o,extrude_x('Diamond rail',prof,length));z+=12
 return o
for code,neck,tabs in [('STACK_TEST_06',.6,False),('STACK_TEST_08',.8,False),('STACK_TEST_TABS',.6,True)]:
 master(code,stack(code,60,3,neck,tabs),f'Three short rails, {neck:g} mm '+('2 mm tabs on 10 mm pitch; 8 mm bridges' if tabs else 'continuous scoring neck')+'; separation experiment')
for count in [1,8]:
 code=f'DIAGONAL_{count}x220'
 master(code,stack(code,220,count,.6,False),f'{count} full-length 220 mm diamond-section rails; sacrificial 0.6 mm necks; 45-degree orientation; not final joinery',Rz(45))
master('DIAGONAL_13x198',stack('Thirteen shorter rails',198,13,.6,False),'Thirteen 198 mm plain rails, 0.6 mm necks; two stacks fit diagonally on one A1 Mini bed',Rz(45))
# Picture-frame-inspired D-shaped magnet lug. Flat paper face is z=0.
# The half cylinder projects into the paper area, leaving the straight rail unchanged.
pts=[(10*math.cos(math.pi*i/48),10*math.sin(math.pi*i/48)) for i in range(49)]
o=prism('Half-cylinder magnet lug',pts,3,material=STEEL)
add(o,box('Test rail flange',(0,-4,1.5),(32,8.05,3),STEEL))
window(o,(0,4.8),3.15,.4)
for x in [-11,11]:window(o,(x,-4),1.7,-1)
master('D_MAGNET_LUG',o,'Half-cylinder edge lug with 0.4 mm paper face and 6.3 mm rear pocket; two M3 holes on test flange')
# Reusable receiving geometry also serves frame nodes and the pipe dock.
def cut_socket(o,origin=(0,0,0),angle=0,clear=.4):
 A=T(*origin)@Rz(angle)
 for c,d in [((10,0,2.5),(20.05,8+2*clear,9)),((24,0,2.5),(8,11.6,9))]:
  q=box('Latch receiving relief',c,d);raw_transform(q,A);boolean(o,q)
 for yy in [-11,11]:
  pr=[(-3-clear,-.1),(3+clear,-.1),(1+clear,2),(1+clear,6),(-1-clear,6),(-1-clear,2)]
  q=extrude_x('Guide channel',[(y+yy,z) for y,z in pr],15,-.1);raw_transform(q,A);boolean(o,q)
o=box('Bolt-on dock receiver',(24,0,2.5),(48,32,5),STEEL);cut_socket(o)
for y in [-5,5]:window(o,(40,y),1.7,-1)
master('DOCK_SOCKET',o,'Click socket bolted to PVC_HALF_33 pad with two M3x22 or longer bolts and nuts; rear access for release')
o=box('Dock tongue root',(-10,0,2.5),(20,32,5));add_male(o,(0,0,0),0)
add(o,box('Vertical frame flange',(-18,0,19.5),(4,32,35)))
# Triangular central gusset; width decreases with height, so no supported ceiling.
q=prism('Dock gusset',[(-16,4.9),(-2,4.9),(-16,25)],10,-5)
raw_transform(q,basis((1,0,0),(0,0,1),(0,1,0),(0,0,0)));add(o,q)
for y in [-8,8]:
 q=extrude_x('Horizontal diamond bolt hole',[(y-2.4,25),(y,22.6),(y+2.4,25),(y,27.4)],8,-22);boolean(o,q)
master('DOCK_TONGUE',o,'One-sided releasable fork dock with vertical frame flange; two M3 frame bolts; supported by solid guide runners')
o=box('Frame docking node',(0,0,2.5),(80,32,5),STEEL)
cut_socket(o,(-40,0,0));cut_socket(o,(40,0,0),180)
for y in [-8,8]:window(o,(0,y),1.7,-1)
master('FRAME_DOCK_NODE',o,'Two opposed frame sockets and two central M3 holes; use same CLICK_KEY to connect rails; bench dock node')

# Unit-aware 3MF exports of every actual coupon.
def export3mf(name,placements):
 ns='http://schemas.microsoft.com/3dmanufacturing/core/2015/02';ET.register_namespace('',ns);root=ET.Element('{'+ns+'}model',unit='millimeter');res=ET.SubElement(root,'resources');build=ET.SubElement(root,'build')
 for i,(code,x,y) in enumerate(placements,1):
  ob=ET.SubElement(res,'object',id=str(i),type='model',name=code);me=ET.SubElement(ob,'mesh');vs=ET.SubElement(me,'vertices');ts=ET.SubElement(me,'triangles');pm=PARTS[code]['print_mesh'];pm.calc_loop_triangles()
  for v in pm.vertices:ET.SubElement(vs,'vertex',x=str(v.co.x*1000+x),y=str(v.co.y*1000+y),z=str(v.co.z*1000))
  for tr in pm.loop_triangles:ET.SubElement(ts,'triangle',v1=str(tr.vertices[0]),v2=str(tr.vertices[1]),v3=str(tr.vertices[2]))
  ET.SubElement(build,'item',objectid=str(i))
 with zipfile.ZipFile(OUT/'printable'/f'{name}.3mf','w',zipfile.ZIP_DEFLATED) as z:
  z.writestr('[Content_Types].xml','<Types xmlns="http://schemas.openxmlformats-package.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/></Types>'.replace('openxmlformats-package.org/package','openxmlformats.org/package'))
  z.writestr('_rels/.rels','<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Target="/3D/3dmodel.model" Id="rel0" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/></Relationships>');z.writestr('3D/3dmodel.model',ET.tostring(root,encoding='utf-8',xml_declaration=True))
for code in PARTS:export3mf(code,[(code,5,5)])
PLATES={
 '01_CLICK_AND_MAGNET_JOINTS':[('CLICK_KEY',5,5),('CLICK_SOCKET_25',78,5),('CLICK_SOCKET_40',78,44),('MAG_RAIL_END',5,86),('MAG_RAIL_END',62,86),('MAG_SPLICE_CAP',120,86)],
 '02_PAPER_CLAMP_TESTS':[('PAPER_WINDOW_04',5,5),('PAPER_WINDOW_08',81,5),('PAPER_WINDOW_12',5,40),('PAPER_PAD',82,41),('MAGNET_POCKET_GAUGE',112,42),('PAPER_SNAP_BASE',5,84),('PAPER_SNAP_CAP_15',38,84),('PAPER_SNAP_CAP_30',71,84)],
 '03_STACK_SEPARATION_TESTS':[('STACK_TEST_06',5,5),('STACK_TEST_08',75,5),('STACK_TEST_TABS',5,40)],
 '04_PVC_COLLAR_TEST':[('PVC_HALF_33',5,5),('PVC_HALF_33',80,5),('PVC_HALF_27',5,60),('PVC_HALF_27',80,60)],
 '05_D_MAGNET_AND_DOCK':[('D_MAGNET_LUG',5,5),('PAPER_PAD',44,5),('DOCK_SOCKET',75,5),('DOCK_TONGUE',5,50),('FRAME_DOCK_NODE',70,50),('PVC_HALF_33',5,100),('PVC_HALF_33',80,100)],
 '06_OVERNIGHT_26_RAILS':[('DIAGONAL_13x198',5+22/math.sqrt(2),5),('DIAGONAL_13x198',5,5+22/math.sqrt(2))]}
for name,items in PLATES.items():export3mf(name,items)
rows=[dict(code=k,**{a:b for a,b in p.items() if a not in ['object','print_mesh']}) for k,p in PARTS.items()]
(OUT/'PROTOTYPE_PARTS.json').write_text(json.dumps({'parts':rows,'plates':PLATES,'production_BOM':False},indent=2))
with (OUT/'PROTOTYPE_PARTS.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=['code','description','print_bounds_mm','file'],extrasaction='ignore',lineterminator='\n');w.writeheader();w.writerows(rows)
# Presentation instances use exact coupon solids; overview rails are explicitly schematic.
def show(code,loc=(0,0,0),rotation=None,printpose=False):
 p=PARTS[code];ob=bpy.data.objects.new(code,p['print_mesh'] if printpose else p['object'].data);COL.objects.link(ob);ob.location=tuple(v/1000 for v in loc)
 if rotation is not None:ob.matrix_world=T(*loc)@rotation
 return ob
S,WID=2700,609.6;BL=S-WID
setup('01_PAPER_GATE',(-3.5,-7.8,4.2),(.6,0,1.45),6.6);coll('01 / architecture only')
for k in range(4):
 M=T(S/2,0,S/2)@Matrix.Rotation(math.radians(-90*k),4,'Y')@T(-S/2,0,BL-S/2)
 q=box('One uncut-width paper strip',(BL/2,0,WID/2),(BL,.18,WID),PAPER_ORANGE);q.matrix_world=M
 # Schematic triangulated strip; printable production rails/nodes follow coupon selection.
 def beam(a,b):tube('Schematic printed support, NOT a production STL',M@Vector(tuple(v/1000 for v in a)),M@Vector(tuple(v/1000 for v in b)),.010,STEEL)
 for z in [12,WID/2,WID-12]:beam((12,10,z),(BL-12,10,z))
 for j in range(11):
  x=12+j*(BL-24)/10;beam((x,10,12),(x,10,WID-12))
 for j in range(10):
  xa=12+j*(BL-24)/10;xb=12+(j+1)*(BL-24)/10
  for row in range(2):
   za=12+row*(WID-24)/2;zb=za+(WID-24)/2
   beam((xa,10,za if j%2==0 else zb),(xb,10,zb if j%2==0 else za))
 # Magnetic pad locations at maximum 150 mm perimeter pitch plus 300 mm middle rail.
 pts=set()
 for z in [12,WID-12]:
  for j in range(15):pts.add((round(12+j*(BL-24)/14,3),z))
 for x in [12,BL-12]:
  for j in range(5):pts.add((x,12+j*(WID-24)/4))
 for j in range(1,7):pts.add((round(12+j*(BL-24)/7,3),WID/2))
 for x,z in pts:
  q=show('D_MAGNET_LUG');q.matrix_world=M@basis((1,0,0),(0,0,1),(0,1,0),(x,0,z))
for z in [300,2400]:tube('Single purchased PVC backing frame',(.3,92/1000,z/1000),(2.4,92/1000,z/1000),.0334,WHITE,.003)
for x in [.3,2.4]:tube('Single purchased PVC backing frame',(x,.092,.3),(x,.092,2.4),.0334,WHITE,.003)
for sx,sz in [(1,1),(-1,1),(1,-1),(-1,-1)]:
 x=1.35+sx*1.05;z=1.35+sz*1.05;tube('PVC corner brace',(x-sx*.4,.092,z),(x,.092,z-sz*.4),.02667,WHITE,.0028)
# Center gate for presentation.
for ob in list(COL.objects):ob.location.x-=1.35
header('01','Paper-roll gate / three joint strategies','A: clicks + snap battens. B: keyed magnetic joints + magnetic pads. C: click frame + magnetic pads (recommended experiment).')
overlay('2700 mm outside\n1480.8 mm opening\n609.6 mm paper width',.73,.35,.017,True)
overlay('Four strips: 2090.4 mm each\nThree complete gates per 100 ft roll\nZero zip ties in proposed joinery',.66,.57,.014)
footer('Architecture study: rails/nodes are schematic. Exported STLs are test coupons; a production gate BOM and wind performance are not yet validated.')
setup('02_CLICK_JOINT',(.08,-.23,.19),(0,0,.006),.32,False);coll('01 / replaceable click key')
show('CLICK_KEY');show('CLICK_SOCKET_25',(42,0,0));show('CLICK_SOCKET_40',(-42,0,0),Rz(180))
header('02','Replaceable click key / exploded','Rigid dovetail guides take alignment and lift loads. Two in-plane fork latches prevent axial pullout; pinch both prongs to release.')
footer('Test 0.25 and 0.40 mm socket clearances. Original prototype geometry, not a Kato-compatible part. Verify both guide fit and complete hook engagement.')
setup('03_MAGNETIC_SPLICE',(.10,-.19,.20),(.006,0,.018),.20,False);coll('01 / magnetic joint coupon')
show('MAG_RAIL_END',(0,0,0));show('MAG_RAIL_END',(0,0,0),Rz(180));show('MAG_SPLICE_CAP',(0,0,16),Matrix.Diagonal((1,1,-1,1)))
for x in [-12,12]:q=cyl('Purchased 6 x 2 mm magnet',(x,0,1.8),3,2,MAGNET)
header('03','Magnets retain; pins locate','Two identical rail-end samples and one keyed cap. Four 6 x 2 mm magnets per completed joint; separate by lifting the cap.')
footer('This joint can release under peel. It is a comparison coupon, not an approved structural gate connector. Magnetic pull is not a shear rating.')
setup('04_PAPER_MAGNET_STACK',(.10,-.19,.18),(0,0,.014),.21,False);coll('01 / paper sandwich')
show('PAPER_WINDOW_04');box('Paper coupon',(0,0,-.4),(85,45,.18),PAPER_ORANGE)
q=cyl('Rear 6x2 magnet',(0,0,6),3,2,MAGNET)
show('PAPER_PAD',(0,0,-12),Matrix.Diagonal((1,1,-1,1)));q=cyl('Front 6x2 magnet',(0,0,-19),3,2,MAGNET)
header('04','Magnet / thin frame / paper / magnet','Compare 0.4, 0.8 and 1.2 mm frame skins. The broad front pad adds a 0.4 mm skin to spread pressure and protect the paper.')
footer('Rear-load pockets. Check polarity and pocket size before adhesive retention. Test normal pull, edge peel and sliding with the actual roll paper.')
setup('05_MECHANICAL_PAPER_CLAMP',(.08,-.16,.12),(.03,0,.008),.16,False);coll('01 / no-magnet paper clamp')
show('PAPER_SNAP_BASE');show('PAPER_SNAP_CAP_15',(0,0,10));box('Paper edge',(30,0,4),(70,16,.18),PAPER_ORANGE)
header('05','Snap-over paper batten','A magnet-free comparison: push the cap over the paper and base. Print both end-up so the spring section lies within print layers.')
footer('Two clearance trials are supplied. Assess paper slip, creasing and release; clamping thin paper without tearing it is not yet demonstrated.')
setup('06_NO_TIE_PVC_COLLAR',(.09,-.12,.11),(0,0,.006),.15,False);coll('01 / collar halves')
show('PVC_HALF_33',(0,6,0));show('PVC_HALF_33',(0,-6,0),Rz(180))
header('06','PVC collar without zip ties','Two identical halves; two M3 bolts, nuts and washers provide clamp preload. This workshop attachment can stay on the pipe.')
footer('Use the mating dock in scene 13 for the 33.4 mm collar. A production angled brace node remains to be designed after collar grip tests.')
setup('07_DIAGONAL_STACK',(.28,-.38,.28),(.11,0,.045),.39,False);coll('01 / diagonal eight-rail stack')
show('DIAGONAL_8x220');header('07','Eight long rails in one vertical stack','220 mm rails. Diamond sections expand at 45 degrees above 0.6 mm sacrificial necks. Starter foot is removed with the separators.')
footer('Exact print-strategy coupon, shown before bed rotation. Same-material PETG necks fuse: separation force and damage must be tested, not assumed.')
setup('08_STACK_COUPONS',(.1,-.20,.20),(.11,.025,.016),.34,False);coll('01 / three separation methods')
for j,code in enumerate(['STACK_TEST_06','STACK_TEST_08','STACK_TEST_TABS']):show(code,(j*80,0,0))
header('08','Score, cut or break: compare first','Three short stacks: 0.6 mm continuous neck, 0.8 mm continuous neck, and 2 mm tabs with 8 mm bridges between them.')
footer('Print this low-cost plate before a tall run. Record separation effort, scars, straightness and layer damage. Tab bridges may sag; inspect the sliced preview.')
setup('09_A1_DIAGONAL_ENVELOPE',(.20,-.31,.40),(.085,.085,.01),.32,False);coll('01 / 180 mm bed envelope')
box('A1 Mini bed',(90,90,-1),(180,180,2),GROUND);show('DIAGONAL_1x220',(5,5,0),printpose=True)
header('09','The diagonal has a width budget','With 5 mm edge margin: rail length + maximum width <= 240.4 mm. The 220 x 20 mm sample occupies 169.7 x 169.7 mm.')
footer('All tongues, hooks, starter feet and brims count. The nominal 254.6 mm diagonal is a zero-width line; stack height must independently fit below 180 mm.')
# Source model is embedded as a reference, credited and separately licensed.
setup('10_PICTURE_FRAME_REFERENCE',(.14,-.13,.19),(.05,.045,.015),.31,False);coll('01 / Tony Youngblood reference CC BY-SA 4.0')
for name,xy in [('ModularFrame2Inch',(0,0)),('ModularFrameCorner',(0,65)),('ModularFrameCalibrator',(80,0))]:
 bpy.ops.wm.stl_import(filepath=str(ROOT/'reference/picture_frame'/f'{name}.stl'))
 o=bpy.context.object;link(o);o.data.materials.append(ORANGE)
 for v in o.data.vertices:v.co/=1000
 lo=Vector([min(v.co[j] for v in o.data.vertices) for j in range(3)])
 for v in o.data.vertices:v.co-=lo
 o.location=(xy[0]/1000,xy[1]/1000,0)
 o['attribution']='Tony Youngblood / Snap-Together Modular Picture Frame / CC BY-SA 4.0 / scale and presentation placement only'
header('10','Your picture-frame reference','Repeated snap teeth, modular lengths and a calibration coupon. Adapt the concept with accessible release and rigid alignment guides.')
footer('Tony Youngblood, CC BY-SA 4.0. Source instructions require supports under some edges; these reference meshes are not in our support-free print kit.')
# Three bracing options, all use the same 2090.4 x 609.6 paper strip envelope.
setup('11_BRACING_COMPARISON',(.001,-4.5,1.33),(0,0,1.33),4.8,False);coll('01 / schematic comparison')
metrics=[]
for row,kind in enumerate(['LADDER','ALTERNATING','CROSSHATCH']):
 zz=1.8-row*.76;X=(BL-24)/1000;Y=(WID-24)/1000;cx=-X/2
 edges=[]
 for z in [0,Y/2,Y]:edges.append(((0,z),(X,z)))
 for j in range(11):edges.append(((j*X/10,0),(j*X/10,Y)))
 if kind!='LADDER':
  for j in range(10):
   for k in range(2):
    a,b=j*X/10,(j+1)*X/10;c,d=k*Y/2,(k+1)*Y/2
    edges.append(((a,c if j%2==0 else d),(b,d if j%2==0 else c)))
    if kind=='CROSSHATCH':edges.append(((a,d if j%2==0 else c),(b,c if j%2==0 else d)))
 for (a,c),(b,d) in edges:tube(kind+' / conceptual beam',(cx+a,0,zz+c),(cx+b,0,zz+d),.009,STEEL if kind!='CROSSHATCH' else ORANGE)
 length=sum(math.dist(a,b) for a,b in edges)
 metrics.append({'option':kind,'rail_m_per_border':length,'rail_m_per_gate':length*4,'members_per_border':len(edges)})
 text(kind,kind+'   /   '+f'{length:.2f} m of members per border',(-X/2,-.012,zz-.075),.043,INK)
header('11','Join the two edges with triangles','Ladder: simplest, relies on stiff joints. Alternating diagonals: preferred trial. Crosshatch: redundancy at higher material and joint count.')
footer('All three include a middle support rail. Geometry comparison only: identical sections assumed; joint compliance, bending and wind performance need physical tests.')
(OUT/'BRACING_COMPARISON.json').write_text(json.dumps(metrics,indent=2))
setup('12_HALF_CYLINDER_LUG',(.085,-.095,.09),(0,0,.007),.115,False);coll('01 / exact half-cylinder clamp')
show('D_MAGNET_LUG');q=cyl('Rear 6 x 2 magnet',(0,4.8,7),3,2,MAGNET)
box('Paper coupon',(0,9,-3),(45,32,.18),PAPER_ORANGE)
show('PAPER_PAD',(0,4.8,-12),Matrix.Diagonal((1,1,-1,1)))
header('12','Half-cylinder magnet holders','A D-shaped tab projects inside the rail. Rear magnet sits behind a 0.4 mm window; a removable front pad sandwiches the paper.')
footer('Exploded. Same lug works along an edge; rotate it at corners. Flat flange is a bolt-on test interface, to become an integral rail/node feature after fit tests.')
# Exact pipe collar / snap socket / tongue / frame node assembly and exploded copy.
setup('13_FRAME_TO_PVC',(.28,-.40,.27),(.005,.045,.045),.48,False);coll('01 / assembled dock and exploded dock')
for ox,explode in [(-60,False),(75,True)]:
 show('PVC_HALF_33',(ox,0,0));show('PVC_HALF_33',(ox,0,0),Rz(180))
 tube('Purchased 33.4 mm OD PVC',(ox/1000,0,-.035),(ox/1000,0,.075),.0334,WHITE,.003)
 # Socket mounting holes x=40 map onto collar pad y=26.9, x=+/-5.
 A=T(ox,66.9,12 if not explode else 30)@Rz(-90)
 q=show('DOCK_SOCKET');q.matrix_world=A
 q=show('DOCK_TONGUE');q.matrix_world=A@T(-18 if explode else 0,0,0)
 # Front node: native XY => flange Z,Y; native Z => flange -X.
 N=basis((0,0,1),(0,1,0),(-1,0,0),(-20 if not explode else -45,0,25))
 q=show('FRAME_DOCK_NODE');q.matrix_world=A@N
 # Purchased fasteners shown at final registered hole locations in assembled copy.
 if not explode:
  for xx in [-5,5]:tube('M3 socket mounting bolt',( (ox+xx)/1000,.0269,-.003),((ox+xx)/1000,.0269,.019),.003,METAL)
  for yy in [-8,8]:
   a=A@Vector((-.027,yy/1000,.025));b=A@Vector((-.013,yy/1000,.025));tube('M3 frame flange bolt',a,b,.003,METAL)
header('13','Frame node clicks into a PVC dock','Left: assembled. Right: exploded. Bolt the receiver to the split collar; slide in the frame tongue until both catches engage.')
footer('Collar stays on PVC; frame tongue stays on the border. Pinch both fork tips at the open rear throat to withdraw. Positive guides carry load; latch retains.')

setup('14_GATE_BACKING_AND_LOAD_PATH',(-3.5,7.8,4.4),(0,0,1.6),6.5,False);coll('01 / architecture with paper removed')
source=next(c for c in bpy.data.scenes['01_PAPER_GATE'].collection.children if 'architecture only' in c.name)
for src in source.objects:
 if src.name.startswith('One uncut-width paper strip'):continue
 ob=src.copy();COL.objects.link(ob)
header('14','One PVC back / four triangulated borders','Paper removed. Edge rails and diagonal webs feed the center rail; four spaced docks per border transfer load to the PVC backing.')
# Four dock positions per border, schematic orange collars on the center rail.
for k in range(4):
 M=T(S/2-1350,0,S/2)@Matrix.Rotation(math.radians(-90*k),4,'Y')@T(-S/2,0,BL-S/2)
 for x in [320,800,1280,1760]:
  q=box('Proposed dock site / see exact joint in scene 13',(x,46,WID/2),(45,88,32),ORANGE);q.matrix_world=M
footer('Dock positions and rail/node geometry are conceptual. PVC remains the primary backbone. Add staked or ballasted feet for the surface; the paper is not structural bracing.')
setup('15_TWO_STACKS_OVERNIGHT',(.26,-.32,.30),(.09,.09,.09),.53,False);coll('01 / exact 26-rail plate')
box('A1 Mini bed',(90,90,-1),(180,180,2),GROUND)
for code,x,y in PLATES['06_OVERNIGHT_26_RAILS']:show(code,(x,y,0),printpose=True)
header('15','More rails per overnight batch','Two diagonal stacks, 13 rails each: 26 x 198 mm. A 2 mm gap separates the starter feet; overall footprint 169.7 mm square.')
footer('161.8 mm tall. Shorter rails trade more eventual joints for 1.8x the rail length per batch versus thirteen 220 mm rails. Test short neck coupons first.')

for name in ['01_ASSEMBLED','00_MASTERS']:
 s=bpy.data.scenes.get(name)
 if s:bpy.data.scenes.remove(s)
start=bpy.data.texts.new('START_HERE.txt');start.write('PAPER ROLL / CLICK + MAGNET + STACK STUDY\nBaseline commit 732f592.\nRead RESEARCH.md, STUDY_AND_TEST_GUIDE.md and PRINT_STRATEGY.md.\nAll exported STLs are experimental coupons. The full gate scene is an architectural layout, not a completed production kit.\n')
bpy.context.window.scene=bpy.data.scenes['01_PAPER_GATE'];bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'Paper_Roll_Joinery_Study.blend'))
for name in os.environ.get('RENDER_SCENES',','.join(s.name for s in bpy.data.scenes)).split(','):
 if name:s=bpy.data.scenes[name];bpy.context.window.scene=s;s.render.filepath=str(OUT/'renders'/f'{name}.png');bpy.ops.render.render(write_still=True,scene=name)
print('STUDY BUILT',len(PARTS),'unique test parts,',len(PLATES),'comparison plates')

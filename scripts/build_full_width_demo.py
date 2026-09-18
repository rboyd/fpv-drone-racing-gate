"""Actual 24 x 8 inch magnetic paper-frame demonstration. Four main printed types."""
from pathlib import Path
exec(Path(__file__).with_name('build_a1_full_size.py').read_text().split('# Registered channel splice:')[0],globals())
import ast,xml.etree.ElementTree as ET,csv
OUT=ROOT/'output/full_width_demo'
for d in ['printable','renders']:(OUT/d).mkdir(parents=True,exist_ok=True)
PARTS={};GUIDE=[(-3,0),(3,0),(1,2),(-1,2)]
source=ast.parse(Path(__file__).with_name('build_paper_roll_study.py').read_text())
for node in source.body:
 if isinstance(node,ast.FunctionDef) and node.name in ['cyl','roundplate','window','add_male','cut_socket','export3mf']:
  exec(compile(ast.Module(body=[node],type_ignores=[]),'<study helpers>','exec'),globals())
PAPER_ORANGE=mat('Roll paper / orange',(.92,.27,.045));MAGNET=mat('Magnets / metal',(.42,.45,.48),.8)
L=141.9;RUNG=111.2;PITCH=L+14;W=609.6;H=203.2
# Both longitudinal sockets and one perpendicular socket use the verified .40 mm interface.
o=box('Three-way edge rail',(L/2,0,2.5),(L,32,5),STEEL)
for x in [L/4,3*L/4]:
 pts=[(x+10*math.cos(math.pi*i/48),15.95+10*math.sin(math.pi*i/48)) for i in range(49)]
 add(o,prism('Integral D magnet lug',pts,3,material=STEEL));window(o,(x,20.75),3.15,.4)
cut_socket(o);cut_socket(o,(L,0,0),180);cut_socket(o,(L/2,16,0),270)
master('DEMO_EDGE',o,'141.9 mm edge rail; three .40 mm click sockets and two integral D magnet holders')
o=box('Short crossmember',(RUNG/2,0,2.5),(RUNG,32,5),STEEL)
cut_socket(o);cut_socket(o,(RUNG,0,0),180)
master('DEMO_RUNG',o,'111.2 mm crossmember; two .40 mm click sockets')
o=box('Replaceable double click key',(0,0,2.5),(14,32,5),ORANGE);add_male(o,(7,0,0),0);add_male(o,(-7,0,0),180)
master('CLICK_KEY',o,'Shared replaceable double-ended click key; pinch both prongs at each end to release')
o=roundplate('Front paper pad',24,24,3,r=6);window(o,(0,0),3.15,.4)
master('PAPER_PAD',o,'Front magnetic pressure pad; rear-load one 6 x 2 mm magnet against .4 mm skin')
for clr in [.25,.4]:
 o=box('Fit-check receiver',(24,0,2.5),(48,32,5),STEEL);cut_socket(o,clear=clr)
 master('FIT_SOCKET_'+str(int(clr*100)),o,f'Fit check only: {clr:g} mm side clearance')
o=box('Magnet gauge',(0,0,1.5),(52,20,3),STEEL)
for x,d in [(-17,6.1),(0,6.3),(17,6.5)]:window(o,(x,0),d/2,.8)
master('MAGNET_GAUGE',o,'Fit check only: left/middle/right 6.1, 6.3, 6.5 mm bores')
PLATES={
 '00_FIT_CHECK':[('CLICK_KEY',5,5),('FIT_SOCKET_25',76,5),('FIT_SOCKET_40',76,42),('MAGNET_GAUGE',5,43),('PAPER_PAD',5,70)],
 '01_FRAME_REPEAT_4_TIMES':[('DEMO_EDGE',5,5),('DEMO_EDGE',5,51.5),('DEMO_RUNG',5,99),('CLICK_KEY',5,136),('CLICK_KEY',75,136),('PAPER_PAD',121,99),('PAPER_PAD',148,99)],
 '02_KEYS_AND_PADS_ONCE':[('CLICK_KEY',5+70*x,5+35*y) for x in range(2) for y in range(3)]+[('PAPER_PAD',5+28*x,114+28*y) for x in range(4) for y in range(2)]}
for code in PARTS:export3mf(code,[(code,5,5)])
for name,items in PLATES.items():export3mf(name,items)
QTY={'DEMO_EDGE':8,'DEMO_RUNG':4,'CLICK_KEY':14,'PAPER_PAD':16}
rows=[dict(code=k,quantity=QTY.get(k,0),**{a:b for a,b in p.items() if a not in ['object','print_mesh']}) for k,p in PARTS.items()]
(OUT/'BOM.json').write_text(json.dumps({'assembled_mm':[W,H,8.2],'parts':rows,'plates':PLATES,'plate_runs':{'00_FIT_CHECK':1,'01_FRAME_REPEAT_4_TIMES':4,'02_KEYS_AND_PADS_ONCE':1},'main_frame_pieces':42,'main_unique_types':4,'magnets_6x2':32,'paper_mm':[W,H]},indent=2))
with (OUT/'BOM.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=['code','quantity','description','print_bounds_mm','file'],extrasaction='ignore',lineterminator='\n');w.writeheader();w.writerows(rows)
# All assembly views use exact exported master solids and transforms.
PLACEMENTS=[]
for i in range(4):
 x=i*PITCH
 PLACEMENTS += [('DEMO_EDGE',T(x,16,0)),('DEMO_EDGE',T(W-x,H-16,0)@Rz(180)),('DEMO_RUNG',T(x+L/2,46,0)@Rz(90)),('CLICK_KEY',T(x+L/2,39,0)@Rz(90)),('CLICK_KEY',T(x+L/2,164.2,0)@Rz(90))]
 if i<3:
  PLACEMENTS += [('CLICK_KEY',T(x+L+7,16,0)),('CLICK_KEY',T(x+L+7,H-16,0))]
# Magnet centers, one pair per D lug.
MAG_SITES=[]
for i in range(4):
 for dx in [L/4,3*L/4]:MAG_SITES += [(i*PITCH+dx,36.75),(W-i*PITCH-dx,H-36.75)]
def inst(code,M=Matrix.Identity(4)):
 o=bpy.data.objects.new(code,PARTS[code]['object'].data);COL.objects.link(o);o.matrix_world=M;return o
def draw_frame():
 for code,M in PLACEMENTS:inst(code,M)
setup('01_FULL_WIDTH_FRAME',(.36,-.63,.64),(.3048,.10,.01),.87,False);coll('01 / exact click frame')
draw_frame()
header('01','24-inch paper frame / actual printable parts','609.6 x 203.2 mm. Eight identical edge rails, four crossmembers and fourteen replaceable click keys. All joints release from the rear.')
footer('Four main printed types including the front pads. This ladder specimen tests click fit, full-width handling and paper grip; it is not a wind-rated gate border.')
setup('02_PAPER_AND_MAGNETS',(.34,-.56,.58),(.3048,.10,-.005),.87,False);coll('01 / exploded paper and pads')
draw_frame();box('Full-roll-width paper, exploded',(W/2,H/2,-22),(W,H,.18),PAPER_ORANGE)
for x,y in MAG_SITES:
 inst('PAPER_PAD',T(x,y,-43)@Matrix.Diagonal((1,1,-1,1)));cyl('Rear magnet, exploded',(x,y,12),3,2,MAGNET)
header('02','Cut one 8-inch length from the 24-inch roll','Thirty-two 6 x 2 mm magnets form sixteen pairs. Integral D-shaped lugs carry the rear magnets; front pads spread pressure on the paper.')
footer('Exploded vertically. Assemble paper against the smooth front face (z=0). Check polarity and magnet fit before bonding magnets into their pockets.')
setup('03_ASSEMBLY_SEQUENCE',(.39,-.6,.62),(.3048,.13,.012),.90,False);coll('01 / separated assemblies')
# Explode top rail away; crossmembers each use a key at both ends.
for code,M in PLACEMENTS:
 pos=M.translation*1000
 shift=0
 if code=='DEMO_EDGE' and pos.y>100:shift=70
 elif code=='CLICK_KEY' and pos.y>160:shift=45
 elif code=='DEMO_RUNG':shift=20
 inst(code,T(0,shift,0)@M)
header('03','Two long edges, then four crossmembers','Build each 609.6 mm edge with four rails and three keys. Add a key to each end of each crossmember, then close the second edge across all four.')
footer('Keep the D lugs facing inward and all pockets on the rear. Engage the rigid guides straight; inspect both hooks. Fit-check first before printing four repeat plates.')
setup('04_REPEAT_PRINT_PLATE',(.21,-.27,.38),(.09,.085,.00),.34,False);coll('01 / seven parts on A1 Mini')
box('A1 Mini 180 mm bed',(90,90,-1),(180,180,2),GROUND)
for code,x,y in PLATES['01_FRAME_REPEAT_4_TIMES']:
 ob=bpy.data.objects.new(code,PARTS[code]['print_mesh']);COL.objects.link(ob);ob.location=(x/1000,y/1000,0)
header('04','Print this plate four times','Each run: two edge rails, one crossmember, two keys and two front pads. A separate single plate supplies the remaining six keys and eight pads.')
footer('Manual plate changes are required on the A1 Mini. Ordinary flat printing preserves the click flexures; this kit does not depend on untested break-apart stacks.')
# Screen four representative mating arrangements by sampled ray classification.
coll('99 / check objects');tests=[]
def intersection(code,A,other,B):
 # Ray entry/exit classification avoids ambiguous coplanar Boolean faces and edge normals.
 from mathutils.bvhtree import BVHTree
 data=[]
 for name,M in [(code,A),(other,B)]:
  me=PARTS[name]['object'].data;me.calc_loop_triangles();vs=[M@v.co for v in me.vertices]
  tree=BVHTree.FromPolygons(vs,[tuple(t.vertices) for t in me.loop_triangles],all_triangles=True)
  lo=[min(v[j] for v in vs)*1000 for j in range(3)];hi=[max(v[j] for v in vs)*1000 for j in range(3)]
  data.append((tree,lo,hi))
 low=[max(a[1][j] for a in data) for j in range(3)];high=[min(a[2][j] for a in data) for j in range(3)]
 deepest=0;where=None;direction=Vector((.317,.527,.789)).normalized()
 for ix in range(math.ceil(low[0]*4),math.floor(high[0]*4)+1):
  for iy in range(math.ceil(low[1]*4),math.floor(high[1]*4)+1):
   for z in [.5,1,1.5,2.5,3.5,4.5]:
    point=Vector((ix/4000,iy/4000,z/1000));inside=[]
    for tree,_,_ in data:
     hit,normal,_,_=tree.ray_cast(point,direction)
     if hit is not None and normal.dot(direction)>0:
      _,_,_,distance=tree.find_nearest(point);inside.append(distance*1000)
     else:inside.append(0)
    if min(inside)>deepest:deepest=min(inside);where=(ix/4,iy/4,z,inside)
 if deepest>.01:print("SAMPLED COLLISION",where,flush=True)
 return deepest
for ca,A,cb,B in [
 ('DEMO_EDGE',T(0,16,0),'CLICK_KEY',T(L+7,16,0)),
 ('DEMO_EDGE',T(0,16,0),'CLICK_KEY',T(L/2,39,0)@Rz(90)),
 ('DEMO_RUNG',T(L/2,46,0)@Rz(90),'CLICK_KEY',T(L/2,39,0)@Rz(90)),
 ('DEMO_EDGE',T(W,H-16,0)@Rz(180),'CLICK_KEY',T(W-L/2,164.2,0)@Rz(90))]:
 v=intersection(ca,A,cb,B);tests.append({'a':ca,'b':cb,'max_sampled_penetration_mm':round(v,5)});assert v<.01,tests
(OUT/'assembly_checks.json').write_text(json.dumps({'method':'Ray entry/exit classification plus nearest-surface distance sampled on 0.25 mm XY grid at Z=0.5/1/1.5/2.5/3.5/4.5 mm. Surface contact tolerance 0.01 mm. This sampling is not an exhaustive collision proof or physical fit test.','interfaces':tests},indent=2))
# Assembly frame-envelope and counts use source meshes, not nominal labels.
co=[]
for code,M in PLACEMENTS:co += [M@v.co for v in PARTS[code]['object'].data.vertices]
bounds=[(max(v[j] for v in co)-min(v[j] for v in co))*1000 for j in range(3)]
assert abs(bounds[0]-W)<.01 and abs(bounds[1]-H)<.01,bounds
assert len(PLACEMENTS)==26 and len(MAG_SITES)==16
for name in ['01_ASSEMBLED','00_MASTERS']:
 if bpy.data.scenes.get(name):bpy.data.scenes.remove(bpy.data.scenes[name])
bpy.context.window.scene=bpy.data.scenes['01_FULL_WIDTH_FRAME'];bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'Full_Width_Demo.blend'))
for s in bpy.data.scenes:
 bpy.context.window.scene=s;s.render.filepath=str(OUT/'renders'/f'{s.name}.png');bpy.ops.render.render(write_still=True,scene=s.name)
print('DEMO BUILT',bounds,'frame pieces',len(PLACEMENTS),'pads',len(MAG_SITES))

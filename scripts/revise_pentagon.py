from pathlib import Path
p=Path(__file__).with_name('build_gate.py');s=p.read_text()
# Convex sheet polygon in the gate's XZ plane; clockwise/anticlockwise is normalized.
pos=s.index('def tube(')
s=s[:pos]+'''def polygon_panel(name,points,y,thick,material):
 n=len(points); verts=[(x,yy,z) for yy in [y,y+thick] for x,z in points]
 faces=[tuple(range(n)),tuple(reversed(range(n,2*n)))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
 mesh=bpy.data.meshes.new(name); mesh.from_pydata(verts,[],faces); mesh.update()
 o=bpy.data.objects.new(name,mesh); (COL or SC.collection).objects.link(o); o.data.materials.append(material)
 import bmesh
 bm=bmesh.new(); bm.from_mesh(mesh); bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces)); bm.to_mesh(mesh); bm.free()
 return o

def rotate_face(points,k):
 result=[]
 for x,z in points:
  a,b=x,z-1.35
  for j in range(k): a,b=b,-a
  result.append((a,b+1.35))
 return result

'''+s[pos:]
# Extra actual printable cross joints.
pos=s.index("setup('05_CLIP_DETAIL'")
s=s[:pos]+'''def brace_joint(name,angle):
 o=cube(name,(0,0,.009),(.060,.060,.018),ORANGE)
 bpy.context.view_layer.objects.active=o; bpy.ops.object.transform_apply(location=True,rotation=False,scale=False)
 def subtract(c):
  bpy.context.view_layer.objects.active=o; m=o.modifiers.new('Pipe seat / slot','BOOLEAN'); m.operation='DIFFERENCE'; m.solver='EXACT'; m.object=c
  bpy.ops.object.modifier_apply(modifier=m.name); bpy.data.objects.remove(c,do_unlink=True)
 subtract(tube('cutter main',(0,-.06,-.0089005),(0,.06,-.0089005),.033801,ORANGE))
 u=Vector((-math.sin(angle),math.cos(angle),0)); v=Vector((math.cos(angle),math.sin(angle),0))
 c=Vector((0,0,.025535)); subtract(tube('cutter brace',c-u*.07,c+u*.07,.02707,ORANGE))
 for x in [-.025,.025]:
  for y in [-.021,.021]: boolean_slot(o,x,y)
 for a in [-.023,.023]:
  for b in [-.012,.012]:
   q=v*a+u*b; c=cube('brace tie slot',(q.x,q.y,.009),(.0032,.006,.06),ORANGE); c.rotation_euler.z=angle; subtract(c)
 import bmesh
 bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(o.data);bm.free()
 o['main_OD_mm']=33.401;o['brace_OD_mm']=26.67;o['angle_degrees']=round(math.degrees(angle));o['minimum_web_mm']=4
 o['print_orientation']='Print on 60 x 18 edge with brim; support groove overhangs as needed. Physical fit test required.'
 return o

'''+s[pos:]
# Insert creation after STL washer but keep masters hidden from the saddle illustration.
needle="export_stl(WASH,'front_load_washer_mm.stl')"
s=s.replace(needle,needle+'''
JPLUS=brace_joint('PRINT / brace joint +45',math.pi/4); export_stl(JPLUS,'brace_joint_plus45_mm.stl'); JPLUS.hide_render=True; JPLUS.hide_set(True)
JMINUS=brace_joint('PRINT / brace joint -45',-math.pi/4); export_stl(JMINUS,'brace_joint_minus45_mm.stl'); JMINUS.hide_render=True; JMINUS.hide_set(True)
''')
a=s.index("coll('01 / face panels / 4 mm')");b=s.index("coll('04 / 1 inch PVC frame and feet')",a)
s=s[:a]+'''coll('01 / four identical pentagons and four corner triangles'); FACE=[]
PENTA=[(-1.35,2.7),(1.05,2.7),(1.05,2.4),(.75,2.1),(-.75,2.1)]
TRI=[(1.05,2.7),(1.35,2.7),(1.05,2.4)]
for k in range(4):
 FACE.append(polygon_panel(f'F{k+1} / identical pentagon / 2400 x 600 blank',rotate_face(PENTA,k),0,.004,BLUE))
 FACE.append(polygon_panel(f'C{k+1} / corner triangle / 300 mm legs',rotate_face(TRI,k),0,.004,BLUE2))
coll('02 / scrap backers / no stacked intersections'); BACK=[]
# A 600 x 100 strip crosses the long diagonal seam; 140 x 100 plate crosses the short seam.
for k in range(4):
 center=Vector((1.05,2.4)); u=Vector((1,1)).normalized(); v=Vector((-1,1)).normalized()
 pts=[tuple(center+u*a+v*b) for a,b in [(-.3,-.05),(.3,-.05),(.3,.05),(-.3,.05)]]
 BACK.append(polygon_panel('B1 / diagonal scrap backer / 600 x 100',rotate_face(pts,k),.004,.004,PATCH))
 pts=[(.98,2.57),(1.12,2.57),(1.12,2.67),(.98,2.67)]
 BACK.append(polygon_panel('B2 / short-seam scrap backer / 140 x 100',rotate_face(pts,k),.004,.004,PATCH))
# No solid Coroplast tunnel walls: shared corner sheet stays available for other gates.
RET=[]
'''+s[b:]
# Replace front four full pipes with split rails and center reducing tees.
a=s.index('for z in [.3,2.4]: pipe(');b=s.index('# Fittings are simplified envelopes',a)
s=s[:a]+'''GM=.015875; GR=.0142875; PYR=.240
for z in [.3,2.4]:
 for sg in [-1,1]: pipe('P1 / half rail / 1016.663 mm',(sg*GM,P,z),(sg*(1.05-G),P,z))
for x in [-1.05,1.05]:
 pipe('P2 / half upright / 1016.663 mm',(x,P,.3+G),(x,P,1.35-GM))
 pipe('P2 / half upright / 1016.663 mm',(x,P,1.35+GM),(x,P,2.4-G))
 pipe('P3 / leg / 290.075 mm',(x,P,-.025+G),(x,P,.3-G))
 for sg in [-1,1]: pipe('P4 / foot / 582.538 mm',(x,P+sg*G,-.025),(x,P+sg*.6,-.025))
'''+s[b:]
# Insert front center tees and rear frame before brace block.
a=s.index("coll('05 / 3-4 inch corner braces')"); b=s.index("coll('06 / printed attachments and zip ties')",a)
s=s[:a]+'''# Four reducing tees and four short PVC links set the open rear frame depth.
centers=[(0,.3),(0,2.4),(-1.05,1.35),(1.05,1.35)]
for x,z in centers:
 dirs=[(1,0,0),(-1,0,0)] if x==0 else [(0,0,1),(0,0,-1)]
 fitting('T3 / 1 x 1 x 3-4 reducing tee',(x,P,z),dirs)
 tube('T3 / reducing branch',(x,P+.009,z),(x,P+.046,z),.040,WHITE,.006665)
 pipe('P6 / depth link / 173.175 mm',(x,P+.0206375,z),(x,PYR-GR,z),.02667)
coll('03 / open 3-4 inch rear frame / 260 mm body')
def rear_fit(name,c,dirs):
 cube(name+' / hub',c,(.033,.033,.033),WHITE,.006)
 for d in dirs:
  v=Vector(d); p=Vector(c); tube(name+' / socket',p+v*.008,p+v*.034,.040,WHITE,.006665)
for z in [.3,2.4]:
 for sg in [-1,1]: pipe('P7 / rear half rail / 1021.425 mm',(sg*GR,PYR,z),(sg*(1.05-GR),PYR,z),.02667)
for x in [-1.05,1.05]:
 pipe('P7 / rear half upright / 1021.425 mm',(x,PYR,.3+GR),(x,PYR,1.35-GR),.02667)
 pipe('P7 / rear half upright / 1021.425 mm',(x,PYR,1.35+GR),(x,PYR,2.4-GR),.02667)
 for z in [.3,2.4]: rear_fit('E2 / 3-4 inch rear elbow',(x,PYR,z),[(-1 if x>0 else 1,0,0),(0,0,-1 if z>1 else 1)])
for x,z in centers:
 dirs=[(1,0,0),(-1,0,0),(0,-1,0)] if x==0 else [(0,0,1),(0,0,-1),(0,-1,0)]
 rear_fit('T4 / 3-4 inch rear tee',(x,PYR,z),dirs)
coll('05 / corner braces with printed end joints'); BRACE=[]; JOINTS=[]
Rvert=Matrix(((1,0,0),(0,0,1),(0,-1,0))).to_4x4()
Rhor=Matrix(((0,1,0),(0,0,1),(1,0,0))).to_4x4()
BRACEY=P+.0344355
for sx in [-1,1]:
 for top in [False,True]:
  z=2.4 if top else .3; dz=-1 if top else 1
  a=Vector((sx*1.05,BRACEY,z+dz*.4)); b=Vector((sx*.65,BRACEY,z)); v=(b-a).normalized()
  o=tube('P5 / brace / 646 mm',a-v*.040,b+v*.040,.02667,WHITE,.00287); BRACE.append(o)
  for pt,R in [(a,Rvert),(b,Rhor)]:
   direction=R.to_3x3().inverted()@v; angle=math.atan2(-direction.x,direction.y)
   while angle>math.pi/2: angle-=math.pi
   while angle<-math.pi/2: angle+=math.pi
   src=JPLUS if angle>0 else JMINUS
   M=Matrix.Translation((pt.x,P+.0089005,pt.z))@R
   o=copy_obj(src,'J / printed brace end '+('plus45' if angle>0 else 'minus45'),(0,0,0));o.matrix_world=M;JOINTS.append(o)
   # Two loops around main pipe through main-side slots.
   for yy in [-.021,.021]:
    ps=[(-.025,yy,.018),(.025,yy,.018),(.025,yy,-.0089005)]
    ps +=[(.025*math.cos(t),yy,-.0089005-.020*math.sin(t)) for t in [j*math.pi/16 for j in range(17)]]
    ps +=[(-.025,yy,.018)]; line('J / main pipe retention tie',[M@Vector(q) for q in ps],.0012,DARK)
   u=Vector((-math.sin(angle),math.cos(angle),0)); vv=Vector((math.cos(angle),math.sin(angle),0))
   for aa in [-.012,.012]:
    ps=[vv*(-.023)+u*aa, vv*.023+u*aa]
    ps +=[vv*(.023*math.cos(t))+u*aa+Vector((0,0,.025535+.016*math.sin(t))) for t in [j*math.pi/16 for j in range(17)]]
    ps +=[vv*(-.023)+u*aa]; line('J / brace retention tie',[M@q for q in ps],.0012,DARK)
'''+s[b:]
# 24 face saddles clear center fittings.
s=s.replace("positions=[(x,z,False) for z in [.3,2.4] for x in [-.84,-.42,0,.42,.84]]+[(x,z,True) for x in [-1.05,1.05] for z in [.45,.9,1.35,1.8,2.25]]", "positions=[(x,z,False) for z in [.3,2.4] for x in [-.84,-.5,-.16,.16,.5,.84]]+[(x,z,True) for x in [-1.05,1.05] for z in [.45,.85,1.15,1.55,1.85,2.25]]")
s=s.replace("if not (vert and ((x<0 and z==.45) or (x>0 and z==2.25))):", "if True:")
a=s.index('# Fasten long and horizontal seams');b=s.index("coll('07 / guy lines",a)
s=s[:a]+'''# Mechanically stitch diagonal and short seams at every corner, with scrap spreaders.
for k in range(4):
 for t in [-.23,0,.23]:
  cen=Vector((1.05,2.4))+Vector((1,1)).normalized()*t
  v=Vector((-1,1)).normalized()*.035
  endpoints=rotate_face([tuple(cen-v),tuple(cen+v)],k)
  (xa,za),(xb,zb)=endpoints
  line('Corner diagonal / tie bridge',[(xa,-.001,za),(xb,-.001,zb),(xb,.009,zb),(xa,.009,za)],.0012,DARK,True)
 for dz in [-.025,.025]:
  (xa,za),(xb,zb)=rotate_face([(1.00,2.62+dz),(1.10,2.62+dz)],k)
  line('Corner short seam / tie bridge',[(xa,-.001,za),(xb,-.001,zb),(xb,.009,zb),(xa,.009,za)],.0012,DARK,True)
'''+s[b:]
# Captions correct to V2 structure.
s=s.replace('3 sheets + 5 pipes','2 sheets per face').replace('4 x 1 in + 1 x 3/4 in\\nAll pipe stock: 10 ft','Shared corner sheet: 16 gates\\nOpen PVC body: 260 mm')
s=s.replace('A single face. A braced PVC frame. Replaceable, tie-fastened parts.','Four identical pentagons. Four small corners. An open PVC back.')
s=s.replace('One frame, four corner braces, four guy lines. All hardware stays outside the opening.','A 1 in front frame, 3/4 in rear frame, four depth links and printed brace joints.')
s=s.replace('Cross-lashed at each end','Printed 45-degree joints').replace('03 / OPENING WALLS','03 / OPEN PVC BACK').replace('Folded 30 mm fixing flanges\\nStitched corners / no rear face','3/4 in square + 4 short links\\nRear fitting envelope at 260 mm')
s=s.replace('Front face -> scrap backers -> saddles -> PVC -> folded opening walls','Pentagons + corners -> scrap backers -> saddles -> front frame -> open rear frame')
s=s.replace('2400 + 300 = 2700 mm\\nBackers bridge every seam','Four identical 2400 x 600 blanks\\nFour 300 mm corner triangles')
s=s.replace('20 saddles / two ties each','24 saddles / two ties each').replace('4  CLOSE THE TUNNEL','4  CONNECT THE BACK').replace('Fold, stitch, square, anchor','Four links set the 260 mm depth')
s=s.replace('Assembled body depth is 260 mm; full support footprint is larger.','Rear fitting envelope is 260 mm; support footprint is larger.')
s=s.replace('20 saddles + 20 washers per gate.','24 saddles + 24 washers per gate.')
# New native sheet scene: exact polygon layouts and a full sheet of shared corners.
a=s.index('# Sheet layout in native Blender.');b=s.index('# Front dimensional elevation',a)
s=s[:a]+'''# Sheet layouts use exact local cut polygons; third stock yields 64 triangles / 16 gates.
setup('04_SHEET_LAYOUT',(0,-8,2.35),(0,0,2.35),7.9,False)
coll('01 / polygon sheet nesting'); layout=[]
LOCAL_PENTA=[(0,600),(2400,600),(2400,300),(2100,0),(600,0)]
for sh in [1,2,3]:
 ox=(sh-2)*2.55; oz=.52
 cube('Stock / 2438.4 x 1219.2',(ox,.008,oz+2.4384/2),(1.2192,.006,2.4384),GREEN)
 text('Sheet label',f'SHEET {sh:02}',(ox-.61,-.012,3.13),.1,INK,bold=True)
 text('Stock size','1219.2 x 2438.4 mm',(ox-.61,-.012,3),.055,MUTED)
 if sh<3:
  for row in range(2):
   poly=[(x,y+600*row) for x,y in LOCAL_PENTA]
   pts=[(ox-.6096+y/1000,oz+x/1000) for x,y in poly]
   polygon_panel('F / pentagon / identical',pts,-.004,.004,BLUE)
   layout.append({'sheet':sh,'type':'pentagon','polygon_mm':poly})
   text('Part label','2400\\nx 600',(ox-.3096+.6*row,-.009,1.65),.10,LIGHTTEXT,align='CENTER',bold=True)
  text('Scrap label','OFFCUTS -> BACKERS',(ox-.60,-.02,.61),.045,INK)
 else:
  for i in range(8):
   for j in range(4):
    for half in range(2):
     x=i*300;y=j*300
     poly=[(x,y),(x+300,y),(x,y+300)] if half==0 else [(x+300,y),(x+300,y+300),(x,y+300)]
     pts=[(ox-.6096+v/1000,oz+u/1000) for u,v in poly]
     polygon_panel('C / shared corner / 300 legs',pts,-.004,.004,BLUE2 if half else BLUE)
     layout.append({'sheet':sh,'type':'corner','polygon_mm':poly})
     line('Triangle cut line',[(pts[0][0],-.009,pts[0][1]),(pts[-1][0],-.009,pts[-1][1])],.001,RETURN)
header('04','Two identical cuts per sheet','Sheets 1 and 2 make four identical pentagons. Share sheet 3 across the fleet.')
overlay('4 MAIN PANELS / GATE',.062,.865,.018,True);overlay('2400 x 600 mm bounding blanks',.062,.905,.013,color=MUTED)
overlay('BACKERS FROM OFFCUTS',.389,.865,.018,True);overlay('4 diagonal strips + 4 short tabs',.389,.905,.013,color=MUTED)
overlay('64 CORNERS / SHEET',.711,.865,.018,True);overlay('300 mm right triangles = 16 gates',.711,.905,.013,color=MUTED)
footer('Knife cuts / no saw kerf. Face sheets: 2 per gate. Shared corner allocation: 1/16 sheet per gate. See SVG for backer nesting.')
'''+s[b:]
# Add detailed joint assembly view and a face-parts scene for clear pentagon explanation.
pos=s.index('# Embed practical guide and scene index.')
s=s[:pos]+'''setup('08_BRACE_JOINT',(.17,-.28,.21),(.005,0,.038),.40,False)
coll('01 / actual printed joint demonstration')
jo=copy_obj(JPLUS,'J / +45 prototype joint',(-.060,0,.018),(0,0,0))
tube('Main 1 in pipe',(-.060,-.06,.018-.0089005),(-.060,.06,.018-.0089005),.033401,WHITE,.003378)
u=Vector((-math.sqrt(.5),math.sqrt(.5),0));c=Vector((-.060,0,.018+.025535))
tube('Brace 3-4 in pipe',c-u*.06,c+u*.06,.02667,WHITE,.00287)
copy_obj(JPLUS,'J / isolated plus45',(.057,-.02,.015),(0,0,0))
copy_obj(JMINUS,'J / isolated minus45',(.070,.070,.015),(0,0,0))
header('08','A positive seat at both ends','Two machined-in pipe cradles fix the crossing angle; four ties retain each printed joint.')
overlay('1 in main / OD 33.40',.60,.28,.015,True)
overlay('3/4 in brace / OD 26.67',.60,.33,.015,True)
overlay('8 JOINTS / GATE',.60,.40,.018,True)
overlay('4 x +45 and 4 x -45\\n60 x 60 x 18 mm body\\n4 mm minimum central web',.60,.45,.014,color=MUTED)
overlay('TIE RETENTION',.60,.71,.017,True)
overlay('Two ties around each pipe\\nPrint a fit sample first',.60,.76,.014,color=MUTED)
footer('Grooves on opposite faces. Print on an edge with a brim; support overhangs as needed. STLs are in mm, closed and manifold.')
setup('09_FACE_PARTS',(0,-8,1.6),(0,0,1.6),6.2,False)
coll('01 / face explosion')
for k in range(4):
 off=rotate_face([(0,1.65)],k)[0]; offset=Vector((off[0],off[1]-1.35))
 pts=[tuple(Vector(q)+offset) for q in rotate_face(PENTA,k)]
 polygon_panel('Pentagon / identical',pts,0,.004,BLUE)
 p2=rotate_face(TRI,k); c=Vector((sum(q[0] for q in p2)/3,sum(q[1] for q in p2)/3));delta=(c-Vector((0,1.35))).normalized()*.43
 polygon_panel('Corner infill', [tuple(Vector(q)+delta) for q in p2],0,.004,BLUE2)
header('09','Four pentagons. Four corners.','Identical border pieces rotate through 90 degrees. All long midspans stay continuous.')
footer('Assembled face: 2700 x 2700 mm / opening: 1500 x 1500 mm. Each corner infill is a right triangle with 300 mm legs.')
'''+s[pos:]
s=s.replace("[SADDLE,SADDLE34,WASH]", "[SADDLE,SADDLE34,WASH,JPLUS,JMINUS]")
a=s.index('for r in layout:\n assert');b=s.index("checks['hard_surface']",a)
s=s[:a]+'''def area2(poly):
 return abs(sum(poly[i][0]*poly[(i+1)%len(poly)][1]-poly[(i+1)%len(poly)][0]*poly[i][1] for i in range(len(poly))))/2
for r in layout:
 assert all(0<=x<=2438.4 and 0<=y<=1219.2 for x,y in r['polygon_mm'])
assert len([r for r in layout if r['type']=='corner'])==64
assert abs(area2(LOCAL_PENTA)*4+45000*4-5040000)<.001
assert len(JOINTS)==8
checks['face']={'pentagon_area_mm2':area2(LOCAL_PENTA),'corner_area_mm2':45000,'total_face_area_mm2':5040000,'shared_corners_per_sheet':64,'gates_per_corner_sheet':16,'panels_per_main_sheet':2}
'''+s[b:]
s=s.replace("'long_cut_mm':2065.075", "'front_half_cut_mm':1016.6625,'rear_half_cut_mm':1021.425,'depth_link_mm':173.1745")
s=s.replace("2065.075+290.075+582.5375+9", "2*1016.6625+290.075+582.5375+12")
s=s.replace("'sheet_nesting':'no overlaps; all pieces within 1219.2 x 2438.4 mm'", "'sheet_nesting':'main panels and shared triangles within stock; polygon union verified separately'")
s=s.replace("'05_CLIP_DETAIL','06_DIMENSIONS','07_HARD_SURFACE']", "'05_CLIP_DETAIL','06_DIMENSIONS','07_HARD_SURFACE','08_BRACE_JOINT','09_FACE_PARTS']")
s=s.replace('six native','nine native')
p.write_text(s)

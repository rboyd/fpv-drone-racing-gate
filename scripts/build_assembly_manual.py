"""Build a printable, bookmarked two-part instruction manual from current CAD/BOM.
Requires reportlab. For preview/validation also install pymupdf and Pillow.
CAD mesh source: output/a1_full_size/manual_assets/part_meshes.json.
"""
from pathlib import Path
import json,math
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor,Color,white
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph,Table,TableStyle
from reportlab.lib.styles import ParagraphStyle
R=Path(__file__).resolve().parents[1];O=R/'output/a1_full_size';A=O/'manual_assets';A.mkdir(exist_ok=True)
B=json.loads((O/'BOM.json').read_text());CHECK=json.loads((O/'print_checks.json').read_text());MESH=json.loads((A/'part_meshes.json').read_text())
assert B['unique_printed_parts']==19 and B['printed_piece_count']==740
FONT=Path('/System/Library/Fonts/Supplemental')
for name,fn in [('Body','Arial.ttf'),('Bold','Arial Bold.ttf')]:pdfmetrics.registerFont(TTFont(name,str(FONT/fn)))
W,H=612,792;LEFT=42;CW=528
NAVY=HexColor('#173148');BLUE=HexColor('#26779b');ORANGE=HexColor('#de7e3b');PALE=HexColor('#edf3f6');INK=HexColor('#27333c');GRAY=HexColor('#62727c');GREEN=HexColor('#26714e');RED=HexColor('#ad493c')
C=canvas.Canvas(str(O/'Assembly_and_Test_Instructions.pdf'),pagesize=(W,H));C.setTitle('FPV gate | Nine-piece prototype and full-gate assembly');C.setAuthor('FPV racing gate design project');C.setSubject('Two-part assembly and test instructions; two-channel A1 Mini revision')
STYLE=ParagraphStyle('body',fontName='Body',fontSize=10.2,leading=14,textColor=INK,spaceAfter=0)
SMALL=ParagraphStyle('small',parent=STYLE,fontSize=8.7,leading=11.7)
PAGENO=0;HEADINGS=[];OVERFLOW=[]
def rect(x,y,w,h,fill=PALE,stroke=None,r=0):
 C.setFillColor(fill or white);C.setStrokeColor(stroke or fill or white)
 if r:C.roundRect(x,H-y-h,w,h,r,fill=bool(fill),stroke=bool(stroke))
 else:C.rect(x,H-y-h,w,h,fill=bool(fill),stroke=bool(stroke))
def ln(x1,y1,x2,y2,color=INK,width=1,dash=None):
 C.setStrokeColor(color);C.setLineWidth(width);C.setDash(dash or []);C.line(x1,H-y1,x2,H-y2);C.setDash([])
def txt(s,x,y,size=10,color=INK,bold=False):
 C.setFont('Bold' if bold else 'Body',size);C.setFillColor(color);C.drawString(x,H-y-size*.82,str(s))
def para(s,y,x=LEFT,w=CW,small=False):
 p=Paragraph(s,SMALL if small else STYLE);_,h=p.wrap(w,1000);p.drawOn(C,x,H-y-h)
 if y+h>746:OVERFLOW.append((PAGENO,s[:50],y+h))
 return y+h+8

def heading(s,y):txt(s,LEFT,y,13,NAVY,True);return y+23

def note(s,y,color=PALE):
 p=Paragraph(s,STYLE);_,h=p.wrap(CW-24,1000);rect(LEFT,y,CW,h+20,color,r=5);p.drawOn(C,LEFT+12,H-y-10-h)
 if y+h+20>746:OVERFLOW.append((PAGENO,'note',y+h+20))
 return y+h+30

def step(n,s,y):
 rect(LEFT,y,23,23,BLUE,r=4);txt(str(n),LEFT+7,y+5,12,white,True)
 return max(y+31,para(s,y,LEFT+34,CW-34))

def table(headers,rows,y,widths=None,small=True):
 st=SMALL if small else STYLE
 vals=[[Paragraph(str(a),ParagraphStyle('th',parent=st,fontName='Bold',textColor=white)) for a in headers]]+[[Paragraph(str(a),st) for a in row] for row in rows]
 t=Table(vals,colWidths=widths or [CW/len(headers)]*len(headers),hAlign='LEFT')
 t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),NAVY),('VALIGN',(0,0),(-1,-1),'TOP'),('ROWBACKGROUNDS',(0,1),(-1,-1),[white,PALE]),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5),('LINEBELOW',(0,-1),(-1,-1),.6,HexColor('#ced8de'))]))
 _,h=t.wrap(CW,1000);t.drawOn(C,LEFT,H-y-h)
 if y+h>746:OVERFLOW.append((PAGENO,'table',y+h))
 return y+h+12

def page(section,title,sub=''):
 global PAGENO
 if PAGENO:C.showPage()
 PAGENO+=1;HEADINGS.append(title);key=f'p{PAGENO}';C.bookmarkPage(key);C.addOutlineEntry(f'{PAGENO:02d}  {title}',key,0,False)
 rect(0,0,W,7,ORANGE if section.startswith('PART 1') else BLUE)
 txt('FIELDWORK / FPV RACING GATE',LEFT,24,8,GRAY,True);txt(section,360,24,8,GRAY,True)
 txt(title,LEFT,47,22,NAVY,True)
 if sub:txt(sub,LEFT,76,9,GRAY)
 ln(LEFT,750,W-LEFT,750,HexColor('#d7e0e5'),.6)
 txt('A1 Mini · Two-channel revision · Prototype instructions · 17 Sep 2026',LEFT,763,7.4,GRAY)
 txt(f'{PAGENO:02d}',W-58,760,11,NAVY,True)
 return 101

def arrow(a,b,color=BLUE,width=1.3):
 ln(*a,*b,color,width);ang=math.atan2(b[1]-a[1],b[0]-a[0]);sz=6
 for da in [-.48,.48]:ln(b[0],b[1],b[0]-sz*math.cos(ang+da),b[1]-sz*math.sin(ang+da),color,width)

def dim(a,b,label,offset=12):
 # Horizontal dimension only, top-coordinate system.
 y=max(a[1],b[1])+offset;ln(a[0],a[1],a[0],y+4,GRAY,.6);ln(b[0],b[1],b[0],y+4,GRAY,.6);ln(a[0],y,b[0],y,GRAY,.7)
 for x in [a[0],b[0]]:ln(x-2,y+3,x+2,y-3,GRAY,.8)
 txt(label,(a[0]+b[0])/2-pdfmetrics.stringWidth(label,'Body',8)/2,y+5,8,GRAY)

def dot(a,b):return sum(x*y for x,y in zip(a,b))
def cross(a,b):return [a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]]
def norm(a):
 l=math.sqrt(dot(a,a));return [x/l for x in a]
def add(a,b):return [x+y for x,y in zip(a,b)]
def sub(a,b):return [x-y for x,y in zip(a,b)]
I=((1,0,0),(0,1,0),(0,0,1))
def rz(deg):
 a=math.radians(deg);return ((math.cos(a),-math.sin(a),0),(math.sin(a),math.cos(a),0),(0,0,1))
def xf(v,mat=I,off=(0,0,0)):return [dot(row,v)+off[j] for j,row in enumerate(mat)]
def inst(code,off=(0,0,0),mat=I,color=None):return (code,off,mat,color)
BLUE_PARTS={'SPLINT','CORNER_NODE','RIB_ANCHOR','RIB_CROSS','BORDER_BRIDGE','FIELD_RECEIVER','DOCK_CAP','DOCK_PEDESTAL','BRACE_LINK_45'}
def meshview(items,box,view=(.55,-1,1.1),paths=None):
 # Orthographic projection of exact CAD triangles; no AI or approximate substitute meshes.
 vx,vy,vw=box[0],box[1],box[2];vh=box[3];front=norm(view);right=norm(cross(front,(0,0,1)));up=cross(right,front)
 faces=[];allv=[]
 for code,off,mat,color in items:
  m=MESH[code];vs=[xf(v,mat,off) for v in m['vertices']];allv+=vs
  base=color or (BLUE if code in BLUE_PARTS else ORANGE);det=dot(mat[0],cross(mat[1],mat[2]))
  for inds in m['triangles']:
   a,b,c=[vs[i] for i in inds]
   n=cross(sub(b,a),sub(c,a))
   if det<0:n=[-q for q in n]
   length=math.sqrt(dot(n,n))
   if length<1e-10:continue
   n=[q/length for q in n]
   if dot(n,front)<-.0001:continue
   light=.69+.28*max(0,dot(n,norm((-.3,-.7,1))))
   col=Color(base.red*light,base.green*light,base.blue*light)
   faces.append((sum(dot(p,front) for p in [a,b,c])/3,[a,b,c],col))
 uv=[(dot(p,right),dot(p,up)) for p in allv];lo=[min(p[i] for p in uv) for i in [0,1]];hi=[max(p[i] for p in uv) for i in [0,1]]
 scale=min(vw/max(hi[0]-lo[0],.01),vh/max(hi[1]-lo[1],.01))*.94;cx=(hi[0]+lo[0])/2;cy=(hi[1]+lo[1])/2
 def project(p):return (vx+vw/2+(dot(p,right)-cx)*scale,vy+vh/2-(dot(p,up)-cy)*scale)
 for _,pts,color in sorted(faces,key=lambda q:q[0]):
  p=C.beginPath();a=project(pts[0]);p.moveTo(a[0],H-a[1])
  for pt in pts[1:]:a=project(pt);p.lineTo(a[0],H-a[1])
  p.close();C.setFillColor(color);C.setStrokeColor(color);C.setLineWidth(.12);C.drawPath(p,fill=1,stroke=1)
 for pts,color in (paths or []):
  for a,b in zip(pts,pts[1:]):ln(*project(a),*project(b),color,1.6)
 return project

def checkbox(s,y,x=LEFT,w=CW):
 rect(x,y+2,9,9,white,GRAY);return para(s,y,x+18,w-18,True)

def gate_diagram(x,y,size,labels=True):
 S=B['gate_mm']['outside'];L=B['gate_mm']['border'][0];PY=B['gate_mm']['border'][1];PX=L/3;sc=size/S
 # Map gate CAD x/right, y/up into page coordinates.
 def pt(a,b):return x+a*sc,y+(S-b)*sc
 colors=[HexColor('#de7e3b'),HexColor('#438eac'),HexColor('#669571'),HexColor('#a88bbb')]
 for k in range(4):
  ang=-k*math.pi/2
  def q(a,b):
   dx=a-S/2;dy=L+b-S/2
   return (S/2+dx*math.cos(ang)-dy*math.sin(ang),S/2+dx*math.sin(ang)+dy*math.cos(ang))
  for bay in range(3):
   ps=[pt(*q(a,b)) for a,b in [(bay*PX,0),((bay+1)*PX,0),((bay+1)*PX,PY),(bay*PX,PY)]]
   pp=C.beginPath();pp.moveTo(ps[0][0],H-ps[0][1])
   for a,b in ps[1:]:pp.lineTo(a,H-b)
   pp.close();C.setFillColor(colors[k]);C.setStrokeColor(white);C.setLineWidth(1);C.drawPath(pp,fill=1,stroke=1)
   if labels:
    cx,cy=pt(*q((bay+.5)*PX,PY/2));txt(f'{"ABCD"[k]}{bay+1}',cx-9,cy-4,8,white,True)
 return pt

# 01
page('ASSEMBLY & TEST MANUAL','Whole-sheet FPV racing gate','Part 1: nine-piece concept print  /  Part 2: complete gate')
gate_diagram(LEFT,117,267)
y=para('<b>Current design</b><br/>12 whole 22 × 28 inch sheets<br/>4 rigid borders, about 2.15 m long<br/>1 PVC backing frame + 4 braces<br/>2 channel types; 19 printed types total',126,331,239)
y=para('<b>Start small.</b> Print the nine-piece plate, check the interfaces, then build one complete sheet bay before producing the remaining bays.',y+6,331,239)
y=para('Geometry fits the A1 Mini. Snap durability, assembled stiffness and outdoor performance still need physical testing.',y+6,331,239)
y=406
y=heading('Use this manual at the workbench',y)
for label,dest in [('Part 1 — Print, assemble and test nine pieces',2),('Part 2 — Full gate: inventory and workshop assembly',7),('PVC frame, printed brace joints and both bases',13),('Field setup, inspection and teardown',16)]:
 txt(label,LEFT,y,10.5,NAVY,True);txt(str(dest),548,y,10,NAVY,True);C.linkRect('',f'p{dest}',(LEFT,H-y-17,W-LEFT,H-y+2),relative=0,thickness=0);y+=29
y=note('All dimensions are <b>millimeters</b> unless stated otherwise. Illustrations are not cutting templates. Printed part names match the STL filenames.',y+10)
y=para('Orange = channel/rib/snap/pipe-saddle parts. Blue = locating nodes, caps and links. Exact CAD illustrations are identified in captions; flat diagrams explain layout and tie routing.',y,small=True)
para('Companion files: BOM.csv, PVC_CUT_LIST.csv, CHANNEL_ASSEMBLY_MAP.json and MINIMAL_TEST_PARTS.csv in output/a1_full_size. This manual uses the current LONG / SHORT channels, not the retired CHANNEL_01–09 files.',y,small=True)

# 02
page('PART 1 / PREPARE','Print nine pieces','One of each part. Reuse the channels between the straight and corner tests.')
codes=['CHANNEL_LONG','CHANNEL_SHORT','SPLINT','CORNER_NODE','RIB_H_LOW_DOCK','DOCK_PEDESTAL','DOCK_CAP','PIPE_33','SNAP_BRIDGE']
for i,code in enumerate(codes):
 col=i%3;row=i//3;x=LEFT+col*180;y=104+row*115
 rect(x,y,168,105,PALE,r=5);meshview([inst(code)],(x+7,y+8,154,61))
 txt(f'{i+1}. {code}',x+8,y+78,8,NAVY,True);txt('Print 1',x+8,y+91,8,GRAY)
y=459
y=note('<b>One A1 Mini plate: 32.4 g PETG / about 95 minutes.</b><br/>Use Minimal_Concept_Test_9_Parts_A1Mini_PETG.3mf from the sliced/Minimal_Concept_Test_9_Parts folder. These are full-size parts; print at 100%.',y)
y=para('<b>Settings:</b> A1 Mini, 0.4 mm nozzle, 0.20 mm layers, 3 walls, 15% infill, Generic PETG, Textured PEI Plate, supports off. Keep the supplied orientations. Check the printer, filament and plate before starting.',y)
y=para('<b>Bring:</b> actual posterboard; a short 1-inch nominal PVC offcut (33.40 mm OD); six 2.5 mm-wide ties; one roughly 3.6 × 250 mm keeper tie; ruler or calipers; flush cutters; a deburring tool. Releasable ties help when reusing the channels.',y)
para('<b>After printing:</b> clear strings and brim/first-layer burrs from slots, windows and snap hooks. Keep the original sizes. Do not scale the whole kit to correct one tight interface.',y)

# 03
page('PART 1 / TEST 1–2','Paper fit, then a straight splice','Use CHANNEL_LONG + CHANNEL_SHORT + SPLINT. Two narrow ties.')
# Exact profile enlarged, with paper shown in its slot.
profile=[(0,0),(6,0),(6,1.2),(1.8,1.2),(1.8,2),(6,2),(6,3.2),(1.8,3.2),(1.8,7),(2.4,7),(2.4,14),(0,14)]
ox,oy,sc=72,121,9
pp=C.beginPath()
for i,(yy,zz) in enumerate(profile):
 a,b=ox+yy*sc,H-(oy+zz*sc)
 (pp.moveTo if i==0 else pp.lineTo)(a,b)
pp.close();C.setFillColor(ORANGE);C.drawPath(pp,fill=1,stroke=0)
rect(ox+3*sc,oy+1.2*sc,146,0.4*sc,HexColor('#b6d4dc'))
arrow((290,135),(ox+5*sc,oy+1.6*sc));txt('0.8 mm paper slot',296,128,10,NAVY,True)
para('Front lips face the flying side. The deep spine and mounting windows sit behind the paper. Slot shown with approximately 0.4 mm stock.',159,290,265)
y=264
y=step(1,'Slide a sheet edge into each channel. It should enter without creasing or forcing the lips apart. Check the paper near both ends. Use the actual sheet; no cutting or punching is needed.',y)
y=step(2,'Align the channels end-to-end, with slots facing the same way and a <b>0.2 mm gap</b>. A long-to-short joint is only a test combination; production joins equal-length pieces.',y)
items=[inst('CHANNEL_LONG',(-140.94,0,0)),inst('CHANNEL_SHORT',(.1,0,0)),inst('SPLINT',(0,18,10),((1,0,0),(0,0,-1),(0,1,0)))]
meshview(items,(LEFT,363,CW,96),view=(.10,-1,1.4));txt('Exact CAD: splint lifted away to show the four hollow locating bosses.',LEFT,464,8,GRAY)
y=486
y=step(3,'Seat all four splint bosses in the end windows. The flat splint body sits on the <b>inward</b> side of the rail spine. Thread one tie through the two bosses on the left, and one through the two on the right. Keep ties out of the paper slot.',y)
# Simple tie routing viewed through the rail spine: ties pair holes on each side, not across seam.
for x in [196,223,281,308]:rect(x,585,15,14,white,BLUE)
ln(260,568,260,621,GRAY,1,[3,3])
for a,b in [(203.5,230.5),(288.5,315.5)]:
 ln(a,592,a,577,INK,1.5);ln(a,577,b,577,INK,1.5);ln(b,577,b,592,INK,1.5)
arrow((114,608),(203,589));txt('One tie per side',LEFT,627,9,NAVY,True);txt('Joint gap',239,628,8,GRAY)
y=651
y=para('<b>Pass:</b> bosses seat fully; ties snug the splint without crushing the spine; gentle hand bending/sliding does not open the joint or release a boss. Recheck that paper still slides.',y)
para('<b>If it binds:</b> remove burrs and inspect the boss/window fit. Do not force or trim away a locating shoulder. Record the mismatch on page 6.',y)

# 04
page('PART 1 / TEST 3','Reconfigure as a frame corner','Remove the splint. Reuse the two channels with CORNER_NODE and two fresh/reusable ties.')
# Reflecting X/Y is safe here because end-for-end channel features are symmetric.
items=[inst('CHANNEL_LONG',(6.1,0,0)),inst('CHANNEL_SHORT',(0,6.1,0),((0,1,0),(1,0,0),(0,0,1))),inst('CORNER_NODE',(0,0,17),((1,0,0),(0,1,0),(0,0,-1)))]
meshview(items,(LEFT,106,CW,206),view=(.65,-1,1.7))
txt('Exact CAD: the node is behind the paper, inside the corner.',LEFT,316,8,GRAY)
y=339
y=step(1,'Place the rails at 90° with both slots opening into the paper area. Align their outside spine lines to define a virtual corner. Each channel begins <b>6.1 mm from that corner</b>; do not jam the two channel tips together.',y)
y=step(2,'Put the blue L-shaped node on the rear of the rails, inside the corner. Its locating fences point toward the paper and sit against the inward faces of the rail spines.',y)
y=step(3,'Tie one arm of the node to each rail. Use the node hole about 14.1 mm from the virtual corner and the matching spine window. The other paired holes are reserved for full-gate bridges.',y)
y=step(4,'Fit a posterboard corner into both slots. Check squareness with a ruler or square, then gently try to rack the joint. Keep tie heads and cut tails behind the paper.',y)
y=note('<b>Pass:</b> the corner remains square under gentle handling; paper fits both grooves without folding; the node stays seated. This checks a sheet-frame corner, not the removable seam between full borders.',y+5)
para('If the node will not seat, check rail orientation and the 6.1 mm setback first. Loosen ties and align the fences before retightening; do not use tie tension to force misaligned parts into place.',y)

# 05
page('PART 1 / TEST 4','Build the complete PVC dock','Five parts: docking rib, pedestal, cap, pipe saddle and snap bridge.')
items=[inst('RIB_H_LOW_DOCK',(-63.433,0,17)),inst('DOCK_PEDESTAL',(0,0,33)),inst('DOCK_CAP',(0,0,61)),inst('PIPE_33',(-50,-25.8,55)),inst('SNAP_BRIDGE',(-24,-1.5,101),((1,0,0),(0,0,1),(0,-1,0)))]
meshview(items,(LEFT,103,335,231),view=(.5,-1,1.2))
for i,(label,yy) in enumerate([('9  SNAP_BRIDGE',118),('7  DOCK_CAP',158),('6  DOCK_PEDESTAL',190),('8  PIPE_33',231),('5  RIB_H_LOW_DOCK',277)]):txt(label,393,yy,8,NAVY,True)
txt('Numbers match page 2',393,306,8,GRAY)
txt('Exact CAD, exploded for clarity. Pipe saddle shifted aside; final socket spacing is 24 mm.',LEFT,338,8,GRAY)
y=360
y=step(1,'Hold <b>RIB_H_LOW_DOCK</b> with its small paper-contact shoe pointing toward the future paper face. Use this rib, which has four extra holes around its center; the ordinary low rib does not.',y)
y=step(2,'Center <b>DOCK_PEDESTAL</b> on the back of the rib: its solid base on the rib, two walls upward. Put <b>DOCK_CAP</b> on those walls. The cap’s diamond socket must open into the hollow space beneath it.',y)
y=step(3,'Use two narrow ties through the cap and rib’s matching holes—one at each end of the pedestal. Tighten evenly. Do not run a strap through the central snap opening.',y)
y=step(4,'Seat <b>PIPE_33</b> around the actual PVC offcut. Add the long keeper tie around pipe and saddle, near an axial edge so it clears the snap socket and hooks. Keep its head out of the release path. The open C shape alone is not the retainer.',y)
y=step(5,'Bring the cap and saddle socket centers <b>24 mm apart</b>, with their rear faces level. Insert <b>SNAP_BRIDGE</b> from the rear. Press its solid crossbar until both rigid stop pairs seat and the hooks emerge through the sockets.',y)
para('<b>Pass:</b> both ends latch, the cap stays on its pedestal, and the fork tips have free space behind the socket plates. Gentle pulls do not release the dock or rotate the saddle on the pipe.',y)

# 06
page('PART 1 / TEST & RECORD','Release it, repeat it, record it','A fit-and-handling check—not a structural load or wind rating.')
meshview([inst('SNAP_BRIDGE')],(LEFT,106,175,115),view=(.2,-.7,2))
y=para('<b>Release one end at a time.</b> Pinch that fork’s two prongs inward so the hooks clear the socket. Lift that end slightly, then release the other. Hold the nearby rigid parts; do not lever the crossbar until a prong bends.',110,243,327)
para('Check access in the assembled dock, not just loose parts. Blunt tweezers can diagnose tight clearance, but record if tools are needed. Do not claim quick hand release until it works physically.',y,243,327)
y=240
y=step(1,'As an initial screening exercise, try <b>20 insert/release cycles</b>. This is a chosen workshop check, not a certified durability threshold. Stop for cracks, whitening, permanent bend, binding or unintended release.',y)
y=step(2,'After cycling, repeat a gentle hand pull and the pipe-slip check. Run paper over the rib’s contact shoe and inspect for catching or scratching. Recheck every tie and its clearance.',y)
y=heading('Fill in after printing',y+4)
y=table(['Check','Pass / issue / measurement'],[['Filament / nozzle / layer height','_____________________________________'],['Measured sheet thickness / pipe OD','_____________________________________'],['Paper slides in both channels','_____________________________________'],['Splice bosses seat; joint stays together','_____________________________________'],['Corner fits; remains square by hand','_____________________________________'],['Dock seats; pipe does not rotate/slip','_____________________________________'],['Snap cycles completed / release by hand?','_____________________________________'],['Cracks / permanent bend / paper marking','_____________________________________'] ],y,[240,288])
y=note('<b>Next:</b> correct any fit failure, then make one complete sheet bay (pages 9–11) and check paper flutter, cap removal and racking. The nine pieces cannot test a full border’s stiffness.',y)
para('<b>Optional samples:</b> add BRACE_LINK_45 + PIPE_27 for a brace end (reuse PIPE_33). Add RIB_H_HIGH, RIB_V_HIGH, RIB_CROSS and RIB_ANCHOR for rib-joint tests; reuse the docking rib between those checks.',y,small=True)

# 07
page('PART 2 / PLAN','The full gate at a glance','Build twelve sheet bays → four rigid borders → one gate on the PVC backing.')
gate_diagram(LEFT,107,312)
y=para('<b>Front layout</b><br/>A, B, C and D are the four rigid borders. Each border contains bays 1–3 and rotates 90° around the opening.',114,382,188)
y=para('<b>Transport</b><br/>Four rigid borders, each 2151.6 × 564.8 mm. No hinges. Workshop ties remain installed.',y+8,382,188)
para('<b>Field face joints</b><br/>16 PVC dock keys<br/>8 corner keys<br/>24 SNAP_BRIDGE total',y+8,382,188)
y=444
y=table(['Dimension / material','Target'],[['Outer face / nominal opening','2716.4 mm square / 1586.8 mm square'],['Whole insert / bay envelope','711.2 × 558.8 mm / 717.2 × 564.8 mm'],['Single PVC backing frame','2100 × 2100 mm between pipe axes'],['Main pipe / brace pipe OD','33.40 mm / 26.67 mm'],['Printed kit','19 unique types; 740 pieces; all fit 180 mm cubed'],['Filament planning','2.97 kg sliced PETG; 3.26 kg with 10% reserve → four 1 kg spools'] ],y,[236,292])
y=note('This is a substantial workshop build: <b>856 working ties</b>. Batch printing is sensible after fit approval. Build one full bay before committing to eleven more.',y)
para('The face drawings show the nominal clear opening. Keep every pipe, brace, guy and fastener out of that opening. Ordinary posterboard is a dry-use consumable.',y,small=True)

# 08
page('PART 2 / INVENTORY','Print and purchase checklist','Totals are per gate, including all printed face, dock and brace connectors.')
rows=[]
for code in ['CHANNEL_LONG','CHANNEL_SHORT','SPLINT','CORNER_NODE','RIB_ANCHOR','RIB_CROSS','BORDER_BRIDGE','FIELD_RECEIVER','SNAP_BRIDGE','RIB_H_LOW','RIB_H_LOW_DOCK','RIB_H_HIGH','RIB_V_LOW','RIB_V_HIGH','PIPE_33','PIPE_27','DOCK_CAP','DOCK_PEDESTAL','BRACE_LINK_45']:
 a=next(p for p in B['parts'] if p['code']==code);rows.append([code,str(a['quantity']),' × '.join(f'{n:g}' for n in a['print_bounds_mm'])])
y=table(['STL name','Qty','Print X × Y × Z (mm)'],rows,103,[238,48,242])
y=para('<b>Face supplies:</b> 12 whole posterboard sheets; 744 standard 2.5 mm ties; 48 narrow releasable ties (or removable cord loops); 32 pipe keeper ties about 3.6 × 250 mm; 32 brace-link ties about 3.6 × 150 mm; 20 m of smooth 0.8 mm front cord. Buy spare ties.',y,small=True)
y=para('<b>PVC fittings:</b> 2 upper elbows, 2 lower frame tees, 2 foot tees and 4 end caps, all 1 inch nominal. Pipe cuts are on page 13. Retain working sockets positively; fittings must not pull apart during handling.',y,small=True)
para('<b>Anchoring supplies:</b> four guy lines (about 4 m each), suitable ground anchors for soil; or four strapped ballast bags with anti-slip pads for hard surfaces. The base arrangement and test limits are on page 15.',y,small=True)

# 09
page('PART 2 / WORKSHOP 1','Build one sheet-frame perimeter','Work face-down on a flat surface. The same two channel types serve every bay.')
# Rear plan diagram; CAD corner reference and rail segment centers.
x0,y0,ww,hh=106,116,400,210
for i in range(5):
 for yy in [y0,y0+hh]:rect(x0+i*80+2,yy,76,7,ORANGE)
for i in range(4):
 for xx in [x0-7,x0+ww]:rect(xx,y0+i*52.5+2,7,49,ORANGE)
for x,y in [(x0,y0),(x0+ww,y0),(x0,y0+hh),(x0+ww,y0+hh)]:rect(x-7,y-3,14,14,BLUE)
for x,y in [(x0+ww/2,y0),(x0+ww/2,y0+hh),(x0,y0+hh/2),(x0+ww,y0+hh/2)]:rect(x-10,y-3,20,12,BLUE)
txt('5 × CHANNEL_LONG',223,139,10,NAVY,True);txt('5 × CHANNEL_LONG — removable top cap',166,292,9,NAVY,True)
# diagram screen upper edge corresponds local bottom? Explicit local labels needed: label top cap at upper.
rect(151,135,317,21,white);txt('Local top: 5 × LONG — removable cap',166,139,9,NAVY,True)
rect(151,287,317,22,white);txt('Local bottom: 5 × LONG',205,292,9,NAVY,True)
txt('4 × SHORT',LEFT,221,8,GRAY);txt('4 × SHORT',508,221,8,GRAY)
dim((x0,y0+hh+8),(x0+ww,y0+hh+8),'717.2 mm bay envelope',15)
y=379
y=step(1,'Make two long edge chains of <b>five LONG</b> channels and two short chains of <b>four SHORT</b> channels. Fit a SPLINT and two ties at every straight joint. Keep a 0.2 mm body gap. Per bay: 18 channels, 14 splints, 28 splice ties.',y)
y=step(2,'Fit four CORNER_NODE parts as on page 4. Set the outside reference rectangle to <b>717.2 × 564.8 mm</b>. Each channel chain starts 6.1 mm from its virtual corner. Face lips point toward the tabletop; spine and nodes face you.',y)
y=step(3,'Add one RIB_ANCHOR at the midpoint of each edge: 358.6 mm on long edges, 282.4 mm on short edges. Its fence locates against the rail’s inward face. Use two rail ties per anchor.',y)
y=step(4,'Use releasable fasteners at the top cap’s two corner-to-top-rail joints and the top anchor’s two rail ties: <b>four releasable ties per bay</b>. The corner nodes remain attached to the side rails when the cap is lifted.',y)
para('<b>Check:</b> square corners, continuous paper slots, fully seated splice bosses and no tie across the paper groove. Ordinary ties may be cut for the first test; use removable fasteners for routine paper changes.',y)

# 10
page('PART 2 / WORKSHOP 2','Add the stepped rear ribs','“Horizontal” and “vertical” refer to a bay lying landscape on the bench.')
# Diagram each horizontal half low-high-low, short half low-high; center cross and layer keys.
xx,yy=305,234
rect(xx-16,yy-16,32,32,BLUE)
for sign in [-1,1]:
 for j,col in enumerate([ORANGE,HexColor('#b95a22'),ORANGE]):rect(xx+sign*(35+j*61)-(54 if sign<0 else 0),yy-6,54,12,col)
 for j,col in enumerate([HexColor('#b95a22'),ORANGE]):rect(xx-6,yy+sign*(30+j*47)-(40 if sign<0 else 0),12,40,col)
txt('LOW → HIGH → LOW',80,217,9,NAVY,True);txt('LOW ← HIGH ← LOW',347,217,9,NAVY,True)
txt('Outer edge → LOW → HIGH → center',181,103,9,NAVY,True)
txt('Outer edge → LOW → HIGH → center',181,354,9,NAVY,True)
txt('Raised vertical seats',337,271,8,GRAY);arrow((337,270),(313,247))
y=371
y=step(1,'Set RIB_CROSS at the bay center (358.6, 282.4). Its horizontal seats are lower; its vertical seats are 3 mm higher. The ribs cross at different heights and must not be forced into one plane.',y)
y=step(2,'Each horizontal half, from edge to center, is <b>H_LOW → H_HIGH → H_LOW</b>. Each vertical half is <b>V_LOW → V_HIGH</b>. Keep all contact shoes pointing toward the paper. Substitute docking low ribs only at the stations on page 12.',y)
y=step(3,'Overlap adjacent beam ends by <b>16 mm</b>. Align the two hole pairs and thread one tie through both layers, returning through the second hole. Repeat at each anchor and each cross-node attachment. The holes are 8 mm apart.',y)
# Layer overlap detail drawn large; one tie around aligned diamond-hole pair.
rect(LEFT+50,588,177,9,ORANGE);rect(LEFT+195,579,177,9,HexColor('#b95a22'))
for x in [LEFT+203,LEFT+219]:ln(x,574,x,602,INK,1.5)
ln(LEFT+203,574,LEFT+219,574,INK,1.5);ln(LEFT+203,602,LEFT+219,602,INK,1.5)
dim((LEFT+195,603),(LEFT+227,603),'16 mm overlap (schematic)',13)
y=650
y=para('<b>Per bay:</b> six horizontal pieces + four vertical pieces, four anchors, one cross. Rib connections use 14 ties: 6 intermediate laps, 4 outer endpoints and 4 cross-node attachments.',y)
para('<b>Check:</b> both holes align at every lap; low/high shoes reach the same paper plane; opposing ends stop short of each other at the center. A tightly tied joint must not crush or bow the beam.',y)

# 11
page('PART 2 / WORKSHOP 3','Insert the paper and retention cord','Keep every 22 × 28 inch sheet whole. No holes through the posterboard.')
# Paper front with two retention spans and top cap lift arrow.
rect(125,135,363,212,HexColor('#faf9f4'),GRAY)
for x in [122,488]:rect(x,135,4,212,ORANGE)
rect(122,347,370,4,ORANGE);rect(122,121,370,4,ORANGE)
ln(125,241,488,241,INK,1.1);ln(306.5,135,306.5,347,INK,1.1)
arrow((502,143),(502,113));txt('Lift top cap',422,102,9,NAVY,True)
txt('Two front cord spans',187,281,10,NAVY,True);txt('Rear ribs and shoes sit behind this sheet',174,302,8,GRAY)
y=373
y=step(1,'Open the four releasable top-cap ties and lift off the complete five-piece cap chain. Keep its four internal splints tied. The top rib anchor may stay on its rib; it clears the paper plane.',y)
y=step(2,'Slide the whole sheet down the two side grooves and into the bottom groove. Support the sheet to avoid buckling. Refit the top cap and its four releasable ties. Do not tighten so hard that the paper slot closes.',y)
y=step(3,'Run smooth 0.8 mm cord across the front in both directions, through the edge midpoints. At each end, use the V-notch, wrap around the outside edge, and tie off at a rear-spine window. The short-edge notch lies at the central channel joint.',y)
y=step(4,'Tension only enough to retain the sheet toward the rear contact shoes. Do not bow the frame or indent the paper. Keep knots and tie tails behind the face. Leave the top-cap cord end easy to undo for replacement.',y)
y=note('<b>One-bay test before production:</b> lift and gently rack the framed sheet; check that it stays square, paper remains captured, cords do not cut the edge, and the top cap removes/refits without damage. Record any flutter or slack.',y+3)
para('Contact shoes and front cord oppose movement in both directions. This does not make the paper weatherproof. Let the one-bay result determine whether to continue with the full gate.',y)

# 12
page('PART 2 / WORKSHOP 4','Join three bays into a rigid border','Repeat this border four times. All coordinates below are viewed from the rear, face-down.')
# Border rear local coordinate map: x from left, y up. Four docks plus four receivers.
x0,y0,ww,hh=LEFT+7,123,514,139;sc=ww/2151.6
for bay in range(3):
 rect(x0+bay*ww/3,y0,ww/3,hh,HexColor('#faf9f4'),GRAY)
 txt(f'BAY {bay+1}',x0+bay*ww/3+55,y0+16,10,NAVY,True)
for x in [717.2,1434.4]:
 for y in [10,554.8]:rect(x0+x*sc-8,y0+hh-y*hh/564.8-3,16,6,BLUE)
for x in [424.0333,788.6333,1362.9667,1727.5667]:
 xx=x0+x*sc;rect(xx-4,y0+hh/2-4,8,8,ORANGE);arrow((xx,y0+hh+26),(xx,y0+hh/2+8))
for x,y in [(64,0),(500.8,0),(2151.6,64),(2151.6,500.8)]:rect(x0+x*sc-3,y0+hh-y*hh/564.8-3,6,6,GREEN)
txt('Green: field receivers',LEFT,306,9,GREEN,True);txt('Blue: fixed cell bridges',304,306,9,BLUE,True)
y=330
y=step(1,'Lay out bays 1–3 side by side. At each seam, fit a BORDER_BRIDGE near the top and another near the bottom, across the neighboring corner nodes. Thread two ties per bridge through the spare paired node holes. Per border: four bridges, eight ties.',y)
y=step(2,'Install four docking ribs at the stations below. Fit a pedestal and cap to each as on page 5 (two ties per dock). The cap socket centers lie on the bay midline, 282.4 mm from its bottom edge.',y)
y=table(['Bay / horizontal half-rib','Replace this LOW piece','Socket X from border left'],[['1 / right half','Innermost, next to cross','424.03 mm'],['2 / left half','Outermost, next to anchor','788.63 mm'],['2 / right half','Outermost, next to anchor','1362.97 mm'],['3 / left half','Innermost, next to cross','1727.57 mm']],y,[152,224,152])
y=step(3,'Add four FIELD_RECEIVER parts: two on bay 1’s bottom edge at X = <b>64 and 500.8 mm</b>; two on bay 3’s right edge at Y = <b>64 and 500.8 mm</b>. Seat fences inward and use two rail ties each. These are positions along a 564.8 mm field seam—not the full 717.2 mm bay width.',y)
para('<b>Check:</b> border size 2151.6 × 564.8 mm; three sheets remain removable; all four dock sockets align to one straight line; all four field receivers face rearward. Do not remove the fixed bridge ties for transport.',y)

# 13
page('PART 2 / PVC 1','Build the single backing frame','All main-frame and foot fittings are purchased 1-inch nominal PVC fittings.')
# Frame topology (lower tee continuation to legs); diagram not dimensioned outline pipe outer.
x1,x2,yt,yb=130,372,124,322
for a,b in [((x1,yt),(x2,yt)),((x1,yt),(x1,yb+32)),((x2,yt),(x2,yb+32)),((x1,yb),(x2,yb))]:ln(*a,*b,GRAY,6)
for x,y in [(x1,yt),(x2,yt),(x1,yb),(x2,yb)]:rect(x-7,y-7,14,14,BLUE)
for x in [x1,x2]:ln(x-34,yb+34,x+34,yb+34,GRAY,6);rect(x-6,yb+28,12,12,BLUE)
dim((x1,yt),(x2,yt),'2100 mm between axes',-24)
txt('Upper elbows × 2',398,142,9,NAVY,True);txt('Lower tees × 2',398,285,9,NAVY,True);txt('Legs continue down',398,304,8,GRAY)
arrow((396,297),(x2+10,yb));txt('Foot tees × 2',398,345,9,NAVY,True)
y=389
y=table(['Cut item','Qty','Example length','Nominal PVC'],[['Frame sides','4','2065.08 mm','1 inch'],['Legs','2','298.28 mm','1 inch'],['Grass half-feet','4','582.54 mm','1 inch'],['Hard-floor half-feet','4','1182.54 mm','1 inch; instead of short feet'],['Diagonal braces','4','425.69 mm','3/4 inch']],y,[149,35,108,236])
y=para('<b>Measure fittings before cutting.</b> For socketed pipes: cut length = required fitting-center span − take-up at each end. Take-up = center-to-mouth distance − actual pipe engagement. Examples use 17.4625 mm per fitting end; actual dry engagement may differ.',y)
y=para('Square the 2100 mm frame, then positively retain working sockets with the established screw/pin or permanent-joint method. The lower tees continue to two legs; foot tees turn across the frame plane and receive two half-feet each. Add four end caps.',y)
para('Keep the feet centered under the frame. With foot axes 25 mm below face datum, the leg center span is 333.2 mm. The main pipe axes are 55 mm behind the front face. The example cuts are not permission to substitute an unmeasured fitting.',y,small=True)

# 14
page('PART 2 / PVC 2','Install all eight printed brace joints','Each of the four diagonal braces has this connection at both ends.')
items=[inst('BRACE_LINK_45'),inst('PIPE_33',(0,0,38)),inst('PIPE_27',(90/math.sqrt(2),90/math.sqrt(2),33.95),rz(45))]
meshview(items,(LEFT,105,CW,187),view=(.5,-1,1.4))
txt('Exact CAD, saddles lifted off the link. Main-pipe saddle is larger; brace saddle is smaller.',LEFT,296,8,GRAY)
y=319
y=step(1,'Mark points 400 mm from each theoretical main-frame corner along its two pipe axes. Those points define the diagonal centerline. The 400 × 400 mm diagonal is 565.7 mm long.',y)
y=step(2,'Trim the brace tube 70 mm back from each theoretical endpoint: <b>425.7 mm actual tube length</b>. At either end, its saddle center lies 90 mm from the theoretical main-pipe intersection, or 20 mm from the trimmed tube end.',y)
y=step(3,'Put PIPE_33 and PIPE_27 on the same face of BRACE_LINK_45, over its two pads. Use two heavy ties per pad—<b>four link ties total</b>—through the pad slots and around each saddle foot. Flip the reversible flat link as required at mirrored corners.',y)
y=step(4,'Seat the main pipe and brace pipe in their saddles. Add one keeper tie around each saddle and its pipe. Check pipe seating and the frame’s squareness before tightening. A finished endpoint has four link ties plus two pipe keepers.',y)
y=note('<b>Gate totals:</b> 8 links + 8 main-pipe saddles + 8 brace saddles + 32 link ties + 16 brace pipe keepers. The other 16 PIPE_33 saddles and 16 keepers belong to the removable face docks.',y+4)
para('Use releasable pipe keepers if the PVC square must break down for transport. Retain the link-to-saddle ties. The printed joints position the brace; verify resistance to pipe sliding and joint rotation physically.',y)

# 15
page('PART 2 / BASES','Set up for grass or hard surfaces','Anchor the PVC structure before attaching the paper face. These are prototype base arrangements.')
# Two top views. y is fore-aft; frame line is across middle. Guys kept outboard.
for idx,title,span in [(0,'GRASS / SOIL','1200 mm foot span'),(1,'HARD SURFACE','2400 mm foot span')]:
 x=LEFT+idx*272;rect(x,112,256,217,PALE,r=5);txt(title,x+12,124,10,NAVY,True)
 ln(x+54,219,x+202,219,GRAY,4)
 for xx in [x+54,x+202]:
  ln(xx,166,xx,279,GRAY,4)
  for yy in [166,279]:
   if idx:rect(xx-11,yy-9,22,18,ORANGE);ln(xx,219,xx,yy,BLUE,1,[3,3])
   else:
    anchorx=xx-25 if xx<x+128 else xx+25;ln(xx,219,anchorx,yy,BLUE,1,[3,3]);rect(anchorx-3,yy-3,6,6,ORANGE)
 txt(span,x+37,300,9,NAVY,True)
y=350
y=heading('Grass: short feet + four opposing guys',y)
y=para('Use four short half-feet, giving 1200 mm fore–aft span at each foot. Tie four guys around the upper PVC corner fittings, two forward and two rearward. Put anchors outside the opening and away from the flight line; the prior layout uses X ≈ ±1600 mm and ±1200 mm fore–aft from the frame plane.',y)
y=para('Use suitable anchors for the actual soil. Check each installed anchor in its guy direction for movement. Keep lines only taut enough to brace the frame; do not bow the PVC. Mark the lines and anchors visibly.',y)
y=heading('Hard surface: long feet + strapped ballast + guys',y+5)
y=para('Swap in the long half-feet for 2400 mm fore–aft span. Put a weighed 15 kg bag near each foot end (four bags / 60 kg as an initial trial arrangement), with anti-slip material beneath. Strap each bag to its actual foot pipe. Attach its guy to the same foot end, about 1150 mm from the center.',y)
y=note('<b>60 kg is a starting test arrangement, not a validated wind rating.</b> Check sliding, foot lift, bag/strap movement, socket retention and frame distortion under gentle load in both directions. A loose bag placed nearby is not an anchored foot.',y+3)
para('Both setups need physical site checks. If the frame moves, an anchor loosens, or paper/joins start to fail, stop and lower the gate. No operating wind-speed limit has been established for this revision.',y)

# 16
page('PART 2 / FIELD','Attach, inspect and pack away','Four rigid face borders. Twenty-four removable snap bridges.')
y=101
y=step(1,'With the PVC backing supported and anchored, use two people to position a rigid border. Seat its four PIPE_33 saddles on the corresponding pipe and install/verify their keeper ties. Align the four cap/saddle sockets, then install four SNAP_BRIDGE keys as on page 5.',y)
y=step(2,'Repeat for the other three borders in the pinwheel layout on page 7. Adjacent border receivers meet at each field seam. Fit two SNAP_BRIDGE keys per seam, at 64 mm from each end of the 564.8 mm seam. Total: <b>16 dock keys + 8 seam keys</b>.',y)
y=heading('Before the first flight',y+3)
for s in ['All 24 keys fully seated; no cracked, permanently bent or partly engaged snap prongs.', 'All 32 pipe keeper ties installed; eight brace links secure; PVC sockets retained.', 'Every sheet captured; top caps secure; front cord lightly tensioned; no sharp tails toward the opening.', 'Face approximately 2716.4 mm square; nominal opening 1586.8 mm square. Check equal diagonals and that pipes, braces and guys stay outside the flight opening.', 'Gentle front/back and side loading causes no anchor creep, foot lift, slipping or joint movement. Start a monitored low-wind trial only after these checks.']:
 y=checkbox(s,y)
y=heading('Teardown and maintenance',y+7)
y=para('<b>1.</b> Support the face with two people. Release the eight seam keys and the dock keys one border at a time. Pinch/release each fork rather than prying a locked bridge. Put keys in a labeled pouch.',y)
y=para('<b>2.</b> Carry and store four rigid borders flat or well supported. Leave the channel splints, rib laps, cell bridges and other workshop ties installed. Release backing-frame keepers/socket retainers only if breaking the PVC structure down.',y)
y=para('<b>3.</b> Remove guys/ballast only after the structure is supported or lowered. Inspect keys, pipe clips, ties and paper before the next setup. Replace damaged prints and wet or torn paper.',y)
y=para('<b>Paper replacement:</b> loosen the appropriate cord and four top-cap ties; lift the five-piece cap chain, slide out the sheet, fit a new whole sheet, then refit and retension. The bay’s corner nodes and rear ribs can remain attached.',y)
para('<b>Record:</b> first-build date __________  location/surface __________  observed fit or movement ______________________________  parts revised ______________________________',y,small=True)

assert not OVERFLOW,OVERFLOW
C.save()
(O/'manual_assets'/'manual_manifest.json').write_text(json.dumps({'pdf':'Assembly_and_Test_Instructions.pdf','pages':PAGENO,'headings':HEADINGS,'printed_types':19,'printed_count':740,'prototype_parts':9,'overflow_checks':OVERFLOW},indent=2))
print('Built',PAGENO,'pages:',O/'Assembly_and_Test_Instructions.pdf')

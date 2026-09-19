"""PVC-dominant paper gate study. CAD mm; scene metres. Printable fabrication prototypes."""
from pathlib import Path
exec(Path(__file__).with_name('build_a1_full_size.py').read_text().split('# Registered channel splice:')[0],globals())
import ast,csv
OUT=ROOT/'output/pvc_paper_gate'
for d in ['printable','renders']:(OUT/d).mkdir(parents=True,exist_ok=True)
PARTS={}
for node in ast.parse(Path(__file__).with_name('build_paper_roll_study.py').read_text()).body:
 if isinstance(node,ast.FunctionDef) and node.name in ['cyl','window','roundplate','export3mf']:exec(compile(ast.Module(body=[node],type_ignores=[]),'<helpers>','exec'),globals())
ORANGE_PAPER=mat('Paper / orange',(.96,.255,.028));MAGNET=mat('Exposed front magnets',(.43,.47,.5),.82);THREAD=mat('Tension cord / turquoise',(.015,.55,.41))
S=2700.;W=609.6;A=50.;B=W-A;C=S-B;D=S-A;H2=2*S-W;AXIS=24.;BORE=34.2;RI=BORE/2
CORNER_STOP=50.;CORNER_MOUTH=80.;TEE_STOP=50.;TEE_MOUTH=80.;MAG_OFFSET=32.
def tear(r):return [(r*math.cos(math.radians(135+270*i/72)),r*math.sin(math.radians(135+270*i/72))) for i in range(73)]+[(0,r*2**.5)]
def axprof(name,prof,length,start,angle=0):
 o=extrude_x(name,prof,length,start,STEEL);raw_transform(o,Rz(angle));return o
# Closed horizontal sockets use the accepted support-free peaked roof, all printed face down.
def socket(angle,stop,mouth,wall=4):
 ro=RI+wall;prof=[(-ro,0),(ro,0),(ro,AXIS),(ro/2**.5,AXIS+ro/2**.5),(0,AXIS+ro*2**.5),(-ro/2**.5,AXIS+ro/2**.5),(-ro,AXIS)]
 return axprof('Socket shell and broad flat foot',prof,mouth-stop+5,stop-5,angle)
def bore(angle,stop,mouth):return axprof('Blind pipe socket / positive stop',[(y,z+AXIS) for y,z in tear(RI)],mouth-stop+1,stop,angle)
def eye(o,xy,angle=0):
 # Raised fairlead, horizontal diamond tunnel. Its floor stays behind the paper.
 q=box('Cord fairlead',(xy[0],xy[1],6),(12,10,12),STEEL);add(o,q)
 q=axprof('Cord eye',[(0,3.2),(2.2,5.4),(0,7.6),(-2.2,5.4)],16,-8,angle);raw_transform(q,T(*xy,0));boolean(o,q)
def lug(o,xy):
 add(o,cyl('Magnet face lug',(xy[0],xy[1],.2),9,2.8,STEEL));window(o,xy,3.15,.4)
def cleat(o,xy):
 # Twin low horns, with sloping underside; figure-eight wraps plus final half hitch.
 for dx in [-8,8]:
  add(o,cyl('Cleat stem',(xy[0]+dx,xy[1],2.8),3,6,STEEL,n=32))
  vs=[(xy[0]+dx+r*math.cos(i*math.tau/32),xy[1]+r*math.sin(i*math.tau/32),z) for r,z in [(3,8),(5,10) ] for i in range(32)]
  add(o,mesh('45 degree cleat horn',vs,[tuple(reversed(range(32))),tuple(range(32,64))]+[(i,(i+1)%32,(i+1)%32+32,i+32) for i in range(32)],STEEL))
  add(o,cyl('Horn cap',(xy[0]+dx,xy[1],9.9),5,1.6,STEEL,n=32))
# Inner and outer corners need different diagonal directions. One is not a rotated copy of the other.
for code,angles,mp in [('OUTER_90_45',[0,90,45],(-32,-32)),('INNER_90_45',[0,90,225],(32,32))]:
 o=box('Corner core',(0,0,6),(44,44,12),STEEL)
 for angle in angles:
  # Rib joins the blind socket stop to the center over its whole width.
  q=axprof('Root web',[(-16,0),(16,0),(16,12),(-16,12)],CORNER_STOP,0,angle);add(o,q)
  add(o,socket(angle,CORNER_STOP,CORNER_MOUTH))
 # Corner magnet pad + wide connected gusset, placed 18 mm inside paper boundary.
 # Use a rectangle to guarantee a connected generous pad support for either quadrant.
 add(o,box('Pad support',(mp[0]/2,mp[1]/2,1.5),(abs(mp[0])+20,abs(mp[1])+20,3),STEEL));lug(o,mp)
 for angle in angles:boolean(o,bore(angle,CORNER_STOP,CORNER_MOUTH))
 sign=-1 if code.startswith('OUTER') else 1
 eye(o,(20*sign,32*sign),90);eye(o,(32*sign,20*sign),0);cleat(o,(0,0))
 master(code,o,'1-inch PVC 90-degree corner + '+('inward' if code.startswith('OUTER') else 'outward')+' 45-degree socket; 30 mm engagement; integral magnet lug and cord cleat')
# T body: native ports left/right/down; face pad lies in open quadrant above the horizontal run.
o=box('T central core',(0,0,6),(44,44,12),STEEL)
for angle in [0,180,270]:
 add(o,axprof('T root web',[(-16,0),(16,0),(16,12),(-16,12)],TEE_STOP,0,angle));add(o,socket(angle,TEE_STOP,TEE_MOUTH));boolean(o,bore(angle,TEE_STOP,TEE_MOUTH))
add(o,box('T face pad support',(0,0,1.5),(84,84,3),STEEL))
for xx in [-32,32]:
 for yy in [-32,32]:lug(o,(xx,yy))
for xx in [-1,1]:
 for yy in [-1,1]:
  eye(o,(20*xx,32*yy),90);eye(o,(32*xx,20*yy),0)
cleat(o,(-10,-10))
master('STACK_TEE',o,'Three coplanar 1-inch PVC sockets; 30 mm engagement; same tee rotates for all divider junctions; optional unused port in single-height gate')
# Universal slide-on paper edge sleeve: local pipe axis X, magnetic face offset +32 in Y.
ro=RI+3.2;prof=[(-ro,0),(ro,0),(ro,AXIS),(ro/2**.5,AXIS+ro/2**.5),(0,AXIS+ro*2**.5),(-ro/2**.5,AXIS+ro/2**.5),(-ro,AXIS)]
o=axprof('Slide sleeve with broad foot',prof,14,-7)
boolean(o,axprof('Through bore',[(y,z+AXIS) for y,z in tear(RI)],16,-8))
add(o,box('Offset face web',(0,17,1.5),(20,50,3),STEEL));lug(o,(0,32));eye(o,(0,23),0)
master('EDGE_SLEEVE',o,'One slide-on part for every straight edge; 14 mm engagement; offset magnet center 32 mm toward paper edge; cord eye clocks/locates clip')
# Tiny cord-supported backing pads hold the short paper overlap seams between the two PVC rails.
o=roundplate('Cord magnet saddle',32,20,3,r=4,material=STEEL);window(o,(0,0),3.15,.4)
for x in [-11,11]:eye(o,(x,0),0)
master('CORD_SADDLE',o,'Small backing magnet on a seam cord; two fairleads; no printed spanning rail')
# A compact fit gauge shares the actual sleeve bore, roof and print orientation.
o=axprof('Fit gauge outer',prof,8,-4);boolean(o,axprof('Gauge bore',[(y,z+AXIS) for y,z in tear(RI)],10,-5));master('FIT_GAUGE',o,'34.2 mm nominal bore, print flat in same orientation as production sleeves; fit test only')
# Optional front pad remains the previous production geometry.
o=roundplate('Optional paper pad',24,24,3,r=6);window(o,(0,0),3.15,.4);master('PAPER_PAD',o,'Optional front magnet pad; frame-side .4 mm plastic skin is always retained')
# Exact assembly graph. XY are front-face coordinates, Z is depth behind paper.
def V(x,y):return Vector((x,y,0))
def gate(kind):
 stack=kind=='split_s';ready=kind!='basic';H=H2 if stack else S
 nodes={};edges=[];placements=[];magnets=[];seams=[]
 def node(n,code,x,y,rot,mag=True):
  nodes[n]={'code':code,'xy':(x,y),'rot':rot,'stop':TEE_STOP if code=='STACK_TEE' else CORNER_STOP}
  placements.append((code,(x,y),rot))
  if mag:
   q={'OUTER_90_45':(-32,-32),'INNER_90_45':(32,32),'STACK_TEE':(32,32)}[code];v=Rz(rot)@Vector((q[0]/1000,q[1]/1000,0));magnets.append((x+v.x*1000,y+v.y*1000))
 def edge(n,a,b,clips=0,side=1):
  aa=V(*nodes[a]['xy']);bb=V(*nodes[b]['xy']);u=(bb-aa).normalized();length=(bb-aa).length-nodes[a]['stop']-nodes[b]['stop'];start=aa+u*nodes[a]['stop'];end=bb-u*nodes[b]['stop']
  e={'name':n,'a':a,'b':b,'length_mm':round(length,3),'start':list(start[:2]),'end':list(end[:2])};edges.append(e)
  # Offset toward requested paper edge, common part rotates about its bore.
  angle=math.degrees(math.atan2(u.y,u.x))+(0 if side==1 else 180)
  for i in range(1,clips+1):
   t=i/(clips+1);p=aa+(bb-aa)*t;placements.append(('EDGE_SLEEVE',tuple(p[:2]),angle));v=Rz(angle)@Vector((0,.032,0));magnets.append((p.x+v.x*1000,p.y+v.y*1000))
 for name,x,y,r in [('OLB',A,A,0),('ORB',D,A,90),('ORT',D,H-A,180),('OLT',A,H-A,270)]:node(name,'OUTER_90_45',x,y,r)
 if ready:
  node('OCB','STACK_TEE',S/2,A,180,False);node('OCT','STACK_TEE',S/2,H-A,0,False)
  edge('Outer bottom left','OLB','OCB',3,-1);edge('Outer bottom right','OCB','ORB',3,-1)
  edge('Outer top left','OLT','OCT',3,1);edge('Outer top right','OCT','ORT',3,1)
  magnets.extend([(S/2-32,18),(S/2+32,H-18)])
 else:edge('Outer bottom','OLB','ORB',7,-1);edge('Outer top','OLT','ORT',7,1)
 if not stack:
  for name,x,y,r in [('ILB',B,B,0),('IRB',C,B,90),('IRT',C,C,180),('ILT',B,C,270)]:node(name,'INNER_90_45',x,y,r)
  for n,a,b,side in [('Inner bottom','ILB','IRB',1),('Inner top','ILT','IRT',-1),('Inner left','ILB','ILT',-1),('Inner right','IRB','IRT',1)]:edge(n,a,b,4,side)
  if ready:
   node('JLL','STACK_TEE',A,C,90,False);node('JRL','STACK_TEE',D,C,270,False)
   for side,base,top,j in [(1,'OLB','OLT','JLL'),(-1,'ORB','ORT','JRL')]:
    edge('Outer lower riser '+j,base,j,5,side);edge('Outer short riser '+j,j,top,1,side)
  else:
   edge('Outer left','OLB','OLT',7,1);edge('Outer right','ORB','ORT',7,-1)
  for a,b in [('OLB','ILB'),('ORB','IRB'),('ORT','IRT'),('OLT','ILT')]:edge('Diagonal '+a,a,b)
 else:
  for name,x,y,r in [('ILB',B,B,0),('IRB',C,B,90),('IRT',C,H-B,180),('ILT',B,H-B,270)]:node(name,'INNER_90_45',x,y,r)
  # Two full divider rails; no crossing PVC diagonals and no coincident nested frames.
  for row,y in [('L',C),('U',D)]:
   for col,x,r in [('OLEFT',A,90),('ILEFT',B,0 if row=='L' else 180),('IRIGHT',C,0 if row=='L' else 180),('ORIGHT',D,270)]:node(row+col,'STACK_TEE',x,y,r,False)
   edge('Divider left stub '+row,row+'OLEFT',row+'ILEFT',1,1 if row=='L' else -1)
   edge('Divider opening rail '+row,row+'ILEFT',row+'IRIGHT',4,-1 if row=='L' else 1)
   edge('Divider right stub '+row,row+'IRIGHT',row+'ORIGHT',1,1 if row=='L' else -1)
  for side,base,top,k in [(1,'OLB','OLT','OLEFT'),(-1,'ORB','ORT','ORIGHT')]:
   edge('Outer lower riser '+k,base,'L'+k,5,side);edge('Outer divider riser '+k,'L'+k,'U'+k,1,side);edge('Outer upper riser '+k,'U'+k,top,5,side)
  edge('Inner bottom','ILB','IRB',4,1);edge('Inner top','ILT','IRT',4,-1)
  for side,base,top,k in [(-1,'ILB','ILT','ILEFT'),(1,'IRB','IRT','IRIGHT')]:
   edge('Inner lower riser '+k,base,'L'+k,4,side);edge('Inner upper riser '+k,'U'+k,top,4,side)
  for a,b in [('OLB','ILB'),('ORB','IRB'),('ORT','IRT'),('OLT','ILT')]:edge('Diagonal '+a,a,b)
 # Paper: full horizontal bands and side inserts with 36 mm overlap at each end.
 openings=[(W,S-W)] if not stack else [(W,S-W),(S,H-W)]
 paper=[(0,0,S,W),(0,H-W,S,W)]+([(0,S-W,S,W)] if stack else [])
 for low,high in openings:
  for x in [0,S-W]:paper.append((x,low-36,W,high-low+72))
  for sy in [low-18,high+18]:
   for x0,x1 in [(18,W-18),(S-W+18,S-18)]:
    seams.append([(x0,sy,5.4),(x1,sy,5.4)])
    # End on the outer rail plus its inward line; outside clip turns toward outer edge.
    ox=A if x0<100 else D;angle=90 if ox==A else 270
    # Do not place sleeves over socket bodies. Near inner ends, integral corner pads or tee tabs carry the line.
    near_tee=any(n['code']=='STACK_TEE' and abs(n['xy'][0]-ox)<.01 and abs(abs(n['xy'][1]-sy)-32)<.01 for n in nodes.values())
    if not near_tee:placements.append(('EDGE_SLEEVE',(ox,sy),angle))
    magnets.append((18 if ox==A else S-18,sy))
    for t in [1/3,2/3]:
     x=x0+(x1-x0)*t;placements.append(('CORD_SADDLE',(x,sy),0));magnets.append((x,sy))
 # T divider magnet pads are at 32x32 offsets. Populate only those aligning with overlap endpoints.
 if stack:
  # Inner tee pads can be oriented only 0 or 180 while retaining the required pipe directions.
  for n in ['LILEFT','LIRIGHT','UILEFT','UIRIGHT']:
   x,y=nodes[n]['xy'];magnets.append((x+(32 if 'ILEFT' in n else -32),y+(-32 if n.startswith('L') else 32)))
 return {'kind':kind,'height_mm':H,'nodes':nodes,'edges':edges,'placements':placements,'magnets':magnets,'seams':seams,'paper_rectangles':paper,'openings':openings,'counts':dict(collections.Counter(p[0] for p in placements))}
GATES={k:gate(k) for k in ['basic','stack_ready','split_s']}
EYES={'OUTER_90_45':[(-20,-32),(-32,-20)],'INNER_90_45':[(20,32),(32,20)],'STACK_TEE':[(20*x,32*y) for x in [-1,1] for y in [-1,1]]+[(32*x,20*y) for x in [-1,1] for y in [-1,1]],'EDGE_SLEEVE':[(0,23)],'CORD_SADDLE':[(-11,0),(11,0)]}
def world_eyes(code,xy,angle):
 return [(xy[0]+(Rz(angle)@Vector((x/1000,y/1000,0))).x*1000,xy[1]+(Rz(angle)@Vector((x/1000,y/1000,0))).y*1000,5.4) for x,y in EYES[code]]
for g in GATES.values():
 g['eyes']=[{'code':code,'part_xy':xy,'holes':world_eyes(code,xy,r)} for code,xy,r in g['placements']]
 g['cord_routes']=[]
 for e in g['edges']:
  aa=V(*g['nodes'][e['a']]['xy']);bb=V(*g['nodes'][e['b']]['xy']);u=(bb-aa).normalized();dd=(bb-aa).length;ee=[]
  for code,xy,r in g['placements']:
   if code!='EDGE_SLEEVE':continue
   d=V(*xy)-aa;t=d.dot(u)
   if abs(d.x*u.y-d.y*u.x)<.01 and 0<t<dd:ee.append((t,world_eyes(code,xy,r)[0]))
  ee.sort();mid=tuple((aa+bb)/2)
  if e['name'].startswith('Diagonal'):
   # Retaining line wraps over the back of each socket shell, then ties to the central cleats.
   q=aa+u*55;r=bb-u*55
   g['cord_routes'].append({'name':e['name'],'points':[(aa.x,aa.y,11),(q.x,q.y,56),(r.x,r.y,56),(bb.x,bb.y,11)],'routing':'Over backs of socket shells; finish on central cleats. Schematic bend centers.'})
   continue
  target0=ee[0][1] if ee else mid;target1=ee[-1][1] if ee else mid
  ends=[]
  for n,t in [(g['nodes'][e['a']],target0),(g['nodes'][e['b']],target1)]:
   origin=V(*n['xy']);target=V(t[0],t[1])-origin;side=target.x*u.y-target.y*u.x
   candidates=world_eyes(n['code'],n['xy'],n['rot'])
   def lateral(v):return (v[0]-origin.x)*u.y-(v[1]-origin.y)*u.x
   good=[v for v in candidates if abs(abs(lateral(v))-32)<.01 and (not ee or lateral(v)*side>0)]
   ends.append(min(good or candidates,key=lambda v:(v[0]-t[0])**2+(v[1]-t[1])**2))
  g['cord_routes'].append({'name':e['name'],'points':[ends[0]]+[p for _,p in ee]+[ends[1]],'routing':'Through raised fairleads; hand tension, figure-eight wraps and locking half hitch.'})
 # Seam lines use actual raised eye positions, with backing saddles between them.
 all_eyes=[p for r in g['eyes'] if r['code']!='CORD_SADDLE' for p in r['holes']]
 g['seam_routes']=[]
 for a,c in g['seams']:
  candidates=[v for v in all_eyes if abs(v[1]-a[1])<.01]
  first=min(candidates,key=lambda v:abs(v[0]-a[0]));last=min(candidates,key=lambda v:abs(v[0]-c[0]))
  g['seam_routes'].append([first,last])
 g['brace_routes']=[]
 for lo,hi in g['openings']:
  for x0,x1 in [(27,W-27),(S-W+27,S-27)]:
   corners=[min(all_eyes,key=lambda v:(v[0]-xx)**2+(v[1]-yy)**2) for xx,yy in [(x0,lo),(x1,hi),(x1,lo),(x0,hi)]]
   g['brace_routes'].extend([corners[:2],corners[2:]])
# Nested cuts use real stops, 3 mm kerf, 10 mm reserve for damaged stock ends.
def stock_plan(edges):
 bins=[]
 for e in sorted(edges,key=lambda e:-e['length_mm']):
  need=e['length_mm']+3
  fits=[(b['remaining_mm']-need,i) for i,b in enumerate(bins) if b['remaining_mm']>=need]
  if fits:i=min(fits)[1]
  else:i=len(bins);bins.append({'stock':i+1,'remaining_mm':3038.,'cuts':[]})
  bins[i]['cuts'].append({'name':e['name'],'length_mm':e['length_mm']});bins[i]['remaining_mm']-=need
 return bins
for k,g in GATES.items():
 g['stock_plan']=stock_plan(g['edges']);g['PVC_sticks']=len(g['stock_plan']);g['PVC_cost_usd']=6*g['PVC_sticks'];g['PVC_cut_length_m']=sum(e['length_mm'] for e in g['edges'])/1000
 g['magnet_pairs']=len(g['magnets']);g['printed_pieces']=sum(g['counts'].values())
# Slicing recipes: one large fitting each, batch sleeve / seam backing parts, and fit plate.
PLATES={}
for c in ['OUTER_90_45','INNER_90_45','STACK_TEE','EDGE_SLEEVE','CORD_SADDLE','FIT_GAUGE']:
 PLATES['ONE_'+c]=[(c,5,5)];export3mf('ONE_'+c,PLATES['ONE_'+c])
for code in ['EDGE_SLEEVE','CORD_SADDLE']:
 w,h,_=PARTS[code]['print_bounds_mm'];nx=int(173//(w+3));ny=int(173//(h+3));p=[(code,5+i*(w+3),5+j*(h+3)) for j in range(ny) for i in range(nx)];PLATES['BATCH_'+code]=p;export3mf('BATCH_'+code,p)
PLATES['FIRST_FIT']=[('OUTER_90_45',5,5),('EDGE_SLEEVE',145,5),('CORD_SADDLE',136,86),('FIT_GAUGE',5,134),('PAPER_PAD',55,140)]
export3mf('FIRST_FIT',PLATES['FIRST_FIT'])
# Exact quantity queues; batch tail plates avoid printing unnecessary spares.
for kind,g in GATES.items():
 g['print_queue']={}
 for code,qty in g['counts'].items():
  recipe='BATCH_'+code if 'BATCH_'+code in PLATES else 'ONE_'+code;cap=len(PLATES[recipe]);full,tail=divmod(qty,cap)
  if full:g['print_queue'][recipe]=full
  if tail:
   n='TAIL_'+code+'_'+str(tail)
   if n not in PLATES:PLATES[n]=PLATES[recipe][:tail];export3mf(n,PLATES[n])
   g['print_queue'][n]=1
rows=[{'code':c,**{k:v for k,v in p.items() if k not in ['object','print_mesh']}} for c,p in PARTS.items()]
(OUT/'BOM.json').write_text(json.dumps({'paper_width_mm':W,'width_mm':S,'opening_mm':S-2*W,'pipe_OD_mm':33.4,'socket_bore_mm':BORE,'pipe_axis_depth_mm':AXIS,'parts':rows,'gates':GATES,'plates':PLATES,'optional_front_pads':True,'PVC_stock_price':{'length_mm':3048,'USD':6,'source':'user supplied'},'estimate_scope':'Face skeleton only. Separate base, guys, anchors, paper, magnets and cord are not included in print/PVC frame cost.'},indent=2))
# Assembly visibility audit: every printed vertex and pipe endpoint radius stays within opaque paper face.
def covered(x,y,g,eps=.01):return any(x0-eps<=x<=x0+w+eps and y0-eps<=y<=y0+h+eps for x0,y0,w,h in g['paper_rectangles'])
CHECKS={}
for kind,g in GATES.items():
 bad=[]
 for code,xy,r in g['placements']:
  M=T(*xy,0)@Rz(r)
  for v in PARTS[code]['object'].data.vertices:
   p=M@v.co
   if not covered(p.x*1000,p.y*1000,g):bad.append([code,round(p.x*1000,2),round(p.y*1000,2)]);break
 CHECKS[kind]={'printed_parts_with_vertices_outside_paper':bad,'magnets_outside_paper':[(x,y) for x,y in g['magnets'] if not covered(x,y,g)]}
(OUT/'geometry_checks.json').write_text(json.dumps(CHECKS,indent=2))
# Visual scenes use the exact masters and pipe cut ledger.
def instance(code,xy=(0,0),angle=0,M=Matrix.Identity(4)):
 ob=bpy.data.objects.new(code,PARTS[code]['object'].data);COL.objects.link(ob);ob.matrix_world=M@T(*xy,0)@Rz(angle);return ob
FRONT=basis((1,0,0),(0,0,1),(0,1,0),(-1350,0,50))
def ln(name,pts,r=1.2,material=THREAD,M=FRONT):return line(name,[M@Vector(tuple(x/1000 for x in p)) for p in pts],r/1000,material)
def render_gate(g,paper=True,cord=True,M=FRONT):
 coll('01 / exact printable parts')
 for code,xy,a in g['placements']:instance(code,xy,a,M)
 coll('02 / 1 inch PVC from cut ledger')
 for e in g['edges']:
  aa=M@Vector((e['start'][0]/1000,e['start'][1]/1000,AXIS/1000));bb=M@Vector((e['end'][0]/1000,e['end'][1]/1000,AXIS/1000));tube(e['name'],aa,bb,.0334,WHITE,.00338)
 coll('03 / paper and aligned magnets')
 if paper:
  for i,(x,y,w,h) in enumerate(g['paper_rectangles']):
   o=box('Paper '+str(i+1),(x+w/2,y+h/2,-.18-i*.01),(w,h,.18),ORANGE_PAPER);raw_transform(o,M)
 for x,y in g['magnets']:
  o=cyl('Front magnet',(x,y,-2.5),3,2,MAGNET,n=32);raw_transform(o,M)
 if cord:
  coll('04 / prethreaded tension and paper seam cords')
  for path in g['cord_routes']:ln('Socket retaining / locating cord '+path['name'],path['points'],M=M)
  for p in g['seam_routes']:ln('Paper overlap seam cord',p,M=M)
  for p in g['brace_routes']:ln('Side-band anti-racking X',p,M=M)
def ground_support(g):
 # Anchoring study only; deliberately not counted as a certified base.
 H=g['height_mm']/1000+.05
 coll('80 / anchoring concept, purchase hardware separately')
 for x in [-1.18,1.18]:
  cube('Low ballast foot',(x,.04,.035),(.19,1.5,.07),DARK)
  for y in [-.6,.7]:cube('Illustrative ballast bag',(x,y,.11),(.35,.30,.16),DARK)
 for x in [-1.30,1.30]:
  for y in [-1.65,1.72]:line('External guy / anchor required',[(x,.06,H-.16),(x,y,.06)],.002,THREAD)
setup('01_SINGLE_FRONT',(0,-6,1.67),(0,0,1.67),5.9,False);render_gate(GATES['stack_ready'],True)
header('01','PVC carries the frame / paper is the face','2700 mm square. Every pipe and printed fitting sits behind paper; front magnets align 18 mm inside its boundaries.')
footer('Single-height, stack-ready configuration. All rendered frame parts are the printable masters. Base/anchors are a separate installation requirement.')
setup('02_SINGLE_BACK',(3.3,4.6,3.4),(0,0,1.67),5.9,False);render_gate(GATES['stack_ready'],False)
header('02','Two PVC perimeters / four diagonal PVC links','Printed 90 + 45 corners, sliding magnetic sleeves, and prethreaded cord. Two side tees prepare the single gate for upward extension.')
footer('Blue fittings are printed PETG; white members are 1-inch PVC. Cord preloads the sockets and supports overlap seams; no zip ties or rail printing.')
setup('03_SPLIT_S_FRONT',(0,-8,2.80),(0,0,2.80),10.2,False);render_gate(GATES['split_s'],True)
header('03','Add the second opening / share the middle band','2700 x 4790.4 mm paper outline. Two 1480.8 mm square openings and one 609.6 mm shared divider.')
footer('Full-height extension concept. This is about 4.84 m above ground with the shown 50 mm clearance; anchoring and physical qualification are still required.')
setup('04_SPLIT_S_BACK',(4,7,4.8),(0,0,2.80),10.2,False);render_gate(GATES['split_s'],False)
header('04','A shared divider / no colliding PVC diagonals','Eight divider tees join the openings and outer uprights; two more tees split the top and bottom rails for transport.')
footer('The top four corner fittings and their two diagonals move upward. Preinstalled side tees let the stack-ready version extend without recutting its PVC.')
setup('05_PRINTED_PARTS',(.29,-.50,.42),(.07,.06,.02),.73,False);coll('01 / part family')
for c,xy,r in [('OUTER_90_45',(-125,0),0),('INNER_90_45',(65,0),0),('STACK_TEE',(245,0),0),('EDGE_SLEEVE',(-100,155),0),('CORD_SADDLE',(20,155),0)]:instance(c,xy,r)
header('05','Five structural part types / PVC spans the gate','Two corner orientations, one universal tee, one slide-on sleeve, and one small cord-supported seam backing.')
footer('All sockets target 33.4 mm OD PVC with 34.2 mm trial clearance. Each prints flat on the paper face; peaked bores avoid support inside the sockets.')
# Flat native coordinates give clear detail in CAD and rendering.
setup('06_CORNER_AND_DIAGONAL',(.9,-1.1,.95),(.30,.30,.02),1.26,False);coll('01 / two different corner sockets')
instance('OUTER_90_45');instance('INNER_90_45',(509.6,509.6))
tube('45 degree PVC diagonal',(.050/2**.5,.050/2**.5,.024),((509.6-50/2**.5)/1000,(509.6-50/2**.5)/1000,.024),.0334,WHITE,.00338)
for c,xy in [('OUTER_90_45',(0,0)),('INNER_90_45',(509.6,509.6))]:
 for a in [0,90]:
  u=Vector((math.cos(math.radians(a)),math.sin(math.radians(a)),0));start=Vector((xy[0]/1000,xy[1]/1000,.024))+u*.05;tube('Perimeter pipe',start,start+u*.17,.0334,WHITE,.00338)
ln('Diagonal retaining cord',[(0,0,11),(39,39,56),(470.6,470.6,56),(509.6,509.6,11)],M=Matrix.Identity(4))
header('06','90 degree corner + 45 degree spoke socket','Outer and inner fittings point their diagonal sockets in opposite directions. Broad webs support the sockets and integral magnetic face pads.')
footer('PVC inserts 30 mm to a hard stop. An accessible cord tie draws the two fittings together and retains the diagonal. Do not rely on dry friction alone.')
setup('07_MAGNET_SLEEVE',(.17,-.22,.18),(.00,.018,.028),.26,False);coll('01 / actual universal paper sleeve')
instance('EDGE_SLEEVE');tube('1 inch PVC',(-.078,0,.024),(.078,0,.024),.0334,WHITE,.00338)
cube('Paper cutaway',(.008,.033,-.0002),(.1,.030,.00018),ORANGE_PAPER)
o=cyl('Rear magnet',(0,32,.4),3,2,MAGNET);o=cyl('Bare front magnet',(0,32,-2.4),3,2,MAGNET)
ln('Locating cord through sleeve eye',[(-80,23,5.4),(80,23,5.4)],M=Matrix.Identity(4))
header('07','Slide on / align with the paper / tension the cord','The rear magnet stays behind a 0.4 mm plastic face. The front magnet contacts the paper; optional front pads remain available.')
footer('Pipe centerline is 50 mm behind the paper boundary in plan. The 32 mm offset puts every standard edge magnet 18 mm inside the paper.')
setup('08_SHARED_DIVIDER',(1.5,4.0,3.2),(0,0,2.50),4.4,False)
g=GATES['split_s'];coll('01 / divider printed fittings')
for code,xy,r in g['placements']:
 if C-100<=xy[1]<=D+100:instance(code,xy,r,FRONT)
coll('02 / divider PVC pipes')
for e in g['edges']:
 if not (e['name'].startswith('Divider') or e['name'].startswith('Outer divider')):continue
 aa=FRONT@Vector((e['start'][0]/1000,e['start'][1]/1000,AXIS/1000));bb=FRONT@Vector((e['end'][0]/1000,e['end'][1]/1000,AXIS/1000));tube(e['name'],aa,bb,.0334,WHITE,.00338)
header('08','Divider upgrade / one tee used in eight positions','Two horizontal PVC rails border the shared paper band. Four short stubs connect them to the outer uprights.')
footer('The two retained outer riser tees become four; four more tees connect the two inner openings. The four displaced corner fittings move to the new top.')
setup('09_FIRST_FIT_PLATE',(.30,-.30,.37),(.09,.09,.025),.38,False);coll('01 / supplied first prototype plate')
box('180 mm A1 Mini bed',(90,90,-1),(180,180,2),GROUND)
for code,x,y in PLATES['FIRST_FIT']:
 pm=PARTS[code]['print_mesh'];o=bpy.data.objects.new(code,pm);COL.objects.link(o);o.location=(x/1000,y/1000,0)
header('09','First fit / one corner, sleeve, seam saddle and gauge','Five pieces including one optional front paper pad. Test actual PVC, magnet grip, cord retention and hand assembly before a full build.')
footer('Use FIRST_FIT_A1Mini_PETG.3mf after slicing. PETG / 0.4 mm nozzle / 0.20 mm layers / no supports / no scaling.')
# Isolated structural study with anchors visible, no claim that their schematic dimensions are qualified.
setup('10_SPLIT_S_ANCHORING',(5,-7,5.7),(0,0,2.80),10.7,True);render_gate(GATES['split_s'],True);ground_support(GATES['split_s'])
header('10','Working layout / four external guys and anchored feet','Keep guys outside the flight openings. The tall configuration needs a separately qualified ground or ballast system.')
footer('Illustrative anchoring only: bags and foot sizes are placeholders, not a ballast specification or wind rating. Erect the frame flat with helpers.')
for name in ['01_ASSEMBLED','00_MASTERS']:
 if bpy.data.scenes.get(name):bpy.data.scenes.remove(bpy.data.scenes[name])
bpy.context.window.scene=bpy.data.scenes['01_SINGLE_FRONT'];bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'PVC_Paper_Gate.blend'))
if '--no-render' not in sys.argv:
 for sc in bpy.data.scenes:
  selected=os.environ.get('RENDER_SCENES','')
  if selected and sc.name not in selected.split(','):continue
  bpy.context.window.scene=sc;sc.render.filepath=str(OUT/'renders'/f'{sc.name}.png');bpy.ops.render.render(write_still=True,scene=sc.name)
print('PVC GATE BUILT',json.dumps({k:{'counts':g['counts'],'PVC_sticks':g['PVC_sticks'],'magnet_pairs':g['magnet_pairs']} for k,g in GATES.items()}),flush=True)
print('VISIBILITY',json.dumps(CHECKS),flush=True)

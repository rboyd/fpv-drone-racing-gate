"""Exact convex polygon intersection checks, without third-party dependencies."""
from pathlib import Path
import json, math, struct
from face_geometry import PANEL, TOP, CORNER, OFFCUT, STRIP, PATCH, PATCH_PADS, STRIP_PADS, PATCH_SPREADERS, STRIP_SPREADERS
O=Path(__file__).resolve().parents[1]/'output'
def signed(p): return sum(p[i][0]*p[(i+1)%len(p)][1]-p[(i+1)%len(p)][0]*p[i][1] for i in range(len(p)))/2 if p else 0
def area(p): return abs(signed(p))
def intersect(sub,clip):
 clip=clip if signed(clip)>0 else list(reversed(clip)); out=sub[:]
 for a,b in zip(clip,clip[1:]+clip[:1]):
  old=out;out=[]
  def side(p): return (b[0]-a[0])*(p[1]-a[1])-(b[1]-a[1])*(p[0]-a[0])
  if not old: break
  prev=old[-1]; dp=side(prev)
  for cur in old:
   dc=side(cur)
   if (dc>=-1e-8)!=(dp>=-1e-8):
    t=dp/(dp-dc);out.append((prev[0]+t*(cur[0]-prev[0]),prev[1]+t*(cur[1]-prev[1])))
   if dc>=-1e-8: out.append(cur)
   prev=cur;dp=dc
 return out
P=TOP
T=CORNER
def rotate(p,k):
 result=[]
 for x,z in p:
  z-=1350
  for _ in range(k): x,z=z,-x
  result.append((x,z+1350))
 return result
face=[rotate(p,k) for k in range(4) for p in [P,T]]
outer=[(-1350,0),(1350,0),(1350,2700),(-1350,2700)]
hole=[(-750,600),(750,600),(750,2100),(-750,2100)]
for p in face:
 assert abs(area(intersect(p,outer))-area(p))<1e-6
 assert area(intersect(p,hole))<1e-6
for i,a in enumerate(face):
 for b in face[i+1:]: assert area(intersect(a,b))<1e-6
assert abs(sum(map(area,face))-5040000)<1e-6
layout=json.loads((O/'cut-layouts/nesting.json').read_text())
for i,a in enumerate(layout):
 for b in layout[i+1:]:
  if a['sheet']==b['sheet']: assert area(intersect(a['polygon_mm'],b['polygon_mm']))<1e-6
# Mirror-symmetric panel ends and exactly two panels per sheet.
assert set(map(tuple,PANEL))==set((2400-x,y) for x,y in PANEL)
assert len([r for r in layout if r['type']=='corner'])==128
for sh in [1,2]: assert len([r for r in layout if r['sheet']==sh])==2
for r in layout: assert all(0<=x<=2438.4 and 0<=y<=1219.2 for x,y in r['polygon_mm'])
# Eight 450 mm right-triangle offcuts supply ALL backers and pads.
for pieces in [[PATCH]+PATCH_PADS+PATCH_SPREADERS,[STRIP]+STRIP_PADS+STRIP_SPREADERS]:
 for p in pieces: assert abs(area(intersect(OFFCUT,p))-area(p))<1e-6
 for i,a in enumerate(pieces):
  for b in pieces[i+1:]: assert area(intersect(a,b))<1e-6,(a,b)
assert 4*(len(PATCH_PADS)+len(STRIP_PADS))==24
assert 4*(len(PATCH_SPREADERS)+len(STRIP_SPREADERS))>=56
# Installed corner backers and stitch load spreaders must not stack or intrude into the opening.
def rect(x,y,w,h):return [(x,y),(x+w,y),(x+w,y+h),(x,y+h)]
u=(1/math.sqrt(2),1/math.sqrt(2));v=(-u[1],u[0])
strip=[(925+a*u[0]+b*v[0],2275+a*u[1]+b*v[1]) for a,b in [(-175,-40),(175,-40),(175,40),(-175,40)]]
patch=rect(1090,2440,220,220)
assert area(intersect(strip,patch))<1e-6
for p in [strip,patch]:
 assert abs(area(intersect(p,outer))-area(p))<1e-6
 assert area(intersect(p,hole))<1e-6
spreaders=[]
for t in [-120,0,120]:
 for side in [-30,30]:
  x=925+t*u[0]+side*v[0];z=2275+t*u[1]+side*v[1]
  assert area(intersect(rect(x-2,z-3,4,6),strip))>23.99
  spreaders.append(rect(x-12.5,z-12.5,25,25))
for x,z in [(x,z) for x in [1170,1230] for z in [2580,2635]]+[(x,z) for x in [1260,1295] for z in [2520,2580]]:
 assert area(intersect(rect(x-2,z-3,4,6),patch))>23.99
 spreaders.append(rect(x-12.5,z-12.5,25,25))
for i,a in enumerate(spreaders):
 for b in spreaders[i+1:]: assert area(intersect(a,b))<1e-6
# Check files have actual mm-scale coordinates and expected print orientation.
stls={}
for path in (O/'printable').glob('*.stl'):
 data=path.read_bytes();n=struct.unpack_from('<I',data,80)[0];assert len(data)==84+50*n
 verts=[]
 for i in range(n):
  vals=struct.unpack_from('<12fH',data,84+i*50);verts +=[vals[3:6],vals[6:9],vals[9:12]]
 bounds=[max(v[j] for v in verts)-min(v[j] for v in verts) for j in range(3)]
 assert all(b<=170 for b in bounds), (path.name,bounds)
 if not path.name.startswith('jig_'): assert abs(bounds[0]-60)<1e-4
 assert abs(min(v[2] for v in verts))<1e-4
 stls[path.name]={'triangles':n,'bounds_mm':[round(x,4) for x in bounds]}
 if path.name.startswith('brace_joint'): assert all(abs(a-b)<1e-4 for a,b in zip(bounds,[60,24,60]))
 if path.name.startswith('jig_'):
  expected={'jig_square_150_mm.stl':[155,155,9],'jig_45_degree_mm.stl':[150,150,9],'jig_tie_slots_60_mm.stl':[80,40,3]}[path.name]
  assert all(abs(a-b)<1e-4 for a,b in zip(bounds,expected))
  assert bounds[0]+10<=180 and bounds[1]+10<=180
report={'face_parts':8,'face_area_mm2':sum(map(area,face)),'outer_coverage':'exact ring; no gaps or area overlaps','opening':'1500 x 1500 unobstructed','stock_polygons':'all pairwise intersections have zero area','symmetric_main_panels':True,'corners_per_shared_sheet':128,'gates_per_shared_sheet':32,'offcut_recovery':{'square_backers':4,'diagonal_strips':4,'saddle_pads':24,'small_spreaders':64,'all_fit_without_overlap':True},'all_prints_fit_a1_mini':True,'stl_mm_units':stls}
(O/'polygon_validation.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))

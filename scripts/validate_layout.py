"""Exact convex polygon intersection checks, without third-party dependencies."""
from pathlib import Path
import json, math, struct
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
P=[(-1350,2700),(1050,2700),(1050,2400),(750,2100),(-750,2100)]
T=[(1050,2700),(1350,2700),(1050,2400)]
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
# Main offcut can supply the diagonal backer AND an optional corner.
big=[(0,0),(600,0),(0,600)]
u=(1/math.sqrt(2),-1/math.sqrt(2));v=(1/math.sqrt(2),1/math.sqrt(2))
back=[(250+a*u[0]+b*v[0],250+a*u[1]+b*v[1]) for a,b in [(-300,-50),(300,-50),(300,50),(-300,50)]]
corner=[(0,0),(300,0),(0,300)]
assert abs(area(intersect(big,back))-60000)<1e-6
assert area(intersect(back,corner))<1e-6
# Check files have actual mm-scale coordinates and expected print orientation.
stls={}
for path in (O/'printable').glob('*.stl'):
 data=path.read_bytes();n=struct.unpack_from('<I',data,80)[0];assert len(data)==84+50*n
 verts=[]
 for i in range(n):
  vals=struct.unpack_from('<12fH',data,84+i*50);verts +=[vals[3:6],vals[6:9],vals[9:12]]
 bounds=[max(v[j] for v in verts)-min(v[j] for v in verts) for j in range(3)]
 assert abs(bounds[0]-60)<1e-4
 assert abs(min(v[2] for v in verts))<1e-4
 stls[path.name]={'triangles':n,'bounds_mm':[round(x,4) for x in bounds]}
 if path.name.startswith('brace_joint'): assert all(abs(a-b)<1e-4 for a,b in zip(bounds,[60,24,60]))
report={'face_parts':8,'face_area_mm2':sum(map(area,face)),'outer_coverage':'exact ring; no gaps or area overlaps','opening':'1500 x 1500 unobstructed','stock_polygons':'all pairwise intersections have zero area','backer_in_offcut':True,'optional_corner_does_not_overlap_backer':True,'stl_mm_units':stls}
(O/'polygon_validation.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))

from pathlib import Path
import json,math,struct
from posterboard_options import OPTIONS,STOCK, GAP
O=Path(__file__).resolve().parents[1]/'output/posterboard_concepts'
report={}
def overlap(a,b):
 return min(a[0]+a[2],b[0]+b[2])-max(a[0],b[0])>1e-6 and min(a[1]+a[3],b[1]+b[3])-max(a[1],b[1])>1e-6
for o in OPTIONS:
 a,b=o['card'];nx,ny=o['grid'];L,W=o['cassette'];S=o['outer'];I=o['opening'];px,py=o['pitch']
 assert abs(S*S-I*I-4*L*W)<1e-5
 cassettes=[(0,L,L,W),(L,W,W,L),(W,0,L,W),(0,0,W,L)]
 for i,c in enumerate(cassettes):
  for d in cassettes[i+1:]:assert not overlap(c,d)
 assert max(o['leaf_lengths'])<=1200
 for x,y,w,h in o['stock_pattern']:
  assert x>=0 and y>=0 and x+w<=STOCK[0]+1e-6 and y+h<=STOCK[1]+1e-6
  assert abs(w*h-a*b)<1e-5
 for i,c in enumerate(o['stock_pattern']):
  for d in o['stock_pattern'][i+1:]:assert not overlap(c,d)
 assert len(o['stock_pattern'])*o['sheets']==o['inserts']
 assert abs(px-a-GAP)<1e-6 and abs(py-b-GAP)<1e-6
 o['equal_rail_segments_per_gate']=4*nx*ny*2*(math.ceil(px/150)+math.ceil(py/150))
 report[o['id']]={'four_cassettes_cover_exact_ring':True,'one_cardstock_size':True,'stock_nesting_no_overlap':True,'cuts':o['cuts'],'paper_sheets':o['sheets'],'outer_mm':round(S,2),'opening_mm':round(I,2),'packed_longest_mm':round(max(o['leaf_lengths']),2),'no_card_crosses_fold':True,'equal_U_rail_segments':o['equal_rail_segments_per_gate']}
for p in (O/'prototype_coupons').glob('*.stl'):
 data=p.read_bytes();n=struct.unpack_from('<I',data,80)[0];assert len(data)==84+50*n
 vs=[];overhangs=0
 for i in range(n):
  values=struct.unpack_from('<12fH',data,84+50*i);tri=[values[3:6],values[6:9],values[9:12]];vs.extend(tri)
  u=[tri[1][j]-tri[0][j] for j in range(3)];v=[tri[2][j]-tri[0][j] for j in range(3)]
  cross=[u[1]*v[2]-u[2]*v[1],u[2]*v[0]-u[0]*v[2],u[0]*v[1]-u[1]*v[0]]
  area=math.sqrt(sum(c*c for c in cross))/2
  if area>1e-5 and values[2]<-.72 and min(t[2] for t in tri)>.02:overhangs+=1
 dims=[max(v[j] for v in vs)-min(v[j] for v in vs) for j in range(3)]
 assert max(dims)<=170.001 and abs(min(v[2] for v in vs))<1e-5,(p,dims)
 assert overhangs==0,(p,overhangs)
 report.setdefault('coupons',{})[p.name]={'bounds_mm':[round(x,3) for x in dims],'triangles_steeper_than_45deg_down_above_bed':overhangs}
report['limitations']='Geometry, nesting and bed envelopes only; no physical fit, slicing, fatigue or structural validation.'
(O/'layout_validation.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))

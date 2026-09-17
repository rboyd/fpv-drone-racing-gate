"""Nominal rectangular layouts, verified stock nesting and parametric rail estimates."""
from pathlib import Path
from collections import defaultdict
import math,json,csv
O=Path(__file__).resolve().parent
SW,SH=558.8,711.2
rho=1.28;section=28;price_kg=20;price_sheet=.99

def grid_strip(x,y,length,depth,step,band,vertical=False):
 result=[]
 for d in range(0,depth,band):
  for t in range(0,length,step):
   a,b=min(step,length-t),min(band,depth-d)
   result.append((x+d,y+t,b,a) if vertical else (x+t,y+d,a,b))
 return result

def panels(step,band):
 return grid_strip(0,0,2700,600,step,band)+grid_strip(0,2100,2700,600,step,band)+grid_strip(0,600,1500,600,step,band,True)+grid_strip(2100,600,1500,600,step,band,True)

def edges(cells):
 lines=defaultdict(list)
 for x,y,w,h in cells:
  for xx in [x,x+w]:lines[('v',xx)].append((y,y+h))
  for yy in [y,y+h]:lines[('h',yy)].append((x,x+w))
 segs=[]
 for (axis,const),intervals in lines.items():
  pts=sorted(set(q for ab in intervals for q in ab))
  for a,b in zip(pts,pts[1:]):
   if any(lo<=(a+b)/2<=hi for lo,hi in intervals):segs.append((axis,const,a,b))
 return segs

def overlaps(a,b):
 x,y,w,h=a;xx,yy,ww,hh=b
 return min(x+w,xx+ww)-max(x,xx)>1e-7 and min(y+h,yy+hh)-max(y,yy)>1e-7

def check_rects(rects,stock=False):
 for x,y,w,h in rects:
  assert x>=0 and y>=0 and x+w<=(SW if stock else 2700) and y+h<=(SH if stock else 2700)
  if not stock:assert not overlaps((x,y,w,h),(600,600,1500,1500))
 for i,a in enumerate(rects):
  for b in rects[i+1:]:assert not overlaps(a,b),(a,b)

# Cut patterns use full nominal dimensions; actual inserts can be trimmed for fit later.
patterns={
 '600x450':[(0,0,450,600)],
 '300x450':[(0,0,450,300),(0,300,450,300)],
 '300x300':[(0,0,300,300),(0,300,300,300)],
 '300x250':[(x,y,250,300) for x in [0,250] for y in [0,300]],
 '300x200':[(0,y,300,200) for y in [0,200,400]]+[(300,y,200,300) for y in [0,300]],
 '150x150':[(x,y,150,150) for x in [0,150,300] for y in [0,150,300,450]],
}
options=[('600x450',450,600,18,[(0,0,150,600),(150,0,150,600)]),('300x450',450,300,36,[(x,y,150,300) for x in [0,150] for y in [0,300]]),('300x300',300,300,56,[]),('300x250',250,300,64,[(x,y,200,300) for x in [0,200] for y in [0,300]]),('300x200',300,200,84,[]),('150x150',150,150,224,[])]
rows=[];layouts={}
for name,step,band,n_full,trims in options:
 cells=panels(step,band);check_rects(cells)
 assert sum(w*h for _,_,w,h in cells)==5040000
 pattern=patterns[name];check_rects(pattern,True);check_rects(trims,True)
 expected=sorted([(min(w,h),max(w,h)) for _,_,w,h in cells])
 actual=sorted([(min(pattern[0][2:]),max(pattern[0][2:]))]*n_full+[(min(w,h),max(w,h)) for _,_,w,h in trims])
 assert expected==actual
 segs=edges(cells);length=sum(b-a for _,_,a,b in segs)/1000
 perimeter_sum=sum(2*(w+h) for _,_,w,h in cells)/1000
 assert abs(length-(perimeter_sum+16.8)/2)<1e-6
 sheets=math.ceil(n_full/len(pattern))+(1 if trims else 0)
 def mass(area):return (length*area*.00128*1.2+.25)*1.1
 kg=mass(section)
 row={'option':name,'panels':len(cells),'sheets':sheets,'sheet_USD':round(sheets*price_sheet,2),'shared_rails_m':round(length,2),'rail_pieces_max_150mm':sum(math.ceil((b-a)/150) for _,_,a,b in segs),'PETG_kg_base':round(kg,3),'PETG_kg_light_20mm2':round(mass(20),3),'PETG_kg_heavy_36mm2':round(mass(36),3),'spools_base':math.ceil(kg),'face_cost_consumed_USD':round(sheets*price_sheet+price_kg*kg,2),'face_cost_whole_spools_USD':round(sheets*price_sheet+price_kg*math.ceil(kg),2),'separate_cassette_rails_m':round(perimeter_sum,2),'paper_yield_percent':round(5.04/(sheets*SW*SH/1e6)*100,1)}
 rows.append(row);layouts[name]={'panels':cells,'edges':segs,'stock_pattern':pattern,'full_panels_required':n_full,'trim_sheet':trims}
# Same large paper pieces, supported halfway across 600 mm depth.
row=rows[0].copy();row['option']='600x450_with_mid_rib'
extra_rib_m=8.4;extra_kg=extra_rib_m*10*.00128*1.2*1.1
row['PETG_kg_base']=round(rows[0]['PETG_kg_base']+extra_kg,3)
for area,key in [(20,'PETG_kg_light_20mm2'),(36,'PETG_kg_heavy_36mm2')]:row[key]=round(rows[0][key]+extra_kg,3)
row['extra_support_ribs_m']=extra_rib_m;row['extra_support_rib_area_mm2']=10
row['rail_pieces_max_150mm']+=56
row['spools_base']=math.ceil(row['PETG_kg_base'])
row['face_cost_consumed_USD']=round(row['sheet_USD']+row['PETG_kg_base']*price_kg,2)
row['face_cost_whole_spools_USD']=row['sheet_USD']+row['spools_base']*price_kg
rows.append(row)
report={'assumptions':{'stock_mm':[SW,SH],'stock_USD':price_sheet,'PETG_density_g_cm3':rho,'filament_USD_kg':price_kg,'shared_rail_section_mm2':section,'rail_section_sensitivity_mm2':[20,36],'joiner_node_allowance_fraction_of_rails':.2,'PVC_mount_allowance_kg':.25,'waste_fraction':.1,'excludes':'Existing PVC frame, brace connectors, feet, ballast, stakes, labor, coatings, shipping and tax'},'options':rows,'layouts':layouts}
(O/'posterboard_hybrid.json').write_text(json.dumps(report,indent=2))
keys=list(rows[-1]);
with (O/'posterboard_hybrid.csv').open('w') as f:
 writer=csv.DictWriter(f,fieldnames=keys);writer.writeheader();writer.writerows(rows)
for r in rows:print(r)

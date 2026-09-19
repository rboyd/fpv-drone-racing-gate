"""Reposition accepted fittings and choose sleeves from explicit paper-edge gaps.
No new fitting geometry. Dimensions in mm. Paper retention requires physical testing.
"""
from pathlib import Path
import json, math, collections, csv, zipfile, xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'output/compact_gate_study';BASE=ROOT/'output/corner_guide_elbow'
OUT.mkdir(exist_ok=True);(OUT/'printable').mkdir(exist_ok=True)
b=json.loads((BASE/'BOM.json').read_text());base=b['gates']['single'];prices=json.loads((ROOT/'docs/material_costs.json').read_text())
TARGET=350.;OFFSET=57.;STOP=35.;INSET=75.
def rot(p,a):
 c,s=math.cos(math.radians(a)),math.sin(math.radians(a));return (c*p[0]-s*p[1],s*p[0]+c*p[1])
def csvout(path,rows):
 with path.open('w') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
def stock(edges):
 bins=[]
 for e in sorted(edges,key=lambda e:-e['length_mm']):
  need=e['length_mm']+3;choices=[(s['remaining_mm']-need,i) for i,s in enumerate(bins) if s['remaining_mm']>=need-.001]
  if choices:i=min(choices)[1]
  else:i=len(bins);bins.append({'stock':i+1,'remaining_mm':3038.,'cuts':[]})
  bins[i]['remaining_mm']-=need;bins[i]['cuts'].append({'pipe':e['name'],'length_mm':e['length_mm']})
 return bins

def gate(opening,band):
 S=opening+2*band;grid=[75,band-75,S-band+75,S-75];nodes={};placements=[];mags=[]
 for key,old in base['nodes'].items():
  i,j=int(key[1]),int(key[2]);p=(grid[i],grid[j]);code=old['code'];angle=old['angle'];active=[]
  for q in b['magnet_pockets_local_mm'][code]:
   dx,dy=rot(q,angle);oldpos=(old['xy'][0]+dx,old['xy'][1]+dy)
   if min(math.dist(oldpos,m) for m in base['magnets'])<.01:active.append(q);mags.append((round(p[0]+dx,4),round(p[1]+dy,4)))
  nodes[key]={'xy':p,'code':code,'angle':angle,'active_pockets':active};placements.append((code,p,angle))
 fixed_mags=mags.copy();edges=[]
 for old in base['edges']:
  a=nodes[old['a']]['xy'];z=nodes[old['b']]['xy'];dist=math.dist(a,z);u=((z[0]-a[0])/dist,(z[1]-a[1])/dist);angle=old['sleeve_angle'];ox,oy=rot((0,57),angle)
  # Find the facing fixed magnet at each endpoint on this paper-edge/seam line.
  anchor=[]
  for key in [old['a'],old['b']]:
   node=nodes[key];hits=[]
   for q in node['active_pockets']:
    dx,dy=rot(q,node['angle']);p=(node['xy'][0]+dx,node['xy'][1]+dy)
    if abs((p[0]-a[0]-ox)*u[1]-(p[1]-a[1]-oy)*u[0])<.01:hits.append((p[0]-a[0])*u[0]+(p[1]-a[1])*u[1])
   assert hits,(old['name'],key)
   anchor.append(max(hits) if key==old['a'] else min(hits))
  span=anchor[1]-anchor[0];n=max(0,math.ceil(span/TARGET)-1);sleeves=[]
  for k in range(1,n+1):
   t=anchor[0]+span*k/(n+1);p=(a[0]+t*u[0],a[1]+t*u[1]);assert 80<=t<=dist-80,(opening,band,old['name'],t,dist)
   placements.append(('MAG_SLEEVE',p,angle));mags.append((round(p[0]+ox,4),round(p[1]+oy,4)));sleeves.append(round(t-STOP,3))
  edges.append({'name':old['name'],'a':old['a'],'b':old['b'],'length_mm':round(dist-70,3),'sleeve_angle':angle,'sleeves_from_cut_start_mm':sleeves,'sleeve_count':n,'fixed_magnet_span_mm':round(span,3),'maximum_magnet_gap_mm':round(span/(n+1),3),'kind':'long' if dist>500 else 'short'})
 counts=dict(collections.Counter(p[0] for p in placements));queue={f'ONE_{c}':n for c,n in counts.items() if c!='MAG_SLEEVE'}
 full,tail=divmod(counts['MAG_SLEEVE'],7)
 if full:queue['BATCH_MAG_SLEEVE']=full
 if tail:queue[f'TAIL_MAG_SLEEVE_{tail}']=1
 nesting=stock(edges);paper_length=(2*S+2*(opening+72))/1000;area=paper_length*band/1000
 g={'id':f'OPEN_{opening}_PAPER_{round(band/25.4)}','opening_mm':opening,'band_mm':band,'band_inches':round(band/25.4),'outer_mm':S,'nodes':nodes,'edges':edges,'placements':placements,'magnets':mags,'fixed_magnets':fixed_mags,'counts':counts,'print_queue':queue,'stock_plan':nesting,'PVC_sticks':len(nesting),'PVC_m':sum(e['length_mm'] for e in edges)/1000,'paper_m':paper_length,'paper_m2':area,'gates_per_100ft_roll':int(30.48//paper_length),'paper_cuts':[{'quantity':2,'length_mm':S,'width_mm':band},{'quantity':2,'length_mm':opening+72,'width_mm':band}],'magnet_pairs':len(mags),'printed_pieces':sum(counts.values()),'maximum_magnet_gap_mm':max(e['maximum_magnet_gap_mm'] for e in edges),'target_magnet_gap_mm':TARGET,'short_cut_mm':round(band-220,3),'long_cut_mm':opening+80,'paper_rectangles':[(0,0,S,band),(0,S-band,S,band),(0,band-36,band,opening+72),(S-band,band-36,band,opening+72)]}
 assert len(set(mags))==len(mags)
 assert len(edges)==24 and g['maximum_magnet_gap_mm']<=TARGET+.001
 for s in nesting:assert s['remaining_mm']>=-.001
 assert counts['ELBOW']==2 and counts['DUAL_GUY_ELBOW']==2 and counts['TEE']==8 and counts['CROSS']==4
 csvout(OUT/(g['id']+'_PVC_Cuts.csv'),[{k:e[k] for k in ['name','length_mm','sleeve_count','sleeves_from_cut_start_mm','maximum_magnet_gap_mm']} for e in edges])
 csvout(OUT/(g['id']+'_Stock_Layout.csv'),[{'stick':s['stock'],**e} for s in nesting for e in s['cuts']])
 csvout(OUT/(g['id']+'_Paper_Cuts.csv'),g['paper_cuts'])
 csvout(OUT/(g['id']+'_Magnet_Positions.csv'),[{'x_mm':x,'y_mm':y} for x,y in mags])
 return g
GATES=[gate(o,w) for o in [1000,800] for w in [609.6,457.2,304.8]]
# Geometry-only tail plates are subsets of the already validated seven-sleeve plate.
ns={'m':'http://schemas.microsoft.com/3dmanufacturing/core/2015/02'}
ET.register_namespace('',ns['m'])
for tail in sorted({g['counts']['MAG_SLEEVE']%7 for g in GATES}-{0}):
 name=f'TAIL_MAG_SLEEVE_{tail}'
 if (BASE/'printable'/(name+'.3mf')).exists():continue
 with zipfile.ZipFile(BASE/'printable/BATCH_MAG_SLEEVE.3mf') as src:
  doc=ET.fromstring(src.read('3D/3dmodel.model'));resources=doc.find('m:resources',ns);build=doc.find('m:build',ns)
  for ob in list(resources)[tail:]:resources.remove(ob)
  for ob in list(build)[tail:]:build.remove(ob)
  with zipfile.ZipFile(OUT/'printable'/(name+'.3mf'),'w',zipfile.ZIP_DEFLATED) as dst:
   for n in src.namelist():dst.writestr(n,ET.tostring(doc,encoding='utf-8',xml_declaration=True) if n=='3D/3dmodel.model' else src.read(n))
report={'target_gap_mm':TARGET,'gap_status':'Design trial, not validated paper retention or wind rating','PVC_bore_mm':33.5,'gates':GATES}
(OUT/'layouts.json').write_text(json.dumps(report,indent=2))
for g in GATES:print(g['id'],g['counts'],g['maximum_magnet_gap_mm'],'sticks',g['PVC_sticks'],'paper_m2',round(g['paper_m2'],2))

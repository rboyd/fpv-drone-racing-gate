"""Nine full-size parts to test paper channels, splice, corner and complete PVC dock."""
from pathlib import Path
import json,zipfile,xml.etree.ElementTree as ET
O=Path(__file__).resolve().parents[1]/'output/a1_full_size'
NS='http://schemas.microsoft.com/3dmanufacturing/core/2015/02';ET.register_namespace('',NS)
placements=[('CHANNEL_LONG',5,5),('CHANNEL_SHORT',5,25),('SPLINT',5,45),('SNAP_BRIDGE',50,45),('DOCK_CAP',92,45),('PIPE_33',5,75),('CORNER_NODE',75,75),('DOCK_PEDESTAL',120,75),('RIB_H_LOW_DOCK',5,135)]
root=ET.Element('{'+NS+'}model',unit='millimeter');res=ET.SubElement(root,'resources');build=ET.SubElement(root,'build');boxes=[]
for i,(code,x,y) in enumerate(placements,1):
 with zipfile.ZipFile(O/'printable'/f'{code}.3mf') as z:r=ET.fromstring(z.read('3D/3dmodel.model'))
 obj=r.find('.//{*}object');obj.set('id',str(i));obj.set('name',code)
 vs=[]
 for v in obj.findall('.//{*}vertex'):
  v.set('x',str(float(v.get('x'))-5+x));v.set('y',str(float(v.get('y'))-5+y));vs.append([float(v.get(k)) for k in ['x','y','z']])
 lo=[min(v[j] for v in vs) for j in range(3)];hi=[max(v[j] for v in vs) for j in range(3)]
 assert lo[0]>=5 and lo[1]>=5 and abs(lo[2])<.001 and max(hi)<=175
 boxes.append((lo,hi));res.append(obj);ET.SubElement(build,'item',objectid=str(i))
for i,(lo,hi) in enumerate(boxes):
 for low,high in boxes[i+1:]:assert not all(min(hi[j],high[j])-max(lo[j],low[j])>0 for j in [0,1])
with zipfile.ZipFile(O/'printable'/'Minimal_Concept_Test_9_Parts.3mf','w',zipfile.ZIP_DEFLATED) as z:
 z.writestr('[Content_Types].xml','<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/></Types>')
 z.writestr('_rels/.rels','<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Target="/3D/3dmodel.model" Id="rel0" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/></Relationships>')
 z.writestr('3D/3dmodel.model',ET.tostring(root,encoding='utf-8',xml_declaration=True))
(O/'MINIMAL_TEST_PARTS.csv').write_text('part,quantity\n'+''.join(f'{code},1\n' for code,_,_ in placements))
print('Nine-piece concept test created; all parts on the bed, inside A1 Mini volume, no overlaps.')

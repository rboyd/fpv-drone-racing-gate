"""Convert the locally downloaded MK4 STEP assembly for Blender (requires cadquery-ocp)."""
from pathlib import Path
import json,time
from OCP.STEPCAFControl import STEPCAFControl_Reader
from OCP.TDocStd import TDocStd_Document
from OCP.TCollection import TCollection_ExtendedString,TCollection_AsciiString
from OCP.XCAFDoc import XCAFDoc_DocumentTool
from OCP.TDF import TDF_Label
from OCP.collections import Sequence_TDF_Label as TDF_LabelSequence
from OCP.TDataStd import TDataStd_Name
from OCP.Bnd import Bnd_Box
from OCP.BRepBndLib import BRepBndLib
from OCP.BRepMesh import BRepMesh_IncrementalMesh
from OCP.RWGltf import RWGltf_CafWriter
from OCP.collections import IndexedDataMap_TCollection_AsciiString_TCollection_AsciiString as TColStd_IndexedDataMapOfStringString
from OCP.Message import Message_ProgressRange
from OCP.TopLoc import TopLoc_Location
import argparse,zipfile,hashlib
parser=argparse.ArgumentParser();parser.add_argument('--zip',type=Path,default=Path.home()/'Downloads/printable-parts-for-geprc-mk4-7in-fpv-drone-frame-model_files.zip');parser.add_argument('--out',type=Path,default=Path('/tmp/fpv-geprc-reference'));args=parser.parse_args()
P=args.out;P.mkdir(parents=True,exist_ok=True)
with zipfile.ZipFile(args.zip) as archive:
 for n in archive.namelist():
  if n=='3D STEP/geprc-mk4-7in.stp' or n.endswith('.pdf'):
   if not (P/n).resolve().is_relative_to(P.resolve()):raise ValueError('Invalid archive path')
   archive.extract(n,P)
(P/'source.json').write_text(json.dumps({'zip_name':args.zip.name,'zip_sha256':hashlib.sha256(args.zip.read_bytes()).hexdigest(),'source_url':'https://www.printables.com/model/1515387-printable-parts-for-geprc-mk4-7in-fpv-drone-frame','creator':'Dendy','license':'CC-BY-NC-4.0'},indent=2))
doc=TDocStd_Document(TCollection_ExtendedString('geprc'));reader=STEPCAFControl_Reader();reader.SetNameMode(True);reader.SetColorMode(True)
print('READ START',flush=True);assert reader.ReadFile(str(P/'3D STEP/geprc-mk4-7in.stp')).name=='IFSelect_RetDone';print('TRANSFER',flush=True);assert reader.Transfer(doc)
st=XCAFDoc_DocumentTool.ShapeTool_s(doc.Main());roots=TDF_LabelSequence();st.GetFreeShapes(roots);rows=[]
def name(label):
 a=TDataStd_Name()
 return a.Get().ToExtString() if label.FindAttribute(TDataStd_Name.GetID_s(),a) else ''
def walk(label,loc=TopLoc_Location(),trail=''):
 local=st.GetLocation_s(label);world=loc.Multiplied(local);ref=TDF_Label();real=label
 if st.IsReference_s(label):st.GetReferredShape_s(label,ref);real=ref
 title=name(label) or name(real);path=trail+'/'+title
 if st.IsAssembly_s(real):
  seq=TDF_LabelSequence();st.GetComponents_s(real,seq)
  for i in range(1,seq.Length()+1):walk(seq.Value(i),world,path)
 else:
  shape=st.GetShape_s(real).Located(world);box=Bnd_Box();BRepBndLib.AddOptimal_s(shape,box,False,False)
  if not box.IsVoid():rows.append({'name':title,'path':path,'bounds':[box.CornerMin().X(),box.CornerMin().Y(),box.CornerMin().Z(),box.CornerMax().X(),box.CornerMax().Y(),box.CornerMax().Z()]})
for i in range(1,roots.Length()+1):walk(roots.Value(i))
(P/'assembly_bounds.json').write_text(json.dumps(rows,indent=2));print('LEAVES',len(rows),flush=True)
for r in rows:
 if any(x in r['path'].lower() for x in ['2806','7 inch','arms','antena','podvozek']):print(r,flush=True)
print('MESH',flush=True)
for i in range(1,roots.Length()+1):
 shape=st.GetShape_s(roots.Value(i));BRepMesh_IncrementalMesh(shape,.4,False,.4,True).Perform()
print('EXPORT',flush=True);writer=RWGltf_CafWriter(TCollection_AsciiString(str(P/'geprc.glb')),True)
assert writer.Perform(doc,TColStd_IndexedDataMapOfStringString(),Message_ProgressRange())
print('DONE', (P/'geprc.glb').stat().st_size,flush=True)

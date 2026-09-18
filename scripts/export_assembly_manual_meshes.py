import bpy,json
from pathlib import Path
O=Path(__file__).resolve().parents[1]/'output/a1_full_size'
bpy.ops.wm.open_mainfile(filepath=str(O/'A1_Full_Size_Gate.blend'))
parts={}
for ob in bpy.data.scenes['01_FULL_GATE'].objects:
 code=ob.get('part_code')
 if code and code not in parts:
  m=ob.data;m.calc_loop_triangles();parts[code]={'vertices':[[float(v*1000) for v in p.co] for p in m.vertices],'triangles':[list(t.vertices) for t in m.loop_triangles]}
assert len(parts)==19
(O/'manual_assets').mkdir(exist_ok=True)
(O/'manual_assets'/'part_meshes.json').write_text(json.dumps(parts))
print('Exported',len(parts),'actual CAD masters for manual illustrations.')

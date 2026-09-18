import bpy,sys,json
from pathlib import Path
O=Path(__file__).resolve().parents[1]/'output/sleeve_paper_gate'
bpy.ops.wm.open_mainfile(filepath=str(O/'Sleeve_Paper_Gate.blend'))
audit={}
for s in bpy.data.scenes:
 parts={}
 for o in s.objects:
  if o.type=='MESH':
   k=o.name.split('.')[0]
   if k in [p['code'] for p in json.loads((O/'BOM.json').read_text())['parts']]:parts[k]=parts.get(k,0)+1
 audit[s.name]=parts
(O/'scene_counts.json').write_text(json.dumps(audit,indent=2))
wanted=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
for s in bpy.data.scenes:
 if wanted and s.name not in wanted:continue
 bpy.context.window.scene=s
 s.render.filepath=str(O/'renders'/f'{s.name}.png')
 bpy.ops.render.render(write_still=True,scene=s.name)

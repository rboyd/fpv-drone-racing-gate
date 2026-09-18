import bpy,os
from pathlib import Path
O=Path(__file__).resolve().parents[1]/'output/paper_roll_study'
bpy.ops.wm.open_mainfile(filepath=str(O/'Paper_Roll_Joinery_Study.blend'))
for s in bpy.data.scenes:
 if os.environ.get('SCENES') and s.name not in os.environ['SCENES'].split(','):continue
 bpy.context.window.scene=s;s.render.filepath=str(O/'renders'/f'{s.name}.png');bpy.ops.render.render(write_still=True,scene=s.name)

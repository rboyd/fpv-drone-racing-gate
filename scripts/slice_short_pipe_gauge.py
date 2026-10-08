"""Slice the single 84.8 mm pipe cap gauge with the existing A1 Mini PETG preset."""
from pathlib import Path
import subprocess,json
R=Path(__file__).resolve().parents[1];O=R/'output/short_pipe_gauge';CONF=R/'output/corner_guide_elbow/slicer_profiles'
name='ONE_END_CAP_GAUGE_84_8';dest=O/'sliced'/name;dest.mkdir(parents=True,exist_ok=True)
args=['/Applications/BambuStudio.app/Contents/MacOS/BambuStudio','--debug','2','--load-settings',str(CONF/'machine.json')+';'+str(CONF/'process.json'),'--load-filaments',str(CONF/'filament.json'),'--arrange','0','--orient','0','--slice','0','--export-3mf',name+'_A1Mini_PETG.3mf','--outputdir',str(dest),str(O/'printable'/(name+'.3mf'))]
with (dest/'slicer.log').open('w') as f:subprocess.run(args,stdout=f,stderr=subprocess.STDOUT,check=True)
data=json.loads((dest/'result.json').read_text());assert data['return_code']==0
print(data['sliced_plates'],flush=True)

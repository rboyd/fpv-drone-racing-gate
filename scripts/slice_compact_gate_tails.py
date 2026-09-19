"""Slice only new partial sleeve batches with the existing production PETG presets."""
from pathlib import Path
import subprocess,concurrent.futures,json
r=Path(__file__).resolve().parents[1];o=r/'output/compact_gate_study';conf=r/'output/corner_guide_elbow/slicer_profiles'
def run(src):
 dest=o/'sliced'/src.stem;dest.mkdir(parents=True,exist_ok=True)
 cmd=['/Applications/BambuStudio.app/Contents/MacOS/BambuStudio','--debug','2','--load-settings',str(conf/'machine.json')+';'+str(conf/'process.json'),'--load-filaments',str(conf/'filament.json'),'--arrange','0','--orient','0','--slice','0','--export-3mf',src.stem+'_A1Mini_PETG.3mf','--outputdir',str(dest),str(src)]
 with (dest/'slicer.log').open('w') as f:subprocess.run(cmd,stdout=f,stderr=subprocess.STDOUT,check=True)
 data=json.loads((dest/'result.json').read_text());assert data['return_code']==0
 print(src.stem,data['sliced_plates'],flush=True)
if __name__=='__main__':
 with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:list(ex.map(run,(o/'printable').glob('*.3mf')))

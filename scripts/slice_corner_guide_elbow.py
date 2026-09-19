"""Slice the PVC-dominant gate prototypes and batch recipes using resolved local A1 Mini presets."""
from pathlib import Path
import json, subprocess, concurrent.futures
ROOT=Path(__file__).resolve().parents[1]; O=ROOT/'output/corner_guide_elbow'
PRE=Path('/Applications/BambuStudio.app/Contents/Resources/profiles/BBL'); EXE='/Applications/BambuStudio.app/Contents/MacOS/BambuStudio'
CONF=O/'slicer_profiles';CONF.mkdir(exist_ok=True)
def resolve(folder,name):
 d=json.loads((PRE/folder/(name+'.json')).read_text());v={}
 if d.get('inherits'):v.update(resolve(folder,d['inherits']))
 for n in d.get('include',[]):v.update(resolve(folder,n))
 v.update({k:x for k,x in d.items() if k not in ['inherits','include']});return v
settings={'machine':resolve('machine','Bambu Lab A1 mini 0.4 nozzle'),'process':resolve('process','0.20mm Standard @BBL A1M'),'filament':resolve('filament','Generic PETG @BBL A1M')}
settings['process'].update(enable_support='0',brim_type='no_brim',print_sequence='by layer',wall_loops='4',sparse_infill_density='20%',curr_bed_type='Textured PEI Plate')
for k,d in settings.items():(CONF/f'{k}.json').write_text(json.dumps(d,indent=2))
def run(src):
 name=src.stem;dest=O/'sliced'/name;dest.mkdir(parents=True,exist_ok=True)
 args=[EXE,'--debug','2','--load-settings',str(CONF/'machine.json')+';'+str(CONF/'process.json'),'--load-filaments',str(CONF/'filament.json'),'--arrange','0','--orient','0','--slice','0','--export-3mf',name+'_A1Mini_PETG.3mf','--outputdir',str(dest),str(src)]
 with (dest/'slicer.log').open('w') as f:subprocess.run(args,stdout=f,stderr=subprocess.STDOUT,check=True)
 r=json.loads((dest/'result.json').read_text());assert r['return_code']==0,r
 p=r['sliced_plates'][0];print(name, json.dumps(p),flush=True)
 return name
if __name__=='__main__':
 with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:list(ex.map(run,sorted((O/'printable').glob('*.3mf'))))

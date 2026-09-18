"""Use local bundled Bambu presets, resolving includes/inheritance before CLI slicing."""
from pathlib import Path
import json,subprocess
ROOT=Path(__file__).resolve().parents[1];O=ROOT/'output/rigid_whole_sheet';PRE=Path('/Applications/BambuStudio.app/Contents/Resources/profiles/BBL');EXE='/Applications/BambuStudio.app/Contents/MacOS/BambuStudio'
CONF=O/'slicer_profiles';CONF.mkdir(exist_ok=True)
def resolve(folder,name):
 p=PRE/folder/(name+'.json');d=json.loads(p.read_text());v={}
 if d.get('inherits'):v.update(resolve(folder,d['inherits']))
 for n in d.get('include',[]):v.update(resolve(folder,n))
 v.update({k:x for k,x in d.items() if k not in ['inherits','include']});return v
settings={
 'machine':resolve('machine','Bambu Lab A1 mini 0.4 nozzle'),
 'process':resolve('process','0.20mm Standard @BBL A1M'),
 'filament':resolve('filament','Generic PLA @BBL A1M')}
settings['process'].update(enable_support='0',brim_type='no_brim',print_sequence='by layer')
for k,d in settings.items():(CONF/f'{k}.json').write_text(json.dumps(d,indent=2))
for src,name in [('Mini_Fit_Test_and_Feet_LAYOUT.3mf','Mini_Fit_Test_A1Mini_PLA'),('Mini_1to15_Four_Borders_LAYOUT.3mf','Mini_1to15_A1Mini_PLA')]:
 dest=O/'sliced'/name;dest.mkdir(parents=True,exist_ok=True)
 args=[EXE,'--debug','2','--load-settings',str(CONF/'machine.json')+';'+str(CONF/'process.json'),'--load-filaments',str(CONF/'filament.json'),'--arrange','0','--orient','0','--slice','0','--export-3mf',name+'.3mf','--outputdir',str(dest),str(O/'printable'/src)]
 with (dest/'slicer.log').open('w') as f:subprocess.run(args,stdout=f,stderr=subprocess.STDOUT,check=True)
 result=json.loads((dest/'result.json').read_text());assert result['return_code']==0,result
 print(name,json.dumps(result['sliced_plates'][0]),flush=True)

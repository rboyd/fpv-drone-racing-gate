"""First-pass material arithmetic only; no load model or slicer estimate."""
from pathlib import Path
import csv,json,math
OUT=Path(__file__).resolve().parent
area_m2=2.7**2-1.5**2
rho=1.28 # g/cm3; Bambu PETG HF specification
price=20 # USD/kg planning assumption, not a current quote
rows=[]
for name,t in [('0.2 mm film',.2),('0.4 mm sheet',.4),('0.8 mm sheet',.8),('1.0 mm sheet',1),('4 mm sandwich: two 0.4 mm skins and 10% core',.8+(4-.8)*.1),('4 mm solid',4)]:
 kg=area_m2*t*rho
 rows.append({'construction':name,'equivalent_solid_mm':round(t,4),'face_kg':round(kg,4),'minimum_1kg_spools_no_extras':math.ceil(kg),'whole_spool_USD_at_20':20*math.ceil(kg)})
with (OUT/'printed_gate_materials.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
L=150;w=2;depth=3
# Each module includes its OWN perimeter; adjacent tiles have doubled ribs.
a=L*L-(L-2*w)**2 + 2*w*(L-2*w)-w*w
coverage=a/(L*L)
base=224*a*depth*rho/1e6
budgets=[]
for n in [1,2,3]:
 # Reserve 0.5 kg for joiners/mount clips and add 10% waste to entire build.
 max_face=max(0,n/1.1-.5)
 budgets.append({'spools':n,'uniform_sheet_mm_no_extras':n/(area_m2*rho),'max_3mm_lattice_coverage_with_500g_hardware_and_10pct_waste':max_face/(area_m2*rho*3)})
report={'area_m2':area_m2,'PETG_density_g_cm3':rho,'spool_filament_g':1000,'assumed_USD_kg':price,'rows':rows,'tile_grid':{'pitch_mm':150,'outer_tiles':18,'hole_tiles':10,'tiles':224,'tile_to_tile_seams':392,'nominal_flat_tiles_per_A1_mini_plate':1},'example_lattice':{'width_mm':w,'depth_mm':depth,'tile_area_fraction':coverage,'open_fraction':1-coverage,'face_kg':base,'new_joiner_and_PVC_clip_allowance_kg':.5,'waste_allowance_fraction':.1,'total_budget_kg':(base+.5)*1.1,'whole_spools':math.ceil((base+.5)*1.1)},'budgets':budgets}
# Existing brace connectors are retained support hardware, separate from new face.
current=json.loads((OUT.parent/'output/validation.json').read_text())
vol=current['PRINT / brace joint +45']['volume_mm3']*4+current['PRINT / brace joint -45']['volume_mm3']*4
report['retained_8_brace_connectors_solid_volume_kg']=vol*rho/1e6
(OUT/'printed_gate_materials.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))

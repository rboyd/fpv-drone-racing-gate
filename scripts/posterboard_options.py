"""Uniform insert options; mm, nominal stock. Four identical pinwheel cassettes."""
import math
STOCK=(558.8,711.2)
GAP=4.0 # 2 x 1.2 mm channel backs plus 1.6 mm combined paper clearance
OPTIONS=[
 dict(id='A',name='Quarter sheets',card=(355.6,279.4),grid=(6,2),sheets=12,cuts_per_sheet=3,fold_columns=[3],rib=False,stock_pattern=[(x,y,279.4,355.6) for x in [0,279.4] for y in [0,355.6]],note='48 identical inserts; one fold per cassette'),
 dict(id='B',name='Half sheets',card=(355.6,558.8),grid=(6,1),sheets=12,cuts_per_sheet=1,fold_columns=[3],rib=True,stock_pattern=[(0,y,558.8,355.6) for y in [0,355.6]],note='24 identical inserts; one cut per stock sheet'),
 dict(id='C',name='Whole sheets',card=(711.2,558.8),grid=(3,1),sheets=12,cuts_per_sheet=0,fold_columns=[1,2],rib=True,stock_pattern=[(0,0,558.8,711.2)],note='12 uncut inserts; two folds per cassette'),
 dict(id='D',name='Exact-size metric',card=(346.0,196.0),grid=(6,3),sheets=18,cuts_per_sheet=5,fold_columns=[3],rib=False,stock_pattern=[(x,y,196,346) for x in [0,196] for y in [0,346]],note='72 identical inserts; trim to 392 x 692, then quarter'),
]
for o in OPTIONS:
 a,b=o['card'];nx,ny=o['grid'];px,py=a+GAP,b+GAP;L,W=nx*px,ny*py
 o.update(pitch=(px,py),cassette=(L,W),outer=L+W,opening=L-W,inserts=4*nx*ny,cuts=o['sheets']*o['cuts_per_sheet'])
 o['leaf_lengths']=[(j-i)*px for i,j in zip([0]+o['fold_columns'],o['fold_columns']+[nx])]
 o['pack']=(max(o['leaf_lengths']),W,65 if len(o['leaf_lengths'])==3 else 40)
 o['channel_length_m']=4*nx*ny*2*(px+py)/1000
 o['rib_length_m']=(4*L/1000+(4*nx*W/1000 if o['id']=='C' else 0)) if o['rib'] else 0
 kg=o['channel_length_m']*23.52*.00128
 o['PETG_kg']=(kg*1.2+.25+.06*4*len(o['fold_columns'])+.12+o['rib_length_m']*10*.00128)*1.1
 o['spools']=math.ceil(o['PETG_kg']);o['paper_USD']=o['sheets']*.99
 o['consumed_USD']=o['PETG_kg']*20+o['paper_USD'];o['cash_USD']=o['spools']*20+o['paper_USD']
 o['field_fold_locks']=8*len(o['fold_columns']);o['field_corner_keys']=8;o['PVC_docks']=16
 # The first iteration uses two opposed U channels, not an unprintable flat H slot.
 o['max_insert_support_bay_mm']=(a/2 if o['id']=='C' else a,b/2 if o['rib'] else b)

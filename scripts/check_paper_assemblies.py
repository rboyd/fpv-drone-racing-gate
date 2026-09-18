from pathlib import Path
exec(Path(__file__).with_name('build_paper_roll_study.py').read_text().split('# Unit-aware 3MF exports')[0],globals())
def intersection(a,A,b,B):
 aa=a.copy();aa.data=a.data.copy();COL.objects.link(aa);raw_transform(aa,A)
 bb=b.copy();bb.data=b.data.copy();COL.objects.link(bb);raw_transform(bb,B)
 boolean(aa,bb,'INTERSECT');m=bmesh.new();m.from_mesh(aa.data);v=abs(m.calc_volume())*1e9;m.free();bpy.data.objects.remove(aa,do_unlink=True);return round(v,5)
def obj(k):return PARTS[k]['object']
I=Matrix.Identity(4);checks={}
for code in ['CLICK_SOCKET_25','CLICK_SOCKET_40']:
 checks['CLICK_KEY / '+code]=intersection(obj('CLICK_KEY'),I,obj(code),T(7,0,0))
for code in ['PAPER_SNAP_CAP_15','PAPER_SNAP_CAP_30']:
 checks['PAPER_SNAP_BASE / '+code]=intersection(obj('PAPER_SNAP_BASE'),I,obj(code),I)
checks['MAG_SPLICE_CAP / MAG_RAIL_END']=intersection(obj('MAG_SPLICE_CAP'),T(0,0,7)@Matrix.Diagonal((1,1,-1,1)),obj('MAG_RAIL_END'),I)
A=T(0,66.9,12)@Rz(-90);N=basis((0,0,1),(0,1,0),(-1,0,0),(-20,0,25))
pipe=cyl('Test pipe',(0,0,-20),16.7,100)
parts=[('collar front',obj('PVC_HALF_33'),I),('collar back',obj('PVC_HALF_33'),Rz(180)),('socket',obj('DOCK_SOCKET'),A),('tongue',obj('DOCK_TONGUE'),A),('frame node',obj('FRAME_DOCK_NODE'),A@N),('pipe',pipe,I)]
for i,(a,o,M) in enumerate(parts):
 for b,p,P in parts[i+1:]:checks[a+' / '+b]=intersection(o,M,p,P)
(OUT/'assembly_clearance_checks.json').write_text(json.dumps({'method':'Exact mesh boolean intersection at nominal assembly positions; excludes fasteners, adhesive and paper compression. Not a fit or load test.','intersection_mm3':checks},indent=2))
print(json.dumps(checks,indent=2));assert max(checks.values())<.05,checks

"""Executed inside build_gate.py; geometry in metres, STL output in mm."""
setup('10_CUTTING_JIGS',(-.05,-.60,1.8),(-.05,.10,0),1.25,False)
coll('01 / A1 Mini printable cutting jigs')
def jig_prism(name,points,height):
 n=len(points);verts=[(x,y,z) for z in [0,height] for x,y in points]
 faces=[tuple(reversed(range(n))),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
 mesh=bpy.data.meshes.new(name);mesh.from_pydata(verts,[],faces);mesh.update()
 o=bpy.data.objects.new(name,mesh);COL.objects.link(o);o.data.materials.append(ORANGE);return o

def jig_bool(o,c,operation='DIFFERENCE'):
 bpy.context.view_layer.objects.active=o
 m=o.modifiers.new('Jig geometry','BOOLEAN');m.operation=operation;m.solver='EXACT';m.object=c
 bpy.ops.object.modifier_apply(modifier=m.name);bpy.data.objects.remove(c,do_unlink=True)

def fence(o,loc,size):jig_bool(o,cube('Edge registration fence',loc,size,ORANGE),'UNION')
JIGS=[]
a=jig_prism('JIG / 150 mm square / flip fences down',[(0,0),(.155,0),(.155,.155),(0,.155)],.003)
jig_bool(a,cube('Open center',(.0775,.0775,0),(.125,.125,.03),ORANGE))
fence(a,(.0025,.0775,.0055),(.005,.155,.007))
fence(a,(.0775,.0025,.0055),(.155,.005,.007))
a['use']='Print flat with fences UP. Flip for use: fence inner faces register stock corner; opposite outside edges are exactly 150 mm away.'
a['nominal_mm']='155 x 155 x 9; 150 mm from fence contact faces to opposite guide edges'
export_stl(a,'jig_square_150_mm.stl');JIGS.append(a)
a.location=(-.40,-.10,.02)

b=jig_prism('JIG / 45 degree straightedge alignment',[(0,0),(.150,0),(0,.150)],.003)
c=jig_prism('Lightening opening',[(.015,.015),(.120,.015),(.015,.120)],.03);c.location.z=-.01;jig_bool(b,c)
fence(b,(.070,.0025,.0055),(.140,.005,.007))
b['use']='Print fences UP. Flip to register a straight sheet edge; use diagonal edge to set a metal straightedge to 45 degrees through two measured marks.'
export_stl(b,'jig_45_degree_mm.stl');JIGS.append(b);b.location=(-.12,-.10,.02)

c=jig_prism('JIG / seam tie marking / 60 mm span',[(0,0),(.080,0),(.080,.040),(0,.040)],.003)
for x in [.010,.070]:
 jig_bool(c,cube('4 x 6 mm marking aperture',(x,.020,0),(.004,.006,.02),ORANGE))
# Sight notches on both sides align the middle to the seam.
for y in [0,.040]:jig_bool(c,cube('Seam center sight notch',(.040,y,0),(.002,.008,.02),ORANGE))
c['use']='Align both center notches to seam; mark the two 4 x 6 mm slots 60 mm apart. Punch sheet and backer on a sacrificial board; do not drill the plastic template.'
export_stl(c,'jig_tie_slots_60_mm.stl');JIGS.append(c);c.location=(.20,-.06,.02)
# Demonstrate square jig fences down on a sheet corner; world geometry is schematic.
coll('02 / jig use and metal straightedge')
cube('Stock corner / 4 mm sheet',(-.17,.23,.002),(.24,.20,.004),BLUE)
# With X unchanged, flip about X: fence contact faces at x=5 mm and y=-5 mm.
demo=copy_obj(JIGS[0],'USE / square gauge fences DOWN',(-.295,.335,.007),(math.pi,0,0))
# Sheet corner is (-.29,.33), exactly at both inside fences.
line('USE / 150 mm mark', [(-.14,.33,.005),(-.14,.18,.005),(-.29,.18,.005)],.0007,DARK)
cube('Stock under straightedge',(.105,.255,.002),(.26,.26,.004),BLUE)
cube('Metal straightedge / schematic',(.105,.255,.009),(.32,.025,.01),METAL).rotation_euler.z=-math.pi/4
line('Measured 45 degree cut',[(.015,.345,.005),(.195,.165,.005)],.0008,DARK)
header('10','Small jigs. Long straight cuts.','A1 Mini: 180 x 180 mm bed. Largest jig: 155 x 155 mm; add a 5 mm brim if needed.')
overlay('150 mm SQUARE',.07,.77,.015,True)
overlay('Corner cuts + shoulder marks\nFlip fences downward to use',.07,.815,.012,color=MUTED)
overlay('45-DEGREE ALIGNMENT',.39,.77,.015,True)
overlay('Register edge; align a metal ruler\nVerify both measured endpoints',.39,.815,.012,color=MUTED)
overlay('TIE-SLOT TEMPLATE',.72,.77,.015,True)
overlay('60 mm between tie legs\nCenter notches track the seam',.72,.815,.012,color=MUTED)
footer('Jigs are marking/registration tools. Clamp a metal straightedge for knife cuts. Verify a printed gauge with a steel rule before use.')

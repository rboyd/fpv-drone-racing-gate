"""Symmetric face and recoverable offcuts. All coordinates are millimetres."""
import math
PANEL=[(0,600),(2400,600),(2400,450),(1950,0),(450,0),(0,450)]
TOP=[(x-1200,z+2100) for x,z in PANEL]
CORNER=[(1200,2550),(1350,2550),(1350,2700),(1200,2700)]
OFFCUT=[(0,0),(450,0),(0,450)]
u=(1/math.sqrt(2),-1/math.sqrt(2));v=(1/math.sqrt(2),1/math.sqrt(2))
STRIP=[(170+a*u[0]+b*v[0],170+a*u[1]+b*v[1]) for a,b in [(-175,-40),(175,-40),(175,40),(-175,40)]]
PATCH=[(0,0),(220,0),(220,220),(0,220)]
def rect(x,y,w,h):return [(x,y),(x+w,y),(x+w,y+h),(x,y+h)]
# Four of each triangle type per gate. Three saddle pads per triangle = 24.
PATCH_PADS=[rect(230,0,70,50),rect(230,50,70,50),rect(230,100,70,50)]
STRIP_PADS=[rect(0,0,70,50),rect(75,0,70,50),rect(0,55,70,50)]
# Eight small spreaders per triangle = 64; only 56 are required for 28 stitches.
PATCH_SPREADERS=[rect(x,y,25,25) for x in [0,30,60,90] for y in [230,260]]
STRIP_SPREADERS=[rect(x,y,25,25) for x in [0,28,56,84] for y in [110,140]]

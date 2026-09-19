"""Workshop PVC cutting guide: six compact gate layouts, ratchet and saw allowances."""
from pathlib import Path
import json,csv,collections
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph,Table,TableStyle
R=Path(__file__).resolve().parents[1];O=R/'output/compact_gate_study';G=json.loads((O/'layouts.json').read_text())['gates']
# Each tuple is (number of identical sticks, long pieces per stick, short pieces per stick).
# Zero material-removal kerf for the user's ratchet cutter; retain 10 mm stock-end reserve.
PLANS={(1000,24):[(3,2,2),(2,1,5)],(1000,18):[(4,2,3),(1,0,4)],(1000,12):[(4,2,4)],(800,24):[(2,3,1),(2,1,5),(1,0,4)],(800,18):[(4,2,4)],(800,12):[(2,3,4),(1,2,8)]}
BLUE=HexColor('#235775');ORANGE=HexColor('#da8c36');INK=HexColor('#193247');PALE=HexColor('#edf1f4');GRAY=HexColor('#dce1e5')
P=O/'PVC_Cut_Guide.pdf';c=canvas.Canvas(str(P),pagesize=(792,612));c.setTitle('PVC Cut Guide - six compact FPV gate variants');c.setAuthor('FPV Drone Racing Gate project')
style=ParagraphStyle('body',fontName='Helvetica',fontSize=10,leading=14,textColor=INK)
def para(s,x,y,w=720):
 p=Paragraph(s,style);_,h=p.wrap(w,550);p.drawOn(c,x,y-h);return y-h
def title(t,sub,page):
 c.setFillColor(INK);c.setFont('Helvetica-Bold',21);c.drawString(36,570,t);para(sub,36,550)
 c.setFont('Helvetica',8);c.drawString(36,20,'Nominal 1-inch PVC / accepted 33.5 mm fitting bores / all cut dimensions are finished end-to-end lengths')
 c.drawRightString(756,20,f'{page} / 7')
def table(data,x,y,widths,rowh=25):
 t=Table(data,colWidths=widths,rowHeights=rowh);t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),INK),('TEXTCOLOR',(0,0),(-1,0),HexColor('#ffffff')),('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),('FONTNAME',(0,1),(-1,-1),'Helvetica'),('FONTSIZE',(0,0),(-1,-1),10),('VALIGN',(0,0),(-1,-1),'MIDDLE'),('GRID',(0,0),(-1,-1),.4,GRAY)]));_,h=t.wrap(720,550);t.drawOn(c,x,y-h);return y-h
rows=[];md=['# PVC cut guide — all six compact variants','', '[Download the printable seven-page PDF](PVC_Cut_Guide.pdf). Each variant has its own workshop page, cutting checklist and stick layout.','', '**For the HUSKY 1-1/4-inch ratcheting PVC cutter.** All lengths are finished pipe end-to-end dimensions, before inserting into fittings. Use millimetres as the reference; decimal inches are provided for comparison. Every gate uses **8 long pieces + 16 short pieces = 24 pieces** of nominal 1-inch PVC.','', '| Opening | Paper band | Long pieces: cut 8 | Short pieces: cut 16 | 10-ft sticks, ratchet | 10-ft sticks, conservative saw plan |','|---:|---:|---:|---:|---:|---:|']
for g in G:
 key=(g['opening_mm'],g['band_inches']);plan=PLANS[key];L=g['long_cut_mm'];S=g['short_cut_mm'];assert sum(n*l for n,l,s in plan)==8 and sum(n*s for n,l,s in plan)==16
 assert all(l*L+s*S<=3038+.001 for n,l,s in plan)
 # Match the existing CAD edge lengths exactly; no insertion allowance is added to these cuts.
 assert collections.Counter(e['length_mm'] for e in g['edges'])==collections.Counter({float(L):8,float(S):16})
 nsticks=sum(n for n,l,s in plan);g['ratchet_sticks']=nsticks;g['ratchet_plan']=plan
 assert nsticks==__import__('math').ceil((8*L+16*S)/3038),'Ratchet plan must reach stock-length lower bound'
 rows.append({'opening_mm':g['opening_mm'],'paper_inches':g['band_inches'],'long_quantity':8,'long_length_mm':L,'long_length_inches':round(L/25.4,4),'short_quantity':16,'short_length_mm':S,'short_length_inches':round(S/25.4,4),'ratchet_10ft_sticks':nsticks,'conservative_saw_10ft_sticks':g['PVC_sticks']})
 md.append(f"| {g['opening_mm']} mm | {g['band_inches']} in | 8 × {L:.1f} mm | 16 × {S:.1f} mm | {nsticks} | {g['PVC_sticks']} |")
with (O/'PVC_Cut_Summary.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
title('PVC cutting / choose one gate size','Workshop summary. Print the following page for your chosen opening and paper width. Diagrams are not full-size templates.',1)
data=[['Clear opening','Paper width','8 long pieces','16 short pieces','Ratchet sticks','Saw plan*']]+[[f"{g['opening_mm']} mm",f"{g['band_inches']} in",f"{g['long_cut_mm']:.1f} mm",f"{g['short_cut_mm']:.1f} mm",str(g['ratchet_sticks']),str(g['PVC_sticks'])] for g in G]
y=table(data,36,512,[120,100,140,140,110,110],28)
y=para('<b>Do not subtract socket insertion from these numbers.</b> Each end inserts 30 mm into its fitting. The cut lengths already include that engagement. They are neither exposed spans nor node-center distances.',36,y-18)
y=para('<b>For your ratcheting cutter:</b> layouts allow 10 mm per 3048 mm stick for end cleanup, with no saw kerf. Square the starting end, measure each next piece from the new cut end, cut on the waste side of the mark, then check the finished length. Avoid cumulative marks along a full stick.',36,y-14)
y=para('<b>Before batch cutting:</b> make one short and one long piece, remove burrs, mark 30 mm insertion at each end and dry-fit with the accepted fittings. Use the first accurate piece as a comparison master for repeats. For 12-inch paper the short piece is only 84.8 mm: check that trial corner carefully.',36,y-14)
y=para('*The existing saw layouts reserve 10 mm per stick plus 3 mm per cut. With the ratchet, the 1000 mm / 24-inch version needs <b>five sticks instead of six</b>. The other stock counts are unchanged. Confirm actual stick length; trim losses beyond the allowance require another layout or spare stock.',36,y-14)
para('These quantities cover the flat gate grid only; feet, ballast structures and other ground supports are additional. All six use the same printed fittings. Label long pieces L1-L8 and short pieces S1-S16.',36,y-14)
c.showPage()
md += ['', 'The ratchet layouts reserve **10 mm per 3048 mm stick for end cleanup** and assume no material-removal kerf. They reach the minimum stick count permitted by total finished length under that reserve. The earlier conservative saw layouts reserve an additional 3 mm per cut; use them if cutting with a saw. This changes only the **1000 mm / 24-inch** purchase quantity from six sticks to five when using the ratchet. Existing study cost tables intentionally retain the conservative saw allowance.', '', '## Cutting method', '', '1. Check actual stock length. Square the starting end within the 10 mm total cleanup reserve.', '2. Cut one short and one long piece to the finished lengths below. Measure from the current squared end each time; do not rely on cumulative marks along the original stick.', '3. Remove burrs, mark 30 mm insertion from each end and dry-fit the trial pieces. **Do not deduct 30 mm from the cut length.** Both socket engagements are already included.', '4. Batch the remaining cuts, checking against an accurate first piece. Label long pieces L1–L8 and short pieces S1–S16. The diagrams are allocation plans, not full-scale ruler templates.', '5. Slide the required magnet sleeves onto pipes before closing the frame. Use the variant-specific sleeve-position CSV in the study guide.', '', 'A 12-inch-paper short piece is 84.8 mm long: two 30 mm insertions leave 24.8 mm exposed. The existing short-section sleeve is omitted in that variant. Feet and ground supports are not included.', '']
for page,g in enumerate(G,2):
 L=g['long_cut_mm'];S=g['short_cut_mm'];name=f"{g['opening_mm']} mm opening / {g['band_inches']}-inch paper"
 title(name,f"Outside paper square: {g['outer_mm']:.1f} mm. Buy {g['ratchet_sticks']} sticks of 10-ft nominal 1-inch PVC for the gate grid.",page)
 table([['Mark','Cut quantity','Finished length (mm)','Decimal inches'],['L',8,f'{L:.1f}',f'{L/25.4:.4f}'],['S',16,f'{S:.1f}',f'{S/25.4:.4f}']],36,511,[70,110,190,130],28)
 # Schematic fitting grid, deliberately equal spacings: use L/S markings, not drawing scale.
 xs=[601,641,707,747];ys=[432,458,490,516]
 c.setLineWidth(2.5)
 for j,y0 in enumerate(ys):
  for i in range(3):
   c.setStrokeColor(BLUE if i==1 else ORANGE);c.line(xs[i],y0,xs[i+1],y0)
   c.setFillColor(INK);c.setFont('Helvetica',8);c.drawCentredString((xs[i]+xs[i+1])/2,y0+4,'L' if i==1 else 'S')
 for i,x in enumerate(xs):
  for j in range(3):
   c.setStrokeColor(BLUE if j==1 else ORANGE);c.line(x,ys[j],x,ys[j+1]);c.setFillColor(INK);c.setFont('Helvetica',8);c.drawString(x+3,(ys[j]+ys[j+1])/2-3,'L' if j==1 else 'S')
 c.setFillColor(INK)
 for x in xs:
  for y0 in ys:c.circle(x,y0,2.8,fill=1,stroke=0)
 c.setFont('Helvetica',8);c.drawString(602,418,'Front grid / schematic, not to scale')
 c.setFillColor(INK);c.setFont('Helvetica-Bold',12);c.drawString(36,401,'Ratcheting cutter / stick-by-stick allocation')
 c.setFont('Helvetica',9);c.drawString(36,383,'Blue = long (L). Orange = short (S). Gray = spare after 10 mm cleanup reserve. Numbers are quantities.')
 idx=0;csvrows=[];groups=[]
 for n,l,s in g['ratchet_plan']:
  used=l*L+s*S;reserve=3038-used;first=idx+1
  for _ in range(n):
   idx+=1;y=356-(idx-1)*45
   c.setFillColor(INK);c.setFont('Helvetica-Bold',9);c.drawString(36,y+1,f'Stick {idx}')
   # Grouped segments keep even tiny short pieces legible; bar scale remains proportional.
   x=93;scale=486/3038
   for count,length,color,label in [(l,L,BLUE,'L'),(s,S,ORANGE,'S')]:
    if not count:continue
    w=count*length*scale;c.setFillColor(color);c.rect(x,y-4,w,19,fill=1,stroke=0);c.setFillColor(HexColor('#ffffff'));c.setFont('Helvetica-Bold',9);c.drawCentredString(x+w/2,y+2,f'{count} {label}');x+=w
   c.setFillColor(GRAY);c.rect(x,y-4,reserve*scale,19,fill=1,stroke=0)
   c.setFillColor(INK);c.setFont('Helvetica',9);c.drawString(591,y+4,f'{l} L + {s} S');c.drawString(657,y+4,f'{reserve:.1f} mm spare')
   csvrows.append({'stick':idx,'long_quantity':l,'long_length_mm':L,'short_quantity':s,'short_length_mm':S,'finished_pipe_total_mm':round(used,3),'end_cleanup_reserve_mm':10,'extra_cut_allowance_mm':0,'spare_after_reserve_mm':round(reserve,3)})
  label=f'Sticks {first}–{idx}' if n>1 else f'Stick {idx}';groups.append(f'| {label} | {l} × {L:.1f} | {s} × {S:.1f} | {reserve:.1f} |')
 y=356-idx*45-8
 c.setFillColor(INK);c.setFont('Helvetica-Bold',10);c.drawString(36,y,'Finished-piece check:')
 for qty,label,x0 in [(8,'Long: 8',178),(16,'Short: 16',392)]:
  c.setFont('Helvetica',9);c.drawString(x0,y,label)
  for k in range(qty):
   x=x0+(k%8)*17;y0=y-17-(k//8)*17;c.setStrokeColor(INK);c.setLineWidth(.6);c.rect(x,y0,9,9,fill=0,stroke=1)
 para(f'<b>Assembly check:</b> 30 mm insertion at each end. Short-section exposed span = {S-60:.1f} mm; long-section exposed span = {L-60:.1f} mm. Finished gate opening = {g["opening_mm"]} mm square.',36,82,720)
 para('For a hand saw, use the conservative stock-layout CSV linked in the guide; never add saw kerf to a finished part dimension.',36,48,720)
 c.showPage()
 fn=g['id']+'_Ratcheting_Stock_Layout.csv'
 with (O/fn).open('w') as f:
  w=csv.DictWriter(f,fieldnames=list(csvrows[0]),lineterminator='\n');w.writeheader();w.writerows(csvrows)
 md += [f'## {name}', '', f'Cut **8 × {L:.1f} mm** long pieces ({L/25.4:.4f} in) and **16 × {S:.1f} mm** short pieces ({S/25.4:.4f} in). Buy **{g["ratchet_sticks"]} ten-foot sticks**. Outer square: {g["outer_mm"]:.1f} mm.', '', '| Stock | Long pieces | Short pieces | Spare after 10 mm reserve |', '|---|---:|---:|---:|',*groups,'',f'[Ratcheting-cutter stock CSV]({fn}) · [Conservative saw stock CSV]({g["id"]}_Stock_Layout.csv) · [Pipe IDs and sleeve positions]({g["id"]}_PVC_Cuts.csv)','']
c.save();(O/'PVC_Cut_Guide.md').write_text('\n'.join(md).rstrip()+'\n')
print('Created seven-page PVC_Cut_Guide.pdf, guide Markdown, summary CSV and six ratchet stock layouts.')

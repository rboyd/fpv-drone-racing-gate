"""Publish the PVC-dominant iteration, actual slice estimates and fabrication ledgers."""
from pathlib import Path
import json,csv,math,html,re,zipfile,collections
from reportlab.platypus import SimpleDocTemplate,Paragraph,Image,Table,TableStyle,PageBreak,Spacer
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib.colors import HexColor
ROOT=Path(__file__).resolve().parents[1];O=ROOT/'output/pvc_paper_gate';b=json.loads((O/'BOM.json').read_text());v=json.loads((O/'print_checks.json').read_text());gates=b['gates'];stats=v['gates'];ready=gates['stack_ready'];stack=gates['split_s'];rs=stats['stack_ready'];ss=stats['split_s'];fit=v['slices']['FIRST_FIT']
parts={p['code']:p for p in b['parts']}
def csvout(name,rows):
 with (O/name).open('w') as f:w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def length(path):return sum(math.dist(a,c) for a,c in zip(path,path[1:]))
cord_totals={}
for kind,g in gates.items():
 csvout(f'{kind}_Printed_BOM.csv',[{'part':c,'quantity':n,'description':parts[c]['description'],'print_bounds_mm':' x '.join(map(str,parts[c]['print_bounds_mm']))} for c,n in g['counts'].items()])
 csvout(f'{kind}_PVC_Cuts.csv',[{'piece':i+1,'name':e['name'],'from_node':e['a'],'to_node':e['b'],'length_mm':e['length_mm']} for i,e in enumerate(g['edges'])])
 csvout(f'{kind}_PVC_Stock_Layout.csv',[{'stock':r['stock'],'cut_order':i+1,'name':e['name'],'length_mm':e['length_mm'],'kerf_mm':3,'reserved_stock_end_mm':10} for r in g['stock_plan'] for i,e in enumerate(r['cuts'])])
 csvout(f'{kind}_Print_Queue.csv',[{'recipe':name,'runs':n,'pieces_per_run':len(b['plates'][name]),'grams_per_run':v['slices'][name]['grams'],'minutes_per_run':v['slices'][name]['minutes'],'file':f'sliced/{name}/{name}_A1Mini_PETG.3mf'} for name,n in g['print_queue'].items()])
 csvout(f'{kind}_Sleeve_Positions.csv',[{'pipe':p['pipe'],'distance_from_cut_start_mm':p['from_cut_end_mm'],'face_x_mm':round(p['xy'][0],3),'face_y_mm':round(p['xy'][1],3),'part_angle_degrees':p['angle']} for p in stats[kind]['sleeves']])
 csvout(f'{kind}_Magnet_Positions.csv',[{'pair':i+1,'x_from_left_mm':round(x,3),'y_from_bottom_mm':round(y,3),'printed_backing':'Integral pocket at exact XY; rear-loaded magnet behind .4 mm plastic','front':'Bare 6 x 2 magnet; pad optional'} for i,(x,y) in enumerate(g['magnets'])])
 csvout(f'{kind}_Paper_Cuts.csv',[{'piece':i+1,'x_mm':x,'y_mm':y,'width_mm':w,'height_mm':h,'roll_cut_length_mm':max(w,h),'role':'horizontal band' if w==2700 else 'side insert with 36 mm overlap each end'} for i,(x,y,w,h) in enumerate(g['paper_rectangles'])])
 # Cord lengths are conservative cut allowances; exact knot consumption must be set in the physical prototype.
 cords=[{'use':'socket draw / sleeve location','segment':p['name'],'cut_mm':math.ceil((length(p['points'])+400)/50)*50} for p in g['cord_routes']]
 cords += [{'use':'paper seam','segment':str(i+1),'cut_mm':1000} for i,_ in enumerate(g['seam_routes'])]
 cords += [{'use':'side-band X brace','segment':str(i+1),'cut_mm':math.ceil((length(p)+400)/50)*50} for i,p in enumerate(g['brace_routes'])]
 csvout(f'{kind}_Cord_Cuts.csv',cords);cord_totals[kind]=round(sum(p['cut_mm'] for p in cords)/1000,2)
 # Assembly map: opaque paper with real magnet centers, a coordinate reference rather than a drill template.
 W,H=2700,g['height_mm'];shapes=[]
 for i,(x,y,w,h) in enumerate(g['paper_rectangles']):shapes.append(f'<rect x="{x}" y="{H-y-h}" width="{w}" height="{h}" fill="{("#f5a45a" if w==2700 else "#f7bb80")}" stroke="#9a622f" stroke-width="2"/>')
 for x,y in g['magnets']:shapes.append(f'<circle cx="{x}" cy="{H-y}" r="3" fill="#1b4054"/>')
 (O/f'{kind}_Paper_and_Magnet_Map.svg').write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-50 -50 {W+100} {H+100}" width="600"><title>Paper rectangles and true 6 mm magnet locations, {kind}</title>'+''.join(shapes)+'</svg>')
# Upgrade only: accepted single-height pieces are reused.
extra=v['upgrade']['additional_parts'];pipeextra=v['upgrade']['additional_pipe_cuts']
csvout('Upgrade_Additional_Parts.csv',[{'part':c,'quantity':n} for c,n in extra.items()]);csvout('Upgrade_Additional_PVC.csv',[{'cut_length_mm':float(k),'quantity':n} for k,n in pipeextra.items()])
comp=[]
for kind,s in stats.items():comp.append({'configuration':kind,**{k:q for k,q in s.items() if k!='sleeves'},'face_cord_cut_allowance_m':cord_totals[kind],'paper_used_m':sum(max(p[2:]) for p in gates[kind]['paper_rectangles'])/1000})
csvout('Comparison.csv',comp)
priorb=json.loads((ROOT/'output/sleeve_paper_gate/BOM.json').read_text());priorv=json.loads((ROOT/'output/sleeve_paper_gate/print_checks.json').read_text())
prior={k:sum(priorv['slices'][n][k]*r for n,r in priorb['plate_runs'].items() if not any(n.startswith('Q_'+c) for c in ['PAPER_PAD','V_BLOCK','CROSS_PLATE'])) for k in ['grams','minutes']}
parttable='\n'.join(f"| {c} | {ready['counts'].get(c,0)} | {stack['counts'].get(c,0)} | {' x '.join(map(str,parts[c]['print_bounds_mm']))} |" for c in ready['counts'])
comparisontable='\n'.join(f"| {label} | {stats[k]['printed_pieces']} | {stats[k]['grams']/1000:.3f} kg | {stats[k]['minutes']/60:.1f} h | {stats[k]['pipe_sticks']} / ${stats[k]['pipe_cost_usd']} | ${stats[k]['frame_PVC_plus_PETG_usd']:.2f} |" for k,label in [('basic','Basic single; 2.5 m pipes'),('stack_ready','Recommended single; ready to extend'),('split_s','Two-level Split-S')])
readme=f'''# PVC-dominant paper gate / single and Split-S

The previous reinforced print-track design and first click-test plate were committed as **eda5b20**. This new iteration replaces the printed track with **one outer PVC perimeter and one PVC ring around each opening**, joined by four diagonal PVC spokes at the overall corners. All pipe is nominal 1-inch PVC (33.4 mm OD). Paper hides the structure head-on; only paper and bare front magnets are visible in the face area.

[Blender model](PVC_Paper_Gate.blend) · [Visual design/assembly PDF](PVC_Gate_Study.pdf) · [Rendered single gate](renders/01_SINGLE_FRONT.png) · [Rendered Split-S](renders/03_SPLIT_S_FRONT.png) · [Rear structure](renders/04_SPLIT_S_BACK.png) · [Kit](PVC_Paper_Gate_Kit.zip)

## Recommendation and measured cost

Use the **stack-ready single** as the development baseline: **62 printed pieces in five types, {rs['grams']/1000:.3f} kg PETG, {rs['minutes']/60:.1f} print-hours, {rs['plate_runs']} plate runs, and six 10-ft PVC lengths at your $6 price**. The longest cut pipe is 1990.4 mm, retaining the approximately 2.15 m transport limit. Short members disconnect at cord-retained sockets.

| Configuration | Printed pieces | PETG | Print time | PVC sticks / cost | PVC + PETG subtotal* |
|---|---:|---:|---:|---:|---:|
{comparisontable}

*PETG cost assumes $20/kg, not a current supplier quote. Estimates are actual local A1 Mini slices: 0.4 mm nozzle, 0.20 mm layers, four walls, 20% infill, Generic PETG, supports off. The subtotal covers the **face skeleton only**. Add magnets, paper, cord, adhesive, base/feet, ground stakes or ballast, and external guys. It is not a complete installed-obstacle price. Manual work, failures and reprints are excluded from printer-hours.

Two full 1 kg spools cover the recommended single with 10% allowance ({rs['grams']*1.1/1000:.3f} kg). The Split-S uses {ss['grams']/1000:.3f} kg before allowance: three spools nominally, four if budgeting 10% extra. Optional front pads add material and time; they are excluded from these totals.

For a fair printed-face comparison, the prior sleeve design excluding optional pads and PVC-brace clamps used {prior['grams']/1000:.3f} kg / {prior['minutes']/60:.1f} hours. The new recommended single reduces that PETG by {(1-rs['grams']/prior['grams'])*100:.1f}% and print time by {(1-rs['minutes']/prior['minutes'])*100:.1f}%. The tradeoff is more PVC and cord work. The no-transport-joints basic option prints less, but needs seven sticks due to offcuts and has 2500 mm pipe pieces. The recommended version costs only ${rs['frame_PVC_plus_PETG_usd']-stats['basic']['frame_PVC_plus_PETG_usd']:.2f} more in the modeled materials.

## Five printed types

| Part | Single ready | Split-S total | A1 Mini print bounds mm |
|---|---:|---:|---|
{parttable}

**OUTER_90_45** combines two perpendicular sockets and an inward diagonal socket. **INNER_90_45** has the same perpendicular sockets but its diagonal points outward, away from the opening. They cannot be the same rotated part. Each has an integral magnet pocket, broad 32 x 12 mm connecting webs, raised cord eyes, and a two-horn cord cleat. Socket walls are nominally 4 mm, with 30 mm pipe engagement to a positive end stop.

**STACK_TEE** is used in all ten tee locations of the stacked gate: eight divider junctions and two transport joints. It has four available magnet pads so the same part can rotate to either side; populate only the pockets listed in the magnet map. Its unused branch port at a transport joint stays empty and concealed behind paper. The single version includes four tees: two side riser tees for the future divider and two horizontal transport tees.

**EDGE_SLEEVE** slides over bare PVC before fitting the ends. Its 3.2 mm nominal wall and 14 mm axial length support a magnetic pad offset 32 mm from the pipe axis. Use the raised cord eye to set rotation and the indexed cord/stop knots to set position. It is a clearance sleeve, not a friction clamp. **CORD_SADDLE** is a small magnet backing threaded on a seam cord; two span each short paper overlap without an extra PVC member.

Every production part is a connected, manifold mesh and fits inside the A1 Mini's 180 mm cube with the supplied placement margin. Maximum part extent is 160 mm. The pipe axes are only **24 mm behind the paper**, reducing solid material below the sockets. Accepted peaked roofs remain. The magnet pocket remains **6.3 mm diameter with 0.4 mm of plastic between rear magnet and paper**; it is not a flush/open frame-side holder.

## Paper face and magnet alignment

Outside dimensions remain **2700 x 2700 mm** for one opening, or **2700 x 4790.4 mm** for two. Each clear paper opening is **1480.8 x 1480.8 mm**. The shared divider is one 609.6 mm band, not two overlapping full bands. With the illustrative 50 mm ground clearance, the Split-S top is 4840.4 mm above ground.

Use the full 609.6 mm roll width throughout. This iteration changes the pinwheel cutting pattern to simpler horizontal bars and side inserts that also work at the shared divider:

- Single: **two 2700 mm cuts and two 1552.8 mm cuts**. The side inserts overlap the horizontal bands by 36 mm at both ends. Total roll consumption 8.5056 m; three single gates fit on a 100-ft roll.
- Split-S: **three 2700 mm cuts and four 1552.8 mm cuts**. Total 14.3112 m; two stacked gates fit on a 100-ft roll.

The outer PVC axes are 50 mm inside the paper outline. The inner axes sit 50 mm behind the opening boundary in plan. A 32 mm pad offset puts magnets **18 mm inside the paper edges**, and the overlap seam centers are also 18 mm from the side-insert cut ends. No pipe or printed fitting protrudes into the opening or beyond the face in the checked front projection. This is a head-on appearance goal; supports may be visible from oblique/rear views, and paper can deflect in wind.

Use **{rs['magnet_pairs']*2} magnets for the single, {ss['magnet_pairs']*2} for the Split-S**, all 6 x 2 mm, paired front/back. Start with the spacing shown (roughly 300-350 mm on long edges); it is a prototype spacing, not established wind retention. The smaller count than the printed-rail design needs physical paper/grip testing.

Bond the rear magnets with compatible adhesive after checking polarity. Stack without optional pads: **rear magnet -> 0.4 mm printed skin -> paper -> bare front magnet**. Optional PAPER_PAD adds its own 0.4 mm skin and a handle around the front magnet. It is a test/comfort option, not required for the paper-only front appearance. No new front pad design is needed.

For accurate placement, use Sleeve_Positions.csv to mark the PVC, rotate each sleeve until its paper face is coplanar with the corner pads, and lock that position on the prethreaded cord with stopper knots on both sides of its eye. Set the paper edge 18 mm beyond the magnet centers. Attach loose front magnets directly over the fixed rear magnets; they self-align. Do not perforate the paper. The Paper_and_Magnet_Map.svg and Magnet_Positions.csv provide the exact layout; the SVG shows magnets at true scale.

## Cord assembly and retention

Use the previously selected **2.4 mm 275 paracord**. Socket draw lines run from fitting to fitting along each PVC member, through the relevant sleeve eyes on straight members. Keep the line on the paper-edge side of the pipe foot, clear of the socket mouth. They pull the fittings against the pipe end stops; bare dry-fit friction is not treated as retention. Wrap diagonal draw cords **over the backs of the socket shells**, then finish on the central cleats, so they do not pass through a solid socket root.

Tie one fixed end, feed slack through the guides, hold the final tail, and pull only enough to seat both pipe ends. Make two figure-eight wraps around the receiving two-horn cleat and finish with a locking half-hitch. Leave a 100 mm tail. To release, hold the tail, undo the hitch and unwrap. Do not tension until PVC bows. Use separate lines for the seam backers and X braces so replacing paper does not loosen pipe joints. The X cords stay inside the side paper bands and never cross an opening.

The supplied centerline drawings show principal routes and raised eye locations; knots, contact bends around the sockets, and every turn through an eye are not simulated. Prototype the routing and hand access before repeating it. The cord scheme has not been load tested. Printed sleeve rotation, cord stretch and knot slip remain physical-test items. Mark socket insertion depth, sleeve position and cord tail after the first successful fit-up; leave sleeves and their locating cords on the pipes in transport.

Cord_Cuts.csv includes generous tie allowances: **{cord_totals['stack_ready']:.1f} m for the single face, {cord_totals['split_s']:.1f} m for the stacked face**. External guys are additional. These are cut allowances, not a reason to tension hard. Recheck slack after settling and warm exposure.

## Single gate assembly

1. Print the FIRST_FIT plate and test the actual pipe first. Once it passes, print one INNER_90_45 and one STACK_TEE before committing to the full queue. Neither is included in FIRST_FIT.
2. Cut and label PVC from the stock layout. The six-stick single layout reserves 10 mm per stock end allowance and 3 mm kerf per cut, but several sticks have only about 8.3 mm remaining after those allowances. Measure actual stock and kerf before cutting; do not round all cuts upward. Cuts use **center spacing minus 100 mm** because every fitting's pipe stop is 50 mm from its node center.
3. Slide the indicated EDGE_SLEEVEs onto each labeled bare pipe. Use Sleeve_Positions.csv, measured from the cut start named in PVC_Cuts.csv. Thread the locating cords before fitting the pipe ends. Keep every flat paper face in the same plane.
4. Assemble the outer ring on a flat surface. The top and bottom each use two 1200 mm pipes and one tee transport joint. Each side uses a 1990.4 mm pipe, a tee and a 409.6 mm pipe. The tee's spare port points inward. Outer corner-to-corner pipe-axis spacing is 2600 mm.
5. Assemble the inner square from four 1480.8 mm pipes. Its pipe-axis spacing is 1580.8 mm. Connect corresponding corners with four 620.683 mm diagonal pipes. Lay all corners in the orientations shown in Blender before inserting the diagonals.
6. Seat all pipes 30 mm into their sockets. Tension the socket draw cords gradually, check squareness, then set the side-band X cords. Fit the seam cords and slide on two CORD_SADDLEs per seam. Fix their marked positions with small stopper knots.
7. Install rear magnets and allow adhesive to cure. Lay on the two horizontal paper bands, then the side inserts with their 36 mm overlaps. Work from corners along each edge, adding front magnets directly over the rear pockets. Confirm only paper and magnets show from the front.
8. Test retention and handling flat, then install a suitable base and anchoring system before standing the gate. Do not lift or carry the assembly by paper or magnetic pads.

## Upgrade to a two-level Split-S

The digital cut ledger confirms **every existing pipe length is reused without cutting**. Add **six STACK_TEEs, 32 EDGE_SLEEVEs and eight CORD_SADDLEs**. Add PVC cuts: **two 1990.4 mm, four 1480.8 mm and four 409.6 mm**. Those additions fit four more 10-ft sticks, bringing the total to ten. Add 92 magnets, additional cord, one 2700 mm paper band and two 1552.8 mm side inserts.

With the single gate lying flat, remove its paper and slacken the draw cords. Move the entire outer top bar (including its middle tee), its two outer corner fittings, the inner top corner fittings and the two top diagonal pipes to their new top positions. Keep the original inner top 1480.8 mm pipe as the lower divider-opening rail, replacing its two corner fittings with tees. The old upper outer corners become new tees at the upper divider height. The preinstalled side tees form the lower divider junctions.

Connect each divider rail outward to the side uprights with two 409.6 mm stubs. Retain the original two short side risers between the divider's outer tees. Add the upper outer risers, the upper opening's two inner uprights, and its bottom/top horizontal rails. Check the two divider axis heights: **2140.4 and 2650 mm measured from the paper bottom**, a 509.6 mm spacing. This leaves room for the one 609.6 mm paper divider while the sleeves place magnets at its two opening edges.

Re-thread and tension with the assembly flat; then add the additional paper and magnets. The shared middle uses straight tee connections, so there are no crossing in-plane PVC diagonals. The extra tee ports and aligned pipe stops are what make this a reusable extension system rather than two independent square gates stacked into each other.

## First print and acceptance checks

[Open FIRST_FIT_A1Mini_PETG.3mf](sliced/FIRST_FIT/FIRST_FIT_A1Mini_PETG.3mf): **{fit['grams']:.2f} g, {fit['minutes']/60:.2f} hours**, five pieces: one outer 90+45 corner, one edge sleeve, one cord saddle, one short bore gauge, and one optional front pad. It demonstrates the new PVC socket, magnetic face and cord interface; the earlier click-test plate remains available in the committed iteration.

Use actual clean 33.4 mm OD PVC offcuts, a short paracord length, paper and four magnets for two grip sites. Check the gauge first, then full 30 mm socket seating without force; a short gauge does not prove the full socket fit. Check extraction after relaxing cord, loop clocking, knots, cord access around the 45-degree socket and coplanar magnet faces. Test bare front magnet vs optional pad, then repeat assembly at least 20 times. Check whitening, cracks, looseness, pipe withdrawal and permanent deformation. Scale must stay 100%; revise the bore clearance itself if necessary.

All seven exported masters (five production types, a gauge and an optional pad) are connected/manifold and within A1 Mini bounds. All supplied recipes have 5 mm minimum bed margin, no part overlap, no supports and no slicer warnings. Quantities match the modeled parts, magnet positions match real pockets, and sleeves sit on exposed pipe rather than over a fitting. These are digital checks, not physical strength or fatigue certification.

## Base and outdoor limits

The new face skeleton is a **fabrication prototype and assembly study**, not a wind-qualified complete obstacle. Scene 10 shows the required concept of separate feet/ballast and four external guys; the bag sizes and feet are placeholders and are **not** a ballast prescription. For soil use suitable anchored guys/feet; hard surfaces require attached ballast/feet sized for the actual setup. The 4.79 m face is much taller than the single version, so do not reuse the old single-gate ballast amount as an assumed rating. Keep anchors/guys outside the openings, attach them around structural PVC near nodes, and assemble/raise with helpers.

Ground hardware is deliberately excluded from the face cost/queue. Its sizing and attachment are the next engineering step after the corner/cord prototype works. Paper weather resistance, 6 mm magnet pull through the plastic skin, sleeve clocking and cord preload also remain to be proven in real conditions. A paper face at this size can catch wind even if the PVC joints are rigid.

## Sources and assumptions

- [FORMUFIT PVC sizing](https://formufit.com/pages/pvc-101): nominal 1-inch PVC is approximately 1.315 inch OD. The CAD uses 33.4 mm and a 34.2 mm trial bore; measure your pipe rather than treating that clearance as universal.
- [FORMUFIT assembly guidance](https://formufit.com/pages/building-projects-with-pvc-pipe): dry friction joints are a temporary assembly method, not adequate justification for a loaded structure. Our removable cord retention is an original prototype proposal and is not endorsed or validated by that guidance. PVC solvent cement is not assumed to bond PETG.
- [Prusa modeling guidance](https://help.prusa3d.com/article/modeling-with-3d-printing-in-mind_164135): supports/overhangs and tolerances depend on geometry and settings. Peaked bores were also checked by slicing with supports off; successful real printing is still to be tested.

Your PVC price is used as given. No MultiGP compliance or official course dimensions are claimed; the approved dimensions and reference image determine this concept. Rebuild with build_pvc_paper_gate.py, slice_pvc_paper_gate.py, validate_pvc_paper_gate.py and package_pvc_paper_gate.py. No printer job has been submitted.
'''
(O/'README.md').write_text(readme)
styles=getSampleStyleSheet();styles.add(ParagraphStyle(name='Body',fontName='Helvetica',fontSize=10,leading=14,spaceAfter=8,textColor=HexColor('#17374c')))
story=[]
def para(t,style='Body'):story.append(Paragraph(t,styles[style]))
def pic(n):story.append(Image(str(O/'renders'/f'{n}.png'),width=510,height=340))
def table(rows,widths):
 t=Table([[Paragraph(str(x),styles['Body']) for x in row] for row in rows],colWidths=widths,repeatRows=1);t.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('BACKGROUND',(0,0),(-1,0),HexColor('#dce9ee')),('LINEBELOW',(0,0),(-1,-1),.35,HexColor('#a5bbc5')),('BOTTOMPADDING',(0,0),(-1,-1),6)]));story.append(t)
para('PVC frame / single gate and Split-S','Title');pic('03_SPLIT_S_FRONT');para(f'Recommended single: {rs["grams"]/1000:.3f} kg PETG, {rs["minutes"]/60:.1f} print-hours, six $6 PVC sticks. PVC + PETG face-skeleton subtotal: ${rs["frame_PVC_plus_PETG_usd"]:.2f} at $20/kg PETG. Two-level subtotal: ${ss["frame_PVC_plus_PETG_usd"]:.2f}. Magnets, paper, cord and anchoring are additional.');para('Same five printed types; no printed spanning rails. Paper and magnets cover the face head-on. Full height: 4790.4 mm. Digital prototype; physical joints, retention and anchoring remain to be qualified.')
story.append(PageBreak());para('Parts and print comparison','Heading1');table([['Part','Single','Double','Bounds mm']]+[[c,ready['counts'][c],stack['counts'][c],' x '.join(map(str,parts[c]['print_bounds_mm']))] for c in ready['counts']],[145,45,45,275]);table([['Configuration','PETG kg','Hours','PVC $','Subtotal $']]+[[k,round(s['grams']/1000,3),round(s['minutes']/60,1),s['pipe_cost_usd'],s['frame_PVC_plus_PETG_usd']] for k,s in stats.items()],[180,75,75,70,110]);para('The basic option needs 2.5 m transport length. The recommended stack-ready version keeps every pipe under 2 m and reuses every pipe on extension. Subtotals are face skeleton only, excluding installed-base hardware.');pic('05_PRINTED_PARTS')
for n,title,cap in [('01_SINGLE_FRONT','Paper-only face','Single gate: 2700 mm outer / 1480.8 mm opening. Magnet centers are 18 mm inside the paper edges.'),('02_SINGLE_BACK','Single-height PVC skeleton','Two PVC perimeters, four PVC diagonal links, four tees including the two transport joints, and independent cord retention.'),('06_CORNER_AND_DIAGONAL','The 90 + 45 corner pair','The outer diagonal socket points inward; the inner socket points outward. Cord wraps over the backs of the sockets and ties to their central cleats.'),('07_MAGNET_SLEEVE','Sliding magnetic sleeve','Thread before end fittings. Index with cord and marks. Rear magnet / 0.4 mm frame skin / paper / bare front magnet. Printed front pad is optional.'),('04_SPLIT_S_BACK','Extend upward','Ten tees total: eight divider junctions and two retained transport joints. Eight corner fittings serve the overall top/bottom; the top four move upward.'),('08_SHARED_DIVIDER','Shared middle band','All intermediate pipes are coplanar. Straight tees replace potentially colliding middle diagonal braces.'),('09_FIRST_FIT_PLATE','Prototype before production',f'FIRST_FIT: {fit["grams"]:.2f} g / {fit["minutes"]/60:.2f} hours. Five pieces including one optional pad. Test actual pipe fit, cord access, magnetic grip and hand release.'),('10_SPLIT_S_ANCHORING','Installation remains to be qualified','External guys and feet/anchors are necessary. Shown foot and ballast shapes are illustrative, not a rated specification. Cost excludes the base.')]:
 story.append(PageBreak());para(title,'Heading1');pic(n);para(cap)
story.append(PageBreak());para('Fabrication and assembly notes','Heading1')
for block in readme.split('\n\n'):
 if block.startswith('# ') or block.startswith('|'):continue
 if block.startswith('## '):para(block[3:],'Heading2');continue
 block=re.sub(r'\[([^\]]+)\]\(([^)]+)\)',r'\1',block);block=html.escape(block).replace('\n','<br/>');block=re.sub(r'\*\*(.*?)\*\*',r'<b>\1</b>',block);para(block)
def foot(c,d):c.setFont('Helvetica',8);c.drawString(51,22,'PVC-dominant FPV gate / fabrication prototype / 2026-09-17');c.drawRightString(560,22,str(d.page))
SimpleDocTemplate(str(O/'PVC_Gate_Study.pdf'),pagesize=(612,792),leftMargin=51,rightMargin=51,topMargin=36,bottomMargin=40).build(story,onFirstPage=foot,onLaterPages=foot)
links=[]
for kind in ['stack_ready','split_s','basic']:
 links.append(f'<h3>{kind}</h3><p>'+ ' · '.join(f'<a href="{kind}_{name}.csv">{label}</a>' for name,label in [('Printed_BOM','Parts'),('Print_Queue','Print queue'),('PVC_Cuts','PVC cuts'),('PVC_Stock_Layout','Stock nesting'),('Sleeve_Positions','Sleeve positions'),('Magnet_Positions','Magnet positions'),('Paper_Cuts','Paper cuts'),('Cord_Cuts','Cord cuts')])+f' · <a href="{kind}_Paper_and_Magnet_Map.svg">Face map</a></p>')
rows=''.join(f'<tr><td>{label}</td><td>{stats[k]["printed_pieces"]}</td><td>{stats[k]["grams"]/1000:.3f}</td><td>{stats[k]["minutes"]/60:.1f}</td><td>{stats[k]["pipe_sticks"]}</td><td>${stats[k]["frame_PVC_plus_PETG_usd"]:.2f}</td></tr>' for k,label in [('basic','Basic single, long pipes'),('stack_ready','Recommended single'),('split_s','Two-level Split-S')])
figs=''.join(f'<figure><a href="renders/{n}.png"><img src="renders/{n}.png" alt="{n}"></a></figure>' for n in ['01_SINGLE_FRONT','02_SINGLE_BACK','03_SPLIT_S_FRONT','04_SPLIT_S_BACK','05_PRINTED_PARTS','06_CORNER_AND_DIAGONAL','07_MAGNET_SLEEVE','08_SHARED_DIVIDER','09_FIRST_FIT_PLATE'])
(O/'index.html').write_text(f'''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>PVC paper gate and Split-S</title><style>body{{font:17px/1.6 system-ui;max-width:1150px;margin:35px auto;padding:0 24px;color:#17374c;background:#f4f7f9}}img{{width:100%}}figure{{margin:24px 0}}a{{color:#006f91}}aside{{padding:20px;background:#e1edf2}}table{{width:100%;border-collapse:collapse}}td,th{{padding:10px;border-bottom:1px solid #bcced6;text-align:left}}h1{{line-height:1.2}}</style><h1>PVC does the spanning / printed parts do the joining</h1><p>One outer PVC perimeter and a PVC ring around each opening. Paper conceals the pipes and fittings from the front; magnets sit 18 mm inside the edges. The shared divider enables a 2700 × 4790.4 mm two-level obstacle.</p><p><a href="PVC_Paper_Gate.blend">Open Blender</a> · <a href="PVC_Gate_Study.pdf">Design and assembly PDF</a> · <a href="README.md">Full guide</a> · <a href="PVC_Paper_Gate_Kit.zip">Download kit</a></p><table><tr><th>Configuration</th><th>Pieces</th><th>PETG kg</th><th>Print h</th><th>$6 PVC sticks</th><th>Subtotal*</th></tr>{rows}</table><p>*PVC + PETG at $20/kg. Face skeleton only; add magnets, cord, paper, adhesive, base, guys and anchoring. Actual local A1 Mini slicing estimates. Five production part types for the recommended single and double.</p><aside><b>First print:</b> <a href="sliced/FIRST_FIT/FIRST_FIT_A1Mini_PETG.3mf">FIRST_FIT for the A1 Mini</a> — {fit['grams']:.2f} g / {fit['minutes']/60:.2f} hours. One outer corner, sleeve, cord saddle, bore gauge and optional front pad. Check actual pipe and magnet fit before printing the gate.</aside>{figs}<h2>Fabrication ledgers</h2>{''.join(links)}<p><a href="Comparison.csv">Comparison</a> · <a href="Upgrade_Additional_Parts.csv">Upgrade parts</a> · <a href="Upgrade_Additional_PVC.csv">Upgrade PVC</a> · <a href="print_checks.json">Digital checks</a></p><p>All supplied plates fit with at least 5 mm bed clearance and slice without supports or warnings. Front pads are optional; the frame-side plastic skins and peaked sleeve roofs remain. Physical load testing and a qualified base/anchoring design remain outstanding, particularly at the 4.79 m stacked height. No printer job was submitted.</p></html>''')
with zipfile.ZipFile(O/'PVC_Paper_Gate_Kit.zip','w',zipfile.ZIP_DEFLATED) as z:
 for p in O.rglob('*'):
  if not p.is_file() or p.suffix in ['.zip','.log','.gcode','.blend1']:continue
  if 'sliced' in p.parts and p.suffix!='.3mf':continue
  z.write(p,Path('pvc_paper_gate')/p.relative_to(O))
print('PACKAGED',rs['grams'],rs['minutes'],ss['grams'],ss['minutes'],'cord',cord_totals)

from pathlib import Path
import pymupdf as fitz,json
from PIL import Image,ImageOps,ImageDraw
O=Path(__file__).resolve().parents[1]/'output/a1_full_size';A=O/'manual_assets';doc=fitz.open(O/'Assembly_and_Test_Instructions.pdf')
assert len(doc)==16 and len(doc.get_toc())==16
thumbs=[];issues=[]
for i,page in enumerate(doc):
 text=page.get_text();assert len(text)>300,(i,len(text))
 for block in page.get_text('dict')['blocks']:
  for line in block.get('lines',[]):
   for span in line['spans']:
    r=fitz.Rect(span['bbox'])
    if r.x0<0 or r.x1>612.1 or r.y0<0 or r.y1>792.1:issues.append([i+1,span['text'],list(r)])
 pix=page.get_pixmap(matrix=fitz.Matrix(1.3,1.3),alpha=False);pix.save(str(A/f'page_{i+1:02d}.png'))
 im=Image.frombytes('RGB',[pix.width,pix.height],pix.samples);im.thumbnail((306,396));thumbs.append(im)
sheet=Image.new('RGB',(4*326,4*426),'#cbd3d8');draw=ImageDraw.Draw(sheet)
for i,im in enumerate(thumbs):x=(i%4)*326+10;y=(i//4)*426+20;sheet.paste(im,(x,y));draw.text((x,y-16),f'Page {i+1}',fill='black')
sheet.save(A/'contact_sheet.png')
assert not issues,issues
alltext='\n'.join(p.get_text() for p in doc)
for word in ['CHANNEL_LONG','CHANNEL_SHORT','19 unique','740','856','32.4','24 mm','6.1 mm','425.7','1586.8']:assert word in alltext,word
report={'pages':16,'bookmarks':16,'outside_page_text':issues,'all_pages_have_text':True,'pdf_bytes':(O/'Assembly_and_Test_Instructions.pdf').stat().st_size,'part1_pages':[2,6],'part2_pages':[7,16]}
(A/'manual_checks.json').write_text(json.dumps(report,indent=2));print(report)

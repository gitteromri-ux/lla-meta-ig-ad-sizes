from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
root=Path(__file__).parent
out=root/'brand-v3-exports'
font=ImageFont.truetype(str(root/'assets/fonts/Inter.ttf'),20)
for family in ['zoom','portrait','card']:
    files=sorted(out.glob(f'{family}-*.png'))
    sheet=Image.new('RGB',(1200,1830),'#ebe8e0')
    draw=ImageDraw.Draw(sheet)
    for i,p in enumerate(files):
        im=Image.open(p).convert('RGB');im.thumbnail((380,560))
        x=(i%3)*400+(400-im.width)//2;y=(i//3)*610+37
        sheet.paste(im,(x,y));draw.text(((i%3)*400+10,(i//3)*610+8),p.stem,font=font,fill='#111b29')
    sheet.save(out/f'proof-{family}.jpg',quality=93)
sheet=Image.new('RGB',(1200,550),'#ebe8e0');draw=ImageDraw.Draw(sheet)
for i,c in enumerate(['zoom','portrait','card']):
    im=Image.open(out/f'{c}-4x5hi-1440x1800.png').convert('RGB').resize((375,469),Image.Resampling.LANCZOS)
    sheet.paste(im,(i*400+12,48));draw.text((i*400+12,15),['01  Zoom experience','02  Julie portrait','03  Vertical brand card'][i],font=font,fill='#111b29')
sheet.save(out/'phone-size-comparison.jpg',quality=96)

from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
root=Path(__file__).parent
font=ImageFont.truetype(str(root/'assets/fonts/Inter.ttf'),20)
for family in ['zoom','portrait','card']:
    files=sorted((root/'review-exports').glob(f'{family}-*.png'))
    sheet=Image.new('RGB',(1200,3*610),'#e8e5df')
    d=ImageDraw.Draw(sheet)
    for i,p in enumerate(files):
        im=Image.open(p).convert('RGB');im.thumbnail((380,560))
        x=(i%3)*400+(400-im.width)//2;y=(i//3)*610+35
        sheet.paste(im,(x,y));d.text(((i%3)*400+10,(i//3)*610+8),p.stem,font=font,fill='#142036')
    sheet.save(root/'review-exports'/f'proof-{family}.jpg',quality=91)
sheet=Image.new('RGB',(1200,555),'#e8e5df');d=ImageDraw.Draw(sheet)
for i,c in enumerate(['zoom','portrait','card']):
    im=Image.open(root/'review-exports'/f'{c}-4x5hi-1440x1800.png').convert('RGB')
    im=im.resize((375,469),Image.Resampling.LANCZOS)
    sheet.paste(im,(i*400+12,48));d.text((i*400+12,15),['01  Zoom','02  Standing portrait','03  Masterclass card'][i],font=font,fill='#142036')
sheet.save(root/'review-exports'/'three-banners-phone-size.jpg',quality=96)

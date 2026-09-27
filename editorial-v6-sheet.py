from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
r=Path(__file__).parent
out=r/'editorial-v6-exports'
font=ImageFont.truetype(str(r/'assets/fonts/Inter.ttf'),20)
im=Image.new('RGB',(1200,540),'#eae7e0');d=ImageDraw.Draw(im)
for i,c in enumerate(['zoom','portrait','card']):
    x=12+i*400
    d.text((x,12),['Live experience','Age slower','The masterclass'][i],font=font,fill='#132235')
    pic=Image.open(out/f'{c}-blue-1080x1350.png').convert('RGB')
    pic.thumbnail((376,470),Image.Resampling.LANCZOS)
    im.paste(pic,(x,49))
im.save(out/'three-new-directions.jpg',quality=95)

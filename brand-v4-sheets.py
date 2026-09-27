from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
root=Path(__file__).parent
out=root/'brand-v4-exports'
font=ImageFont.truetype(str(root/'assets/fonts/Inter.ttf'),20)
for c in ['zoom','portrait','card']:
    canvas=Image.new('RGB',(1200,1070),'#ebe8e0')
    draw=ImageDraw.Draw(canvas)
    for row,v in enumerate(['a','b']):
        for col,t in enumerate(['gold','blue','white']):
            x=12+col*400;y=12+row*533
            draw.text((x,y),f"{'Protocol revealed' if v=='a' else 'Learn to age slower'} / {t}",font=font,fill='#172337')
            im=Image.open(out/f'{c}-{v}-{t}-4x5-1080x1350.png').convert('RGB')
            im.thumbnail((376,470),Image.Resampling.LANCZOS)
            canvas.paste(im,(x,y+37))
    canvas.save(out/f'{c}-copy-color-comparison.jpg',quality=94)
formats=['1x1-1080x1080','1x1hi-1440x1440','4x5-1080x1350','4x5hi-1440x1800','9x16m-1080x1920','9x16-1080x1920','9x16hi-1440x2560','191x1-1200x628','16x9-1920x1080']
for c in ['zoom','portrait','card']:
    for v in ['a','b']:
        canvas=Image.new('RGB',(1200,1500),'#ebe8e0');draw=ImageDraw.Draw(canvas)
        for i,f in enumerate(formats):
            x=(i%3)*400+12;y=(i//3)*500+12
            draw.text((x,y),f,font=font,fill='#172337')
            im=Image.open(out/f'{c}-{v}-blue-{f}.png').convert('RGB')
            im.thumbnail((376,455),Image.Resampling.LANCZOS)
            canvas.paste(im,(x,y+34))
        canvas.save(out/f'proof-{c}-{v}.jpg',quality=92)

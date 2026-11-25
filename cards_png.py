from pathlib import Path
import json
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parent
SITE=ROOT/'site'
ASSETS=ROOT/'card_assets'
def build():
    d=json.loads((SITE/'market.json').read_text(encoding='utf-8'))
    a=d['analytics']['chains']; g=a['4217']['ranges']['30d']
    cards=[('overview','The market in motion.',[(str(sum(v['task_count'] for v in a.values())),'Tasks retrieved'),('2','Networks')]),('flows','Follow the flow.',[(format(int(g['reward_raw'])/1e6,',.2f'),'Reward units posted / 30d'),(format(int(g['paid_raw'])/1e6,',.2f'),'Reward units paid / 30d')]),('networks','Two networks.',[(str(a['4217']['top5_concentration_pct'])+'%','Tempo / top five requesters'),(str(a['8453']['top5_concentration_pct'])+'%','Base / top five requesters')]),('activity','The market has a rhythm.',[(str(g['posted']),'Tasks posted / 30d'),(str(a['4217']['unique_posters'])+' / '+str(a['8453']['unique_posters']),'Tempo / Base requester addresses')])]
    def fit(draw,text,name,size,width):
        while size>12:
            f=ImageFont.truetype(str(ASSETS/name),size)
            if draw.textlength(text,font=f)<=width: return f
            size-=1
        raise ValueError('Text cannot fit')
    for name,title,metrics in cards:
        im=Image.new('RGB',(1200,630),'#12100E'); draw=ImageDraw.Draw(im)
        draw.text((52,36),'MARKET / PULSE',font=fit(draw,'MARKET / PULSE','inter.ttf',24,1096),fill='#B0A79D')
        draw.text((52,94),title,font=fit(draw,title,'serif.ttf',90,1096),fill='#EFE9E2')
        for i,(value,label) in enumerate(metrics):
            x=52+i*558
            draw.rounded_rectangle((x,250,x+538,460),radius=18,fill='#221E1A',outline='#453E37',width=2)
            draw.text((x+24,273),value,font=fit(draw,value,'inter.ttf',65,490),fill='#EFE9E2')
            draw.text((x+24,385),label,font=fit(draw,label,'inter.ttf',22,490),fill='#B0A79D')
        draw.rectangle((52,500,1148,504),fill='#D9A097')
        stamp='Snapshot: '+d['data']['captured_at'][:16]+' UTC'
        draw.text((52,525),'Independent Taskmarket analytics',font=fit(draw,'Independent Taskmarket analytics','inter.ttf',22,800),fill='#EFE9E2')
        draw.text((52,558),stamp,font=fit(draw,stamp,'inter.ttf',22,800),fill='#B0A79D')
        logo=Image.open(SITE/'assets'/'taskmarket-lockup.png').convert('RGBA'); logo.thumbnail((230,55)); im.paste(logo,(1148-logo.width,520),logo)
        draw.text((918,582),'taskmarket.dev',font=fit(draw,'taskmarket.dev','inter.ttf',20,230),fill='#B0A79D')
        out=SITE/'share'/(name+'.png'); tmp=out.with_suffix('.tmp'); im.save(tmp,format='PNG',optimize=True); tmp.replace(out)
        print('PNG_OK',name,out.stat().st_size)
if __name__=='__main__': build()

from pathlib import Path
import json,html,base64
ROOT=Path(__file__).resolve().parent/'site'
def build():
    d=json.loads((ROOT/'market.json').read_text(encoding='utf-8'))
    a=d['analytics']['chains']
    g=a['4217']['ranges']['30d']
    logo=base64.b64encode((ROOT/'assets'/'taskmarket-lockup.png').read_bytes()).decode('ascii')
    stamp=d['data']['captured_at'][:16]+' UTC'
    cards=[('overview','The market in motion.',[(str(sum(v['task_count'] for v in a.values())),'Tasks retrieved'),('2','Networks')]),('flows','Follow the flow.',[(format(int(g['reward_raw'])/1e6,',.2f'),'Reward units posted / 30d'),(format(int(g['paid_raw'])/1e6,',.2f'),'Reward units paid / 30d')]),('networks','Two networks.',[(str(a['4217']['top5_concentration_pct'])+'%','Tempo / top five requesters'),(str(a['8453']['top5_concentration_pct'])+'%','Base / top five requesters')]),('activity','The market has a rhythm.',[(str(g['posted']),'Tasks posted / 30d'),(str(a['4217']['unique_posters'])+' / '+str(a['8453']['unique_posters']),'Tempo / Base requester addresses')])]
    for name,title,metrics in cards:
        elements=['<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" viewBox="0 0 1200 630">','<rect width="1200" height="630" fill="#12100E"/>','<text x="52" y="60" font-family="monospace" font-size="22" fill="#B0A79D">MARKET / PULSE</text>',f'<text x="52" y="175" font-family="Georgia,serif" font-size="72" fill="#EFE9E2">{html.escape(title)}</text>']
        for i,(value,label) in enumerate(metrics):
            x=52+i*558
            elements.extend([f'<rect x="{x}" y="250" width="538" height="210" rx="18" fill="#221E1A" stroke="#453E37"/>',f'<text x="{x+24}" y="350" font-family="sans-serif" font-size="64" fill="#EFE9E2">{html.escape(value)}</text>',f'<text x="{x+24}" y="410" font-family="sans-serif" font-size="22" fill="#B0A79D">{html.escape(label)}</text>'])
        elements.extend(['<rect x="52" y="500" width="1096" height="4" fill="#D9A097"/>','<text x="52" y="550" font-size="22" fill="#EFE9E2">Independent Taskmarket analytics</text>',f'<text x="52" y="584" font-size="18" fill="#B0A79D">{html.escape(stamp)}</text>',f'<image x="918" y="523" width="230" height="55" href="data:image/png;base64,{logo}"/>','<text x="918" y="603" font-family="monospace" font-size="18" fill="#B0A79D">taskmarket.dev</text>','</svg>'])
        p=ROOT/'share'/(name+'.svg')
        p.parent.mkdir(exist_ok=True)
        tmp=p.with_suffix('.tmp')
        tmp.write_text(''.join(elements),encoding='utf-8')
        tmp.replace(p)
    print('DYNAMIC_SHARE_CARDS',len(cards))
if __name__=='__main__': build()

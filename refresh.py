from pathlib import Path
import sys,subprocess,time,json
ROOT=Path(__file__).resolve().parent
def refresh():
    started=time.monotonic()
    for name in ('collect.py','analyze.py','bundle.py','cards.py','cards_png.py'):
        subprocess.run([sys.executable,str(ROOT/name)],cwd=ROOT,check=True,timeout=240)
    d=json.loads((ROOT/'site'/'market.json').read_text(encoding='utf-8'))
    assert d['data']['captured_at']==d['analytics']['captured_at']
    print('REFRESH_OK',d['data']['captured_at'],round(time.monotonic()-started,2))
if __name__=='__main__': refresh()

import json
from pathlib import Path
ROOT=Path(__file__).resolve().parent/'site'
def build():
    d=json.loads((ROOT/'data.json').read_text(encoding='utf-8'))
    a=json.loads((ROOT/'analytics.json').read_text(encoding='utf-8'))
    assert d['captured_at']==a['captured_at'],'Snapshot mismatch'
    for k,c in d['chains'].items():
        assert sum(c['derived']['statuses'].values())==c['derived']['task_count']
        assert sum(c['derived']['modes'].values())==c['derived']['task_count']
        assert a['chains'][k]['task_count']==c['derived']['task_count']
        if not c['history_complete']: print('WARNING_PARTIAL_HISTORY',k)
    p=ROOT/'market.json'; tmp=p.with_suffix('.tmp'); tmp.write_text(json.dumps({'data':d,'analytics':a},ensure_ascii=False,separators=(',',':')),encoding='utf-8'); tmp.replace(p)
    print('ATOMIC_SNAPSHOT',p.stat().st_size)
if __name__=='__main__': build()

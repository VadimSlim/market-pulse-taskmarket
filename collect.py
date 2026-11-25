import json,urllib.request,urllib.parse,datetime,collections,time
from pathlib import Path
BASE='https://api.taskmarket.dev'
ROOT=Path(__file__).resolve().parent

def get(path,**params):
    url=BASE+path+'?'+urllib.parse.urlencode(params)
    for attempt in range(3):
        try:
            req=urllib.request.Request(url,headers={'Accept':'application/json','User-Agent':'MarketPulse/1.0'})
            with urllib.request.urlopen(req,timeout=25) as r:
                return json.load(r)
        except Exception:
            if attempt==2: raise
            time.sleep(2**attempt)

def task_history(chain):
    tasks={}; cursor=None; seen=set(); complete=False
    for page in range(100):
        params={'chainId':chain,'sort':'newest','limit':100}
        if cursor: params['cursor']=cursor
        d=get('/api/tasks',**params)
        for task in d['tasks']:
            if int(task.get('chainId',-1))==chain: tasks[task['id']]=task
        if not d.get('hasMore'):
            complete=True; break
        cursor=d.get('nextCursor')
        if not cursor or cursor in seen: break
        seen.add(cursor)
    return list(tasks.values()),complete

def derive(tasks):
    weeks=collections.defaultdict(set); statuses=collections.Counter(); modes=collections.Counter(); posters=collections.Counter()
    for t in tasks:
        statuses[str(t.get('status','unknown'))]+=1
        modes[str(t.get('mode','unknown'))]+=1
        try:
            dt=datetime.datetime.fromisoformat(t['createdAt'].replace('Z','+00:00')); week=(dt.date()-datetime.timedelta(days=dt.weekday())).isoformat()
        except (ValueError,KeyError,TypeError): continue
        addr=t.get('requester')
        if addr:
            weeks[week].add(addr.lower()); posters[addr.lower()]+=1
    return {'weekly_posters':[{'week':w,'count':len(v)} for w,v in sorted(weeks.items())],'statuses':dict(statuses),'modes':dict(modes),'task_count':len(tasks),'unique_posters':len(posters),'top5_poster_tasks':sum(n for _,n in posters.most_common(5))}

def build():
    started=datetime.datetime.now(datetime.timezone.utc).isoformat(); result={'capture_started':started,'chains':{},'source':BASE,'schema_version':1}
    for chain in (4217,8453):
        data={'stats':get('/api/market/stats',chainId=chain),'breakdowns':get('/api/stats/breakdowns',chainId=chain),'series':{},'heatmaps':{},'feed':get('/api/stats/activity-feed',chainId=chain,limit=25)}
        for span in ('7d','30d','90d','all'):
            data['series'][span]=get('/api/stats/platform-time-series',chainId=chain,range=span,bucket='week' if span=='all' else 'day')
            data['heatmaps'][span]=get('/api/stats/activity-heatmap',chainId=chain,range=span,dimension='hourOfWeek')
        tasks,complete=task_history(chain); data['derived']=derive(tasks); data['history_complete']=complete
        result['chains'][str(chain)]=data
        print('CHAIN',chain,'TASKS',len(tasks),'HISTORY_COMPLETE',complete,flush=True)
    for c in result['chains'].values():
        c['feed']={'items':[{k:v for k,v in item.items() if k in ('type','timestamp','taskId','taskTitle','chainId','amount','rating')} for item in c['feed'].get('items',[])]}
    a,b=result['chains']['4217'],result['chains']['8453']; result['identical_at_capture']=[k for k in ('breakdowns','series','heatmaps','feed') if a[k]==b[k]]
    result['captured_at']=datetime.datetime.now(datetime.timezone.utc).isoformat()
    out=ROOT/'site'/'data.json'; out.parent.mkdir(parents=True,exist_ok=True); tmp=out.with_suffix('.tmp'); tmp.write_text(json.dumps(result,ensure_ascii=False,separators=(',',':')),encoding='utf-8'); tmp.replace(out)
    print('DATA_BYTES',out.stat().st_size,'IDENTICAL',result['identical_at_capture'],flush=True)

if __name__=='__main__': build()

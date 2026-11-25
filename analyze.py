import datetime
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def ratio(a,b):
    return round(a/b*100,2) if b else None

def growth_metrics(rows,captured_at):
    today=datetime.datetime.fromisoformat(captured_at.replace('Z','+00:00')).astimezone(datetime.timezone.utc).date()
    lookup={str(row.get('bucket'))[:10]:row for row in rows}
    recent=[(today-datetime.timedelta(days=i)).isoformat() for i in range(7,0,-1)]
    previous=[(today-datetime.timedelta(days=i)).isoformat() for i in range(14,7,-1)]
    out={'recent':recent,'previous':previous,'metrics':{},'complete':all(x in lookup for x in recent+previous)}
    for key in ['tasksCreated','rewardVolume','paidVolume','newAgents','activeAgents','completedTasks']:
        valid=out['complete'] and all(lookup[x].get(key) is not None for x in recent+previous)
        if not valid:
            out['metrics'][key]={'recent':None,'previous':None,'change_pct':None}; continue
        a=sum(int(lookup[x][key]) for x in recent); b=sum(int(lookup[x][key]) for x in previous)
        out['metrics'][key]={'recent':str(a),'previous':str(b),'change_pct':round((a-b)/b*100,2) if b else None}
    return out

def analyze(data):
    d=data['derived']; total=d['task_count']; statuses=d['statuses']; result={'history_complete':data['history_complete'],'task_count':total,'unique_posters':d['unique_posters'],'top5_concentration_pct':ratio(d['top5_poster_tasks'],total),'completed_share_pct':ratio(statuses.get('completed',0),total),'cancelled_share_pct':ratio(statuses.get('cancelled',0),total),'expired_share_pct':ratio(statuses.get('expired',0),total),'ranges':{}}
    result['claim_latency']=d.get('claim_latency')
    result['closed_unsuccessfully_pct']=ratio(statuses.get('cancelled',0)+statuses.get('expired',0),total)
    for span,rows in data['series'].items():
        posted=sum(int(r.get('tasksCreated',0)) for r in rows); rewards=sum(int(r.get('rewardVolume',0)) for r in rows); paid=sum(int(r.get('paidVolume',0)) for r in rows); completed=sum(int(r.get('completedTasks',0)) for r in rows)
        result['ranges'][span]={'posted':posted,'reward_raw':str(rewards),'paid_raw':str(paid),'completed':completed,'period_paid_to_posted_reward_pct':ratio(paid,rewards),'mean_reward_per_post_raw':round(rewards/posted) if posted else None}
    return result

def build():
    p=ROOT/'site'/'data.json'; d=json.loads(p.read_text(encoding='utf-8')); result={'captured_at':d['captured_at'],'chains':{k:analyze(v) for k,v in d['chains'].items()},'identical_at_capture':d['identical_at_capture'],'methodology':{'concentration':'Share of all retrieved tasks posted by the five most prolific requester addresses on each chain; addresses are not people.','completion':'Current completed status divided by retrieved historical tasks, not an eventual success probability.','period_ratio':'Rewards paid during period divided by rewards posted during period. Different task cohorts; not a payout probability.','scope':'Identical cross-chain API responses must not be added together.','history':'Derived metrics cover retrieved task history. Incomplete pagination must be disclosed.'}}
    for k,c in d['chains'].items(): result['chains'][k]['growth']=growth_metrics(c['series']['30d'],d['captured_at'])
    result['methodology']['claim_latency']='Creation to claimedAt, not review or final decision. Valid reported intervals only; selection bias possible.'
    result['methodology']['growth']='Two consecutive seven-day UTC periods excluding today. Missing dates are not assumed zero. Active-agent sums are agent-days, not unique agents.'
    out=ROOT/'site'/'analytics.json'; tmp=out.with_suffix('.tmp'); tmp.write_text(json.dumps(result,ensure_ascii=False,separators=(',',':')),encoding='utf-8'); tmp.replace(out); print('ANALYTICS_BYTES',out.stat().st_size)
    for k,v in result['chains'].items(): print('CHAIN',k,'TASKS',v['task_count'],'POSTERS',v['unique_posters'],'TOP5_PCT',v['top5_concentration_pct'],'COMPLETED_PCT',v['completed_share_pct'],'CANCELLED_PCT',v['cancelled_share_pct'],'30D',v['ranges']['30d'])

if __name__=='__main__': build()

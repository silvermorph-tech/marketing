import json, collections
from datetime import datetime, timezone, timedelta
HKT = timezone(timedelta(hours=8))
visits = json.load(open('ezzy_data/visits.json'))
custs  = json.load(open('ezzy_data/customers.json'))
state  = json.load(open('ezzy_data/customer_state.json'))
owner = {c['id']: c['owner'] for c in custs}
owned = collections.Counter(c['owner'] for c in custs)

# 累計每人打卡覆蓋（distinct 機構）
cov = collections.defaultdict(set)
for v in visits: cov[v['visited_by']].add(v['customer_id'])
for r in ('Kelly','Jeffrey','Jordan'):
    print(f"{r}: 名下機構 {owned[r]}, 累計已拜訪 {len(cov[r])}, 完成率 {len(cov[r])/owned[r]*100:.1f}%")

# 有 customer_state 記錄的機構（已進漏斗）按 owner
st = collections.defaultdict(set)
for s in state: st[owner.get(s['customer_id'],'?')].add(s['customer_id'])
print('\n按 owner 已進狀態表機構數:')
for r in ('Kelly','Jeffrey','Jordan'):
    print(f"{r}: {len(st[r])}/{owned[r]} = {len(st[r])/owned[r]*100:.1f}%")

# 未進狀態表 = 未拜訪，各 owner 剩餘
print('\n總機構:', len(custs), '已進狀態表:', len(state))

# 高意向清單
print('\n高意向/已約Demo/試用中:')
for s in state:
    if s['status'] in ('高意向','已約 Demo','已约 Demo'):
        nm = {c['id']:c['name'] for c in custs}.get(s['customer_id'],'?')
        print(f"  {s['status']} | {nm[:40]} | interest={s['interest']} | next={s['next_follow_up']}")

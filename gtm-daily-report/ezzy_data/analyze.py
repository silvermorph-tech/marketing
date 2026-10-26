import json
from datetime import datetime, timezone, timedelta

HKT = timezone(timedelta(hours=8))
tw_end   = datetime(2026,10,12,0,0,tzinfo=HKT)   # 本週一
tw_start = datetime(2026,10,5,0,0,tzinfo=HKT)    # 上週一
pw_start = datetime(2026,9,28,0,0,tzinfo=HKT)

def load(t): return json.load(open(f'ezzy_data/{t}.json'))
visits, state, pipe, contacts, custs = load('visits'), load('customer_state'), load('pipeline'), load('contacts'), load('customers')
cust_name = {c['id']: c['name'] for c in custs}
cust_owner = {c['id']: c['owner'] for c in custs}

def ts(v): return datetime.fromisoformat(v['inserted_at'])

tw = [v for v in visits if tw_start <= ts(v) < tw_end]
pw = [v for v in visits if pw_start <= ts(v) < tw_start]
print('visits total:', len(visits))
print('本週打卡:', len(tw), ' 上週打卡:', len(pw))
print('本週覆蓋機構:', len(set(v['customer_id'] for v in tw)), ' 上週:', len(set(v['customer_id'] for v in pw)))

import collections
def by_rep(vs): return collections.Counter(v['visited_by'] for v in vs)
print('本週 by rep:', dict(by_rep(tw)))
print('上週 by rep:', dict(by_rep(pw)))
print('全量 by rep:', dict(by_rep(visits)))

def rep_newcust(vs): return {r: len(set(v['customer_id'] for v in vs if v['visited_by']==r)) for r in ('Kelly','Jeffrey','Jordan')}
print('本週各rep覆蓋機構:', rep_newcust(tw))
print('上週各rep覆蓋機構:', rep_newcust(pw))

print('\n--- outcome 分佈 本週 ---')
for k,c in collections.Counter(v['outcome'] for v in tw).most_common(): print(f'  {k}: {c}')
print('--- outcome 上週 ---')
for k,c in collections.Counter(v['outcome'] for v in pw).most_common(): print(f'  {k}: {c}')

print('\n--- customer_state status 全量 ---')
for k,c in collections.Counter(s['status'] for s in state).most_common(): print(f'  {k}: {c}')
print('state rows:', len(state))

print('\n--- state 本週更新 (updated_at in 本週) ---')
stw = [s for s in state if tw_start <= datetime.fromisoformat(s['updated_at']) < tw_end]
for s in stw:
    print(f"  {s['customer_id']} {cust_name.get(s['customer_id'],'?')[:30]} -> {s['status']} by {s['latest_visited_by']} interest={s['interest']} next={s['next_follow_up']}")

print('\n--- pipeline 全量 stage ---')
for k,c in collections.Counter(p['stage'] for p in pipe).most_common(): print(f'  {k}: {c}')
ptw = [p for p in pipe if tw_start <= datetime.fromisoformat(p['updated_at']) < tw_end]
print('--- pipeline 本週更新 ---')
for p in ptw:
    print(f"  {p['customer_id']} {cust_name.get(p['customer_id'],'?')[:30]} -> {p['stage']} by {p['updated_by']}")

print('\n--- 本週 note 非空 ---')
for v in tw:
    if v['note'] and v['note'].strip():
        print(f"  [{ts(v).strftime('%m-%d %H:%M')}] {v['visited_by']} @ {cust_name.get(v['customer_id'],'?')[:35]}: {v['note'][:120]} (outcome={v['outcome']}, interest={v['interest']})")

print('\n--- 本週 follow_up_type ---')
print(collections.Counter(v['follow_up_type'] for v in tw))
print('\n--- customers: owner 分佈 / 現場新增 ---')
print('owner:', collections.Counter(c['owner'] for c in custs))
print('created_by:', collections.Counter(c['created_by'] for c in custs))
newc = [c for c in custs if tw_start <= datetime.fromisoformat(c['created_at']) < tw_end]
print('本週新增機構:', len(newc))
for c in newc: print('  ', c['id'], c['name'][:40], 'by', c['created_by'])
print('\ncustomers total:', len(custs))
print('contacts total:', len(contacts))
ctw = [c for c in contacts if tw_start <= datetime.fromisoformat(c['created_at']) < tw_end]
print('本週新增聯絡人:', len(ctw))

import json, collections
from datetime import datetime, timezone, timedelta
HKT = timezone(timedelta(hours=8))
tw_start, tw_end = datetime(2026,10,5,tzinfo=HKT), datetime(2026,10,12,tzinfo=HKT)
pw_start = datetime(2026,9,28,tzinfo=HKT)

visits = json.load(open('ezzy_data/visits.json'))
state  = json.load(open('ezzy_data/customer_state.json'))
pipe   = json.load(open('ezzy_data/pipeline.json'))
custs  = json.load(open('ezzy_data/customers.json'))
name   = {c['id']: c['name'] for c in custs}
region = {c['id']: (c['region'], c['district']) for c in custs}

# 先列出所有原始 outcome 值
print('全部原始 outcome 值:')
for k,c in collections.Counter(v['outcome'] for v in visits).most_common(): print(f'  [{c}] {repr(k)}')

def norm(o):
    if not o: return '未標記'
    s = o.strip()
    if '无人应门' in s or '無人應門' in s or '不在' in s: return '無人應門'
    if '只做電話' in s or '只做电话' in s: return '只做電話'
    if '见到员工' in s or '見到員工' in s or '转交' in s or '轉交' in s: return '見到員工待轉交'
    if '已约' in s or '已約' in s: return '已約 Demo'
    if '見到負責人' in s or '见到负责人' in s: return '見到負責人'
    if '已留資料' in s or '已留资料' in s or '前台' in s or '員工' in s: return '已留資料'
    if '拒絕' in s or '拒绝' in s: return '拒絕'
    return '其他:'+s

for v in visits: v['norm'] = norm(v['outcome'])
def ts(v): return datetime.fromisoformat(v['inserted_at'])
tw = [v for v in visits if tw_start <= ts(v) < tw_end]
pw = [v for v in visits if pw_start <= ts(v) < tw_start]

ORDER = ['無人應門','只做電話','已留資料','見到員工待轉交','見到負責人','已約 Demo','拒絕','未標記']
def show(vs, label):
    cnt = collections.Counter(v['norm'] for v in vs)
    print(f'\n=== {label} (n={len(vs)}) ===')
    for k in ORDER:
        if cnt.get(k): print(f'  {k}: {cnt[k]} ({cnt[k]/len(vs)*100:.0f}%)')
    for k in cnt:
        if k.startswith('其他'): print(f'  {k}: {cnt[k]}')
    return cnt

ctw, cpw = show(tw,'本週'), show(pw,'上週')
call = show(visits,'累計')

# 漏斗（本週）：上門 = 非「只做電話」的拜訪
door = [v for v in tw if v['norm'] != '只做電話']
effective = [v for v in tw if v['norm'] in ('見到員工待轉交','見到負責人','已約 Demo')]
deep = [v for v in tw if v['norm'] in ('見到負責人','已約 Demo')]
print(f'\n本週漏斗: 上門 {len(door)} → 有效接觸 {len(effective)} ({len(effective)/len(door)*100:.0f}%) → 見負責人/約Demo {len(deep)} ({len(deep)/max(len(effective),1)*100:.0f}%)')
print(f'已留資料(未接觸決策人)佔上門: {ctw["已留資料"]}/{len(door)} = {ctw["已留資料"]/len(door)*100:.0f}%')
print(f'無人應門佔上門: {ctw["無人應門"]}/{len(door)} = {ctw["無人應門"]/len(door)*100:.0f}%')

door_a = [v for v in visits if v['norm'] != '只做電話']
eff_a = [v for v in visits if v['norm'] in ('見到員工待轉交','見到負責人','已約 Demo')]
deep_a = [v for v in visits if v['norm'] in ('見到負責人','已約 Demo')]
print(f'累計漏斗: 上門 {len(door_a)} → 有效接觸 {len(eff_a)} ({len(eff_a)/len(door_a)*100:.0f}%) → 深聊/約Demo {len(deep_a)} ({len(deep_a)/max(len(eff_a),1)*100:.0f}%)')
print(f'累計已留資料佔上門: {call["已留資料"]}/{len(door_a)} = {call["已留資料"]/len(door_a)*100:.0f}%')

# 無人應門明細（時段/區域）
print('\n無人應門明細:')
for v in visits:
    if v['norm']=='無人應門':
        print(f"  {ts(v).strftime('%m-%d %H:%M')} {name.get(v['customer_id'],'?')[:30]} {region.get(v['customer_id'])} note={v['note'][:50]}")

# 時段分佈
print('\n本週打卡時段分佈(HKT):')
print(collections.Counter(ts(v).hour for v in tw).most_common())

# 整體覆蓋
print(f'\n總名單: {len(custs)}, 累計打卡覆蓋機構: {len(set(v["customer_id"] for v in visits))}')
print(f'本週打卡 {len(tw)}, 覆蓋 {len(set(v["customer_id"] for v in tw))}; 上週 {len(pw)}, 覆蓋 {len(set(v["customer_id"] for v in pw))}')
print('pipeline:', dict(collections.Counter(p['stage'] for p in pipe)))

# 各 rep 本週（中性呈現）
print('\n本週各成員打卡/覆蓋:')
for r in ('Kelly','Jeffrey','Jordan'):
    rv = [v for v in tw if v['visited_by']==r]
    print(f'  {r}: {len(rv)} 次, {len(set(v["customer_id"] for v in rv))} 家')
own = collections.Counter(c['owner'] for c in custs)
print('名單分配:', dict(own))

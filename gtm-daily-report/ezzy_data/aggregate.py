# -*- coding: utf-8 -*-
"""EZZY GTM 日報聚合腳本 — 以當前 HKT 時間為基準。

用法：在 ezzy_data/ 目錄內執行 `python3 aggregate.py`。
可用環境變數 AGG_NOW 覆蓋基準時間（格式 'YYYY-MM-DD HH:MM'，HKT），用於重跑歷史日期。
"""
import json, os, re
from datetime import datetime, timedelta, timezone
from collections import Counter, defaultdict

HKT = timezone(timedelta(hours=8))
_agg_now = os.environ.get('AGG_NOW')
NOW = datetime.strptime(_agg_now, '%Y-%m-%d %H:%M') if _agg_now else datetime.now(HKT).replace(tzinfo=None)
WINDOW_START = NOW - timedelta(days=7)
TODAY = NOW.strftime('%Y-%m-%d')

def load(t):
    with open(t + '.json', encoding='utf-8') as f:
        return json.load(f)

visits = load('visits')
customer_state = load('customer_state')
pipeline = load('pipeline')
contacts = load('contacts')
customers = load('customers')
cust_by_id = {c['id']: c for c in customers}

OUTCOME_MAP = [
    (r'不在|无人应门|無人應門', '無人應門'),
    (r'只做電話|只做电话', '只做電話'),
    (r'已留資料|已留资料', '已留資料'),
    (r'见到员工|見到員工|需转交|需轉交', '見到員工待轉交'),
    (r'見到負責人|见到负责人', '見到負責人'),
    (r'已約\s*Demo|已约后续\s*Demo|已約Demo', '已約 Demo'),
    (r'拒絕|拒绝', '拒絕'),
]
def norm_outcome(o):
    if not o:
        return '（空）'
    for pat, label in OUTCOME_MAP:
        if re.search(pat, o):
            return label
    return o.strip()

def parse_dt(s):
    if not s:
        return None
    s = str(s).strip()
    for fmt in ('%Y-%m-%d %H:%M', '%Y-%m-%dT%H:%M', '%Y-%m-%d'):
        try:
            return datetime.strptime(s[:len(fmt) + 0] if fmt != '%Y-%m-%dT%H:%M' else s[:16], fmt)
        except ValueError:
            pass
    try:
        return datetime.fromisoformat(s.replace('Z', '+00:00')).replace(tzinfo=None)
    except Exception:
        return None

# ---- visits 標記 ----
for v in visits:
    v['norm'] = norm_outcome(v.get('outcome'))
    dt = parse_dt(v.get('created_at')) or parse_dt(v.get('inserted_at'))
    v['dt'] = dt
    v['in7'] = dt is not None and dt >= WINDOW_START
    v['is_phone_only'] = v['norm'] == '只做電話'
    v['is_door'] = not v['is_phone_only']
    v['is_valid'] = v['norm'] in ('見到員工待轉交', '見到負責人', '已約 Demo')
    v['is_deep'] = v['norm'] in ('見到負責人', '已約 Demo')

in7 = [v for v in visits if v['in7']]
allv = visits

# ---- 漏斗口徑 ----
def funnel(vs):
    return {
        '打卡': len(vs),
        '上門': sum(1 for v in vs if v['is_door']),
        '有效接觸': sum(1 for v in vs if v['is_valid']),
        '深聊': sum(1 for v in vs if v['is_deep']),
    }

out7 = Counter(v['norm'] for v in in7)
out_all = Counter(v['norm'] for v in allv)

print('=== 總體 ===')
print('NOW =', NOW.strftime('%Y-%m-%d %H:%M'), '| window start =', WINDOW_START.strftime('%Y-%m-%d %H:%M'))
print('visits: 全部', len(allv), '| 近7天', len(in7))
print('outcome 近7天:', dict(out7))
print('outcome 全部 :', dict(out_all))
print('漏斗 近7天:', funnel(in7))
print('漏斗 全部 :', funnel(allv))

# 按日打卡（近7天）
byday = Counter(v['dt'].strftime('%m-%d') for v in in7 if v['dt'])
print('按日打卡近7天:', dict(sorted(byday.items())))

# 今日打卡
today = [v for v in visits if v['dt'] and v['dt'].strftime('%Y-%m-%d') == TODAY]
print('今日打卡數:', len(today))
for v in today:
    c = cust_by_id.get(v['customer_id'], {})
    print('  -', c.get('name', v['customer_id']), '|', v['visited_by'], '|', v['norm'], '| interest', v.get('interest'), '| note:', (v.get('note') or '')[:80])

# 按人員
print('近7天打卡按人:', dict(Counter(v['visited_by'] for v in in7)))
print('全部打卡按人 :', dict(Counter(v['visited_by'] for v in allv)))

# ---- 覆蓋 ----
covered = set(v['customer_id'] for v in allv)
covered7 = set(v['customer_id'] for v in in7)
print('名單池:', len(customers), '| 累計覆蓋:', len(covered), f'({len(covered)/len(customers)*100:.1f}%)', '| 近7天新覆蓋:', len(covered7))

# 累計接觸（非只做電話的獨立機構）
touched = set(v['customer_id'] for v in allv if v['is_door'])
print('累計上門接觸機構:', len(touched))

# ---- customer_state 層 ----
st = Counter(s['status'] for s in customer_state)
print('customer_state 狀態分佈:', dict(st))
high = [s for s in customer_state if (s.get('interest') or 0) >= 4]
print('interest>=4 的機構:', [(cust_by_id.get(s['customer_id'], {}).get('name', s['customer_id'])[:30], s['status'], s.get('interest'), s.get('next_follow_up')) for s in high])
no_followup = [s for s in customer_state if not s.get('next_follow_up') and s.get('status') not in ('未接觸',)]
print('無跟進日期的機構數:', len(no_followup))
for s in no_followup:
    c = cust_by_id.get(s['customer_id'], {})
    print('   *', c.get('name', s['customer_id'])[:40], '|', s['status'], '| interest', s.get('interest'), '| by', s.get('latest_visited_by'))

# 今天到期的跟進
due = [s for s in customer_state if s.get('next_follow_up') and s['next_follow_up'] <= TODAY]
print('跟進日期已到期(<=今天):', len(due))
for s in due:
    c = cust_by_id.get(s['customer_id'], {})
    print('   !', c.get('name', s['customer_id'])[:40], '|', s['status'], '| next', s.get('next_follow_up'), '| by', s.get('latest_visited_by'))

# pipeline stage
pst = Counter(p['stage'] for p in pipeline)
print('pipeline stage:', dict(pst))
demo_pipe = [p for p in pipeline if p['stage'] in ('Demo / 試用', '已約 Demo', '試用中')]
for p in demo_pipe:
    c = cust_by_id.get(p['customer_id'], {})
    print('   demo:', c.get('name', p['customer_id'])[:35], '|', p['stage'], '| by', p.get('updated_by'), '|', p.get('updated_at', '')[:10])

# contacts
print('contacts 決策人:', [(c['name'], cust_by_id.get(c['customer_id'], {}).get('name', '')[:25]) for c in contacts])

# ---- 現場反饋分析（近7天，合併重複打卡機構）----
print('\n=== 近7天有內容的 notes ===')
seen = {}
for v in sorted(in7, key=lambda x: x['dt'] or NOW):
    if v.get('note') and v['note'].strip():
        seen[v['customer_id']] = v  # 保留最新一條
notes = [(cust_by_id.get(cid, {}).get('name', cid), v['visited_by'], v['norm'], v['note']) for cid, v in seen.items()]
print('去重後有內容機構數:', len(notes))
for n, by, oc, t in notes:
    print(f'  [{n[:32]}] ({by}|{oc}) {t[:110]}')

# ---- 跟進分級規則（2026-10-26 起）----
# 不是「沒填日期=要跟進」，而是按銷售明確意向信號分級：
# P0 必要跟進：status=高意向/已約 Demo，或 interest>=3，或 note 有明確意向關鍵詞
# P1 培育：interest 1-2 或弱信號（會轉交/留資料/總部在）
# P2 觀察：其餘；排除：不考慮、未拜訪、test
INTEREST_KW = re.compile(r'有興趣|想要|expand|合作|AI|自動.*輸入|價錢OK|預計.*case|重約|傾合作', re.I)
WEAK_KW = re.compile(r'會轉交|交給|留資料|有需要再聯絡|總部在|唔係度|不在')
def follow_tier(s):
    status = s.get('status') or ''
    it = s.get('interest') or 0
    note = latest_notes.get(s['customer_id'], '') or ''
    if status in ('不考慮', '未拜訪') or 'test' in (cust_by_id.get(s['customer_id'], {}).get('name') or '').lower():
        return '排除'
    if status in ('高意向', '已约 Demo', '已約 Demo') or it >= 3 or INTEREST_KW.search(note):
        return 'P0'
    if it >= 1 or WEAK_KW.search(note):
        return 'P1'
    return 'P2'

latest_notes = {}
for v0 in sorted(allv, key=lambda x: x['dt'] or NOW):
    if (v0.get('note') or '').strip():
        latest_notes[v0['customer_id']] = v0['note']
tier_count = Counter()
print('\n=== 跟進分級（新規則）===')
for s in customer_state:
    t = follow_tier(s)
    if t == '排除':
        continue
    tier_count[t] += 1
    if t == 'P0' and not s.get('next_follow_up'):
        c = cust_by_id.get(s['customer_id'], {})
        print('P0 無日期:', c.get('name', s['customer_id'])[:38], '|', s.get('status'), '| interest', s.get('interest'), '| by', s.get('latest_visited_by'))
print('分層:', dict(tier_count))
print('P0 無日期數:', sum(1 for s in customer_state if follow_tier(s) == 'P0' and not s.get('next_follow_up')))
print('P0 總數:', sum(1 for s in customer_state if follow_tier(s) == 'P0'))

# 留資料機構中無跟進日期（淤積層）
liuzi = [s for s in customer_state if s.get('status') == '已留資料' and not s.get('next_follow_up')]
print('\n已留資料無跟進日期:', len(liuzi))
for s in liuzi:
    c = cust_by_id.get(s['customer_id'], {})
    print('   -', c.get('name', s['customer_id'])[:40], '| interest', s.get('interest'), '| by', s.get('latest_visited_by'))

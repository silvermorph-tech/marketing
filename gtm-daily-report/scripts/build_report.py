#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""跑 aggregate.py 並生成當日日報骨架（數據部分），情報欄位留空待人/agent 補完。

用法（repo 根目錄）：
  python3 gtm-daily-report/scripts/build_report.py

輸出：gtm-daily-report/reports/gtm_daily_report_YYYY-MM-DD.md
已存在的同名檔案不會被覆蓋（保護人工改過的內容）。
"""
import datetime
import os
import subprocess
import sys

HKT = datetime.timezone(datetime.timedelta(hours=8))
HERE = os.path.dirname(os.path.abspath(__file__))
GTM = os.path.dirname(HERE)
DATA = os.path.join(GTM, 'ezzy_data')

now = datetime.datetime.now(HKT)
date = now.strftime('%Y-%m-%d')
weekday = '一二三四五六日'[now.weekday()]

r = subprocess.run(
    [sys.executable, 'aggregate.py'],
    cwd=DATA, capture_output=True, text=True,
)
if r.returncode != 0:
    sys.exit(f'aggregate.py 執行失敗：\n{r.stderr}')

agg_out = r.stdout.strip()

report = f"""# EZZY GTM 日報 · {date}（週{weekday}）

> 🤖 本檔由 GitHub Actions 於 {now.strftime('%H:%M')} HKT 自動生成：已拉取 Supabase 五表最新快照，以下為數據聚合結果。
> 🎯 銷售情報 / 💰 商業化情報 / ✅ 今日行動 由人工或 agent 補完；情報去重基準：`sent_intel_log.md`（7 天內同一事件只報一次）。

## 📊 地推漏斗覆盤（截至 {now.strftime('%Y-%m-%d %H:%M')} HKT）

```text
{agg_out}
```

## 🎯 銷售情報

> 待補。

## 💰 商業化情報

> 待補。

## ✅ 今日行動

> 待補（按優先級、標屬主）。
"""

os.makedirs(os.path.join(GTM, 'reports'), exist_ok=True)
path = os.path.join(GTM, 'reports', f'gtm_daily_report_{date}.md')
if os.path.exists(path):
    print(f'已存在，不覆蓋：{path}')
else:
    with open(path, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f'已生成：{path}')

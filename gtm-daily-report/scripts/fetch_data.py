#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""從 Supabase 拉取 GTM 五張表快照 → ezzy_data/*.json

用法：
  SUPABASE_ANON_KEY=xxx python3 scripts/fetch_data.py [輸出目錄，預設 ezzy_data]

預設以 SUPABASE_URL 指向團隊 Supabase 項目；可用環境變數覆蓋。
五表全部要求 HTTP 200，任一失敗即非零退出（數據紀律：區分「拉取失敗」與「零錄入」）。
"""
import json
import os
import sys
import urllib.request
import urllib.error

SUPABASE_URL = os.environ.get('SUPABASE_URL', 'https://igqedzdaeubnexplzloa.supabase.co').rstrip('/')
KEY = os.environ.get('SUPABASE_ANON_KEY') or os.environ.get('SUPABASE_SERVICE_ROLE_KEY')
if not KEY:
    sys.exit('缺少環境變數 SUPABASE_ANON_KEY（或 SUPABASE_SERVICE_ROLE_KEY）')

TABLES = {
    'customers': 'select=*',
    'contacts': 'select=*',
    'pipeline': 'select=*',
    'customer_state': 'select=*',
    'visits': 'select=*&order=inserted_at.desc',
}

def main():
    out_dir = sys.argv[1] if len(sys.argv) > 1 else 'ezzy_data'
    os.makedirs(out_dir, exist_ok=True)
    ok = True
    for table, query in TABLES.items():
        url = f'{SUPABASE_URL}/rest/v1/{table}?{query}'
        req = urllib.request.Request(url, headers={
            'apikey': KEY,
            'Authorization': f'Bearer {KEY}',
        })
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                rows = json.load(r)
        except urllib.error.HTTPError as e:
            print(f'{table}: HTTP {e.code} — {e.read().decode()[:200]}', file=sys.stderr)
            ok = False
            continue
        path = os.path.join(out_dir, f'{table}.json')
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(rows, f, ensure_ascii=False, indent=2)
        print(f'{table}: HTTP 200, {len(rows)} rows → {path}')
    sys.exit(0 if ok else 1)

if __name__ == '__main__':
    main()

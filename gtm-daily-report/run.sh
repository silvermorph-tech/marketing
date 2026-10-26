#!/usr/bin/env bash
# EZZY GTM 日報一鍵本地執行：拉數據 → 生成日報骨架 →（可選）發郵件
#
# 用法（在 gtm-daily-report/ 目錄內）：
#   ./run.sh            # 只更新數據 + 生成骨架
#   ./run.sh --mail     # 完成後發郵件（需 config.env 設好 SMTP_*）
set -euo pipefail
cd "$(dirname "$0")"

# 讀取本地設定（config.env 已被 .gitignore 忽略，不會進 git）
[ -f config.env ] && source config.env

echo "==> 1/3 拉取 Supabase 五表快照"
python3 scripts/fetch_data.py ezzy_data

echo "==> 2/3 生成日報骨架"
python3 scripts/build_report.py

if [ "${1:-}" = "--mail" ]; then
  echo "==> 3/3 發送郵件"
  python3 scripts/send_report.py
else
  echo "==> 3/3 跳過郵件（加 --mail 可發信）"
fi

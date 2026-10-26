#!/usr/bin/env bash
# 雙擊此檔案 = 更新數據 + 發出今日日報郵件
cd "$(dirname "$0")"
./run.sh --mail
echo ""
read -n 1 -s -r -p "完成，按任意鍵關閉..."

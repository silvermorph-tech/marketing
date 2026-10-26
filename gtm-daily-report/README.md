# EZZY GTM 日報工作流

> 📁 **本目錄是「去數據版本」（public repo）**：只收錄腳本與文檔。數據快照、日報歸檔、情報日誌與 GitHub Actions 定時任務都在 private repo `Silvermorph-tech/silvermorph-skills`。本目錄的 `.gitignore` 已擋下 `ezzy_data/*.json`、`reports/`、`sent_intel_log.md`，請勿把含客戶資料的檔案提交到這裡。

每日面向 EZZY 地推團隊（Kelly / Jeffrey / Jordan）的 GTM 日報：漏斗覆盤、銷售情報、商業化情報、P0/P1/P2 跟進分級、今日行動清單。

## 目錄結構

```
gtm-daily-report/
├── ezzy_data/            # 數據快照（JSON）+ 分析腳本（Python）
│   ├── customers.json        # 機構主檔（名稱、地區、屬主 owner）
│   ├── contacts.json         # 聯絡人
│   ├── visits.json           # 地推打卡紀錄（outcome、note、inserted_at）
│   ├── pipeline.json         # 漏斗管線
│   ├── customer_state.json   # 客戶狀態（interest、跟進日期等）
│   ├── aggregate.py          # 主聚合腳本：漏斗統計 + P0/P1/P2 分級重算
│   ├── funnel.py             # 漏斗 outcome 歸一化與分層
│   ├── analyze.py            # 週期對比分析（本週 vs 上週）
│   └── coverage.py           # 每人覆蓋率（名下機構 vs 已拜訪）
├── scripts/
│   ├── fetch_data.py         # 從 Supabase 拉取五表快照（HTTP 200 逐一驗證）
│   └── build_report.py       # 跑 aggregate 並生成當日日報骨架（情報欄位留空）
├── reports/              # 日報歸檔（一份 = 一個工作日）
│   └── gtm_daily_report_YYYY-MM-DD.md
└── sent_intel_log.md     # 已發送情報日誌（去重唯一基準）
```

## 數據來源

打卡系統 = Supabase 項目 `igqedzdaeubnexplzloa`（ezzy-field 打卡 App 寫入），五張表：`customers`（278 seed + 現場新增）/ `contacts` / `visits` / `pipeline` / `customer_state`。本地快照即用 `scripts/fetch_data.py` 從 Supabase REST API 拉取。

## 自動化（GitHub Actions）

`.github/workflows/gtm-report.yml`：**每週一、五 09:00 HKT** 自動執行——

1. 拉取 Supabase 五表快照 → 更新 `ezzy_data/*.json`
2. 跑 `aggregate.py` → 生成當日 `reports/gtm_daily_report_YYYY-MM-DD.md` 骨架（數據部分，情報欄位留空）
3. 有變更才 commit 並推送

需要 repo 設定 Secret `SUPABASE_ANON_KEY`（前端同款 anon key；RLS 已管控權限）。亦可隨時在 Actions 頁手動觸發（workflow_dispatch）。已存在的同日報不會被覆蓋。

## 每日運作流程（人工 / agent 補完部分）

1. **更新數據快照**：✅ 週一、五由 Actions 自動執行；其他日子手動跑 `python3 scripts/fetch_data.py gtm-daily-report/ezzy_data`。
2. **跑聚合**：✅ 已併入 Actions 的骨架生成。手動執行：
   ```bash
   cd gtm-daily-report/ezzy_data && python3 aggregate.py
   ```
   （`analyze.py` / `funnel.py` / `coverage.py` 為輔助分析，依當日需要執行；注意各腳本預設的工作目錄不同。）
3. **撰寫日報**：按最新歸檔的 `reports/` 模板格式產出當日 `gtm_daily_report.md`，核心欄位：
   - 今日一句話（最重要的判斷）
   - 累計覆蓋 / Demo 中 / P0 缺口 摘要表
   - 🎯 銷售情報、💰 商業化情報（各 2 條，附來源連結與「用處／啟發」）
   - 📊 地推漏斗覆盤（7 天流轉 + 累計 outcome 分佈 + 跟進分級清單）
   - ✅ 今日行動（按優先級、標屬主）
4. **情報去重**：同一事件／政策／案例 **7 天內只報一次**（有重大進展除外）。去重基準為 `sent_intel_log.md` 記錄的最近一次**實發**情報（草稿不算數）。
5. **歸檔**：日報發出後，複製為 `reports/gtm_daily_report_YYYY-MM-DD.md`，並把當日實發情報追加到 `sent_intel_log.md`。

## 跟進分級口徑（2026-10-26 起生效）

不再以「沒填跟進日期」一概算作缺口。只有銷售明確留有意向信號的才算**必要跟進（P0）**：

- ① 狀態為高意向／已約 Demo
- ② interest ≥ 3
- ③ 打卡 note 有明確意向關鍵詞（有興趣／想要／AI 自動錄入／價錢 OK／expand／預計 case 數等）

「不考慮」與「未拜訪」直接排除；低意向且無信號的列入培育／觀察層（P1/P2），不作追數要求。

## 數據紀律

- 日報必須包含「近 7 天打卡次數」警報：若打卡為零，要區分是「零錄入」還是「數據丟失」（五表拉取驗證）。
- 數字與前一期的對比以 `reports/` 最近一次歸檔為基準。

## 隱私

`ezzy_data/` 含真實客戶資料，本庫僅限 Silvermorph 團隊內部使用。

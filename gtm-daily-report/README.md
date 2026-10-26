# EZZY GTM 日報 · 一鍵工具

每天早上自動從打卡系統下載最新數據、生成當日日報。
填一次郵箱設定，之後**雙擊一下**就能把日報發出去。

---

## 第一步：安裝（2 分鐘）

打開「終端機」（Terminal，按 `Command + 空格` 輸入 Terminal 就有），貼上：

```bash
git clone https://github.com/Silvermorph-tech/marketing.git ~/gtm
```

然後把設定檔建好（把 key 貼進去，key 找 Kelly 要）：

```bash
cd ~/gtm/gtm-daily-report
cp config.env.example config.env
open -e config.env        # 用文字編輯器打開，貼上 SUPABASE_ANON_KEY，存檔
```

## 第二步：設成每天早上自動更新

終端機再貼一行（每天 09:00 自動下載數據 + 生成日報）：

```bash
(crontab -l 2>/dev/null; echo '0 9 * * * cd ~/gtm/gtm-daily-report && ./run.sh >> cron.log 2>&1') | crontab -
```

**完成 ✅** 之後每天打開 `gtm/gtm-daily-report/reports/` 就能看到當日日報。

## 第三步：連接你的郵箱（要發信才需要）

1. 到 **myaccount.google.com/apppasswords** 建一組「應用程式密碼」（16 位亂碼；公司帳號建不了就先用個人 Gmail）
2. 打開 `config.env`，填三段：

```
SMTP_USER=你的郵箱@gmail.com
SMTP_PASS=那16位密碼
MAIL_TO=收件人（多人用逗號隔開）
```

## 每天使用

| 要做什麼 | 怎麼做 |
|---|---|
| 看日報 | 打開 `reports/` 文件夾 |
| **發日報** | **雙擊 `發送日報.command`**（第一次要右鍵 → 打開） |
| 發信 | 用編輯器把日報裡的「銷售情報 / 商業化情報 / 今日行動」補完，再雙擊發送 |

> ⚠️ `config.env`（含你的郵箱密碼）永遠不會被上傳 GitHub（已設防線）；含客戶資料的檔案也不要手動提交。

管理細節（數據口徑、情報去重規則）見 [WORKFLOW.md](WORKFLOW.md)。

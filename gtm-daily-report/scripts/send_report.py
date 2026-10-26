#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把當日 GTM 日報以電郵發出（SMTP，純標準庫）。

用法（在 gtm-daily-report/ 目錄內）：
  python3 scripts/send_report.py [報告路徑，預設當日骨架]

必填環境變數：
  SMTP_USER   寄件帳號（Gmail 請用「應用程式密碼」，不是登入密碼）
  SMTP_PASS   密碼 / 應用程式密碼
  MAIL_TO     收件人，多個以逗號分隔
選填：
  SMTP_HOST（預設 smtp.gmail.com）、SMTP_PORT（預設 465）、MAIL_FROM（預設同 SMTP_USER）
"""
import datetime
import html
import os
import smtplib
import ssl
import sys
from email.header import Header
from email.mime.text import MIMEText

HKT = datetime.timezone(datetime.timedelta(hours=8))
HERE = os.path.dirname(os.path.abspath(__file__))
GTM = os.path.dirname(HERE)


def md_to_html(md: str) -> str:
    out, in_code, in_table = [], False, False

    def close_table():
        nonlocal in_table
        if in_table:
            out.append('</pre>')
            in_table = False

    for line in md.splitlines():
        s = html.escape(line)
        if line.strip().startswith('```'):
            close_table()
            out.append('<pre>' if not in_code else '</pre>')
            in_code = not in_code
            continue
        if in_code:
            out.append(s)
        elif line.lstrip().startswith('|'):
            if not in_table:
                out.append('<pre style="font-family:ui-monospace,monospace;font-size:13px">')
                in_table = True
            out.append(s)
        else:
            close_table()
            if s.startswith('### '):
                out.append(f'<h3>{s[4:]}</h3>')
            elif s.startswith('## '):
                out.append(f'<h2>{s[3:]}</h2>')
            elif s.startswith('# '):
                out.append(f'<h1>{s[2:]}</h1>')
            elif not s.strip():
                out.append('')
            else:
                out.append(f'<p>{s}</p>')
    close_table()
    if in_code:
        out.append('</pre>')
    return '\n'.join(out)


def main():
    date = datetime.datetime.now(HKT).strftime('%Y-%m-%d')
    path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(GTM, 'reports', f'gtm_daily_report_{date}.md')
    if not os.path.exists(path):
        print(f'找不到當日日報：{path}（略過發信）')
        return

    user, pwd, to = os.environ.get('SMTP_USER'), os.environ.get('SMTP_PASS'), os.environ.get('MAIL_TO')
    missing = [k for k, v in (('SMTP_USER', user), ('SMTP_PASS', pwd), ('MAIL_TO', to)) if not v]
    if missing:
        sys.exit('缺少環境變數：' + ', '.join(missing))

    host = os.environ.get('SMTP_HOST', 'smtp.gmail.com')
    port = int(os.environ.get('SMTP_PORT', '465'))
    from_addr = os.environ.get('MAIL_FROM', user)

    with open(path, encoding='utf-8') as f:
        md = f.read()

    msg = MIMEText(md_to_html(md), 'html', 'utf-8')
    msg['Subject'] = Header(f'EZZY GTM 日報 · {date}', 'utf-8')
    msg['From'] = from_addr
    msg['To'] = to
    with smtplib.SMTP_SSL(host, port, context=ssl.create_default_context()) as s:
        s.login(user, pwd)
        s.sendmail(from_addr, [a.strip() for a in to.split(',') if a.strip()], msg.as_string())
    print(f'已發送：{path} → {to}')


if __name__ == '__main__':
    main()

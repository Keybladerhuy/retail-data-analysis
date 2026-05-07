# Data Analysis Portfolio

**Business-focused data analysis and reporting, delivered in plain language**

---

## Project Overview

This portfolio demonstrates the type of analysis and reporting delivered to clients. The scenario: a UK-based e-commerce company had two years of transaction data with no visibility into trends, product health, or customer behaviour. Starting from raw Excel data, the project answers three questions:

1. Is revenue growing, seasonal, or declining — and why?
2. Which products drive revenue, and which are quietly declining?
3. Who are the most valuable customers, and what should be done for each group?

**Dataset:** UCI Online Retail II — ~800K cleaned transactions, 2009–2011 (public domain)

---

## Sample Output

| Monthly Revenue Trend | Customer Segment Distribution |
|---|---|
| ![Monthly Revenue](output/charts/monthly_revenue_yoy.png) | ![Customer Segments](output/charts/rfm_segment_distribution.png) |

| Product Revenue Concentration | Month-over-Month Change |
|---|---|
| ![Pareto Analysis](output/charts/pareto_revenue.png) | ![MoM Change](output/charts/mom_revenue_change.png) |

Every chart is delivered with plain-language commentary and recommended next actions.

**[Download sample report (PDF) → output/report_sample.pdf](output/report_sample.pdf)**

---

## Analyses Included

| Analysis | What it answers |
|---|---|
| Data Cleaning & Quality Check | Is the data reliable enough to act on? |
| Monthly & Weekly Sales Trend | Is the business growing, and when does it peak? |
| Revenue Drop Investigation | Why did revenue fall last month? |
| Product Performance Ranking | Which products generate revenue, and which are declining? |
| Customer RFM Segmentation | Who are the best customers, and what should we do for each group? |
| SQL Query Examples | Runnable queries for the same analyses (SQLite / DuckDB / BigQuery) |

---

## How Automation Works

This portfolio goes beyond static analysis — it runs as a fully automated weekly reporting pipeline.

**Weekly Schedule**
Every Monday at 8:00 AM Japan time, GitHub Actions automatically runs the report generator. No manual work needed. The updated PDF is committed back to the repository.

**Email Delivery**
After the report is generated, it is sent as a PDF attachment to a configured email address using SendGrid. The email includes a plain-language summary of three headline metrics: total revenue, top-selling product, and the most valuable customer group.

**Live Data Hook**
Instead of a static Excel file, the pipeline can pull fresh data directly from a client's Google Sheet. The client updates their spreadsheet; the system reads it automatically at the next scheduled run. If Google Sheets is not configured, the system falls back to the local Excel file — so it works offline without any extra setup.

---

## For Clients

**How it works for you:**

1. **You provide a Google Sheet** with your sales data (same columns as a standard POS or order export). No technical knowledge required — just copy-paste your data.
2. **Every Monday morning, a report is generated automatically** covering last week's sales, top products, and customer segments.
3. **The report arrives in your inbox as a PDF** with plain-language commentary — no spreadsheets to open, no charts to build yourself.

This is the same pipeline running in this repository. Get in touch to discuss setting it up for your business.

---

## Tech Stack

- **Python** — pandas, numpy, matplotlib, seaborn, statsmodels
- **SQL** — SQLite-compatible (also runs in DuckDB, BigQuery, Redshift)
- **Jupyter Notebooks** — analysis and narrative together
- **nbconvert** — PDF/HTML report export with code hidden
- **SendGrid** — automated PDF email delivery
- **Google Sheets API (gspread)** — live data ingestion from client spreadsheets
- **GitHub Actions** — weekly scheduled pipeline

---

## Environment Variables Setup

Copy `.env.example` to `.env` and fill in your values to enable automation locally.

| Variable | Description |
|---|---|
| `SENDGRID_API_KEY` | SendGrid API key for email delivery |
| `REPORT_RECIPIENT_EMAIL` | Email address to receive the weekly report |
| `REPORT_SENDER_EMAIL` | Verified sender address in your SendGrid account |
| `GOOGLE_SHEETS_KEY_PATH` | Local path to your Google service account JSON key file |
| `GOOGLE_SHEETS_TEMPLATE_ID` | ID of the Google Sheet to load data from |

**GitHub Actions secrets:**
Add these in your repository under `Settings → Secrets and variables → Actions`. For the Google Sheets key, store the full JSON content as a secret named `GOOGLE_SHEETS_KEY_JSON`.

---

## How to Run

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. (Optional) Configure environment variables
cp .env.example .env
# Edit .env with your SendGrid and Google Sheets credentials

# 3. Download the dataset (if running locally without Google Sheets)
#    https://archive.ics.uci.edu/dataset/502/online+retail+ii
#    Save as: data/online_retail_II.xlsx

# 4. Run notebooks in order (01 → 02 → 03 → 04)
jupyter notebook

# 5. Generate the PDF report (and send email if configured)
python generate_report.py
```

---

## About

Senior data scientist at a global semiconductor manufacturer. Day-to-day work covers demand analysis, manufacturing moves forecasting, production data analysis, and operational improvement projects. Speciality: turning data into decisions that people without a technical background can act on.

---

## Contact

Open to freelance data analysis and reporting engagements. Feel free to get in touch by email.

---
---

# データ分析ポートフォリオ

**現役データサイエンティストによる、わかりやすい分析・レポート作成サービス**

---

## こんなお悩みはありませんか？

- データや数字はあるけど、何をすればいいかわからない
- レポートを見ても、次のアクションが思い浮かばない
- 分析を誰かに頼みたいけど、どこに相談すればいいかわからない

**そのお悩み、ぜひご相談ください。**  
データを「使える情報」に変えて、わかりやすくお伝えします。

---

## 納品サンプル

以下は実際の分析結果の例です。このようなグラフとレポートをお届けします。

| 月別売上の推移 | 顧客グループの分布 |
|---|---|
| ![月別売上](output/charts/monthly_revenue_yoy.png) | ![顧客セグメント](output/charts/rfm_segment_distribution.png) |

| 商品別の売上集中度 | 前月比の売上変化 |
|---|---|
| ![パレート分析](output/charts/pareto_revenue.png) | ![前月比](output/charts/mom_revenue_change.png) |

グラフには日本語の解説と「次にとるべきアクション」をセットでお届けします。

**[サンプルレポートをダウンロード（PDF）→ output/report_sample.pdf](output/report_sample.pdf)**

---

## このポートフォリオについて

あるイギリスのネット通販会社が「2年分の売上データはあるが、活かせていない」という状況から、以下の3つの問いに答える分析を行いました。

1. **売上は伸びているのか、落ちているのか？ その理由は？**
2. **どの商品が稼いでいて、どの商品が静かに落ちているのか？**
3. **どのお客様が最も大切で、それぞれに何をすればいいのか？**

データを整理するところから始めて、グラフ作成・原因分析・改善提案まで一貫して対応しています。

---

## できること一覧

| 分析の内容 | こんなときに役立ちます |
|---|---|
| 売上・業績のトレンド分析（月次・週次） | 「今、売上は上がっているのか下がっているのかわからない」 |
| 前年比・前月比の比較 | 「去年と比べてどうなのか知りたい」 |
| 売上が落ちた原因の調査 | 「先月急に数字が落ちた。なぜ？」 |
| 商品・カテゴリ別のパフォーマンス比較 | 「どの商品に力を入れるべきか整理したい」 |
| 顧客の購買パターン分析・グループ分け | 「お客様ごとに施策を変えたい」 |
| データの整理・クレンジング | 「Excelがバラバラで使えない状態」 |

---

## ご導入の流れ（自動レポートをご希望のお客様へ）

毎週自動でレポートが届く仕組みをご希望の場合は、以下の流れで対応しています。

1. **Googleスプレッドシートに売上データをご用意いただくだけ**
   ExcelやPOSのデータをコピー＆ペーストするだけでOKです。専門知識は不要です。
2. **毎週月曜の朝8時（日本時間）に自動でレポートが生成されます**
   前週の売上・商品・顧客データを自動で集計し、PDFレポートとして作成します。
3. **レポートがメールで届きます**
   添付PDFには、売上サマリー・上位商品・顧客グループの分析が含まれます。

> はじめてでも安心してご相談ください。  
> データの準備から設定まで、すべてサポートします。

---

## 自動化の仕組み

| 機能 | 説明 |
|---|---|
| 定期実行 | 毎週月曜8時（JST）にGitHub Actionsが自動でレポートを生成します |
| メール配信 | 生成されたPDFをSendGrid経由で指定のメールアドレスに送信します |
| ライブデータ | Googleスプレッドシートのデータを自動で読み込みます（オプション） |
| ローカル動作 | 環境変数が未設定の場合はローカルのExcelファイルで動作します |

---

## ご依頼の流れ

1. まずはお気軽にご連絡ください（相談無料）
2. データの内容や知りたいことをざっくりお聞きします
3. 分析・レポート作成
4. **グラフ付きレポート（PDF or Excel）**でお届け。日本語でわかりやすく解説します

> ExcelやCSVファイルをそのまま送っていただくだけでOKです。  
> 「何を見ればいいかわからない」状態からでもお気軽にご相談いただけます。

---

## 私について

グローバル半導体メーカーにてシニアデータサイエンティストとして勤務しています。売上分析・需要予測・生産データ解析・業務改善プロジェクトを日常的に担当しており、「データを使って現場の意思決定を助ける」ことを専門としています。

専門的な知識がなくても伝わるよう、結果はすべて**日本語でやさしく説明**します。

---

## 環境変数の設定

自動レポート機能を使用するには、以下の環境変数を設定してください。  
`.env.example` をコピーして `.env` ファイルを作成し、各値を入力してください。

| 変数名 | 説明 |
|---|---|
| `SENDGRID_API_KEY` | SendGridのAPIキー（メール送信に必要） |
| `REPORT_RECIPIENT_EMAIL` | レポートの送付先メールアドレス |
| `REPORT_SENDER_EMAIL` | 送信元メールアドレス（SendGridで認証済みのもの） |
| `GOOGLE_SHEETS_KEY_PATH` | Googleサービスアカウントのキーファイル（JSON）のパス |
| `GOOGLE_SHEETS_TEMPLATE_ID` | データを読み込むGoogleスプレッドシートのID |

**GitHub ActionsでのSecret設定：**  
リポジトリの `Settings → Secrets and variables → Actions` から上記の変数を登録してください。  
Googleスプレッドシートの認証情報はJSONの内容をそのまま `GOOGLE_SHEETS_KEY_JSON` というSecret名で登録します。

---

## ご依頼・お問い合わせ

データ分析・レポート作成のご依頼を承っています。  
まずはお気軽にご連絡ください。

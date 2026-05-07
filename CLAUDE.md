# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Generate the PDF report (optionally sends email if env vars are set)
python generate_report.py

# Run SQL examples against the clean CSV via SQLite (no extra install)
python -c "
import sqlite3, pandas as pd
conn = sqlite3.connect(':memory:')
pd.read_csv('data/clean_retail.csv').to_sql('retail', conn, index=False)
# paste a query from sql/queries.sql
"

# Run notebooks in order
jupyter notebook  # open 01 → 02 → 03 → 04 manually
```

There is no test suite and no linter configuration.

## Architecture

The project is a **two-phase pipeline** separated by the `output/charts/` directory.

**Phase 1 — Analysis (notebooks → charts)**
Four Jupyter notebooks run in sequence and write PNG chart files to `output/charts/`:
- `01_data_cleaning.ipynb` — loads raw Excel, removes cancellations/nulls/invalid rows, saves `data/clean_retail.csv`
- `02_sales_trend_analysis.ipynb` — monthly/weekly revenue trends, YoY comparison, seasonal decomposition
- `03_product_performance.ipynb` — Pareto analysis, top-20 products by revenue and frequency
- `04_customer_rfm.ipynb` — RFM scoring, segment classification (Champions / Loyal / At Risk / New / Lost)

All downstream notebooks read from `data/clean_retail.csv`, not the raw Excel. The `data/` directory is gitignored; charts and the PDF are committed.

**Phase 2 — Report assembly (`generate_report.py`)**
Reads the pre-existing PNG files from `output/charts/` and assembles a 7-page A4 PDF using matplotlib's `PdfPages`. No data loading or computation happens here by default. Pages are individual functions (`page_cover`, `page_summary`, `page_trend`, `page_products`, `page_rfm`, `page_detail`, `page_appendix`).

**Data loading abstraction (`sheets_loader.py`)**
`load_data(spreadsheet_id, sheet_name)` provides a unified data source with this fallback chain:
1. Google Sheets via `gspread` (when `GOOGLE_SHEETS_KEY_PATH` + `spreadsheet_id` are both set)
2. `data/clean_retail.csv` (already cleaned)
3. `data/online_retail_II.xlsx` (applies standard cleaning automatically)

Returns a DataFrame in the same schema as `clean_retail.csv` with a derived `Revenue` column. Used by `generate_report.py` only to extract the three headline email metrics — it does not regenerate charts.

**Automation layer**
`.github/workflows/weekly_report.yml` runs every Monday 08:00 JST (Sunday 23:00 UTC). It generates the PDF, commits any changed `output/` files back to `main` using the `github-actions[bot]` identity, and passes secrets as env vars. All optional integrations (SendGrid email, Google Sheets) are no-ops when their env vars are absent — the script always completes successfully without them.

## Environment variables

All optional. Copy `.env.example` to `.env` for local use; `python-dotenv` loads it automatically.

| Variable | Effect when set |
|---|---|
| `SENDGRID_API_KEY` | Enables email delivery of the PDF after generation |
| `REPORT_RECIPIENT_EMAIL` | Destination address for the report email |
| `REPORT_SENDER_EMAIL` | Verified sender in SendGrid |
| `GOOGLE_SHEETS_KEY_PATH` | Path to service account JSON; enables Sheets data loading |
| `GOOGLE_SHEETS_TEMPLATE_ID` | Spreadsheet ID to load from |

In GitHub Actions, `GOOGLE_SHEETS_KEY_JSON` (the raw JSON secret) is written to `/tmp/gsheets_key.json` and `GOOGLE_SHEETS_KEY_PATH` is set to that path automatically by the workflow.

## Data schema

The canonical clean dataset (`data/clean_retail.csv`) has these columns:

| Column | Type | Notes |
|---|---|---|
| `Invoice` | str | Prefix `C` = cancellation (already removed) |
| `StockCode` | str | Product identifier |
| `Description` | str | Product name |
| `Quantity` | int | Units sold (> 0 after cleaning) |
| `InvoiceDate` | datetime | |
| `Price` | float | Unit price in GBP (> 0 after cleaning) |
| `Customer ID` | int | Anonymous customer ID |
| `Country` | str | |
| `Revenue` | float | `Quantity * Price`, derived |

`sheets_loader._clean()` applies the same cleaning logic to any raw source so the output schema is always consistent.

## Japanese font handling

`generate_report.py` detects a Japanese font at startup (`find_jp_font()`) from a candidate list (Yu Gothic, Meiryo, MS Gothic, Hiragino Sans, Noto Sans CJK JP). Falls back to `sans-serif` with a warning if none found. The GitHub Actions runner (Ubuntu) will not have these fonts — add a `apt-get install fonts-noto-cjk` step to the workflow if Japanese rendering in CI matters.

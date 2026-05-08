# Quickstart

## Prerequisites

```bash
pip install -r requirements.txt
```

Make sure `data/online_retail_II.xlsx` is present (it's committed to the repo, so a fresh clone has it).

Optionally, copy `.env.example` to `.env` and fill in credentials to enable email delivery and Google Sheets data loading.

## Run the full pipeline

```bash
# Step 1 — clean data and generate all charts (notebooks 01 → 04)
./scripts/run_pipeline.sh

# Step 2 — assemble PDF and send email (if SendGrid is configured)
python generate_report.py
python3 generate_report.py (macOs)
```

The PDF is saved to `output/report_sample.pdf`. This runs automatically every Monday 08:00 JST via GitHub Actions.

## Using a client's data

- **Excel:** replace `data/online_retail_II.xlsx` with the client's file (same column schema)
- **Google Sheets:** set `GOOGLE_SHEETS_KEY_PATH` and `GOOGLE_SHEETS_TEMPLATE_ID` in `.env`

Then run the two commands above.

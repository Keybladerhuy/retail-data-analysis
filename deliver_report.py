"""
deliver_report.py
Delivers the generated PDF reports — email by default.
Run from the project root: .venv/bin/python deliver_report.py

Other delivery targets (Slack, Teams, S3, etc.) can be added here
without touching report generation.

Required env vars for email (set in .env or GitHub Secrets):
  GMAIL_SENDER            — Gmail address to send from
  GMAIL_APP_PASSWORD      — 16-character App Password (not your Gmail password)
  REPORT_RECIPIENT_EMAIL  — destination address
"""
import os, base64, logging, smtplib
from email.message import EmailMessage
from datetime import date

from dotenv import load_dotenv
load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
log = logging.getLogger(__name__)

ROOT   = os.path.dirname(os.path.abspath(__file__))
OUT_EN = os.path.join(ROOT, 'output', 'report_sample_en.pdf')
OUT_JA = os.path.join(ROOT, 'output', 'report_sample_ja.pdf')


# ── Data loading & metric extraction ─────────────────────────────────────────

def load_report_data():
    try:
        from sheets_loader import load_data
        df = load_data(
            spreadsheet_id=os.environ.get('GOOGLE_SHEETS_TEMPLATE_ID'),
            sheet_name='Sheet1',
        )
        log.info('Data loaded: %d rows', len(df))
        return df
    except FileNotFoundError as exc:
        log.warning('No data available for metric extraction: %s', exc)
        return None
    except Exception as exc:
        log.warning('Data load error: %s', exc)
        return None


def extract_metrics(df):
    if df is None or df.empty:
        return {
            'total_revenue':   None,
            'top_product':     'N/A',
            'top_segment':     'N/A',
            'top_segment_pct': None,
        }

    total_revenue   = df['Revenue'].sum()
    product_revenue = df.groupby('Description')['Revenue'].sum().sort_values(ascending=False)
    top_product     = product_revenue.index[0] if len(product_revenue) else 'N/A'

    if 'Customer ID' in df.columns:
        last_date   = df['InvoiceDate'].max()
        cutoff      = last_date - __import__('pandas').Timedelta(days=90)
        recent_rev  = df[df['InvoiceDate'] >= cutoff]['Revenue'].sum()
        top_seg_pct = (recent_rev / total_revenue * 100) if total_revenue else 0
        top_segment = 'Champions / Loyal Customers'
    else:
        top_seg_pct = None
        top_segment = 'N/A'

    return {
        'total_revenue':   total_revenue,
        'top_product':     top_product,
        'top_segment':     top_segment,
        'top_segment_pct': top_seg_pct,
    }


# ── Email delivery ────────────────────────────────────────────────────────────

def _build_email_body(metrics, report_date):
    rev     = metrics['total_revenue']
    rev_str = f'£{rev:,.0f}' if rev is not None else 'N/A'
    pct_en  = f'{metrics["top_segment_pct"]:.0f}% of revenue' if metrics['top_segment_pct'] else ''
    pct_jp  = f'売上の{metrics["top_segment_pct"]:.0f}%'      if metrics['top_segment_pct'] else ''

    return (
        f'Weekly Retail Analysis Report — {report_date}\n'
        f'\n'
        f'Key Metrics:\n'
        f'  • Total Revenue:         {rev_str}\n'
        f'  • Top Product:           {metrics["top_product"]}\n'
        f'  • Top Customer Segment:  {metrics["top_segment"]}'
        + (f' ({pct_en})' if pct_en else '') +
        f'\n\nThe full report is attached as a PDF.\n'
        f'\n---\n\n'
        f'週次小売分析レポート — {report_date}\n'
        f'\n'
        f'主要指標：\n'
        f'  ・総売上：　　　　　{rev_str}\n'
        f'  ・売上トップ商品：　{metrics["top_product"]}\n'
        f'  ・主要顧客セグメント：{metrics["top_segment"]}'
        + (f'（{pct_jp}）' if pct_jp else '') +
        f'\n\nPDF形式のレポートを添付しております。\n'
    )


def send_email(metrics):
    from_email   = os.environ.get('GMAIL_SENDER', '')
    app_password = os.environ.get('GMAIL_APP_PASSWORD', '')
    to_email     = os.environ.get('REPORT_RECIPIENT_EMAIL', '')

    if not from_email or not app_password:
        log.warning('GMAIL_SENDER / GMAIL_APP_PASSWORD not set — skipping email delivery.')
        return
    if not to_email:
        log.warning('REPORT_RECIPIENT_EMAIL not set — skipping email delivery.')
        return

    report_date = date.today().strftime('%Y-%m-%d')

    msg = EmailMessage()
    msg['Subject'] = f'Weekly Retail Report — {report_date}'
    msg['From']    = from_email
    msg['To']      = to_email
    msg.set_content(_build_email_body(metrics, report_date))

    for path in [OUT_EN, OUT_JA]:
        if not os.path.exists(path):
            log.warning('Report not found, skipping attachment: %s', path)
            continue
        with open(path, 'rb') as f:
            msg.add_attachment(f.read(), maintype='application', subtype='pdf',
                               filename=os.path.basename(path))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(from_email, app_password)
            server.send_message(msg)
        log.info('Email sent → %s', to_email)
    except Exception as exc:
        log.error('Email delivery failed: %s', exc)


# ── Other delivery targets go here ───────────────────────────────────────────
# Keeping delivery separate from generation means swapping or adding targets
# is just adding a function here — email today, Slack/Teams/S3 tomorrow,
# whatever the client actually uses. The report itself doesn't need to change.
# def send_slack(metrics): ...
# def upload_s3(metrics): ...
# def post_teams(metrics): ...


if __name__ == '__main__':
    df      = load_report_data()
    metrics = extract_metrics(df)
    send_email(metrics)

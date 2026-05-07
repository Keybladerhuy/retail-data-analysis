"""
sheets_loader.py
Loads retail sales data from Google Sheets or falls back to local Excel/CSV.

Usage:
    from sheets_loader import load_data
    df = load_data(
        spreadsheet_id=os.environ.get('GOOGLE_SHEETS_TEMPLATE_ID'),
        sheet_name='Sales'
    )

Returns a cleaned DataFrame with the same columns as data/clean_retail.csv,
including a derived Revenue column. Drop-in replacement for the Excel loader
used in the analysis notebooks.
"""
import os
import logging
from typing import Optional

import pandas as pd

logger = logging.getLogger(__name__)

ROOT          = os.path.dirname(os.path.abspath(__file__))
_FALLBACK_CSV = os.path.join(ROOT, 'data', 'clean_retail.csv')
_FALLBACK_XL  = os.path.join(ROOT, 'data', 'online_retail_II.xlsx')

_REQUIRED_COLS = ['Invoice', 'StockCode', 'Description',
                  'Quantity', 'InvoiceDate', 'Price', 'Customer ID', 'Country']


def _clean(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df = df[~df['Invoice'].astype(str).str.startswith('C')]
    df = df.dropna(subset=['Customer ID'])
    df['Quantity'] = pd.to_numeric(df['Quantity'], errors='coerce')
    df['Price']    = pd.to_numeric(df['Price'],    errors='coerce')
    df = df[(df['Quantity'] > 0) & (df['Price'] > 0)].copy()
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
    df['Revenue']     = df['Quantity'] * df['Price']
    df['Customer ID'] = df['Customer ID'].astype(float).astype(int)
    return df.reset_index(drop=True)


def _load_from_sheets(spreadsheet_id: str, sheet_name: str) -> pd.DataFrame:
    import gspread

    key_path = os.environ.get('GOOGLE_SHEETS_KEY_PATH', '')
    if not key_path or not os.path.exists(key_path):
        raise FileNotFoundError(
            f'Service account key not found at GOOGLE_SHEETS_KEY_PATH={key_path!r}'
        )

    logger.info('Connecting to Google Sheets: %s / %s', spreadsheet_id, sheet_name)
    gc = gspread.service_account(filename=key_path)
    ws = gc.open_by_key(spreadsheet_id).worksheet(sheet_name)
    df = pd.DataFrame(ws.get_all_records())

    missing = [c for c in _REQUIRED_COLS if c not in df.columns]
    if missing:
        raise ValueError(
            f'Google Sheet is missing required columns: {missing}. '
            f'Expected: {_REQUIRED_COLS}'
        )

    return _clean(df)


def _load_fallback() -> pd.DataFrame:
    if os.path.exists(_FALLBACK_CSV):
        logger.info('Loading cleaned CSV: %s', _FALLBACK_CSV)
        return pd.read_csv(_FALLBACK_CSV, parse_dates=['InvoiceDate'])

    if os.path.exists(_FALLBACK_XL):
        logger.info('Loading raw Excel: %s', _FALLBACK_XL)
        s1 = pd.read_excel(_FALLBACK_XL, sheet_name='Year 2009-2010')
        s2 = pd.read_excel(_FALLBACK_XL, sheet_name='Year 2010-2011')
        return _clean(pd.concat([s1, s2], ignore_index=True))

    raise FileNotFoundError(
        'No local data found. Provide data/clean_retail.csv or '
        'data/online_retail_II.xlsx (see README for download link).'
    )


def load_data(
    spreadsheet_id: Optional[str] = None,
    sheet_name: str = 'Sheet1',
) -> pd.DataFrame:
    """
    Load retail sales data.

    Priority:
    1. Google Sheets (when GOOGLE_SHEETS_KEY_PATH and spreadsheet_id are set)
    2. data/clean_retail.csv
    3. data/online_retail_II.xlsx (applies standard cleaning automatically)

    Args:
        spreadsheet_id: Google Sheets ID from the URL. Defaults to None.
        sheet_name:     Name of the worksheet tab. Defaults to 'Sheet1'.

    Returns:
        Cleaned pandas DataFrame with a Revenue column.
    """
    key_path = os.environ.get('GOOGLE_SHEETS_KEY_PATH', '')

    if key_path and spreadsheet_id:
        try:
            return _load_from_sheets(spreadsheet_id, sheet_name)
        except Exception as exc:
            logger.warning(
                'Google Sheets load failed (%s) — falling back to local data.', exc
            )
    else:
        if not key_path:
            logger.info('GOOGLE_SHEETS_KEY_PATH not set — using local data.')
        else:
            logger.info('No spreadsheet_id provided — using local data.')

    return _load_fallback()

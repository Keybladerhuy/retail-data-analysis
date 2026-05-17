#!/usr/bin/env bash
set -euo pipefail

PYTHON="$(dirname "$0")/../.venv/bin/python"

NOTEBOOKS=(
  "01_data_cleaning"
  "02_sales_trend_analysis"
  "03_product_performance"
  "04_customer_rfm"
)

for nb in "${NOTEBOOKS[@]}"; do
  echo "==> Running ${nb}.ipynb"
  "$PYTHON" -m nbconvert --to notebook --execute "notebooks/${nb}.ipynb" \
    --output "/tmp/${nb}_executed.ipynb" \
    --ExecutePreprocessor.timeout=900
done

echo "==> All notebooks completed"

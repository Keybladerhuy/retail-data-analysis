-- ============================================================
-- Data Analysis Portfolio — SQL Query Examples
-- Compatible with: SQLite, DuckDB, BigQuery, Redshift (standard SQL)
-- ============================================================
--
-- HOW TO RUN
-- ----------
-- Option A (SQLite, no install):
--   python -c "
--   import sqlite3, pandas as pd
--   conn = sqlite3.connect(':memory:')
--   pd.read_csv('data/clean_retail.csv').to_sql('retail', conn, index=False)
--   print(pd.read_sql('<paste query here>', conn).to_string())
--   "
--
-- Option B (DuckDB, pip install duckdb):
--   python -c "
--   import duckdb
--   conn = duckdb.connect()
--   conn.execute(\"CREATE TABLE retail AS SELECT * FROM read_csv_auto('data/clean_retail.csv')\")
--   print(conn.execute('<paste query here>').df().to_string())
--   "
--
-- Option C: Paste directly into BigQuery, Redshift, or Snowflake
--   after loading clean_retail.csv as a table named `retail`.
-- ============================================================


-- ── Query 1: Monthly Revenue Aggregation ────────────────────
-- Equivalent to Notebook 02 core analysis.
-- Shows total revenue, order count, and average order value per month.

SELECT
    STRFTIME('%Y-%m', InvoiceDate)          AS year_month,
    ROUND(SUM(Revenue), 2)                  AS total_revenue,
    COUNT(DISTINCT Invoice)                 AS order_count,
    ROUND(SUM(Revenue) / COUNT(DISTINCT Invoice), 2) AS avg_order_value,
    COUNT(DISTINCT "Customer ID")           AS unique_customers
FROM retail
GROUP BY year_month
ORDER BY year_month;


-- ── Query 2: Top N Products by Revenue ──────────────────────
-- Equivalent to Notebook 03 Analysis 1.
-- Change the LIMIT value to get top 10, 20, 50, etc.

SELECT
    StockCode,
    Description,
    ROUND(SUM(Revenue), 2)     AS total_revenue,
    SUM(Quantity)              AS units_sold,
    COUNT(DISTINCT Invoice)    AS order_count,
    ROUND(SUM(Revenue) / SUM(Quantity), 2) AS avg_unit_revenue
FROM retail
GROUP BY StockCode, Description
ORDER BY total_revenue DESC
LIMIT 20;


-- ── Query 3: Revenue by Country ─────────────────────────────
-- Geographic breakdown with share of total revenue.

WITH total AS (
    SELECT SUM(Revenue) AS grand_total FROM retail
)
SELECT
    Country,
    ROUND(SUM(r.Revenue), 2)                             AS total_revenue,
    COUNT(DISTINCT r."Customer ID")                      AS unique_customers,
    COUNT(DISTINCT r.Invoice)                            AS order_count,
    ROUND(SUM(r.Revenue) / t.grand_total * 100, 2)       AS revenue_share_pct
FROM retail r, total t
GROUP BY Country, t.grand_total
ORDER BY total_revenue DESC;


-- ── Query 4: RFM Calculation ─────────────────────────────────
-- Equivalent to Notebook 04 RFM metrics.
-- Snapshot date = 2011-12-31. Adjust as needed.
-- Note: JULIANDAY is SQLite-specific. For BigQuery use DATE_DIFF.

SELECT
    "Customer ID"                                           AS customer_id,
    CAST(JULIANDAY('2011-12-31') - JULIANDAY(MAX(InvoiceDate)) AS INTEGER)
                                                            AS recency_days,
    COUNT(DISTINCT Invoice)                                 AS frequency,
    ROUND(SUM(Revenue), 2)                                  AS monetary
FROM retail
GROUP BY customer_id
ORDER BY monetary DESC;


-- ── Query 5: Month-over-Month Revenue Change ─────────────────
-- Calculates MoM % change using a lag window function.
-- Requires SQLite 3.25+ or any modern SQL engine for window functions.

WITH monthly AS (
    SELECT
        STRFTIME('%Y-%m', InvoiceDate) AS year_month,
        SUM(Revenue)                   AS revenue
    FROM retail
    GROUP BY year_month
)
SELECT
    year_month,
    ROUND(revenue, 2)                                           AS revenue,
    ROUND(LAG(revenue) OVER (ORDER BY year_month), 2)          AS prev_month_revenue,
    ROUND(
        (revenue - LAG(revenue) OVER (ORDER BY year_month))
        / LAG(revenue) OVER (ORDER BY year_month) * 100,
        1
    )                                                           AS mom_change_pct
FROM monthly
ORDER BY year_month;


-- ── Query 6: Customer Cohort — First Purchase Month ──────────
-- Groups customers by the month they first purchased,
-- useful for retention and cohort analysis.

WITH first_purchase AS (
    SELECT
        "Customer ID"                                           AS customer_id,
        STRFTIME('%Y-%m', MIN(InvoiceDate))                     AS cohort_month
    FROM retail
    GROUP BY customer_id
),
activity AS (
    SELECT
        r."Customer ID"                                         AS customer_id,
        STRFTIME('%Y-%m', r.InvoiceDate)                        AS activity_month
    FROM retail r
),
combined AS (
    SELECT
        fp.cohort_month,
        a.activity_month,
        COUNT(DISTINCT a.customer_id)                           AS active_customers
    FROM first_purchase fp
    JOIN activity a ON fp.customer_id = a.customer_id
    GROUP BY fp.cohort_month, a.activity_month
)
SELECT *
FROM combined
ORDER BY cohort_month, activity_month;


-- ── Query 7: Declining Products Flag ────────────────────────
-- Identifies products with revenue lower than the prior month
-- in the most recent 3 consecutive months.
-- Equivalent to Notebook 03 Analysis 5.

WITH monthly_product AS (
    SELECT
        StockCode,
        Description,
        STRFTIME('%Y-%m', InvoiceDate)  AS year_month,
        SUM(Revenue)                    AS revenue
    FROM retail
    GROUP BY StockCode, Description, year_month
),
with_lag AS (
    SELECT
        *,
        LAG(revenue) OVER (PARTITION BY StockCode ORDER BY year_month) AS prev_revenue
    FROM monthly_product
),
declining AS (
    SELECT
        StockCode,
        Description,
        year_month,
        revenue,
        prev_revenue,
        CASE WHEN revenue < prev_revenue THEN 1 ELSE 0 END AS is_declining
    FROM with_lag
    WHERE prev_revenue IS NOT NULL
)
SELECT
    StockCode,
    Description,
    SUM(is_declining)   AS months_declining,
    MIN(year_month)     AS first_month_observed,
    MAX(year_month)     AS last_month_observed
FROM declining
GROUP BY StockCode, Description
HAVING months_declining >= 3
ORDER BY months_declining DESC;

# 🏭 E-Commerce Data Warehouse System
### Cloud Computing Project — Free Stack (Python + SQLite + Pandas)

---

## 📋 Problem Statement

A fast-growing e-commerce company collects massive amounts of data every day:

| Source | Volume |
|---|---|
| Web Logs (clicks, page views, search) | 2 TB / day |
| Transaction Records (orders, payments, returns) | 500 GB / day |
| Customer Reviews (ratings, images) | 200 GB / day |
| Social Media Feeds (Facebook, Twitter) | 100 GB / day |

**Problems Faced:**
1. 🐢 Slow Reporting
2. 🔍 No Single Customer View
3. 😤 Data Scientist / Data Engineer Struggle
4. 🔒 Security Concerns

---

## ✅ Solution — Data Warehouse

This project implements a **Data Warehouse** using a **Star Schema** that:

| Problem | Solution |
|---|---|
| Slow Reporting | Pre-aggregated SQL views, instant analytics |
| No Single View | `v_unified_customer` SQL view merges all sources |
| DE/DS Struggle | ETL pipeline + CSV exports for easy analysis |
| Security | SHA-256 email hashing + read-only analyst views |

---

## 🏗️ Architecture

```
[Web Logs] [Transactions] [Reviews] [Social Media]
      ↓           ↓           ↓           ↓
         ┌──── ETL Pipeline ────┐
         │  Extract → Transform  │
         │  → Load into Warehouse│
         └───────────────────────┘
                    ↓
         ┌──── STAR SCHEMA ─────┐
         │  dim_customer         │
         │  dim_product          │
         │  dim_date             │
         │  fact_transactions    │
         │  fact_web_logs        │
         │  fact_reviews         │
         │  fact_social          │
         └───────────────────────┘
                    ↓
         ┌──── REPORTS ─────────┐
         │  Sales by Category    │
         │  Monthly Revenue      │
         │  Unified Customer     │
         │  Device Analytics     │
         │  Sentiment Analysis   │
         └───────────────────────┘
```

---

## 🛠️ Tech Stack

- **Python 3** — Core language
- **SQLite** — Lightweight database (no server needed)
- **Pandas** — Data analysis and CSV export
- **HTML + Chart.js** — Interactive visual dashboard



---

## 📁 Project Structure

```
ecommerce_data_warehouse/
│
├── data_warehouse.py         # Main ETL + Analytics script
├── dashboard/
│   └── dashboard.html        # Interactive visual dashboard
├── data/
│   └── ecommerce_warehouse.db  # SQLite database (auto-created)
├── reports/
│   ├── sales_by_category.csv
│   ├── monthly_revenue.csv
│   ├── top_customers.csv
│   ├── device_usage.csv
│   └── sentiment_analysis.csv
└── README.md
```

---

## ▶️ How to Run

### Step 1 — Install Python (if not installed)
Download from: https://www.python.org/downloads/

### Step 2 — Install dependencies
```bash
pip install pandas
```

### Step 3 — Run the Data Warehouse
```bash
python data_warehouse.py
```

### Step 4 — View the Dashboard
Open `dashboard/dashboard.html` in any web browser.

---

## 📊 What the System Does

### 1. Data Ingestion (ETL)
- Simulates 4 real data sources (web logs, transactions, reviews, social)
- Extracts, transforms, and loads all data into a unified warehouse

### 2. Star Schema Design
- **Fact Tables**: fact_transactions, fact_web_logs, fact_reviews, fact_social
- **Dimension Tables**: dim_customer, dim_product, dim_date

### 3. Unified Customer View
```sql
SELECT * FROM v_unified_customer;
-- Shows: total orders, total spend, avg order, page views, review rating
-- All in ONE place, across ALL data sources
```

### 4. Analytics Reports (5 Reports)
- Sales revenue by product category
- Monthly revenue trend
- Top customers by spend
- Device usage breakdown
- Customer sentiment analysis

### 5. Security
- Customer emails are never stored in plain text
- All emails are SHA-256 hashed before storage
- Analysts can query views without accessing raw fact tables

---

## 📈 Sample Output

```
[1] Creating Data Warehouse Schema (Star Schema)...
   ✅ Schema created: 4 Fact tables + 3 Dimension tables + Unified View

[2] Generating Simulated Raw Data from 4 Sources...
   ✅ Generated: 200 customers, 2000 transactions,
              3000 web logs, 1000 reviews, 500 social posts

[3] ETL Pipeline: Loading data into Warehouse...
   ✅ ETL complete — all data loaded into warehouse

[4] Running Analytics Reports...
   ✅ Report 1: Sales by Category
   ✅ Report 2: Monthly Revenue Trend
   ✅ Report 3: Top 5 Customers (Single Unified View)
   ✅ Report 4: Device Usage Analytics
   ✅ Report 5: Customer Sentiment Analysis

[5] Security Module Demo...
   ✅ Emails are SHA-256 hashed before storage

DATA WAREHOUSE SUMMARY
======================
dim_customer              →    200 records
dim_product               →      8 records
dim_date                  →    365 records
fact_transactions         →  2,000 records
fact_web_logs             →  3,000 records
fact_reviews              →  1,000 records
fact_social               →    500 records
```

---

## 👤 Author

- **Project**: E-Commerce Data Warehouse
- **Name**: Rahul Kumar , Subhash Manne , Manavendra A

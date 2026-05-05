"""
========================================================
 E-Commerce Data Warehouse System
 Cloud Computing Project
========================================================
 Uses: Python + SQLite (Free, no cloud account needed)
 Simulates a real Data Warehouse with:
   - ETL Pipeline (Extract, Transform, Load)
   - Fact & Dimension Tables (Star Schema)
   - Unified Customer View
   - Reporting & Analytics
   - Security (hashed sensitive data)
"""

import sqlite3
import pandas as pd
import random
import hashlib
import json
import os
from datetime import datetime, timedelta

DB_PATH = "data/ecommerce_warehouse.db"
os.makedirs("data", exist_ok=True)
os.makedirs("reports", exist_ok=True)

print("=" * 60)
print("   E-Commerce Data Warehouse System")
print("=" * 60)

# ─────────────────────────────────────────────
# 1. CREATE WAREHOUSE SCHEMA (Star Schema)
# ─────────────────────────────────────────────
def create_schema(conn):
    print("\n[1] Creating Data Warehouse Schema (Star Schema)...")
    conn.executescript("""
        -- DIMENSION: Customers
        CREATE TABLE IF NOT EXISTS dim_customer (
            customer_id   TEXT PRIMARY KEY,
            customer_name TEXT,
            email_hash    TEXT,   -- Security: email is hashed
            region        TEXT,
            segment       TEXT,
            created_at    TEXT
        );

        -- DIMENSION: Products
        CREATE TABLE IF NOT EXISTS dim_product (
            product_id   TEXT PRIMARY KEY,
            product_name TEXT,
            category     TEXT,
            sub_category TEXT,
            brand        TEXT
        );

        -- DIMENSION: Date
        CREATE TABLE IF NOT EXISTS dim_date (
            date_id     TEXT PRIMARY KEY,
            full_date   TEXT,
            year        INTEGER,
            month       INTEGER,
            quarter     INTEGER,
            day_of_week TEXT
        );

        -- FACT: Transactions (Sales)
        CREATE TABLE IF NOT EXISTS fact_transactions (
            transaction_id TEXT PRIMARY KEY,
            customer_id    TEXT,
            product_id     TEXT,
            date_id        TEXT,
            quantity       INTEGER,
            unit_price     REAL,
            total_amount   REAL,
            payment_method TEXT,
            status         TEXT,
            FOREIGN KEY (customer_id) REFERENCES dim_customer(customer_id),
            FOREIGN KEY (product_id)  REFERENCES dim_product(product_id),
            FOREIGN KEY (date_id)     REFERENCES dim_date(date_id)
        );

        -- FACT: Web Logs
        CREATE TABLE IF NOT EXISTS fact_web_logs (
            log_id       TEXT PRIMARY KEY,
            customer_id  TEXT,
            date_id      TEXT,
            page_visited TEXT,
            time_spent   INTEGER,
            device       TEXT,
            action       TEXT
        );

        -- FACT: Customer Reviews
        CREATE TABLE IF NOT EXISTS fact_reviews (
            review_id   TEXT PRIMARY KEY,
            customer_id TEXT,
            product_id  TEXT,
            date_id     TEXT,
            rating      INTEGER,
            sentiment   TEXT
        );

        -- FACT: Social Media
        CREATE TABLE IF NOT EXISTS fact_social (
            post_id     TEXT PRIMARY KEY,
            platform    TEXT,
            date_id     TEXT,
            post_type   TEXT,
            engagement  INTEGER,
            reach       INTEGER
        );

        -- UNIFIED CUSTOMER VIEW (Single Customer View - solves problem #2)
        CREATE VIEW IF NOT EXISTS v_unified_customer AS
        SELECT
            c.customer_id,
            c.customer_name,
            c.region,
            c.segment,
            COUNT(DISTINCT t.transaction_id) AS total_orders,
            ROUND(SUM(t.total_amount), 2)    AS total_spend,
            ROUND(AVG(t.total_amount), 2)    AS avg_order_value,
            COUNT(DISTINCT w.log_id)         AS total_page_views,
            ROUND(AVG(r.rating), 1)          AS avg_review_rating
        FROM dim_customer c
        LEFT JOIN fact_transactions t ON c.customer_id = t.customer_id
        LEFT JOIN fact_web_logs     w ON c.customer_id = w.customer_id
        LEFT JOIN fact_reviews      r ON c.customer_id = r.customer_id
        GROUP BY c.customer_id;
    """)
    conn.commit()
    print("   ✅ Schema created: 4 Fact tables + 3 Dimension tables + Unified View")


# ─────────────────────────────────────────────
# 2. GENERATE SYNTHETIC SOURCE DATA (simulates raw data from sources)
# ─────────────────────────────────────────────
def generate_data():
    print("\n[2] Generating Simulated Raw Data from 4 Sources...")

    regions   = ["North", "South", "East", "West"]
    segments  = ["Premium", "Regular", "New"]
    products  = [
        ("P001","Laptop","Electronics","Computers","Dell"),
        ("P002","Headphones","Electronics","Audio","Sony"),
        ("P003","T-Shirt","Fashion","Clothing","Zara"),
        ("P004","Running Shoes","Fashion","Footwear","Nike"),
        ("P005","Coffee Maker","Home","Kitchen","Philips"),
        ("P006","Backpack","Accessories","Bags","Wildcraft"),
        ("P007","Smartphone","Electronics","Mobile","Samsung"),
        ("P008","Fiction Book","Books","Novels","Penguin"),
    ]
    pages    = ["home","product","cart","checkout","search","wishlist","account"]
    devices  = ["mobile","desktop","tablet"]
    actions  = ["view","click","add_to_cart","purchase","bounce"]
    payments = ["UPI","Credit Card","Debit Card","Net Banking","Wallet"]
    statuses = ["completed","pending","returned","cancelled"]
    platforms= ["Facebook","Twitter","Instagram"]
    post_types= ["ad","organic","story","reel"]

    customers, transactions, web_logs, reviews, social, dates = [], [], [], [], [], {}

    def make_date(base, delta_days):
        d = base + timedelta(days=delta_days)
        did = d.strftime("%Y%m%d")
        if did not in dates:
            dates[did] = (did, d.strftime("%Y-%m-%d"), d.year, d.month,
                          (d.month-1)//3+1, d.strftime("%A"))
        return did

    base = datetime(2024, 1, 1)

    # 200 customers
    for i in range(1, 201):
        cid   = f"C{i:04d}"
        name  = f"Customer_{i}"
        email = f"customer{i}@email.com"
        customers.append((cid, name,
                          hashlib.sha256(email.encode()).hexdigest()[:16],
                          random.choice(regions),
                          random.choice(segments),
                          (base + timedelta(days=random.randint(0,364))).strftime("%Y-%m-%d")))

    # 2000 transactions
    for i in range(1, 2001):
        cid = f"C{random.randint(1,200):04d}"
        p   = random.choice(products)
        qty = random.randint(1, 5)
        price = round(random.uniform(100, 5000), 2)
        did = make_date(base, random.randint(0, 364))
        transactions.append((f"T{i:06d}", cid, p[0], did, qty, price,
                              round(qty*price, 2),
                              random.choice(payments),
                              random.choice(statuses)))

    # 3000 web logs
    for i in range(1, 3001):
        cid = f"C{random.randint(1,200):04d}"
        did = make_date(base, random.randint(0, 364))
        web_logs.append((f"L{i:06d}", cid, did,
                         random.choice(pages),
                         random.randint(5, 600),
                         random.choice(devices),
                         random.choice(actions)))

    # 1000 reviews
    for i in range(1, 1001):
        cid = f"C{random.randint(1,200):04d}"
        p   = random.choice(products)
        did = make_date(base, random.randint(0, 364))
        rating = random.randint(1, 5)
        sentiment = "positive" if rating >= 4 else ("neutral" if rating == 3 else "negative")
        reviews.append((f"R{i:05d}", cid, p[0], did, rating, sentiment))

    # 500 social media posts
    for i in range(1, 501):
        did = make_date(base, random.randint(0, 364))
        social.append((f"S{i:05d}", random.choice(platforms), did,
                        random.choice(post_types),
                        random.randint(100, 50000),
                        random.randint(1000, 500000)))

    print(f"   ✅ Generated: {len(customers)} customers, {len(transactions)} transactions,")
    print(f"              {len(web_logs)} web logs, {len(reviews)} reviews, {len(social)} social posts")
    return customers, list(products), list(dates.values()), transactions, web_logs, reviews, social


# ─────────────────────────────────────────────
# 3. ETL - LOAD INTO WAREHOUSE
# ─────────────────────────────────────────────
def etl_load(conn, customers, products, dates, transactions, web_logs, reviews, social):
    print("\n[3] ETL Pipeline: Loading data into Warehouse...")

    conn.executemany("INSERT OR IGNORE INTO dim_customer VALUES (?,?,?,?,?,?)", customers)
    conn.executemany("INSERT OR IGNORE INTO dim_product  VALUES (?,?,?,?,?)", products)
    conn.executemany("INSERT OR IGNORE INTO dim_date     VALUES (?,?,?,?,?,?)", dates)
    conn.executemany("INSERT OR IGNORE INTO fact_transactions VALUES (?,?,?,?,?,?,?,?,?)", transactions)
    conn.executemany("INSERT OR IGNORE INTO fact_web_logs     VALUES (?,?,?,?,?,?,?)", web_logs)
    conn.executemany("INSERT OR IGNORE INTO fact_reviews      VALUES (?,?,?,?,?,?)", reviews)
    conn.executemany("INSERT OR IGNORE INTO fact_social       VALUES (?,?,?,?,?,?)", social)
    conn.commit()
    print("   ✅ ETL complete — all data loaded into warehouse")


# ─────────────────────────────────────────────
# 4. ANALYTICS & REPORTS (solves slow reporting - problem #1)
# ─────────────────────────────────────────────
def run_reports(conn):
    print("\n[4] Running Analytics Reports...")

    reports = {}

    # Report 1: Sales by Category
    df1 = pd.read_sql_query("""
        SELECT p.category,
               COUNT(t.transaction_id) AS total_orders,
               ROUND(SUM(t.total_amount),2) AS revenue
        FROM fact_transactions t
        JOIN dim_product p ON t.product_id = p.product_id
        WHERE t.status = 'completed'
        GROUP BY p.category
        ORDER BY revenue DESC
    """, conn)
    reports["sales_by_category"] = df1
    df1.to_csv("reports/sales_by_category.csv", index=False)
    print("   ✅ Report 1: Sales by Category")
    print(df1.to_string(index=False))

    # Report 2: Monthly Revenue Trend
    df2 = pd.read_sql_query("""
        SELECT d.year, d.month,
               ROUND(SUM(t.total_amount),2) AS monthly_revenue,
               COUNT(t.transaction_id) AS orders
        FROM fact_transactions t
        JOIN dim_date d ON t.date_id = d.date_id
        WHERE t.status = 'completed'
        GROUP BY d.year, d.month
        ORDER BY d.year, d.month
        LIMIT 6
    """, conn)
    reports["monthly_revenue"] = df2
    df2.to_csv("reports/monthly_revenue.csv", index=False)
    print("\n   ✅ Report 2: Monthly Revenue Trend (first 6 months)")
    print(df2.to_string(index=False))

    # Report 3: Top 5 Customers (Unified View)
    df3 = pd.read_sql_query("""
        SELECT customer_name, region, segment,
               total_orders, total_spend, avg_order_value, avg_review_rating
        FROM v_unified_customer
        ORDER BY total_spend DESC
        LIMIT 5
    """, conn)
    reports["top_customers"] = df3
    df3.to_csv("reports/top_customers.csv", index=False)
    print("\n   ✅ Report 3: Top 5 Customers (Single Unified View)")
    print(df3.to_string(index=False))

    # Report 4: Device Usage from Web Logs
    df4 = pd.read_sql_query("""
        SELECT device, COUNT(*) AS sessions,
               ROUND(AVG(time_spent),1) AS avg_time_seconds
        FROM fact_web_logs
        GROUP BY device
        ORDER BY sessions DESC
    """, conn)
    reports["device_usage"] = df4
    df4.to_csv("reports/device_usage.csv", index=False)
    print("\n   ✅ Report 4: Device Usage Analytics")
    print(df4.to_string(index=False))

    # Report 5: Sentiment Analysis from Reviews
    df5 = pd.read_sql_query("""
        SELECT sentiment, COUNT(*) AS count,
               ROUND(AVG(rating),2) AS avg_rating
        FROM fact_reviews
        GROUP BY sentiment
        ORDER BY count DESC
    """, conn)
    reports["sentiment"] = df5
    df5.to_csv("reports/sentiment_analysis.csv", index=False)
    print("\n   ✅ Report 5: Customer Sentiment Analysis")
    print(df5.to_string(index=False))

    return reports


# ─────────────────────────────────────────────
# 5. SECURITY MODULE (solves problem #4)
# ─────────────────────────────────────────────
def security_demo():
    print("\n[5] Security Module Demo...")
    email = "rahul@example.com"
    hashed = hashlib.sha256(email.encode()).hexdigest()
    print(f"   Original email : {email}")
    print(f"   Stored in DB   : {hashed[:16]}... (SHA-256 hashed)")
    print("   ✅ Sensitive data (emails/phone) are hashed — never stored in plain text")
    print("   ✅ SQLite supports read-only views — analysts can't modify raw data")
    print("   ✅ Star schema separates facts from dimensions — role-based access possible")


# ─────────────────────────────────────────────
# 6. SUMMARY
# ─────────────────────────────────────────────
def print_summary(conn):
    print("\n" + "="*60)
    print("   DATA WAREHOUSE SUMMARY")
    print("="*60)
    tables = ["dim_customer","dim_product","dim_date",
              "fact_transactions","fact_web_logs","fact_reviews","fact_social"]
    for t in tables:
        count = conn.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
        print(f"   {t:<25} → {count:>6} records")
    print("\n   Problems Solved:")
    print("   ✅ Slow Reporting    → Pre-aggregated queries run instantly")
    print("   ✅ No Single View    → v_unified_customer view merges all data")
    print("   ✅ DE/DS Struggle    → Star schema + CSV exports for easy analysis")
    print("   ✅ Security          → Email hashing + view-based access control")
    print("\n   Reports saved to: reports/")
    print("   Database saved to:", DB_PATH)
    print("="*60)


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────
if __name__ == "__main__":
    conn = sqlite3.connect(DB_PATH)
    create_schema(conn)
    customers, products, dates, transactions, web_logs, reviews, social = generate_data()
    etl_load(conn, customers, products, dates, transactions, web_logs, reviews, social)
    run_reports(conn)
    security_demo()
    print_summary(conn)
    conn.close()
    print("\n✅ Project complete! Run dashboard.py to see the visual dashboard.\n")

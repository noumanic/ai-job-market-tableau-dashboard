"""
02_clean.py
===========
Applies all preprocessing steps to the raw dataset:
  Step 1 — Keep Full-Time (FT) only
  Step 2 — Keep 2022–2025 (data density threshold)
  Step 3 — Remove salary outliers (1st–99th percentile)

Input  : ../data/raw/salaries.csv
Output : ../data/processed/salaries_clean.csv  (intermediate — no title grouping yet)

Run AFTER 01_explore.py.
"""

import pandas as pd
import numpy as np

RAW_PATH  = "../data/raw/salaries.csv"
OUT_PATH  = "../data/processed/salaries_clean.csv"

print("Loading raw data...")
df = pd.read_csv(RAW_PATH)
print(f"  Raw rows : {len(df):,}")

# ── Step 1: Full-Time only ────────────────────────────────────────────────────
df_ft = df[df["employment_type"] == "FT"].copy()
print(f"\nStep 1 — FT filter")
print(f"  Removed  : {len(df) - len(df_ft):,} rows (PT/CT/FL)")
print(f"  Remaining: {len(df_ft):,} rows")

# ── Step 2: 2022–2025 only ────────────────────────────────────────────────────
df_yr = df_ft[df_ft["work_year"] >= 2022].copy()
removed_yr = len(df_ft) - len(df_yr)
print(f"\nStep 2 — Year filter (2022–2025)")
print(f"  Removed  : {removed_yr:,} rows (2020–2021, only 293 rows — too sparse)")
print(f"  Remaining: {len(df_yr):,} rows")

# ── Step 3: Outlier removal (1st–99th percentile) ────────────────────────────
q01 = df_yr["salary_in_usd"].quantile(0.01)
q99 = df_yr["salary_in_usd"].quantile(0.99)
df_clean = df_yr[
    (df_yr["salary_in_usd"] >= q01) &
    (df_yr["salary_in_usd"] <= q99)
].copy()
removed_out = len(df_yr) - len(df_clean)
print(f"\nStep 3 — Outlier removal (1st–99th percentile)")
print(f"  Lower bound : ${q01:,.0f}")
print(f"  Upper bound : ${q99:,.0f}")
print(f"  Removed     : {removed_out:,} rows")
print(f"  Remaining   : {len(df_clean):,} rows")

# ── Summary ───────────────────────────────────────────────────────────────────
print(f"\n{'='*50}")
print(f"CLEAN DATASET SUMMARY")
print(f"{'='*50}")
print(f"  Total rows    : {len(df_clean):,}")
print(f"  Columns       : {df_clean.shape[1]}")
print(f"  Years         : {sorted(df_clean['work_year'].unique())}")
print(f"  Countries     : {df_clean['company_location'].nunique()}")
print(f"  Unique titles : {df_clean['job_title'].nunique()}")
print(f"  Median salary : ${df_clean['salary_in_usd'].median():,.0f}")
print(f"  Mean salary   : ${df_clean['salary_in_usd'].mean():,.0f}")
print(f"  Missing values: {df_clean.isnull().sum().sum()}")

# ── Save ──────────────────────────────────────────────────────────────────────
df_clean.to_csv(OUT_PATH, index=False)
print(f"\nSaved: {OUT_PATH}")
print("Next: run 03_title_grouping.py")

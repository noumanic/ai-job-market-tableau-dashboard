"""
05_feature_engineering.py
=========================
Adds 12 new analytically meaningful columns to the clean dataset,
making it significantly richer for Tableau storytelling.

New columns added (12):
  salary_band          — 6-tier salary bracket label
  salary_quartile      — Q1/Q2/Q3/Q4 label (bottom→top 25%)
  exp_order            — numeric sort key for experience axis (1–4)
  region               — 6-region geographic grouping
  is_us                — 'United States' vs 'Rest of World'
  is_ai_core           — 'AI/ML Core' vs 'Data & Tech'
  year_avg_salary      — average salary for that year (context field)
  salary_vs_year_avg   — $ difference from year's average
  salary_vs_year_avg_pct — % above/below year average
  role_avg_salary      — average salary for that title_group
  salary_vs_role_avg   — $ difference from role average
  salary_vs_role_avg_pct — % above/below role average

Input  : ../data/processed/salaries_clean_final.csv
Output : ../data/processed/salaries_enhanced.csv

Run AFTER 04_summary_stats.py.
"""

import pandas as pd
import numpy as np

IN_PATH  = "../data/processed/salaries_clean_final.csv"
OUT_PATH = "../data/processed/salaries_enhanced.csv"

print("Loading clean data...")
df = pd.read_csv(IN_PATH)
print(f"  Rows: {len(df):,}  |  Columns: {df.shape[1]}")

# ─────────────────────────────────────────────────────────────────────────────
# 1. SALARY BAND — 6 tiers, meaningful for histogram & filter
# ─────────────────────────────────────────────────────────────────────────────
bins   = [0, 60_000, 100_000, 150_000, 200_000, 260_000, 385_001]
labels = ["<$60K", "$60K–$100K", "$100K–$150K", "$150K–$200K", "$200K–$260K", "$260K+"]
df["salary_band"] = pd.cut(df["salary_in_usd"], bins=bins, labels=labels)
print("\n1. salary_band")
print(df["salary_band"].value_counts().sort_index().to_string())

# ─────────────────────────────────────────────────────────────────────────────
# 2. SALARY QUARTILE — bottom/top 25% labels for distribution charts
# ─────────────────────────────────────────────────────────────────────────────
df["salary_quartile"] = pd.qcut(
    df["salary_in_usd"], q=4,
    labels=["Q1 — Bottom 25%", "Q2 — 25–50%", "Q3 — 50–75%", "Q4 — Top 25%"]
)
print("\n2. salary_quartile")
print(df["salary_quartile"].value_counts().sort_index().to_string())

# ─────────────────────────────────────────────────────────────────────────────
# 3. EXP ORDER — numeric sort key so Tableau axes show correct order
# ─────────────────────────────────────────────────────────────────────────────
exp_order_map = {"Entry Level": 1, "Mid Level": 2, "Senior": 3, "Executive": 4}
df["exp_order"] = df["exp_label"].map(exp_order_map)
print("\n3. exp_order — sort key for experience axis")
print(df.groupby(["exp_order", "exp_label"])["salary_in_usd"].mean().round(0).to_string())

# ─────────────────────────────────────────────────────────────────────────────
# 4. REGION — 6-group geographic dimension for regional comparison
# ─────────────────────────────────────────────────────────────────────────────
region_map = {
    # North America
    "US": "North America", "CA": "North America", "MX": "North America",
    # Europe
    "GB": "Europe", "DE": "Europe", "FR": "Europe", "NL": "Europe",
    "ES": "Europe", "IT": "Europe", "PL": "Europe", "AT": "Europe",
    "LT": "Europe", "LV": "Europe", "FI": "Europe", "SE": "Europe",
    "IE": "Europe", "CH": "Europe", "PT": "Europe", "BE": "Europe",
    "DK": "Europe", "NO": "Europe", "GR": "Europe", "CZ": "Europe",
    "HU": "Europe", "RO": "Europe", "SK": "Europe", "HR": "Europe",
    "BG": "Europe", "EE": "Europe", "SI": "Europe", "RS": "Europe",
    "MK": "Europe", "AL": "Europe", "LU": "Europe", "MT": "Europe",
    # Asia Pacific
    "AU": "Asia Pacific", "NZ": "Asia Pacific", "SG": "Asia Pacific",
    "IN": "Asia Pacific", "JP": "Asia Pacific", "CN": "Asia Pacific",
    "KR": "Asia Pacific", "HK": "Asia Pacific", "TH": "Asia Pacific",
    "PH": "Asia Pacific", "MY": "Asia Pacific", "ID": "Asia Pacific",
    "VN": "Asia Pacific", "TW": "Asia Pacific", "PK": "Asia Pacific",
    "BD": "Asia Pacific",
    # Latin America
    "BR": "Latin America", "AR": "Latin America", "CO": "Latin America",
    "CL": "Latin America", "PE": "Latin America", "EC": "Latin America",
    "UY": "Latin America", "BO": "Latin America", "PY": "Latin America",
    "VE": "Latin America",
    # Middle East & Africa
    "EG": "Middle East & Africa", "ZA": "Middle East & Africa",
    "NG": "Middle East & Africa", "KE": "Middle East & Africa",
    "IL": "Middle East & Africa", "TR": "Middle East & Africa",
    "AE": "Middle East & Africa", "SA": "Middle East & Africa",
    "GH": "Middle East & Africa", "ET": "Middle East & Africa",
    "QA": "Middle East & Africa", "OM": "Middle East & Africa",
    "MA": "Middle East & Africa", "TN": "Middle East & Africa",
}
df["region"] = df["company_location"].map(region_map).fillna("Other")
print("\n4. region — 6-group geographic dimension")
print(df.groupby("region")["salary_in_usd"].agg(["mean", "count"]).round(0)
      .sort_values("mean", ascending=False).to_string())

# ─────────────────────────────────────────────────────────────────────────────
# 5. IS_US — US vs Rest of World binary split (90%+ data is US)
# ─────────────────────────────────────────────────────────────────────────────
df["is_us"] = df["company_location"].apply(
    lambda x: "United States" if x == "US" else "Rest of World"
)
print("\n5. is_us — US vs Rest of World")
print(df.groupby("is_us")["salary_in_usd"].agg(["mean", "count"]).round(0).to_string())

# ─────────────────────────────────────────────────────────────────────────────
# 6. IS_AI_CORE — AI/ML core roles vs broader data & tech roles
# ─────────────────────────────────────────────────────────────────────────────
ai_core_roles = {
    "ML Engineer / MLOps", "AI / ML Researcher",
    "Data Scientist", "Research Scientist"
}
df["is_ai_core"] = df["title_group"].apply(
    lambda x: "AI / ML Core" if x in ai_core_roles else "Data & Tech"
)
print("\n6. is_ai_core — AI/ML Core vs Data & Tech")
print(df.groupby("is_ai_core")["salary_in_usd"].agg(["mean", "count"]).round(0).to_string())

# ─────────────────────────────────────────────────────────────────────────────
# 7–9. SALARY vs YEAR AVERAGE — how each record sits relative to its year
# ─────────────────────────────────────────────────────────────────────────────
year_avg = df.groupby("work_year")["salary_in_usd"].mean()
df["year_avg_salary"]        = df["work_year"].map(year_avg).round(0)
df["salary_vs_year_avg"]     = (df["salary_in_usd"] - df["year_avg_salary"]).round(0)
df["salary_vs_year_avg_pct"] = (df["salary_vs_year_avg"] / df["year_avg_salary"] * 100).round(1)
print("\n7–9. salary vs year average ($ and %)")
print(df[["work_year","salary_in_usd","year_avg_salary","salary_vs_year_avg_pct"]].head(3).to_string())

# ─────────────────────────────────────────────────────────────────────────────
# 10–12. SALARY vs ROLE AVERAGE — how each record sits relative to its role
# ─────────────────────────────────────────────────────────────────────────────
role_avg = df.groupby("title_group")["salary_in_usd"].mean()
df["role_avg_salary"]        = df["title_group"].map(role_avg).round(0)
df["salary_vs_role_avg"]     = (df["salary_in_usd"] - df["role_avg_salary"]).round(0)
df["salary_vs_role_avg_pct"] = (df["salary_vs_role_avg"] / df["role_avg_salary"] * 100).round(1)
print("\n10–12. salary vs role average ($ and %)")
print(df[["title_group","salary_in_usd","role_avg_salary","salary_vs_role_avg_pct"]].head(3).to_string())

# ─────────────────────────────────────────────────────────────────────────────
# FINAL VALIDATION
# ─────────────────────────────────────────────────────────────────────────────
new_cols = [
    "salary_band", "salary_quartile", "exp_order",
    "region", "is_us", "is_ai_core",
    "year_avg_salary", "salary_vs_year_avg", "salary_vs_year_avg_pct",
    "role_avg_salary", "salary_vs_role_avg", "salary_vs_role_avg_pct",
]

print(f"\n{'='*55}")
print("VALIDATION — NULL CHECK ON ALL NEW COLUMNS")
print(f"{'='*55}")
print(df[new_cols].isnull().sum().to_string())

print(f"\n{'='*55}")
print("FINAL DATASET SUMMARY")
print(f"{'='*55}")
print(f"  Total rows    : {len(df):,}")
print(f"  Total columns : {df.shape[1]}  (was 15, added {df.shape[1]-15})")
print(f"\nAll columns:")
for i, col in enumerate(df.columns, 1):
    dtype = str(df[col].dtype)
    nuniq = df[col].nunique()
    print(f"  {i:2d}. {col:<30s}  {dtype:<10s}  {nuniq:>6,} unique")

# ─────────────────────────────────────────────────────────────────────────────
# SAVE
# ─────────────────────────────────────────────────────────────────────────────
df.to_csv(OUT_PATH, index=False)
print(f"\nSaved: {OUT_PATH}")
print(f"Shape: {df.shape}")
print("\nThis file is your final Tableau data source.")
print("Connect Tableau directly to: data/processed/salaries_enhanced.csv")

"""
04_summary_stats.py
===================
Generates all KPI numbers, chart data, and annotation values
used in the Tableau dashboard and written proposal.

Input  : ../data/processed/salaries_clean_final.csv
Output : prints to console (reference for building Tableau calculated fields)

Run AFTER 03_title_grouping.py.
"""

import pandas as pd
import numpy as np

PATH = "../data/processed/salaries_clean_final.csv"

df = pd.read_csv(PATH)
print(f"Loaded: {len(df):,} rows, {df.shape[1]} columns\n")

sep = "=" * 55

# ── KPI CARDS (Sheet 6) ───────────────────────────────────────────────────────
print(sep)
print("KPI CARDS")
print(sep)
print(f"  Median salary      : ${df['salary_in_usd'].median():,.0f}")
print(f"  Mean salary        : ${df['salary_in_usd'].mean():,.0f}")
print(f"  Total records      : {len(df):,}")
en_avg = df[df["experience_level"]=="EN"]["salary_in_usd"].mean()
ex_avg = df[df["experience_level"]=="EX"]["salary_in_usd"].mean()
print(f"  EX avg salary      : ${ex_avg:,.0f}")
print(f"  EN avg salary      : ${en_avg:,.0f}")
print(f"  EX / EN ratio      : {ex_avg/en_avg:.2f}x")
remote_pct = (df["work_mode"]=="Remote").mean()*100
onsite_pct = (df["work_mode"]=="On-site").mean()*100
print(f"  Remote %           : {remote_pct:.1f}%")
print(f"  On-site %          : {onsite_pct:.1f}%")

# ── SALARY TREND (Sheet 1) ────────────────────────────────────────────────────
print(f"\n{sep}")
print("SALARY TREND BY YEAR (Sheet 1 — Dual-Axis)")
print(sep)
yt = df.groupby("work_year")["salary_in_usd"].agg(
    avg="mean", median="median", count="count"
).round(0)
print(yt.to_string())

# ── SALARY BY ROLE (Sheet 2) ──────────────────────────────────────────────────
print(f"\n{sep}")
print("SALARY BY ROLE — ALL 15 CATEGORIES (Sheet 2)")
print(sep)
role = df.groupby("title_group")["salary_in_usd"].agg(
    avg="mean", median="median", count="count"
).sort_values("avg", ascending=False).round(0)
print(role.to_string())

# ── WORK MODE SPLIT (Sheet 3) ─────────────────────────────────────────────────
print(f"\n{sep}")
print("WORK MODE SPLIT (Sheet 3 — Donut)")
print(sep)
wm = df["work_mode"].value_counts()
wm_pct = (wm / len(df) * 100).round(1)
for mode in wm.index:
    print(f"  {mode:<10}: {wm[mode]:>7,}  ({wm_pct[mode]:.1f}%)")

# ── TOP COUNTRIES (Sheet 4) ───────────────────────────────────────────────────
print(f"\n{sep}")
print("TOP 15 COUNTRIES BY COUNT (Sheet 4 — Map)")
print(sep)
ct = df.groupby("company_location")["salary_in_usd"].agg(
    avg="mean", count="count"
).sort_values("count", ascending=False).head(15).round(0)
print(ct.to_string())

# ── SALARY VS EXPERIENCE (Sheet 5) ───────────────────────────────────────────
print(f"\n{sep}")
print("SALARY BY EXPERIENCE LEVEL (Sheet 5)")
print(sep)
exp_order = ["Entry Level", "Mid Level", "Senior", "Executive"]
exp = df.groupby("exp_label")["salary_in_usd"].agg(
    avg="mean", median="median", count="count"
).round(0)
print(exp.loc[exp_order].to_string())

# ── REMOTE TREND (Sheet 7 — Bonus) ───────────────────────────────────────────
print(f"\n{sep}")
print("REMOTE WORK TREND BY YEAR % (Sheet 7 — Stacked Bar)")
print(sep)
rt = df.groupby(["work_year", "work_mode"]).size().unstack(fill_value=0)
print((rt.div(rt.sum(axis=1), axis=0) * 100).round(1).to_string())

# ── COMPANY SIZE (Dual-Axis bonus) ────────────────────────────────────────────
print(f"\n{sep}")
print("SALARY BY COMPANY SIZE")
print(sep)
sz = df.groupby("size_label")["salary_in_usd"].agg(
    avg="mean", count="count"
).round(0)
print(sz.to_string())

# ── ANNOTATION VALUES ─────────────────────────────────────────────────────────
print(f"\n{sep}")
print("ANNOTATION VALUES (copy into Tableau annotations)")
print(sep)
med_2022 = df[df["work_year"]==2022]["salary_in_usd"].median()
med_2024 = df[df["work_year"]==2024]["salary_in_usd"].median()
pct_change = (med_2024 - med_2022)/med_2022*100
print(f"  Salary Trend   : Median grew from ${med_2022:,.0f} (2022) to ${med_2024:,.0f} (2024) — {pct_change:.0f}% increase")
remote_2022 = (df[df["work_year"]==2022]["work_mode"]=="Remote").mean()*100
remote_2025 = (df[df["work_year"]==2025]["work_mode"]=="Remote").mean()*100
print(f"  Remote Trend   : Remote peaked at {remote_2022:.0f}% in 2022 → fell to {remote_2025:.0f}% in 2025")
print(f"  Exp Gap        : Executive earns {ex_avg/en_avg:.2f}x entry level — ${ex_avg:,.0f} vs ${en_avg:,.0f}")
us_count = (df["company_location"]=="US").sum()
us_pct = us_count/len(df)*100
us_avg = df[df["company_location"]=="US"]["salary_in_usd"].mean()
print(f"  Map            : US leads with {us_count:,} submissions ({us_pct:.0f}%) — avg ${us_avg:,.0f}")
top_role = role.index[0]
top_avg = role.iloc[0]["avg"]
bottom_role = "Data Analyst"
bottom_avg = role.loc["Data Analyst","avg"]
pct_diff = (top_avg - bottom_avg)/bottom_avg*100
print(f"  Salary by Role : {top_role} tops at ${top_avg:,.0f} — {pct_diff:.0f}% above {bottom_role}")

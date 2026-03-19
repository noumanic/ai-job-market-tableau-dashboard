"""
01_explore.py
=============
Initial exploratory data analysis of the raw aijobs.net salary dataset.
Run this first before any cleaning to understand the raw data.

Output: prints to console — no files written.
"""

import pandas as pd
import numpy as np

RAW_PATH = "../data/raw/salaries.csv"

df = pd.read_csv(RAW_PATH)

print("=" * 60)
print("SHAPE & COLUMNS")
print("=" * 60)
print(f"Rows: {len(df):,}")
print(f"Columns: {df.shape[1]}")
print(f"\nColumn names: {df.columns.tolist()}")

print("\n" + "=" * 60)
print("DTYPES")
print("=" * 60)
print(df.dtypes)

print("\n" + "=" * 60)
print("MISSING VALUES")
print("=" * 60)
print(df.isnull().sum())

print("\n" + "=" * 60)
print("FIRST 5 ROWS")
print("=" * 60)
print(df.head().to_string())

print("\n" + "=" * 60)
print("SALARY DISTRIBUTION (salary_in_usd)")
print("=" * 60)
print(df["salary_in_usd"].describe().round(0))
print(f"Skewness : {df['salary_in_usd'].skew():.3f}")
print(f"Kurtosis : {df['salary_in_usd'].kurtosis():.3f}")
print(f"Records > $500K : {(df['salary_in_usd'] > 500000).sum()}")
print(f"Records < $20K  : {(df['salary_in_usd'] < 20000).sum()}")

print("\n" + "=" * 60)
print("YEAR DISTRIBUTION")
print("=" * 60)
print(df["work_year"].value_counts().sort_index())

print("\n" + "=" * 60)
print("EXPERIENCE LEVEL")
print("=" * 60)
print(df["experience_level"].value_counts())

print("\n" + "=" * 60)
print("EMPLOYMENT TYPE")
print("=" * 60)
print(df["employment_type"].value_counts())

print("\n" + "=" * 60)
print("COMPANY SIZE")
print("=" * 60)
print(df["company_size"].value_counts())

print("\n" + "=" * 60)
print("REMOTE RATIO")
print("=" * 60)
print(df["remote_ratio"].value_counts().sort_index())

print("\n" + "=" * 60)
print("CURRENCY DISTRIBUTION (top 10)")
print("=" * 60)
print(df["salary_currency"].value_counts().head(10))

print("\n" + "=" * 60)
print("TOP 10 COUNTRIES (company_location)")
print("=" * 60)
print(df["company_location"].value_counts().head(10))
print(f"Total unique countries: {df['company_location'].nunique()}")

print("\n" + "=" * 60)
print("JOB TITLES")
print("=" * 60)
print(f"Total unique titles: {df['job_title'].nunique()}")
print("\nTop 20 by count:")
print(df["job_title"].value_counts().head(20))

print("\n" + "=" * 60)
print("SALARY BY EXPERIENCE LEVEL")
print("=" * 60)
print(df.groupby("experience_level")["salary_in_usd"]
      .agg(["mean", "median", "count"]).round(0))

print("\n" + "=" * 60)
print("SALARY BY YEAR")
print("=" * 60)
print(df.groupby("work_year")["salary_in_usd"]
      .agg(["mean", "median", "count"]).round(0))

print("\n" + "=" * 60)
print("REMOTE TREND BY YEAR (%)")
print("=" * 60)
remote_yr = df.groupby(["work_year", "remote_ratio"]).size().unstack(fill_value=0)
print((remote_yr.div(remote_yr.sum(axis=1), axis=0) * 100).round(1))

# AI Job Market Intelligence
### Salaries, Roles & Global Hiring Trends (2020–2025)

> **CS3012 Fundamentals of Data Visualization** · Group 8 · FAST-NUCES Islamabad · Spring 2026
> Submitted to Dr. Atif Mughees

Interactive Tableau dashboard built on **147,348 real salary submissions** from aijobs.net and foorilla.com, visualizing AI/ML/Data Science compensation trends, the remote work collapse (53% in 2022 to 20% in 2025), salary progression across career levels, and global hiring patterns across 87 countries from 2022 to 2025.

---

## Live Links

| Resource | URL |
|----------|-----|
| Tableau Public Dashboard | *(link after publish — Week 7)* |
| Project Repository | https://github.com/noumanic/ai-job-market-analytics |
| Dataset — GitHub (source) | https://github.com/foorilla/ai-jobs-net-salaries |
| Dataset — Kaggle (official aijobs account) | https://www.kaggle.com/datasets/aijobs/global-salaries-in-ai-ml-data-science |
| Live Job Platform | https://aijobs.net |
| Parent Platform | https://foorilla.com |

---

## Group Members

| # | Name | Roll Number |
|---|------|-------------|
| 1 | Muhammad Nouman Hafeez | 21i-0416 |
| 2 | Muhammad Asim | 21i-0852 |
| 3 | Sara Jabeen | 21i-0623 |

---

## Project Overview

This project is the final deliverable for CS3012 Fundamentals of Data Visualization. It uses a real, crowdsourced salary dataset published under CC0 Public Domain by aijobs.net to build an interactive Tableau dashboard that answers five core questions:

- Which AI/ML/Data Science roles pay the most?
- How does salary grow from Entry Level to Executive?
- How has remote work changed year over year from 2022 to 2025?
- Which countries lead global AI hiring, and how do salaries differ by region?
- What does the salary distribution look like across pay bands and quartiles?

---

## Dataset

### Source

| Field | Details |
|-------|---------|
| Dataset Name | Global Salaries in AI, ML, Data Science and Big Data |
| Primary Source | aijobs.net — anonymous professional salary survey and live job listings |
| Parent Platform | foorilla.com — real-time job aggregation and analytics |
| Repository | github.com/foorilla/ai-jobs-net-salaries |
| Kaggle (official) | kaggle.com/datasets/aijobs/global-salaries-in-ai-ml-data-science |
| File | salaries.csv |
| Raw rows | 151,445 |
| Raw columns | 11 |
| Time period | 2020 to 2025 |
| Update frequency | Weekly |
| License | CC0 1.0 Public Domain — no restrictions |

### Why This Dataset Is Real

The Kaggle page is published under the `aijobs` account — the same organization that owns the platform — confirming it is a first-party release, not a third-party re-upload. Real-world indicators include: the United States dominates with 90% of submissions as expected in a real tech labor market, salary distributions are right-skewed (skewness = 1.35), full-time employment is 99.4% of entries, and 406 unique raw job title variants reflect genuine naming variation rather than a clean synthetic list.

---

## Key Findings

| Metric | Value |
|--------|-------|
| Median salary (clean dataset) | $147,000 |
| Mean salary | $156,237 |
| Total records after preprocessing | 147,348 |
| Salary range after outlier removal | $37,974 to $385,000 |
| Entry Level average | $102,743 |
| Mid Level average | $140,382 |
| Senior average | $170,351 |
| Executive average | $195,935 |
| EX / EN ratio | 1.91x |
| Top paying role | ML Engineer / MLOps at $194,303 avg |
| Remote work in 2022 | 53.5% |
| Remote work in 2025 | 20.3% |
| US share of all submissions | 90.4% |
| US average salary | $161,381 |
| Rest of World average salary | $108,024 |
| AI/ML Core roles average | $171,009 |
| Data and Tech roles average | $150,685 |

### Salary Growth by Year

| Year | Average | Median | Record Count |
|------|---------|--------|--------------|
| 2022 | $138,188 | $135,000 | 1,587 |
| 2023 | $154,304 | $145,900 | 8,423 |
| 2024 | $158,107 | $149,000 | 60,914 |
| 2025 | $155,334 | $146,000 | 76,424 |

### Remote Work Trend

| Year | On-site | Remote | Hybrid |
|------|---------|--------|--------|
| 2022 | 43.5% | 53.5% | 3.0% |
| 2023 | 68.2% | 31.2% | 0.6% |
| 2024 | 80.9% | 19.1% | 0.1% |
| 2025 | 79.6% | 20.3% | 0.0% |

---

## Preprocessing Pipeline

All preprocessing is done in Python. No synthetic data was added at any stage. Every row in the final output file is a real salary submission.

### Stage 1 — Cleaning (`02_clean.py`)

| Step | Action | Rows Before | Rows After | Removed |
|------|--------|-------------|------------|---------|
| 1 | Keep Full-Time (FT) only | 151,445 | 150,541 | 904 |
| 2 | Keep 2022 to 2025 only | 150,541 | 150,264 | 277 |
| 3 | Remove outliers (1st to 99th percentile) | 150,264 | 147,348 | 2,916 |

Outlier bounds: $37,974 lower to $385,000 upper

### Stage 2 — Label Columns (`03_title_grouping.py`)

Four readable label columns added. Row count unchanged.

| New Column | Technique | Example |
|------------|-----------|---------|
| `title_group` | Keyword string matching — 406 raw titles mapped to 15 categories | "ML Eng." maps to "ML Engineer / MLOps" |
| `work_mode` | Dictionary mapping | 0 maps to "On-site", 50 to "Hybrid", 100 to "Remote" |
| `exp_label` | Dictionary mapping | "EN" maps to "Entry Level", "EX" to "Executive" |
| `size_label` | Dictionary mapping | "S" maps to "Small", "M" to "Medium", "L" to "Large" |

### Stage 3 — Feature Engineering (`05_feature_engineering.py`)

Twelve analytically derived columns added using four techniques. Row count unchanged at 147,348. No synthetic data.

| Column | Technique | What It Enables in Tableau |
|--------|-----------|---------------------------|
| `salary_band` | Fixed-width binning (pd.cut) | Color encode by pay tier, salary tier filter |
| `salary_quartile` | Quantile binning (pd.qcut) | Color encode relative position Q1 through Q4 |
| `exp_order` | Ordinal encoding via dict map | Fixes experience axis sort order in Tableau |
| `region` | Dictionary lookup — 87 ISO codes to 6 regions | Regional salary comparison chart |
| `is_us` | Binary flag via lambda | United States vs Rest of World split |
| `is_ai_core` | Set membership via lambda | AI/ML Core vs Data and Tech comparison |
| `year_avg_salary` | GroupBy aggregation + merge back | Reference line on trend chart, tooltip context |
| `salary_vs_year_avg` | Arithmetic subtraction | Dollar gap from year average in tooltip |
| `salary_vs_year_avg_pct` | Percentage calculation | Color encode above or below year average |
| `role_avg_salary` | GroupBy aggregation + merge back | Reference line per role on bar chart |
| `salary_vs_role_avg` | Arithmetic subtraction | Dollar gap from role average in tooltip |
| `salary_vs_role_avg_pct` | Percentage calculation | Green/red color encode on scatter plot |

Full documentation with Python code, worked examples, and output tables:
`docs/preprocessing_documentation.docx`

### Final Dataset — `salaries_enhanced.csv`

| Property | Value |
|----------|-------|
| Rows | 147,348 |
| Columns | 27 (11 original + 4 label + 12 engineered) |
| Missing values | 0 |
| Salary range | $37,974 to $385,000 |
| Years covered | 2022, 2023, 2024, 2025 |
| Countries | 87 |
| Unique role categories | 15 |

**Connect Tableau to this file: `data/processed/salaries_enhanced.csv`**

---

## Dashboard

### Sheets

| Sheet | Chart Type | Key Columns Used |
|-------|-----------|-----------------|
| 1 — Salary Trend | Dual-Axis Line + Bar | `work_year`, `salary_in_usd` (avg + median + count) |
| 2 — Salary by Role | Horizontal Bar + Parameter | `title_group`, `salary_in_usd` |
| 3 — Work Mode Split | Donut | `work_mode` |
| 4 — Global Hiring Map | Choropleth | `company_location`, `salary_in_usd` |
| 5 — Salary vs Experience | Bar + Line Overlay | `exp_label`, `exp_order`, `salary_in_usd` |
| 6 — KPI Cards | Text Tiles | Multiple aggregated measures |
| 7 — Remote Work Trend | 100% Stacked Bar (Bonus) | `work_year`, `work_mode` |

### Bonus Features

| Feature | Implementation |
|---------|---------------|
| Dual-axis chart | Submission count as bar on secondary axis, avg salary as line on primary axis |
| Global filters | Year, Experience Level, Company Size, Employment Type applied to all sheets |
| Highlight actions | Click any mark to highlight related records across all other sheets |
| Parameter toggle | Top 5, Top 10, or All 15 roles on the salary bar chart |
| 5 story annotations | Key callouts placed on Sheets 1, 2, 3, 4, and 5 |

### Canvas

1200 x 900 px fixed. Primary color: navy #003875. Accent: sky blue #378ADD.

See `tableau/TABLEAU_NOTES.md` for all calculated fields, parameters, filter action setup, and step-by-step build instructions for every sheet.

---

## Repository Structure

```
ai-job-market-tableau-dashboard/
|
+-- data/
|   +-- raw/
|   |   +-- salaries.csv                     # original download — do not modify
|   |   +-- DATA_SOURCE.md                   # all source URLs and column reference
|   |
|   +-- processed/
|       +-- salaries_clean_final.csv          # 147,348 rows x 15 cols — cleaned + labels
|       +-- salaries_enhanced.csv             # 147,348 rows x 27 cols — final Tableau source
|
+-- preprocessing/
|   +-- 01_explore.py                         # EDA: shape, nulls, distributions, skewness
|   +-- 02_clean.py                           # FT filter + year filter + outlier removal
|   +-- 03_title_grouping.py                  # 406 raw titles mapped to 15 categories
|   +-- 04_summary_stats.py                   # all KPI numbers for dashboard and proposal
|   +-- 05_feature_engineering.py             # 12 derived columns via 4 techniques
|   +-- requirements.txt                      # pandas, numpy, scipy
|
+-- tableau/
|   +-- ai_job_market_dashboard.twbx          # packaged workbook — added Week 5
|   +-- TABLEAU_NOTES.md                      # calculated fields, parameters, actions
|
+-- docs/
|   +-- Group8_CS3012_ProjectProposal_
|   |   AI_Job_Market_Intelligence_
|   |   Spring2026.pdf                        # submitted project proposal
|   +-- proposal_final.tex                    # LaTeX source for proposal
|   +-- preprocessing_documentation.docx      # full preprocessing + feature engineering doc
|   +-- preprocessing_documentation.pdf       # PDF version of above
|   +-- dashboard_screenshot.png              # added Week 7
|   +-- written_summary.pdf                   # added Week 7
|
+-- recordings/
|   +-- RECORDING_LINK.md                     # Loom walkthrough URL — added Week 7
|
+-- assets/
|   +-- pic1_foorilla_hiring.png              # platform source verification screenshot
|   +-- pic2_foorilla_media.png
|   +-- pic3_foorilla_insight.png
|   +-- pic4_aijobs_search.png
|
+-- .gitignore
+-- LICENSE
+-- README.md
```

---

## How to Run Preprocessing

```bash
cd preprocessing
pip install -r requirements.txt

python 01_explore.py                # explore raw data — prints to console, no output file
python 02_clean.py                  # output: data/processed/salaries_clean_final.csv
python 03_title_grouping.py         # output: data/processed/salaries_clean_final.csv (updated)
python 04_summary_stats.py          # prints all KPI numbers — no output file
python 05_feature_engineering.py    # output: data/processed/salaries_enhanced.csv
```

---

## Complete Column Reference — salaries_enhanced.csv

| # | Column | Type | Origin | Tableau Use |
|---|--------|------|--------|-------------|
| 1 | `work_year` | int | raw | Time axis on salary trend chart |
| 2 | `experience_level` | str | raw | Reference only — use `exp_label` for display |
| 3 | `employment_type` | str | raw | Constant FT — exclude from all charts |
| 4 | `job_title` | str | raw | Tooltips only — 406 unique raw title values |
| 5 | `salary` | int | raw | Local currency — do not use for analysis |
| 6 | `salary_currency` | str | raw | Filter reference only |
| 7 | `salary_in_usd` | int | raw | Primary measure — use on every sheet |
| 8 | `employee_residence` | str | raw | Country of employee — geographic filter |
| 9 | `remote_ratio` | int | raw | 0/50/100 numeric — use `work_mode` for display |
| 10 | `company_location` | str | raw | ISO 2-letter code — geographic role for map |
| 11 | `company_size` | str | raw | S/M/L codes — use `size_label` for display |
| 12 | `title_group` | str | label | Bar chart axis — 15 standardized role categories |
| 13 | `work_mode` | str | label | Donut chart and stacked bar sheet |
| 14 | `exp_label` | str | label | Experience axis label — 4 career levels |
| 15 | `size_label` | str | label | Company size filter and dual-axis comparison |
| 16 | `salary_band` | category | engineered | Color encode pay tier, salary tier filter dropdown |
| 17 | `salary_quartile` | category | engineered | Color encode relative position Q1 through Q4 |
| 18 | `exp_order` | int | engineered | Drag to Sort field to fix axis order in Tableau |
| 19 | `region` | str | engineered | Regional salary comparison bar chart |
| 20 | `is_us` | str | engineered | United States vs Rest of World toggle |
| 21 | `is_ai_core` | str | engineered | AI/ML Core vs Data and Tech salary comparison |
| 22 | `year_avg_salary` | float | engineered | Reference line value on trend chart tooltip |
| 23 | `salary_vs_year_avg` | float | engineered | Dollar deviation from year average in tooltip |
| 24 | `salary_vs_year_avg_pct` | float | engineered | Percentage above or below year average |
| 25 | `role_avg_salary` | float | engineered | Reference line per role on bar chart |
| 26 | `salary_vs_role_avg` | float | engineered | Dollar deviation from role average in tooltip |
| 27 | `salary_vs_role_avg_pct` | float | engineered | Percentage above or below role average |

---

## Project Deliverables

| Deliverable | Status | Location |
|-------------|--------|----------|
| Project Proposal (PDF) | Done | `docs/` |
| Project Proposal (LaTeX source) | Done | `docs/` |
| Preprocessing Documentation (Word + PDF) | Done | `docs/` |
| Raw Dataset | Done | `data/raw/` |
| Clean Dataset (15 cols) | Done | `data/processed/` |
| Enhanced Dataset (27 cols) | Done | `data/processed/` |
| Preprocessing Scripts (5 scripts) | Done | `preprocessing/` |
| Tableau Notes and Calculated Fields | Done | `tableau/` |
| Tableau Dashboard (.twbx) | Week 5 | `tableau/` |
| Dashboard Screenshot | Week 7 | `docs/` |
| Written Summary Report | Week 7 | `docs/` |
| Video Walkthrough (Loom) | Week 7 | `recordings/` |

---

---

## Dataset License

The aijobs.net salary dataset is published under **CC0 1.0 Public Domain**.
No restrictions on use, modification, or distribution.
Attribution appreciated: https://aijobs.net/salaries

---

*FAST-NUCES Islamabad · CS3012 Data Visualization · Spring 2026*
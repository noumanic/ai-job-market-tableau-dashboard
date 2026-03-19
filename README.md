# AI Job Market Intelligence: Salaries, Roles & Global Hiring Trends (2020–2025)

> CS3012 Fundamentals of Data Visualization · Group 8 · FAST-NUCES Islamabad · Spring 2026  
> Submitted to Dr. Atif Mughees

Interactive Tableau dashboard built on **147,348 real salary submissions** from aijobs.net,
visualizing AI/ML/Data Science compensation trends, remote work collapse (53% → 20%), and
global hiring patterns across 87 countries from 2022 to 2025.

---

## Live Links

| Resource | URL |
|----------|-----|
| Tableau Public Dashboard | *(link after publish)* |
| Dataset — GitHub (source) | https://github.com/foorilla/ai-jobs-net-salaries |
| Dataset — Kaggle (official) | https://www.kaggle.com/datasets/aijobs/global-salaries-in-ai-ml-data-science |
| Platform | https://aijobs.net · https://foorilla.com |

---

## Group Members

| # | Name | Roll Number |
|---|------|-------------|
| 1 | Muhammad Nouman Hafeez | 21i-0416 |
| 2 | Muhammad Asim | 21i-0852 |
| 3 | Sara Jabeen | 21i-0623 |

---

## Key Findings

| Metric | Value |
|--------|-------|
| Median salary (clean dataset) | $147,000 |
| Mean salary | $156,237 |
| Total records (after preprocessing) | 147,348 |
| Remote work 2022 | 53.5% |
| Remote work 2025 | 20.3% |
| Entry Level avg | $102,743 |
| Executive avg | $195,935 |
| EX / EN ratio | 1.91× |
| Top paying role | ML Engineer / MLOps — $194,303 avg |
| US share of data | 90.4% |

---

## Dashboard Sheets

| Sheet | Chart Type | Description |
|-------|-----------|-------------|
| 1 — Salary Trend | Dual-Axis Line + Bar | Avg & median salary by year (2020–2025) with submission count |
| 2 — Salary by Role | Horizontal Bar | 15 job categories ranked by avg salary · parameter toggle Top 5/10/All |
| 3 — Work Mode Split | Donut | On-site / Remote / Hybrid share |
| 4 — Global Hiring Map | Choropleth | Avg salary + submission count by country (87 countries) |
| 5 — Salary vs Experience | Bar + Line overlay | EN / MI / SE / EX avg & median comparison |
| 6 — KPI Cards | Text/Number tiles | Median, Mean, Total Records, Remote %, EX/EN Ratio |
| 7 — Remote Trend (Bonus) | 100% Stacked Bar | On-site vs Remote vs Hybrid share per year 2022–2025 |

**Bonus features:** Dual-axis chart · Global filters (Year, Experience, Size, Employment Type) ·
Highlight actions · Parameter toggle (Top 5/10/All roles) · Custom tooltips · 5 annotations

---

## Preprocessing Summary

| Step | Action | Rows Before | Rows After |
|------|--------|-------------|------------|
| 1 | Keep Full-Time (FT) only | 151,445 | 150,541 |
| 2 | Keep 2022–2025 (data density) | 150,541 | 150,264 |
| 3 | Remove outliers (1st–99th pct) | 150,264 | 147,348 |
| 4 | Add `title_group` column | 147,348 | 147,348 |
| 5 | Add `work_mode`, `exp_label`, `size_label` | 147,348 | 147,348 |

Outlier bounds: $37,974 — $385,000

---

## Repo Structure

```
ai-job-market-tableau-dashboard/
├── data/
│   ├── raw/
│   │   ├── salaries.csv               # original — do not modify
│   │   └── DATA_SOURCE.md             # all 3 source URLs documented
│   └── processed/
│       └── salaries_clean_final.csv   # 147,348 rows · 15 columns · Tableau-ready
├── preprocessing/
│   ├── 01_explore.py                  # EDA — shape, nulls, distributions
│   ├── 02_clean.py                    # FT filter + year filter + outlier removal
│   ├── 03_title_grouping.py           # 406 titles → 15 categories
│   ├── 04_summary_stats.py            # KPI numbers for dashboard & proposal
│   └── requirements.txt
├── tableau/
│   ├── ai_job_market_dashboard.twbx   # packaged workbook (data embedded)
│   └── TABLEAU_NOTES.md               # calculated fields, parameters, filter actions
├── docs/
│   ├── Group8_CS3012_ProjectProposal_AI_Job_Market_Intelligence_Spring2026.pdf
│   ├── proposal_final.tex
│   ├── dashboard_screenshot.png
│   └── written_summary.pdf            # added Week 7
├── recordings/
│   └── RECORDING_LINK.md              # Loom walkthrough URL
├── assets/
│   ├── pic1_foorilla_hiring.png
│   ├── pic2_foorilla_media.png
│   ├── pic3_foorilla_insight.png
│   └── pic4_aijobs_search.png
├── .gitignore
├── LICENSE
└── README.md
```

---

## How to Run Preprocessing

```bash
cd preprocessing
pip install -r requirements.txt
python 01_explore.py
python 02_clean.py
python 03_title_grouping.py
python 04_summary_stats.py
```

Output: `data/processed/salaries_clean_final.csv`

---

## Dataset License

The aijobs.net salary dataset is published under **CC0 1.0 Public Domain**.
No restrictions on use, modification, or distribution.

---

*FAST-NUCES Islamabad · CS3012 Data Visualization · Spring 2026*

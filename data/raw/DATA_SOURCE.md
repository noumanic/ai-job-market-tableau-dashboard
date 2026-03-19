# Dataset Sources

## Primary Dataset

**Name:** Global Salaries in AI, ML, Data Science & Big Data  
**Collected by:** aijobs.net / foorilla.com  
**License:** CC0 1.0 Public Domain — no restrictions on use

| Access Point | URL |
|--------------|-----|
| GitHub (raw CSV, weekly updated) | https://github.com/foorilla/ai-jobs-net-salaries |
| Kaggle (official aijobs account) | https://www.kaggle.com/datasets/aijobs/global-salaries-in-ai-ml-data-science |
| Live salary survey | https://aijobs.net/salaries |
| Parent platform | https://foorilla.com |

## File Used

`salaries.csv` — downloaded March 2026  
151,445 rows · 11 columns · 2020–2025

## Columns

| Column | Type | Description |
|--------|------|-------------|
| work_year | int | Year salary was reported (2020–2025) |
| experience_level | str | EN / MI / SE / EX |
| employment_type | str | FT / PT / CT / FL |
| job_title | str | Raw job title (406 unique in clean set) |
| salary | int | Original salary in local currency |
| salary_currency | str | ISO currency code |
| salary_in_usd | int | Salary standardized to USD |
| employee_residence | str | Country of employee (ISO 2-letter) |
| remote_ratio | int | 0 = On-site, 50 = Hybrid, 100 = Remote |
| company_location | str | Country of company (ISO 2-letter) |
| company_size | str | S / M / L |

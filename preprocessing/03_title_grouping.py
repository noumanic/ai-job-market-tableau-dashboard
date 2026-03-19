"""
03_title_grouping.py
====================
Maps 406 raw job title strings to 15 standardized categories
using keyword matching. Also adds human-readable label columns
for experience, remote ratio, and company size.

Input  : ../data/processed/salaries_clean.csv
Output : ../data/processed/salaries_clean_final.csv  (Tableau-ready)

New columns added:
  title_group  — 15 standardized role categories
  work_mode    — 'On-site' / 'Hybrid' / 'Remote'
  exp_label    — 'Entry Level' / 'Mid Level' / 'Senior' / 'Executive'
  size_label   — 'Small' / 'Medium' / 'Large'

Run AFTER 02_clean.py.
"""

import pandas as pd

IN_PATH  = "../data/processed/salaries_clean.csv"
OUT_PATH = "../data/processed/salaries_clean_final.csv"

# ── Title grouping function ───────────────────────────────────────────────────
def group_title(title: str) -> str:
    """Map a raw job title string to one of 15 standard categories."""
    t = title.lower()

    if any(x in t for x in [
        "data scientist", "data science", "applied scientist", "applied data"
    ]):
        return "Data Scientist"

    elif any(x in t for x in [
        "data engineer", "data engineering", "etl", "dataops", "data pipeline",
        "data infrastructure", "data integration", "data platform",
        "data ops", "big data engineer", "big data dev"
    ]):
        return "Data Engineer"

    elif any(x in t for x in [
        "machine learning engineer", "ml engineer", "ml ops", "mlops",
        "ml infrastructure", "ml platform", "machine learning model",
        "machine learning software", "machine learning quality",
        "machine learning performance", "machine learning modeler",
        "machine learning lead", "ml scientist", "machine learning dev",
        "machine learning tech", "lead machine learning"
    ]):
        return "ML Engineer / MLOps"

    elif any(x in t for x in [
        "software engineer", "software developer", "software development",
        "software architect", "full stack", "fullstack", "backend engineer",
        "backend dev", "frontend engineer", "platform engineer", "devops",
        "site reliability", "sre", "systems engineer", "system engineer",
        "cloud engineer", "python dev", "java dev", "backend software"
    ]):
        return "Software Engineer"

    elif any(x in t for x in [
        "data analyst", "analytics analyst", "bi analyst",
        "data reporting", "data analysis", "data and reporting",
        "data viz", "data visualization analyst", "data visualization spec",
        "reporting analyst", "insight analyst", "marketing analyst",
        "financial data analyst", "marketing data analyst",
        "product data analyst", "people data analyst",
        "business intelligence analyst", "compliance data analyst",
        "sales data analyst", "crm data analyst", "fraud data analyst",
        "marketing data analyst", "research data analyst",
        "bi data analyst", "admin & data analyst"
    ]):
        return "Data Analyst"

    elif any(x in t for x in [
        "ai engineer", "ai developer", "ai architect", "ai researcher",
        "ai scientist", "ai specialist", "ai research", "ai software",
        "ai product", "ai solution", "ai tech", "ai machine",
        "artificial intelligence", "genai", "llm engineer", "prompt engineer",
        "deep learning", "computer vision", "nlp engineer",
        "robotics", "autonomous", "conversational ai"
    ]):
        return "AI / ML Researcher"

    elif any(x in t for x in [
        "analytics engineer", "bi engineer", "bi developer",
        "business intelligence engineer", "business intelligence dev",
        "power bi", "tableau dev", "bi & data", "databricks"
    ]):
        return "Analytics Engineer"

    elif any(x in t for x in [
        "research scientist", "research engineer", "principal researcher",
        "applied research", "postdoc", "researcher", "research associate",
        "research fellow", "research professional", "computational",
        "bioinform", "statistician", "quantitative", "actuary",
        "research team lead", "research specialist", "research assistant"
    ]):
        return "Research Scientist"

    elif any(x in t for x in [
        "head of", "director", "vp of", "chief",
        "engineering manager", "machine learning manager", "data manager",
        "analytics manager", "data analytics manager", "data lead",
        "analytics lead", "lead data", "staff data", "staff machine",
        "data strategy", "manager data"
    ]):
        return "Manager / Director"

    elif any(x in t for x in [
        "data architect", "solutions architect", "solution architect",
        "architect", "data modeler", "data model"
    ]):
        return "Data Architect"

    elif any(x in t for x in [
        "product manager", "product lead", "product owner",
        "product analyst", "product spec", "data product", "product designer"
    ]):
        return "Product Manager"

    elif any(x in t for x in [
        "data governance", "master data", "data quality", "data steward",
        "data integrity", "data management", "data operations",
        "data specialist", "data team", "data compliance",
        "data and reporting professional", "encounter data"
    ]):
        return "Data Governance & Ops"

    elif any(x in t for x in [
        "consultant", "specialist", "advisor", "account exec",
        "sales engineer", "sales development", "business analyst",
        "business development", "customer success", "technical recruiter",
        "technical writer", "technical support", "technical specialist",
        "forward deployed", "solution specialist", "developer advocate"
    ]):
        return "Consultant / Analyst"

    else:
        return "Other"


# ── Load & process ────────────────────────────────────────────────────────────
print("Loading cleaned data...")
df = pd.read_csv(IN_PATH)
print(f"  Rows: {len(df):,}")

# Add title_group
df["title_group"] = df["job_title"].apply(group_title)

# Add readable labels
df["work_mode"]  = df["remote_ratio"].map({0: "On-site", 50: "Hybrid", 100: "Remote"})
df["exp_label"]  = df["experience_level"].map(
    {"EN": "Entry Level", "MI": "Mid Level", "SE": "Senior", "EX": "Executive"}
)
df["size_label"] = df["company_size"].map({"S": "Small", "M": "Medium", "L": "Large"})

# ── Verify ────────────────────────────────────────────────────────────────────
print(f"\nTitle group distribution:")
print(df["title_group"].value_counts().to_string())

print(f"\nMissing values in new columns:")
new_cols = ["title_group", "work_mode", "exp_label", "size_label"]
print(df[new_cols].isnull().sum())

print(f"\nFinal columns ({df.shape[1]}):")
print(df.columns.tolist())

# ── Save ──────────────────────────────────────────────────────────────────────
df.to_csv(OUT_PATH, index=False)
print(f"\nSaved: {OUT_PATH}")
print(f"Final shape: {df.shape}")
print("Next: run 04_summary_stats.py")

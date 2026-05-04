# AI Job Market Intelligence — Full Tableau Build Plan

**Project:** CS3012 Fundamentals of Data Visualization · Group 8 · FAST-NUCES Islamabad · Spring 2026
**Dataset:** `data/processed/salaries_enhanced.csv` — 147,348 rows × 27 columns
**Target deliverable:** `tableau/ai_job_market_dashboard.twbx` — 7 sheets + 5 KPI tiles + 1 master dashboard at 1200×900 px

This is the single, end-to-end build guide. Work top-to-bottom; every section is a checklist you can tick off.

---

## Table of Contents

1. [Project at a glance](#1-project-at-a-glance)
2. [Tableau Desktop setup](#2-tableau-desktop-setup-one-time-10-min)
3. [Calculated fields & parameters](#3-calculated-fields-and-parameters-build-before-any-sheet)
4. [Global filters](#4-global-filters-configure-once-apply-to-all-sheets)
5. [Color theme](#5-color-theme-set-once-via-format--workbook)
6. [Sheet-by-sheet build](#6-sheet-by-sheet-build)
   - [Sheet 1 — Salary Trend](#sheet-1--salary-trend-20222025-dual-axis-line--bar)
   - [Sheet 2 — Salary by Role](#sheet-2--salary-by-role-horizontal-bar--top-n-parameter)
   - [Sheet 3 — Work Mode Donut](#sheet-3--work-mode-split-donut)
   - [Sheet 4 — Global Hiring Map](#sheet-4--global-hiring-map-choropleth)
   - [Sheet 5 — Salary vs Experience](#sheet-5--salary-vs-experience-bar--line-overlay)
   - [Sheet 6 — KPI Cards](#sheet-6--kpi-cards-5-separate-tile-sheets)
   - [Sheet 7 — Remote Work Trend](#sheet-7--remote-work-trend-100-stacked-bar--bonus)
7. [Master dashboard assembly](#7-master-dashboard-assembly)
8. [Final dashboard mock](#8-final-dashboard-mock--what-the-user-will-see)
9. [Verification checklist](#9-verification-checklist-before-submitting)
10. [Build order & time budget](#10-suggested-build-order-one-focused-session-34-hours)
11. [Troubleshooting cheat sheet](#11-troubleshooting-cheat-sheet)

---

## 1. Project at a glance

### What is already done (do NOT redo)

| Asset | Location |
|---|---|
| Raw CSV (151,445 rows) | `data/raw/salaries.csv` |
| Cleaning + outlier removal | `preprocessing/02_clean.py` |
| Title grouping → 15 categories | `preprocessing/03_title_grouping.py` |
| 12 engineered columns | `preprocessing/05_feature_engineering.py` |
| Final Tableau-ready CSV | `data/processed/salaries_enhanced.csv` (147,348 × 27) |
| EDA reference PNGs | `notebooks/figures/01–20.png` |
| Summary CSVs | `notebooks/outputs/summary_*.csv` |
| Project proposal & docs | `docs/` |

### What this plan covers

- Tableau Desktop build only — no further data engineering needed
- All 7 analytical sheets + 5 KPI tile sheets
- All 9 calculated fields and 1 parameter
- 3 global filters + filter & highlight actions
- 5 story annotations
- The 1200×900 master dashboard

### Authoritative data source note

The README and `TABLEAU_NOTES.md` disagree on which CSV to use. **Use `salaries_enhanced.csv` (27 cols)** — the seven sheets need engineered columns (`region`, `salary_band`, `exp_order`, `role_avg_salary`, `is_us`, `is_ai_core`, etc.) that don't exist in `salaries_clean_final.csv`.

### Reference numbers (memorize for annotations)

| Metric | Value |
|---|---|
| Total records | 147,348 |
| Median salary | $147,000 |
| Mean salary | $156,237 |
| Remote % overall | 20.8% |
| EX / EN ratio | 1.91× |
| Top role (ML Eng/MLOps avg) | $194,303 |
| Bottom role (Data Analyst avg) | $107,465 |
| US share of submissions | 90.4% |
| US average salary | $161,381 |
| RoW average salary | $108,024 |

---

## 2. Tableau Desktop setup (one-time, 10 min)

1. Open Tableau Desktop → **Connect → Text File** → select `data/processed/salaries_enhanced.csv`.
2. On the Data Source tab, verify:
   - Rows = **147,348**
   - Columns = **27**
   - `salary_in_usd` is a number (#)
   - `work_year` is a number (#) — convert to discrete on each sheet as needed
3. Right-click `company_location` → **Geographic Role → Country/Region** (Tableau recognizes ISO-2 codes).
4. Right-click `employee_residence` → same Country/Region role (used in tooltips).
5. **Hide unused columns** in the Data pane (right-click → Hide):
   - `salary` — local-currency raw, not standardized
   - `employment_type` — constant FT after preprocessing
6. Keep `experience_level` available (used by EX/EN ratio calc) but use `exp_label` for display.
7. Save workbook as `tableau/ai_job_market_dashboard.twb`. Extract is optional — the CSV is small enough.

### Dimensions vs Measures (verify in Data pane)

| Field | Role | Notes |
|---|---|---|
| `work_year` | Dimension (discrete) | Convert per-sheet to discrete |
| `experience_level` | Dimension | Use `exp_label` for display only |
| `job_title` | Dimension | Tooltips only — 406 unique raw values |
| `salary_currency` | Dimension | Filter reference |
| `employee_residence` | Dimension | Geographic |
| `remote_ratio` | Dimension | 0/50/100 — use `work_mode` for display |
| `company_location` | Dimension (Geographic) | ISO-2; map role |
| `company_size` | Dimension | Use `size_label` for display |
| `title_group` | Dimension | 15 standardized categories |
| `work_mode` | Dimension | On-site / Remote / Hybrid |
| `exp_label` | Dimension | Entry / Mid / Senior / Executive |
| `size_label` | Dimension | Small / Medium / Large |
| `salary_band` | Dimension (categorical) | 6 tier labels |
| `salary_quartile` | Dimension (categorical) | Q1–Q4 |
| `region` | Dimension | 6 regions |
| `is_us` | Dimension | US vs Rest of World |
| `is_ai_core` | Dimension | AI/ML Core vs Data & Tech |
| `salary_in_usd` | Measure | **Primary salary measure — use everywhere** |
| `exp_order` | Measure (use as Dim sort) | Drag to Sort to fix axis order |
| `year_avg_salary` | Measure | Reference field |
| `salary_vs_year_avg` | Measure | Tooltip / color encode |
| `salary_vs_year_avg_pct` | Measure | Tooltip / color encode |
| `role_avg_salary` | Measure | Reference field |
| `salary_vs_role_avg` | Measure | Tooltip |
| `salary_vs_role_avg_pct` | Measure | Tooltip / color encode |

---

## 3. Calculated fields and parameters (build before any sheet)

### Calculated fields (right-click Data pane → Create Calculated Field)

#### 1. Avg Salary USD
```
AVG([Salary In Usd])
```
Format: Currency ($) · 0 decimals

#### 2. Median Salary USD
```
MEDIAN([Salary In Usd])
```
Format: Currency ($) · 0 decimals

#### 3. EX Avg Salary
```
IF [Experience Level] = "EX" THEN [Salary In Usd] END
```
Used inside the EX/EN ratio.

#### 4. EN Avg Salary
```
IF [Experience Level] = "EN" THEN [Salary In Usd] END
```

#### 5. EX/EN Ratio
```
AVG(IF [Experience Level] = "EX" THEN [Salary In Usd] END)
/
AVG(IF [Experience Level] = "EN" THEN [Salary In Usd] END)
```
Format: Number · 2 decimals · suffix `x`

#### 6. Remote %
```
SUM(IF [Work Mode] = "Remote" THEN 1 ELSE 0 END)
/
COUNT([Salary In Usd])
```
Format: Percentage · 1 decimal

#### 7. On-site %
```
SUM(IF [Work Mode] = "On-site" THEN 1 ELSE 0 END)
/
COUNT([Salary In Usd])
```
Format: Percentage · 1 decimal

#### 8. Role Rank (table calc — for Sheet 2 Top-N)
```
RANK_UNIQUE(AVG([Salary In Usd]))
```
After dragging to a sheet, right-click → **Compute Using → Table (across)**.

#### 9. Top N Filter
```
[Role Rank] <= [Top N Roles]
```
Boolean. Drop on Filters shelf, keep `True`.

### Parameter

| Parameter | Type | Allowable values | Default |
|---|---|---|---|
| `Top N Roles` | Integer, **List** | `5` → "Top 5", `10` → "Top 10", `15` → "All 15" | `10` |

Right-click → **Show Parameter Control** when on Sheet 2.

---

## 4. Global filters (configure once, apply to all sheets)

On any worksheet, drag each field to Filters → right-click → **Apply to Worksheets → All Using This Data Source**:

| Filter | Field | Mode | Default |
|---|---|---|---|
| Year | `work_year` | Multiple values (list) | All |
| Experience | `exp_label` | Multiple values (list) | All |
| Company Size | `size_label` | Multiple values (list) | All |

These dropdowns will live in the dashboard header (Row 1).

---

## 5. Color theme (set once via Format → Workbook)

| Use | Hex | Where applied |
|---|---|---|
| Primary navy | `#003875` | Title, headers, KPI numbers |
| Accent blue | `#378ADD` | Avg salary line, primary bars |
| Light blue | `#85B7EB` | Bar fills (Sheet 5) |
| Teal | `#1D9E75` | Median line, Remote color |
| Amber | `#EF9F27` | Count bars, Hybrid color |
| Coral | `#D85A30` | Overlay lines (Sheet 5) |
| Deep blue (On-site) | `#185FA5` | Donut, stacked bar |
| Gray | `#888780` | Axis labels, subtitles |
| Card background | `#F5F7FA` | KPI tiles |

Save these as a **Custom Color Palette** in `Preferences.tps` if you want consistency across sessions (optional).

---

## 6. Sheet-by-sheet build

Each sheet has the same structure: **Purpose → Reference figure → Build steps → Annotation → What it should look like.** Open the EDA reference PNG side-by-side as you build.

---

### Sheet 1 — Salary Trend 2022–2025 (Dual-Axis Line + Bar)

**Purpose:** Show avg + median salary growth alongside submission volume across 4 years.
**Reference figure:** `notebooks/figures/03_salary_trend_dual_axis.png`

**Pills**

| Shelf | Field |
|---|---|
| Columns | `work_year` (discrete) |
| Rows (1) | `AVG(salary_in_usd)` — left axis |
| Rows (2) | `MEDIAN(salary_in_usd)` — left axis (same) |
| Rows (3) | `COUNT(salary_in_usd)` — right axis |
| Mark 1 | Line (avg), color `#378ADD`, thickness 3, dot markers on |
| Mark 2 | Line (median), dashed, color `#1D9E75` |
| Mark 3 | Bar (count), color `#EF9F27`, opacity 40% |

**Steps**
1. Drag `work_year` to Columns, set to discrete.
2. Drag `salary_in_usd` to Rows → AVG → Line mark.
3. Drag `salary_in_usd` to Rows again → change to MEDIAN → Line mark, dashed style.
4. Drag `salary_in_usd` a third time → CNT → right-click → **Dual Axis**.
5. Right-click the right axis → **Synchronize Axis = OFF**.
6. Change CNT mark to **Bar**, color `#EF9F27`, opacity 40%.
7. Add value labels on the avg line at each year.
8. Edit tooltip: include year, avg, median, count.

**Annotation:** Anchor at 2024 mark
> "Median grew from $102K (2022) to $149K (2024) — a 46% jump in 3 years."

**What it looks like:**
- X-axis: 4 years (2022–2025)
- Left Y-axis: USD; two lines climbing from ~$138K (avg) / ~$135K (median) to ~$155K / ~$146K
- Right Y-axis: submission count; four amber bars growing from 1,587 → 76,424 (huge spike in 2024–25)
- Visual story: salaries plateau while sample size explodes 48× → market maturing

---

### Sheet 2 — Salary by Role (Horizontal Bar + Top-N Parameter)

**Purpose:** Rank 15 job categories by average salary; toggle 5 / 10 / 15 visible.
**Reference figure:** `notebooks/figures/04_salary_by_role.png`

**Pills**

| Shelf | Field |
|---|---|
| Columns | `AVG(salary_in_usd)` |
| Rows | `title_group` |
| Color | `AVG(salary_in_usd)` continuous (navy → sky) |
| Detail | `Role Rank` (table calc, compute using Table across) |
| Filter | `Top N Filter` = True |

**Steps**
1. Drag `title_group` to Rows.
2. Drag `salary_in_usd` (AVG) to Columns.
3. Sort `title_group` descending by AVG([Salary In Usd]).
4. Drag `Role Rank` to Detail; right-click → Compute Using → **Table (across)**.
5. Drag `Top N Filter` to Filters shelf; keep `True`.
6. Right-click parameter `Top N Roles` → **Show Parameter Control**.
7. Drag `AVG(salary_in_usd)` again to Color → choose continuous blue, navy → sky.
8. Show mark labels at end of bars in `$XXXk` format.
9. Edit tooltip: title_group, avg, median, count, % vs Data Analyst baseline.

**Annotation:** Anchor on top bar
> "ML Engineer / MLOps tops at $194K — 81% above Data Analyst."

**What it looks like:**
- Up to 15 horizontal bars sorted high → low
- ML Engineer/MLOps ($194,303) at top, Data Analyst ($107,465) at bottom
- Color deepens with salary
- A small dropdown on the right of the dashboard lets the user pick Top 5 / 10 / 15

---

### Sheet 3 — Work Mode Split (Donut)

**Purpose:** Show On-site / Remote / Hybrid share of all records.
**Reference figure:** `notebooks/figures/05_work_mode_donut.png`

**Pills**

| Shelf | Field |
|---|---|
| Mark type | Pie |
| Angle | `COUNT(salary_in_usd)` |
| Color | `work_mode` (On-site `#185FA5` · Remote `#1D9E75` · Hybrid `#EF9F27`) |
| Size | `COUNT(salary_in_usd)` |
| Rows | `MIN(1)` (twice — for donut hole) |

**Steps**
1. New sheet → Marks card → set type to **Pie**.
2. Drag `work_mode` to Color, `salary_in_usd` (CNT) to Angle, same to Size.
3. Set palette: On-site `#185FA5`, Remote `#1D9E75`, Hybrid `#EF9F27`.
4. Donut hole technique:
   - Drag `MIN(1)` to Rows
   - Drag `MIN(1)` to Rows again
   - On the second pill → right-click → **Dual Axis**
   - Right-click axis → **Synchronize Axis**
5. On the second axis Marks card, change type to **Circle**, size very small, color **white**, no border. This punches the hole.
6. Hide row headers, hide axis ticks, remove all gridlines (Format → Lines → None).
7. Add label = % of total + work_mode name (drag CNT to Label, then % of Total quick table calc).
8. Move legend to the dashboard.

**Annotation:**
> "79% of 2025 AI roles are fully on-site — remote work is retreating."

**What it looks like:**
- A three-color ring with a clean white center
- Large blue On-site arc (~74% overall, ~80% in 2025)
- Medium green Remote arc (~21%)
- Tiny amber Hybrid sliver (~5%)

---

### Sheet 4 — Global Hiring Map (Choropleth)

**Purpose:** Avg salary + submission count by country, world view.
**Reference figure:** `notebooks/figures/06_top_countries_salary.png` (EDA shows bar; Tableau builds choropleth as README specifies)

**Pills**

| Shelf | Field |
|---|---|
| Detail (Geographic) | `company_location` (Country/Region role) |
| Color | `AVG(salary_in_usd)` — sequential blue |
| Size | `COUNT(salary_in_usd)` |
| Tooltip | Country · Avg · Median · Count |

**Steps**
1. Double-click `company_location` — Tableau auto-builds the world map.
2. If ISO-2 codes are unrecognized, right-click field → Geographic Role → Country/Region.
3. Drag `salary_in_usd` (AVG) to Color → sequential blue palette, **stepped 6**.
4. Drag `salary_in_usd` (CNT) to Size — set max small so the US doesn't dominate.
5. Map → Background Maps → **Light**.
6. Map → Map Layers → turn off country labels, keep borders only.
7. Edit tooltip:
   ```
   <Company Location>
   Avg salary: <AVG(salary_in_usd)>
   Median: <MEDIAN(salary_in_usd)>
   Submissions: <CNT(salary_in_usd)>
   ```

**Annotation:** pinned to US
> "United States: 133,171 submissions (90%) · $161,381 avg."

**What it looks like:**
- World map, light background
- US in deepest navy + largest bubble
- EU countries mid-blue, smaller bubbles
- Latin America / Middle East / Africa pale and tiny
- Visual story: massive US dominance in both volume and pay

---

### Sheet 5 — Salary vs Experience (Bar + Line overlay)

**Purpose:** Compare avg + median salary across the 4 experience levels.
**Reference figure:** `notebooks/figures/07_salary_vs_experience.png`

**Pills**

| Shelf | Field |
|---|---|
| Columns | `exp_label` (sorted via `exp_order`) |
| Rows (1) | `AVG(salary_in_usd)` — bar, `#85B7EB` 60% opacity |
| Rows (2) | `MEDIAN(salary_in_usd)` — line + dots, `#D85A30` |
| Reference line | Mean = $156K, gray |

**Steps**
1. Drag `exp_label` to Columns.
2. Drag `exp_order` to Detail and right-click → Sort by → manual: Entry → Mid → Senior → Executive.
3. Drag `salary_in_usd` (AVG) to Rows → Mark = Bar, color `#85B7EB`, opacity 60%.
4. Drag `salary_in_usd` (MEDIAN) to Rows → right-click → **Dual Axis** → **Synchronize Axis**. Mark = Line with dot markers, color `#D85A30`.
5. Show value labels on bars: $103K, $140K, $170K, $196K.
6. Add reference band: $156K (overall mean) — light gray dashed.
7. Tooltip includes: count, avg, median, q25, q75, % above entry.

**Annotation:**
> "Executives earn 1.91× Entry Level — $196K vs $103K."

**What it looks like:**
- Four ascending light-blue bars, climbing staircase
- Coral median line + dots tracking just above the bars
- Gray reference band at $156K crosses between Mid and Senior

---

### Sheet 6 — KPI Cards (5 separate tile sheets)

**Purpose:** 5 headline numbers across the dashboard top.
**Reference figure:** `notebooks/figures/09_kpi_summary_cards.png`

Build five tiny sheets. Save them with names: `KPI_Median`, `KPI_Mean`, `KPI_Records`, `KPI_RemotePct`, `KPI_ExEnRatio`.

| Card | Measure on Text mark | Display |
|---|---|---|
| Median Salary | `Median Salary USD` | $147,000 |
| Mean Salary | `Avg Salary USD` | $156,237 |
| Total Records | `COUNT([Salary In Usd])` | 147,348 |
| Remote % | `Remote %` | 20.8% |
| EX / EN Ratio | `EX/EN Ratio` | 1.91× |

**Steps per card**
1. New sheet → drag the calc to **Text** mark.
2. Format the number on Text mark: font 28 pt bold, color navy `#003875`, center aligned.
3. Add a small label above using the sheet **Title** in 12 pt gray (e.g., "Median Salary").
4. Format → Borders → none. Format → Lines → none (rows + columns + grid).
5. Hide column/row dividers.
6. Sheet background → light gray `#F5F7FA` (Format → Shading → Worksheet).
7. Hide the "Show Worksheet Title" checkbox (or use it as the label).

**What they look like:**
- Five flat tiles, big number centered, small gray label above
- Sit in a single row across the dashboard top, equal width

---

### Sheet 7 — Remote Work Trend (100% Stacked Bar — Bonus)

**Purpose:** Year-over-year share of On-site / Remote / Hybrid.
**Reference figure:** `notebooks/figures/10_remote_trend_stacked.png`

**Pills**

| Shelf | Field |
|---|---|
| Columns | `work_year` (discrete) |
| Rows | `COUNT(salary_in_usd)` — % of total |
| Color | `work_mode` (same palette as Sheet 3) |
| Mark | Bar (stacked) |

**Steps**
1. Drag `work_year` to Columns.
2. Drag `salary_in_usd` (CNT) to Rows.
3. Drag `work_mode` to Color.
4. Right-click CNT pill → **Quick Table Calculation → Percent of Total**.
5. Edit Table Calculation: **Compute Using → Cell**, **Specific Dimensions → work_mode**.
6. Add labels showing % inside each segment (drag CNT to Label, format as %).
7. Tooltip: year, work_mode, count, % of year.

**Annotation:** anchor on 2022 Remote segment
> "Remote peaked at 53% in 2022. By 2025, 79% are fully on-site."

**What it looks like:**
- Four 100%-tall bars, one per year (2022–2025)
- Green Remote segment shrinks dramatically: 54% → 31% → 19% → 20%
- Blue On-site swells: 43% → 68% → 81% → 80%
- Amber Hybrid disappears almost entirely after 2022

---

## 7. Master dashboard assembly

### Canvas
- Dashboard menu → New Dashboard
- Size: **Fixed → 1200 × 900 px**
- Show grid in Layout panel for alignment

### Layout grid (5 horizontal rows)

```
┌─────────────────────────────────────────────────────────────────────┐
│  ROW 1 (h=80)  Title text │ Year filter │ Exp filter │ Size filter   │
├──┬──────┬──────┬──────┬──────┬──────────────────────────────────────┤
│2 │KPI_Med│KPI_Mn│KPI_Rec│KPI_Rem│KPI_Ratio              h=120        │
├──┴──────┴──────┴──────┴──────┴──────────────────────────────────────┤
│  ROW 3 (h=300)                                                       │
│  Sheet 1 Salary Trend  (50%)  │  Sheet 2 Salary by Role (50%)        │
├──────────────────────────────────────────────────────────────────────┤
│  ROW 4 (h=280)                                                       │
│ Sheet 3 Donut (25%) │ Sheet 5 Exp (25%) │ Sheet 4 Map (50%)          │
├──────────────────────────────────────────────────────────────────────┤
│  ROW 5 (h=120)  Sheet 7 Remote Trend (100% width — bonus)            │
└──────────────────────────────────────────────────────────────────────┘
```

### Build order

1. **Row 1 — Header (h=80):**
   Drop a horizontal container. Inside it:
   - Text object on the left at 60% width: **"AI Job Market Intelligence — Salaries, Roles & Global Hiring Trends 2022–2025"** (navy `#003875`, 22 pt bold)
   - 3 filter dropdowns (Year, Experience, Size) — pulled from the host sheets via "More Options → Apply to Worksheets → All Using This Data Source"

2. **Row 2 — KPI strip (h=120):**
   Horizontal container. Drag the 5 KPI sheets in order: Median, Mean, Records, Remote %, EX/EN. For each: dropdown → Layout → **Fit = Entire View**, **Hide Title**.

3. **Row 3 — Trends (h=300):**
   Horizontal container. Drop **Sheet 1** (left, 50%) then **Sheet 2** (right, 50%). On Sheet 2, **Show Parameter Control** for `Top N Roles`.

4. **Row 4 — Distributions + Geo (h=280):**
   Horizontal container. Drop **Sheet 3** (25%), **Sheet 5** (25%), **Sheet 4** (50%) left to right.

5. **Row 5 — Bonus stacked (h=120):**
   Horizontal container, full width. Drop **Sheet 7**.

6. Hide unused legends/titles per sheet for a tight look. Keep ONE work_mode legend (above Sheet 3) and ONE salary color scale (above Sheet 4) on the dashboard.

### Filter actions (Dashboard → Actions → Add Action)

| Action | Source | Target | Run on | On clear |
|---|---|---|---|---|
| Year/Exp/Size global filters | Dashboard filters | All sheets | Select | Show all values |
| Filter by Role | Sheet 2 | All other sheets | Select | Show all values |
| Filter by Country | Sheet 4 (map) | All other sheets | Select | Show all values |
| Highlight global | All sheets | All sheets | Hover | Leave |

### Story annotations (5 required, one per chart)

Place as floating text boxes anchored to a mark on each chart. Use 11pt italic gray.

| # | Sheet | Text |
|---|---|---|
| 1 | Sheet 1 | "Median grew 46% from $102K (2022) → $149K (2024)." |
| 2 | Sheet 2 | "ML Engineer/MLOps tops at $194K — 81% above Data Analyst." |
| 3 | Sheet 3 | "79% of 2025 AI roles are fully on-site — remote is retreating." |
| 4 | Sheet 4 | "US = 90% of submissions; $161,381 avg vs $108K rest of world." |
| 5 | Sheet 5 | "Executives earn 1.91× Entry Level — $196K vs $103K." |

---

## 8. Final dashboard mock — what the user will see

```
╔═══════════════════════════════════════════════════════════════════════╗
║  AI JOB MARKET INTELLIGENCE                  [Year▾][Exp▾][Size▾]     ║
║  Salaries · Roles · Global Hiring Trends 2022–2025                    ║
╠═══════════════════════════════════════════════════════════════════════╣
║  $147,000   $156,237   147,348    20.8%      1.91×                    ║
║   Median     Mean     Records    Remote     EX/EN                     ║
╠══════════════════════════════════════╦════════════════════════════════╣
║  SALARY TREND (2022–2025)            ║  SALARY BY ROLE  [Top 10 ▾]    ║
║  ┃         ───── avg                 ║  ML Eng/MLOps   ████████ $194K ║
║  ┃   ╱╲    ╱─── median (dashed)      ║  Software Eng   ███████  $180K ║
║  ┃  ╱  ╲  ╱      📊 count bars       ║  Research Sci   ███████  $175K ║
║  ┗━━━━━━━━━━━━                       ║  ...                           ║
║  2022 2023 2024 2025                 ║  Data Analyst   ████     $107K ║
╠════════════════════╦═════════════════╩════════════════════════════════╣
║  WORK MODE DONUT   ║ EXPERIENCE      ║ GLOBAL HIRING MAP              ║
║   ◯ blue On-site   ║  ▁ ▃ ▆ █        ║  🗺 Choropleth — US deepest    ║
║   green Remote     ║  Entry→Exec     ║  EU mid-blue, others pale      ║
║   amber Hybrid     ║  $103→$196K     ║  Bubble size = volume          ║
╠════════════════════╩═════════════════╩════════════════════════════════╣
║  REMOTE WORK TREND (100% stacked)                                     ║
║   2022 ████ 54% Remote · 43% Onsite · 3% Hybrid                       ║
║   2023 ███▏ 31% Remote · 68% Onsite · 1% Hybrid                       ║
║   2024 ██▏  19% Remote · 81% Onsite                                   ║
║   2025 ██▏  20% Remote · 80% Onsite                                   ║
╚═══════════════════════════════════════════════════════════════════════╝
```

---

## 9. Verification checklist (before submitting)

| # | Check | Pass criteria |
|---|---|---|
| 1 | Row count | All sheets show **147,348** records when filters cleared |
| 2 | Sheet count | 7 working sheets + 5 KPI sub-sheets = **12 sheets** in workbook |
| 3 | Calculated fields | All 9 from §3 present and used somewhere |
| 4 | Parameter | `Top N Roles` toggles 5 / 10 / 15 on Sheet 2 |
| 5 | Global filters | Year / Experience / Size apply to all 7 sheets |
| 6 | Filter actions | Click on Sheet 2 bar → other sheets respond |
| 7 | Highlight action | Hover a country on map → other sheets dim non-matches |
| 8 | Annotations | 5 story callouts visible (one per Sheet 1, 2, 3, 4, 5) |
| 9 | Dual-axis bonus | Sheet 1 has line + bar + dual axis (un-synchronized) |
| 10 | Color theme | Navy / sky / teal / amber palette consistent everywhere |
| 11 | Canvas | Fixed 1200×900 — fits without scroll |
| 12 | Map geographic role | Country/Region role applied on `company_location` |
| 13 | Sort orders | Experience axis = Entry → Mid → Senior → Executive (via `exp_order`) |
| 14 | Tooltips | All sheets have custom tooltip (no raw field names) |
| 15 | File output | Save as `tableau/ai_job_market_dashboard.twbx` (packaged workbook) |
| 16 | Screenshot | Export `docs/dashboard_screenshot.png` for the report |

---

## 10. Suggested build order (one focused session, 3–4 hours)

| Time | Step |
|---|---|
| 0:00–0:15 | Connect data source, set geographic role, hide unused fields |
| 0:15–0:35 | Build all 9 calculated fields + 1 parameter |
| 0:35–1:00 | Sheet 1 — Salary Trend (dual-axis line + bar) |
| 1:00–1:25 | Sheet 2 — Salary by Role (with Top-N parameter) |
| 1:25–1:45 | Sheet 5 — Salary vs Experience (bar + line overlay) |
| 1:45–2:05 | Sheet 3 — Work Mode Donut |
| 2:05–2:20 | Sheet 7 — Remote Work Trend (stacked %) |
| 2:20–2:45 | Sheet 4 — Global Hiring Map (verify ISO match) |
| 2:45–3:05 | Sheet 6 — Build the 5 KPI tile sheets |
| 3:05–3:30 | Master dashboard layout + filter/highlight actions |
| 3:30–3:45 | Drop the 5 story annotations |
| 3:45–3:55 | Polish: titles, fonts, gridlines, tooltips, color audit |
| 3:55–4:00 | Run §9 verification checklist, save `.twbx`, export screenshot |

---

## 11. Troubleshooting cheat sheet

| Symptom | Likely cause | Fix |
|---|---|---|
| Map shows ambiguous countries | ISO codes not auto-detected | Right-click `company_location` → Geographic Role → Country/Region |
| Top N filter shows wrong number | Table calc compute direction wrong | Right-click `Role Rank` → Edit Table Calculation → Compute Using **Table (across)** |
| Donut hole won't appear | Second axis not synchronized OR circle size too large | Synchronize axes, then shrink the circle to ~10% size |
| Experience axis out of order | `exp_label` is alphabetical | Use `exp_order` to manually sort: Entry → Mid → Senior → Executive |
| Dual axis has same scale, hides bars | Axes synchronized | Right-click right axis → uncheck **Synchronize Axis** (Sheet 1 only) |
| KPI numbers misaligned | Sheet not set to "Entire View" | Sheet dropdown → Fit → Entire View |
| Filter doesn't apply across sheets | Forgot to share filter | Right-click filter → Apply to Worksheets → All Using This Data Source |
| Stacked bar shows raw counts not % | Quick Table Calculation not applied | Right-click CNT pill → Quick Table Calculation → Percent of Total, then Edit → Compute Using = Cell, Specific Dimensions = work_mode |
| Tooltip shows ugly field names | Default tooltip | Worksheet → Tooltip → write custom HTML-like template |
| Map renders blank | No internet connection (Tableau pulls map tiles) | Connect to internet OR Map → Background Maps → Offline |
| `.twbx` is too large | Live data extract bundled | Data → Extract → keep CSV unpacked, or filter the extract |

---

## Appendix A — Column reference (quick lookup)

| # | Column | Type | Tableau use |
|---|---|---|---|
| 1 | `work_year` | int | Time axis (Sheet 1, 7) + global filter |
| 2 | `experience_level` | str | EX/EN ratio calcs only |
| 3 | `employment_type` | str | Hidden (constant FT) |
| 4 | `job_title` | str | Tooltips only |
| 5 | `salary` | int | Hidden (local currency) |
| 6 | `salary_currency` | str | Filter reference |
| 7 | `salary_in_usd` | int | **Primary measure — every sheet** |
| 8 | `employee_residence` | str | Geographic filter (tooltip) |
| 9 | `remote_ratio` | int | Use `work_mode` instead |
| 10 | `company_location` | str | Map (Sheet 4) — Country/Region role |
| 11 | `company_size` | str | Use `size_label` instead |
| 12 | `title_group` | str | Sheet 2 axis (15 categories) |
| 13 | `work_mode` | str | Sheet 3 (donut), Sheet 7 (stacked) |
| 14 | `exp_label` | str | Sheet 5 axis + global filter |
| 15 | `size_label` | str | Global filter |
| 16 | `salary_band` | category | Color encode pay tier |
| 17 | `salary_quartile` | category | Color encode Q1–Q4 |
| 18 | `exp_order` | int | Sort key for experience axis |
| 19 | `region` | str | Regional comparisons (optional drill) |
| 20 | `is_us` | str | US vs RoW toggle |
| 21 | `is_ai_core` | str | AI/ML Core vs Data & Tech |
| 22 | `year_avg_salary` | float | Reference line / tooltip |
| 23 | `salary_vs_year_avg` | float | Tooltip |
| 24 | `salary_vs_year_avg_pct` | float | Tooltip / color encode |
| 25 | `role_avg_salary` | float | Reference line / tooltip |
| 26 | `salary_vs_role_avg` | float | Tooltip |
| 27 | `salary_vs_role_avg_pct` | float | Tooltip / color encode |

---

## Appendix B — Sheet-to-figure cross-reference

When you build each Tableau sheet, open the matching EDA PNG side-by-side:

| Sheet | Reference figure |
|---|---|
| 1 — Salary Trend | `notebooks/figures/03_salary_trend_dual_axis.png` |
| 2 — Salary by Role | `notebooks/figures/04_salary_by_role.png` |
| 3 — Work Mode Donut | `notebooks/figures/05_work_mode_donut.png` |
| 4 — Global Hiring Map | `notebooks/figures/06_top_countries_salary.png` |
| 5 — Salary vs Experience | `notebooks/figures/07_salary_vs_experience.png` |
| 6 — KPI Cards | `notebooks/figures/09_kpi_summary_cards.png` |
| 7 — Remote Work Trend | `notebooks/figures/10_remote_trend_stacked.png` |

---

*FAST-NUCES Islamabad · CS3012 Data Visualization · Spring 2026 · Group 8*

# Tableau Implementation Notes

Complete reference for all calculated fields, parameters, filter actions,
and sheet-by-sheet build instructions.

---

## Data Connection

- **File:** `data/processed/salaries_clean_final.csv`
- **Connection type:** Text file (CSV)
- **Rows:** 147,348
- **Columns:** 15

### Dimensions vs Measures in Tableau

| Field | Role | Notes |
|-------|------|-------|
| work_year | Dimension (discrete) | Convert to string or keep as int — use as discrete |
| experience_level | Dimension | EN/MI/SE/EX — use exp_label instead for display |
| employment_type | Dimension | All FT — keep as filter reference only |
| job_title | Dimension | Raw title — for tooltips only |
| salary_currency | Dimension | Filter reference |
| employee_residence | Dimension | Geographic filter |
| remote_ratio | Dimension | 0/50/100 — use work_mode instead for display |
| company_location | Dimension | ISO 2-letter code — use for map |
| company_size | Dimension | S/M/L — use size_label instead for display |
| title_group | Dimension | 15 categories — primary for bar chart |
| work_mode | Dimension | On-site / Hybrid / Remote |
| exp_label | Dimension | Entry Level / Mid Level / Senior / Executive |
| size_label | Dimension | Small / Medium / Large |
| salary | Measure | Local currency — do NOT use for analysis |
| salary_in_usd | Measure | Primary salary measure — use this everywhere |

---

## Calculated Fields

Create these in Tableau before building any sheet.
Right-click in Data pane → Create Calculated Field.

### 1. Avg Salary USD
```
AVG([Salary In Usd])
```
Format: Currency ($) · 0 decimal places

### 2. Median Salary USD
```
MEDIAN([Salary In Usd])
```
Format: Currency ($) · 0 decimal places

### 3. EX Avg Salary
```
IF [Experience Level] = "EX" THEN [Salary In Usd] END
```
Then use AVG() of this field on the sheet.

### 4. EN Avg Salary
```
IF [Experience Level] = "EN" THEN [Salary In Usd] END
```

### 5. EX/EN Ratio (KPI)
```
AVG(IF [Experience Level] = "EX" THEN [Salary In Usd] END)
/
AVG(IF [Experience Level] = "EN" THEN [Salary In Usd] END)
```
Format: Number · 2 decimal places · suffix "x"

### 6. Remote % (KPI)
```
SUM(IF [Work Mode] = "Remote" THEN 1 ELSE 0 END)
/
COUNT([Salary In Usd])
```
Format: Percentage · 1 decimal place

### 7. On-site % (KPI)
```
SUM(IF [Work Mode] = "On-site" THEN 1 ELSE 0 END)
/
COUNT([Salary In Usd])
```

### 8. Role Rank (for parameter toggle — Sheet 2)
```
RANK_UNIQUE(AVG([Salary In Usd]))
```
Table calculation: Compute using → Table (across)

### 9. Top N Filter (for parameter toggle)
```
[Role Rank] <= [Top N Parameter]
```
Use as filter on Sheet 2 — keep TRUE only.

---

## Parameters

### Top N Parameter (Sheet 2 — Salary by Role)
- **Name:** Top N Roles
- **Data type:** Integer
- **Current value:** 10
- **Allowable values:** List
  - 5 — Top 5
  - 10 — Top 10
  - 15 — All 15

Show parameter control on Sheet 2 dashboard panel.

---

## Global Filters (apply to ALL sheets)

Create these as worksheet filters, then use "Apply to Worksheets → All Using This Data Source":

| Filter | Field | Type |
|--------|-------|------|
| Year | work_year | Multiple values (list) — default: All |
| Experience | exp_label | Multiple values (list) — default: All |
| Company Size | size_label | Multiple values (list) — default: All |

---

## Sheet Build Instructions

---

### Sheet 1 — Salary Trend (Dual-Axis Line + Bar)

**Purpose:** Show avg & median salary growth 2022–2025 with submission volume.

| Role | Field |
|------|-------|
| Columns | work_year (discrete) |
| Rows | AVG(salary_in_usd) — left axis |
| Rows (dual) | COUNT(salary_in_usd) — right axis (bar) |
| Mark type 1 | Line (avg salary) · color #378ADD |
| Mark type 2 | Bar (count) · color #EF9F27 · opacity 40% |

Steps:
1. Drag `work_year` to Columns
2. Drag `AVG(salary_in_usd)` to Rows → line chart
3. Drag `COUNT(salary_in_usd)` to Rows → right-click → Dual Axis
4. Right-click right axis → Synchronize Axis (uncheck)
5. Set count to Bar, salary to Line
6. Add `MEDIAN(salary_in_usd)` as a second line (dashed, #1D9E75)

**Annotation:**
> "Median salary grew from $102K (2022) to $149K (2024) — a 46% increase in three years."
Place at 2022 and 2024 data points.

---

### Sheet 2 — Salary by Role (Horizontal Bar + Parameter)

**Purpose:** Rank 15 job categories by average salary with toggle.

| Role | Field |
|------|-------|
| Columns | AVG(salary_in_usd) |
| Rows | title_group |
| Color | Continuous blue scale (navy → sky) |
| Filter | Top N Filter = TRUE |

Steps:
1. Drag `title_group` to Rows
2. Drag `AVG(salary_in_usd)` to Columns
3. Sort descending by AVG salary
4. Add `Role Rank` as table calc — compute using table (across)
5. Drag `Top N Filter` to Filters shelf → Keep True
6. Show the Top N Parameter control
7. Add value labels at end of bars

**Annotation:**
> "ML Engineers / MLOps tops the ladder at $194K avg — 81% above Data Analysts."

---

### Sheet 3 — Work Mode Split (Donut Chart)

**Purpose:** Show On-site / Remote / Hybrid share.

| Role | Field |
|------|-------|
| Angle | COUNT(salary_in_usd) |
| Color | work_mode |
| Color palette | On-site: #185FA5 · Remote: #1D9E75 · Hybrid: #EF9F27 |

Steps to make a donut in Tableau:
1. Create a Pie chart with `work_mode` on Color, COUNT on Angle
2. In Rows, add `MIN(1)` twice (duplicate)
3. Make dual axis → synchronize
4. Set inner axis to Circle mark, size very small, color white
5. This creates the hole

**Annotation:**
> "79% of 2025 AI roles are fully on-site — remote work is retreating."

---

### Sheet 4 — Global Hiring Map (Choropleth)

**Purpose:** Show avg salary and submission count by country.

| Role | Field |
|------|-------|
| Geographic role | company_location → Country/Region |
| Color | AVG(salary_in_usd) — sequential blue |
| Size | COUNT(salary_in_usd) |
| Tooltip | Country · Avg Salary · Submission Count |

Steps:
1. Drag `company_location` to Detail (Tableau auto-creates map)
2. If ISO codes not recognized: right-click field → Geographic Role → Country/Region
3. Drag `AVG(salary_in_usd)` to Color → sequential blue scale
4. Drag `COUNT(salary_in_usd)` to Size (optional — or tooltip only)
5. Edit tooltip to show formatted values

**Annotation:**
> "United States leads with 133,171 submissions (90%) and a $161,381 average salary."

---

### Sheet 5 — Salary vs Experience (Bar + Line overlay)

**Purpose:** Compare avg and median salary across 4 experience levels.

| Role | Field |
|------|-------|
| Columns | exp_label (in order: Entry → Mid → Senior → Executive) |
| Rows | AVG(salary_in_usd) — bar |
| Dual axis | MEDIAN(salary_in_usd) — line with dots |
| Bar color | Light blue #85B7EB · opacity 60% |
| Line color | #D85A30 |

Steps:
1. Set `exp_label` sort order manually: Entry Level, Mid Level, Senior, Executive
2. Add AVG as bar, MEDIAN as dual-axis line
3. Synchronize axes
4. Format: show value labels on bars

**Annotation:**
> "Executive roles earn 1.91× entry level — $196K vs $103K."

---

### Sheet 6 — KPI Cards

**Purpose:** Five headline summary numbers at top of dashboard.

Create 5 separate sheets, each showing one aggregated value as a large number:

| Card | Formula | Display |
|------|---------|---------|
| Median Salary | MEDIAN([Salary In Usd]) | $147,000 |
| Mean Salary | AVG([Salary In Usd]) | $156,237 |
| Total Records | COUNT([Salary In Usd]) | 147,348 |
| Remote % | Remote % calculated field | 20.8% |
| EX / EN Ratio | EX/EN Ratio calculated field | 1.91× |

Steps per card:
1. New sheet → Drag measure to Text mark
2. Format: large font (28pt), center aligned
3. Add dimension label above in smaller font (12pt, gray)
4. Remove all gridlines, borders, headers

---

### Sheet 7 — Remote Work Trend (Bonus Stacked Bar)

**Purpose:** Show year-over-year remote/onsite/hybrid breakdown.

| Role | Field |
|------|-------|
| Columns | work_year (discrete) |
| Rows | COUNT(salary_in_usd) — as % of total |
| Color | work_mode |
| Mark type | Bar (stacked) |
| Table calc | Percent of Total (compute using work_mode) |

Steps:
1. Drag `work_year` to Columns
2. Drag `COUNT(salary_in_usd)` to Rows
3. Drag `work_mode` to Color
4. Right-click COUNT → Quick Table Calculation → Percent of Total
5. Edit Table Calculation: Compute using → Cell, Specific Dimensions → work_mode

**Annotation:**
> "Remote work peaked at 53% in 2022. By 2025, 79% of AI roles are fully on-site."

---

## Dashboard Assembly

1. Create new Dashboard → size 1200 × 900 px (fixed)
2. Layout from top to bottom:
   - **Row 1:** Title text object + 4 filter controls
   - **Row 2:** 5 KPI card sheets (equal width)
   - **Row 3:** Sheet 1 (50% width) | Sheet 2 (50% width)
   - **Row 4:** Sheet 3 (25%) | Sheet 5 (25%) | Sheet 4 (50%)
   - **Row 5:** Sheet 7 (100% width — bonus)

### Filter Actions
Dashboard menu → Actions → Add Action → Filter:
- Source: any sheet → Target: all sheets
- Run on: Select
- Clearing selection: Show all values

### Highlight Actions
Dashboard menu → Actions → Add Action → Highlight:
- Source: all sheets → Target: all sheets
- Run on: Hover

---

## Color Theme Reference

| Use | Hex | Where |
|-----|-----|-------|
| Primary blue | #003875 | Title, headers |
| Accent blue | #378ADD | Line charts, bars |
| Light blue | #85B7EB | Bar fills |
| Teal | #1D9E75 | Median line, Remote |
| Amber | #EF9F27 | Count bars, Hybrid |
| Coral | #D85A30 | Overlay lines |
| Gray | #888780 | Axis labels, subtitles |

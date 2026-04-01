# Solution Plan — AI Dashboard Generator

## Goal

Accept any input file with unknown structure → automatically generate an HTML dashboard with charts, KPIs, and insights.

---

## Tech Stack

| Layer | Tool | Purpose |
|-------|------|---------|
| Data ingestion | `pandas` | Load CSV/Excel/JSON, detect schema |
| LLM | `Groq` (LLaMA / Mistral) | Schema understanding, metric selection, narrative |
| Chart rendering | `plotly` | Generate interactive charts (JSON) |
| Dashboard assembly | `jinja2` | Render HTML dashboard with charts and KPIs |

---

## Pipeline

```
Input file (CSV / Excel / JSON)
        ↓
[Step 1] Schema Discovery — pandas
  - detect column names, data types
  - identify nulls, cardinality, value ranges
  - separate numeric (metrics) from categorical (dimensions)
        ↓
[Step 2] LLM Call 1 — Schema Analysis (Groq)
  - send schema summary (NOT raw data)
  - LLM outputs structured JSON:
    {
      "dashboard_title": "...",
      "kpis": ["col_a", "col_b"],
      "charts": [
        {"type": "bar", "x": "region", "y": "revenue", "agg": "sum"},
        {"type": "line", "x": "date", "y": "qty", "agg": "mean"},
        {"type": "pie", "x": "category", "y": "revenue", "agg": "sum"}
      ],
      "group_by": "region"
    }
        ↓
[Step 3] Data Aggregation — pandas
  - execute aggregations based on LLM JSON decisions
  - compute KPI values (sum, mean, count, etc.)
  - prepare chart-ready dataframes
        ↓
[Step 4] Chart Rendering — plotly
  - generate each chart from aggregated dataframes
  - export each chart as JSON/Plotly spec
        ↓
[Step 5] LLM Call 2 — Narrative Generation (Groq)
  - send aggregated results (KPI values, top N)
  - LLM outputs insight text per chart and overall summary
        ↓
[Step 6] HTML Assembly — jinja2
  - render HTML template with KPI cards
  - embed interactive plotly charts in grid layout
  - add insight text sections
  - apply consistent CSS theme (colors, fonts)
        ↓
Output: dashboard.html
```

---

## Dashboard Slide Layout

```
┌──────────────────────────────────────────────────┐
│  Title + Subtitle (AI generated)                 │
├────────────┬────────────┬────────────┬───────────┤
│  KPI Card  │  KPI Card  │  KPI Card  │  KPI Card │
├────────────────────────┬─────────────────────────┤
│                        │                         │
│    Chart 1 (bar/line)  │    Chart 2 (pie/donut)  │
│                        │                         │
├────────────────────────┴─────────────────────────┤
│           Chart 3 (full width — trend/table)     │
├──────────────────────────────────────────────────┤
│  AI Insight text                                 │
└──────────────────────────────────────────────────┘
```

---

## LLM Prompt Design

### Prompt 1 — Schema Analysis
```
You are a data analyst. Given the following dataset schema, decide:
1. A dashboard title
2. Which columns are KPIs (metrics to highlight)
3. Which charts to generate (max 3) with type, x-axis, y-axis, aggregation
4. The primary dimension to group by

Return ONLY valid JSON. No explanation.

Schema:
{schema_summary}
```

### Prompt 2 — Narrative
```
You are a business analyst. Given these aggregated results,
write one short insight (2 sentences max) for each chart
and one overall summary (3 sentences max).

Results:
{aggregated_results}
```

---

## Project Structure

```
ai_dashboard/
├── main.py               # entry point
├── schema_detector.py    # pandas schema analysis
├── llm_client.py         # Groq API calls
├── aggregator.py         # pandas aggregations from LLM JSON
├── chart_builder.py      # plotly chart → JSON spec
├── html_builder.py       # jinja2 HTML dashboard assembly
├── prompts.py            # all LLM prompt templates
├── templates/
│   └── dashboard.html    # jinja2 HTML template
└── requirements.txt
```

---

## Key Challenges & Mitigations

| Challenge | Mitigation |
|-----------|------------|
| Ambiguous column names | Send sample values + dtype in schema summary |
| Too many columns (40+) | LLM instructed to pick max 3 charts, 4 KPIs |
| Bad data quality | pandas pre-cleaning: drop nulls, fix dtypes before analysis |
| LLM returns invalid JSON | Validate + retry with stricter prompt |
| Chart doesn't fit layout | Fixed grid slots — LLM picks max 3 charts |

---

## Phase Plan

| Phase | Scope |
|-------|-------|
| Phase 1 | Schema detection + LLM JSON output (no HTML yet) |
| Phase 2 | pandas aggregation + plotly charts |
| Phase 3 | jinja2 HTML assembly with fixed layout |
| Phase 4 | LLM narrative + polish (CSS theme, typography) |
| Phase 5 | Test on diverse real datasets |
| Phase 6 | Build web UI (Flask/Streamlit) for file upload & dashboard preview |

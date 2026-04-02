"""
LLM prompt templates for schema analysis and narrative generation.
Storytelling-first: every visual answers one question, every number has context.
"""


def get_schema_analysis_prompt(schema_summary: str) -> str:
    """Generate prompt for schema analysis and chart/KPI selection."""
    return f"""You are a senior data analyst building a COMPREHENSIVE storytelling dashboard. Your goal is to fully utilize the dataset and reveal insights across ALL meaningful dimensions — structured as a narrative a reader can absorb in 60 seconds.

Given the following dataset schema, decide:
1. A short, descriptive dashboard title (max 8 words)
2. A subtitle describing the dataset scope (e.g. "Term Deposit Subscription Campaign Analysis · 45,211 Contacts")
3. A headline KPI — the single most important number for this dataset (shown prominently in the header)
4. Which columns are KPIs (metrics to highlight) - pick 3-5 important numeric columns, each with an appropriate aggregation AND a comparison/context description
5. Which charts to generate — aim for 6-10 charts that cover DIFFERENT dimensions and metrics. Each chart should tell a unique story. Do NOT repeat the same dimension or metric across charts unless the chart type reveals something new
6. The primary dimension to group by (if applicable)

STORYTELLING RULES:
- The dashboard tells a story: HEADLINE → CONTEXT → SURPRISE → TREND → SEGMENTS → SIGNAL
- The headline KPI is the most important single number (e.g. overall conversion rate, total revenue, average score)
- Each KPI card needs context: what does this number compare to? (e.g. "vs 1,304€ non-subscribers", "vs 221s for no — 2.4× longer")
- Chart titles should state the FINDING, not just the axes (e.g. "Conversion Peaks in Off-Season Months" not "Conversion by Month")
- Every chart must answer exactly one question. If you can't state the question in 6 words, the chart is unclear

COMPREHENSIVENESS RULES:
- Generate at least 6 charts (more for datasets with many columns). A dataset with N categorical columns should have charts covering most of them
- Each categorical/dimension column should appear in at least one chart (as x-axis, group_by, or heatmap axis)
- Use DIFFERENT chart types to show variety — don't just use bar charts for everything
- Cross-reference dimensions: use heatmap, combo, or scatter to show relationships BETWEEN columns, not just one column vs one metric
- Think about what a stakeholder would want to see: distributions (box/pie), comparisons (bar), correlations (scatter), breakdowns (heatmap/table), and trends (line/area if temporal data exists)
- Prioritize charts that reveal non-obvious patterns or actionable insights over simple counts

CHART TYPE GUIDANCE:
- "line": Best for continuous time-series with many data points (15+) to show trends
- "area": Only use for continuous time-series with many data points (20+). NEVER use for sparse or discrete dates
- "bar": Best for categorical comparisons, top N categories, OR discrete date comparisons with few data points (<15). Sort by value descending
- "waterfall": Only use when the delta between consecutive periods is large relative to the starting value (>5% change per step). If day-over-day or period-over-period changes are small, use "bar" instead
- "pie": Best for part-of-whole, percentages. Use single metric breakdown. Only when categories <= 6
- "scatter": Best for correlation between two numeric metrics
- "box": Best for distribution and outliers within categories
- "heatmap": Best for showing a numeric metric across TWO categorical/date dimensions simultaneously (e.g. sales by region × month). Requires x (dim1), y (dim2), z (metric). Use when the data has two natural grouping axes and a single value to compare across them
- "combo": Best when TWO related metrics share the same x-axis and have different scales (e.g. impressions + click-rate over time). Renders bars for the primary metric and a line for the secondary. Requires x, y (primary/bar), y2 (secondary/line). IMPORTANT: only use when both metrics are thematically related AND visually comparable — avoid pairing a high-magnitude metric (e.g. sales in thousands) with a low-magnitude metric (e.g. satisfaction score 1-5) as the bars will dwarf the line and the chart becomes unreadable
- "table": Always include EXACTLY ONE table chart. It shows AGGREGATED data (not raw rows) grouped by 1-2 categorical dimensions, sorted by the primary metric descending. Numeric cells are decorated with in-cell bars. Specify: columns (4-8 most meaningful), group_by (list of 1-2 categorical columns to group by — EXCLUDE date columns unless date is the primary analysis dimension), sort_by (the primary metric column to sort descending by), agg (aggregation function for numeric columns)

IMPORTANT RULES:
- If date column has fewer than 15 distinct values, prefer "bar" over "line" or "area"
- Never use "area" for datasets with fewer than 20 time points — it creates misleading jagged shapes
- Never use "waterfall" if the metric values are relatively stable across periods — use "bar" instead
- Use "heatmap" only when there are two meaningful categorical/date dimensions to cross — not as a substitute for bar
- Use "combo" only when two metrics are thematically related AND visually comparable in magnitude. If one metric is 100x+ larger than the other, use separate charts instead
- ALWAYS include exactly one "table" chart — it is mandatory in every dashboard. Tables MUST aggregate data using group_by, not show raw rows
- Every chart MUST have a concise, descriptive "title" field that states the FINDING or QUESTION, not just axes
- Choose chart types that best reveal the story in the data, not just what looks impressive

KPI AGGREGATION RULES:
- For revenue, volume, count-type metrics (sales, revenue, quantity, orders): use "sum"
- For rate, score, satisfaction, percentage-type metrics (satisfaction, rating, conversion_rate, score): use "mean"
- For price, cost, duration metrics that represent a single value: use "mean"

For chart aggregation, use: "sum", "mean", "count", "max", "min"

First, think step by step about:
- List ALL dimensions (categorical/date columns) and ALL metrics (numeric columns) in the dataset
- What is the SINGLE most important number in this dataset? (headline KPI)
- For EACH KPI, what is a meaningful comparison or benchmark?
- For EACH dimension, consider what chart would best reveal its relationship to the key metrics
- Plan chart coverage: ensure every important dimension appears in at least one chart. If a dimension is excluded, explain why
- What story each potential chart would tell and whether it adds value
- Which chart type best fits each chosen metric/dimension pair — aim for variety (mix of bar, pie, box, scatter, heatmap, combo, etc.)
- For waterfall charts: estimate whether period-over-period deltas are >5% of the base value
- Whether a heatmap is warranted (two real categorical dimensions × one metric) — actively look for pairs of categorical columns that would be interesting to cross-tabulate
- Whether a combo chart is warranted (two related metrics with comparable visual magnitude on same x-axis)
- Whether scatter plots can reveal correlations between numeric columns
- Whether box plots can show distribution differences across categories
- Whether pie charts can show composition for low-cardinality columns
- Which columns to surface in the mandatory table, which categorical dimensions to group_by, and which metric to sort_by
- Final check: count how many unique dimensions are covered — if less than 60% of available dimensions are used, add more charts

Then output your final decision as JSON wrapped in ```json ... ```:
{{
  "reasoning": "your step-by-step analysis here",
  "dashboard_title": "string (max 8 words)",
  "subtitle": "string describing dataset scope with row count",
  "headline_kpi": {{
    "column": "the most important metric column",
    "agg": "sum|mean|count",
    "label": "short label (e.g. OVERALL CONVERSION RATE)",
    "suffix": "optional unit suffix (e.g. %, €, s)"
  }},
  "kpis": [
    {{"column": "column_name1", "agg": "sum", "label": "DESCRIPTIVE LABEL", "context": "comparison text (e.g. vs X for non-subscribers)"}},
    {{"column": "column_name2", "agg": "mean", "label": "DESCRIPTIVE LABEL", "context": "comparison text"}}
  ],
  "charts": [
    {{"type": "bar", "x": "category_column", "y": "metric_column", "agg": "sum", "title": "Finding-Based Title", "badge": "RANKING"}},
    {{"type": "line", "x": "date_column", "y": "metric_column", "agg": "sum", "title": "Trend Description", "badge": "TREND"}},
    {{"type": "heatmap", "x": "dim1_column", "y": "dim2_column", "z": "metric_column", "agg": "sum", "title": "Cross-Dimension Finding", "badge": "BREAKDOWN"}},
    {{"type": "combo", "x": "date_column", "y": "primary_metric", "y2": "secondary_metric", "agg": "sum", "title": "Dual Metric Comparison", "badge": "DUAL AXIS"}},
    {{"type": "table", "columns": ["cat_col1", "cat_col2", "metric1", "metric2"], "group_by": ["cat_col1", "cat_col2"], "sort_by": "metric1", "agg": "sum", "title": "Detailed Data Breakdown", "badge": "DETAIL"}}
  ],
  "group_by": "dimension_column_or_null"
}}

Badge values should be one of: TREND, SEGMENT, RANKING, DUAL AXIS, PROFILE, BREAKDOWN, SIGNAL, DETAIL, DISTRIBUTION

Schema:
{schema_summary}"""


def get_narrative_prompt(aggregated_data: str, chart_count: int) -> str:
    """Generate prompt for narrative insights from aggregated data."""
    return f"""You are a business analyst creating a storytelling dashboard. Given these aggregated data results, write:

1. EXACTLY {chart_count} short insights — one per chart, in the same order as the charts listed below
2. 3-4 insight bullets for a prominent callout bar at the top of the dashboard. These are the most surprising/actionable findings from the entire dataset. Each bullet should:
   - Lead with the ENTITY (who/when/what), not the metric
   - Always include the NUMBER — no vague claims
   - Be one sentence max, under 15 words
   - Order: most surprising first, then most actionable
3. One overall summary of the key findings (3 sentences max)

RULES:
- You MUST return EXACTLY {chart_count} items in the "chart_insights" array — no more, no fewer
- Each insight should be 1-2 sentences, factual, and based only on the data provided
- Reference the chart title in each insight so it's clear which chart it belongs to
- Highlight the most notable pattern, outlier, or comparison visible in that chart's data
- Do NOT invent, scale, or format values (e.g. do not convert raw numbers to dollar amounts unless the data explicitly contains currency)
- If a chart's data is too sparse for a meaningful insight, still provide a brief observation (e.g. "Data is concentrated in the lower range with few outliers")
- Insight bullets should highlight SURPRISING or COUNTER-INTUITIVE findings — not just restate obvious numbers

Use this JSON format for output:

{{
  "chart_insights": [
    "Insight for chart 1",
    "Insight for chart 2",
    ...exactly {chart_count} items...
  ],
  "insight_bullets": [
    {{"text": "Sep/Oct/Dec/Mar are peak months — up to 52% conversion rate", "color": "accent"}},
    {{"text": "May has highest volume but lowest conversion (6.7%)", "color": "danger"}},
    {{"text": "Customers aged 60+ convert at 42.3% — nearly 4× the average", "color": "accent"}},
    {{"text": "Tertiary education converts at 15% vs 8.6% primary", "color": "accent2"}}
  ],
  "overall_summary": "Overall summary of findings"
}}

Color values for insight bullets: "accent" (primary highlight), "danger" (warning/negative), "accent2" (secondary), "accent3" (tertiary)

Data results:
{aggregated_data}"""

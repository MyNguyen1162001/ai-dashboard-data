"""
LLM prompt templates for schema analysis and narrative generation.
"""


def get_schema_analysis_prompt(schema_summary: str) -> str:
    """Generate prompt for schema analysis and chart/KPI selection."""
    return f"""You are a data analyst. Given the following dataset schema, decide:
1. A short, descriptive dashboard title (max 8 words)
2. Which columns are KPIs (metrics to highlight) - pick 2-4 important numeric columns
3. Which charts to generate with type, x-axis, y-axis, and aggregation function
4. The primary dimension to group by (if applicable)

CHART TYPE GUIDANCE:
- "line": Best for continuous time-series with many data points (15+) to show trends
- "area": Only use for continuous time-series with many data points (20+). NEVER use for sparse or discrete dates
- "bar": Best for categorical comparisons, top N categories, OR discrete date comparisons with few data points (<15). Sort by value descending
- "waterfall": Best for showing sequential change or delta between a small number of discrete periods (e.g. month-over-month, day-over-day with <15 points). Preferred over "bar" when the story is about how values rise and fall over time
- "pie": Best for part-of-whole, percentages. Use single metric breakdown. Only when categories <= 6
- "scatter": Best for correlation between two numeric metrics
- "box": Best for distribution and outliers within categories

IMPORTANT RULES:
- If date column has fewer than 15 distinct values, prefer "bar" or "waterfall" over "line" or "area"
- Never use "area" for datasets with fewer than 20 time points — it creates misleading jagged shapes
- Choose chart types that best reveal the story in the data, not just what looks impressive

For aggregation, use: "sum", "mean", "count", "max", "min"

First, think step by step about:
- What dimensions (categorical/date columns) and metrics (numeric columns) exist
- What story each potential chart would tell and whether it adds value
- Why you are including or excluding each metric from the charts
- Which chart type best fits each chosen metric/dimension pair

Then output your final decision as JSON wrapped in ```json ... ```:
{{
  "dashboard_title": "string",
  "kpis": ["column_name1", "column_name2"],
  "charts": [
    {{"type": "bar", "x": "date_or_category_column", "y": "metric_column", "agg": "sum"}},
    {{"type": "bar", "x": "category_column", "y": "metric_column", "agg": "sum"}}
  ],
  "group_by": "dimension_column_or_null"
}}

Schema:
{schema_summary}"""


def get_narrative_prompt(aggregated_data: str) -> str:
    """Generate prompt for narrative insights from aggregated data."""
    return f"""You are a business analyst. Given these aggregated data results, write:
1. One short insight (2 sentences max) for each chart
2. One overall summary of the key findings (3 sentences max)

Keep insights factual and based only on the data provided.
IMPORTANT: Only reference actual values present in the data. Do not invent, scale, or format values
(e.g. do not convert raw numbers to dollar amounts unless the data explicitly contains currency).
Use this JSON format for output:

{{
  "chart_insights": [
    "Insight for first chart",
    "Insight for second chart",
    "Insight for third chart"
  ],
  "overall_summary": "Overall summary of findings"
}}

Data results:
{aggregated_data}"""

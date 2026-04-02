"""
Main entry point for AI Dashboard Generator.
"""
import json
import os
import sys
import argparse
from pathlib import Path
import pandas as pd
from dotenv import load_dotenv

from schema_detector import SchemaDetector
from llm_client import LLMClient
from aggregator import DataAggregator
from chart_builder import ChartBuilder
from html_builder import HTMLBuilder, format_human_readable


def load_data(file_path: str) -> pd.DataFrame:
    """Load data from CSV, Excel, or JSON file."""
    file_ext = Path(file_path).suffix.lower()

    if file_ext == ".csv":
        # Auto-detect separator by sniffing the first line
        with open(file_path, "r", encoding="utf-8", errors="replace") as f:
            sample = f.read(4096)
        import csv
        dialect = csv.Sniffer().sniff(sample, delimiters=",;\t|")
        df = pd.read_csv(file_path, sep=dialect.delimiter)
    elif file_ext in [".xlsx", ".xls"]:
        try:
            df = pd.read_excel(file_path, engine='openpyxl')
        except Exception:
            try:
                df = pd.read_excel(file_path, engine='xlrd')
            except Exception:
                # File may actually be CSV with wrong extension
                with open(file_path, "r", encoding="utf-8", errors="replace") as f:
                    sample = f.read(4096)
                import csv as csv_mod
                dialect = csv_mod.Sniffer().sniff(sample, delimiters=",;\t|")
                df = pd.read_csv(file_path, sep=dialect.delimiter)
    elif file_ext == ".json":
        df = pd.read_json(file_path)
    else:
        raise ValueError(f"Unsupported file type: {file_ext}")

    print(f"✓ Loaded {len(df)} rows, {len(df.columns)} columns")
    return df


def compute_headline_kpi(df: pd.DataFrame, headline_config: dict) -> dict:
    """Compute the headline KPI value from LLM config."""
    if not headline_config:
        return None

    col = headline_config.get("column")
    agg = headline_config.get("agg", "mean")
    label = headline_config.get("label", "KEY METRIC")
    suffix = headline_config.get("suffix", "")

    if not col or col not in df.columns:
        return None

    if not pd.api.types.is_numeric_dtype(df[col]):
        return None

    if agg == "sum":
        raw_value = float(df[col].sum())
    elif agg == "mean":
        raw_value = float(df[col].mean())
    elif agg == "count":
        raw_value = int(df[col].count())
    elif agg == "max":
        raw_value = float(df[col].max())
    elif agg == "min":
        raw_value = float(df[col].min())
    else:
        raw_value = float(df[col].mean())

    formatted = format_human_readable(raw_value)

    return {
        "value": formatted,
        "label": label,
        "suffix": suffix,
        "sub": f"{int(raw_value):,}" if raw_value > 10000 else ""
    }


def main():
    parser = argparse.ArgumentParser(description="AI Dashboard Generator")
    parser.add_argument("input_file", help="Input data file (CSV, Excel, or JSON)")
    parser.add_argument("--output", "-o", default="dashboard.html", help="Output HTML file")
    args = parser.parse_args()

    # Load environment variables
    load_dotenv(Path(__file__).parent / ".env")

    # Get LLM model from environment variable (required)
    model = os.getenv("AI_MODEL")
    if not model:
        print("❌ Error: AI_MODEL environment variable not set")
        print("Please set it in your .env file or export AI_MODEL='your-model'")
        return 1

    print("🚀 AI Dashboard Generator")
    print("-" * 50)

    # Step 1: Load data
    print(f"\n📁 Loading data from: {args.input_file}")
    try:
        df = load_data(args.input_file)
    except Exception as e:
        print(f"❌ Error loading file: {e}")
        return 1

    # Step 2: Detect schema
    print("\n🔍 Analyzing schema...")
    detector = SchemaDetector(df)
    schema = detector.detect()
    schema_summary = detector.get_summary_for_llm()
    print(f"✓ Found {len(schema['dimensions'])} dimensions, {len(schema['metrics'])} metrics")

    # Step 3: LLM Schema Analysis
    print("\n🤖 Analyzing data with AI...")
    try:
        llm = LLMClient(model=model)
        schema_analysis = llm.analyze_schema(schema_summary)

        if not schema_analysis or not schema_analysis.get("charts"):
            print("⚠️  LLM returned empty analysis, using defaults")
            schema_analysis = {
                "dashboard_title": "Data Dashboard",
                "subtitle": "",
                "headline_kpi": None,
                "kpis": [{"column": col, "agg": "sum"} for col in schema['metrics'][:4]],
                "charts": [],
                "group_by": schema['dimensions'][0] if schema['dimensions'] else None
            }
        else:
            print(f"✓ Dashboard title: {schema_analysis.get('dashboard_title')}")
            print(f"✓ KPIs: {schema_analysis.get('kpis')}")
            print(f"✓ Charts: {len(schema_analysis.get('charts', []))}")
            print(f"\n📋 Full LLM schema analysis response:\n{json.dumps(schema_analysis, indent=2)}")
    except Exception as e:
        print(f"⚠️  LLM error: {e}, using defaults")
        schema_analysis = {
            "dashboard_title": "Data Dashboard",
            "subtitle": "",
            "headline_kpi": None,
            "kpis": [{"column": col, "agg": "sum"} for col in schema['metrics'][:4]],
            "charts": [],
            "group_by": schema['dimensions'][0] if schema['dimensions'] else None
        }

    # Step 4: Compute headline KPI
    headline_kpi = compute_headline_kpi(df, schema_analysis.get("headline_kpi"))
    if headline_kpi:
        print(f"✓ Headline KPI: {headline_kpi['value']} {headline_kpi.get('suffix', '')}")

    # Step 5: Data Aggregation
    print("\n📊 Aggregating data...")
    aggregator = DataAggregator(df)

    # Calculate KPIs
    kpi_columns = schema_analysis.get("kpis", schema['metrics'][:4])
    kpis = aggregator.process_kpis(kpi_columns)
    print(f"✓ Calculated {len(kpis)} KPI metrics")

    # Prepare chart data
    charts_config = schema_analysis.get("charts", [])
    chart_data_dict = aggregator.prepare_all_charts(charts_config)
    print(f"✓ Prepared {len(chart_data_dict)} charts")

    # Step 6: Generate Charts
    print("\n📈 Generating charts...")
    charts_json = []
    for idx, (data, metadata) in chart_data_dict.items():
        try:
            config = charts_config[idx] if idx < len(charts_config) else {}
            chart_json = ChartBuilder.build_chart(data, {**metadata, **config})
            charts_json.append(chart_json)
            print(f"  ✓ Chart {idx + 1}: {config.get('type', 'unknown')}")
        except Exception as e:
            print(f"  ⚠️  Chart {idx + 1} failed: {e}")

    # Step 7: Generate Narrative
    print("\n✍️  Generating insights...")
    chart_insights = []
    overall_summary = ""
    insight_bullets = []

    try:
        aggregated_summary = aggregator.get_summary_string()
        narrative = llm.generate_narrative(aggregated_summary, chart_count=len(charts_json))
        chart_insights = narrative.get("chart_insights", [])
        overall_summary = narrative.get("overall_summary", "")
        insight_bullets = narrative.get("insight_bullets", [])
        print(f"✓ Generated {len(chart_insights)} chart insights + {len(insight_bullets)} callout bullets")
    except Exception as e:
        print(f"⚠️  Narrative generation failed: {e}")
        chart_insights = ["Chart analysis in progress."] * len(charts_json)
        overall_summary = "Analysis complete."

    # Extract chart badges and titles from config
    chart_badges = [c.get("badge", "") for c in charts_config[:len(charts_json)]]
    chart_titles = [c.get("title", "") for c in charts_config[:len(charts_json)]]

    # Step 8: Build HTML
    print("\n🎨 Building HTML dashboard...")
    html_builder = HTMLBuilder(template_dir="templates")
    html_content = html_builder.build(
        title=schema_analysis.get("dashboard_title", "Data Dashboard"),
        kpis=kpis,
        charts_json=charts_json,
        chart_insights=chart_insights,
        overall_summary=overall_summary,
        subtitle=schema_analysis.get("subtitle", ""),
        headline_kpi=headline_kpi,
        insight_bullets=insight_bullets,
        kpi_configs=schema_analysis.get("kpis", []),
        chart_badges=chart_badges,
        chart_titles=chart_titles
    )

    # Step 9: Save output
    output_path = Path(args.output)
    output_path.write_text(html_content)
    print(f"✓ Dashboard saved to: {output_path.absolute()}")

    print("\n" + "=" * 50)
    print("✅ Dashboard generation complete!")
    print("=" * 50)

    return 0


if __name__ == "__main__":
    sys.exit(main())

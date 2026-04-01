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
from html_builder import HTMLBuilder


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
        df = pd.read_excel(file_path)
    elif file_ext == ".json":
        df = pd.read_json(file_path)
    else:
        raise ValueError(f"Unsupported file type: {file_ext}")

    print(f"✓ Loaded {len(df)} rows, {len(df.columns)} columns")
    return df


def main():
    parser = argparse.ArgumentParser(description="AI Dashboard Generator")
    parser.add_argument("input_file", help="Input data file (CSV, Excel, or JSON)")
    parser.add_argument("--output", "-o", default="dashboard.html", help="Output HTML file")
    parser.add_argument("--model", "-m", default="qwen/qwen-max", help="OpenRouter model ID")
    args = parser.parse_args()

    # Load environment variables
    load_dotenv(Path(__file__).parent / ".env")

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
        llm = LLMClient(model=args.model)
        schema_analysis = llm.analyze_schema(schema_summary)

        if not schema_analysis or not schema_analysis.get("charts"):
            print("⚠️  LLM returned empty analysis, using defaults")
            schema_analysis = {
                "dashboard_title": "Data Dashboard",
                "kpis": schema['metrics'][:4],
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
            "kpis": schema['metrics'][:4],
            "charts": [],
            "group_by": schema['dimensions'][0] if schema['dimensions'] else None
        }

    # Step 4: Data Aggregation
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

    # Step 5: Generate Charts
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

    # Step 6: Generate Narrative
    print("\n✍️  Generating insights...")
    chart_insights = []
    overall_summary = ""

    try:
        aggregated_summary = aggregator.get_summary_string()
        narrative = llm.generate_narrative(aggregated_summary)
        chart_insights = narrative.get("chart_insights", [])
        overall_summary = narrative.get("overall_summary", "")
        print(f"✓ Generated {len(chart_insights)} chart insights + overall summary")
    except Exception as e:
        print(f"⚠️  Narrative generation failed: {e}")
        chart_insights = ["Chart analysis in progress."] * len(charts_json)
        overall_summary = "Analysis complete."

    # Step 7: Build HTML
    print("\n🎨 Building HTML dashboard...")
    html_builder = HTMLBuilder(template_dir="templates")
    html_content = html_builder.build(
        title=schema_analysis.get("dashboard_title", "Data Dashboard"),
        kpis=kpis,
        charts_json=charts_json,
        chart_insights=chart_insights,
        overall_summary=overall_summary
    )

    # Step 8: Save output
    output_path = Path(args.output)
    output_path.write_text(html_content)
    print(f"✓ Dashboard saved to: {output_path.absolute()}")

    print("\n" + "=" * 50)
    print("✅ Dashboard generation complete!")
    print("=" * 50)

    return 0


if __name__ == "__main__":
    sys.exit(main())

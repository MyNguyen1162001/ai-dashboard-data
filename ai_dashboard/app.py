"""
Streamlit web UI for AI Dashboard Generator.
Provides file upload, configuration, and dashboard preview.
"""

import streamlit as st
import pandas as pd
import csv
import io
import os
from pathlib import Path
from dotenv import load_dotenv
import sys

from schema_detector import SchemaDetector
from llm_client import LLMClient
from aggregator import DataAggregator
from chart_builder import ChartBuilder
from html_builder import HTMLBuilder
from prompts import get_schema_analysis_prompt

# Load environment variables
load_dotenv(Path(__file__).parent / ".env")

# Page configuration
st.set_page_config(
    page_title="AI Dashboard Generator",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5em;
        color: #667eea;
        font-weight: 700;
        margin-bottom: 0.5em;
    }
    .subtitle {
        font-size: 1.2em;
        color: #999;
        margin-bottom: 2em;
    }
    .success-box {
        padding: 1em;
        border-radius: 0.5em;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
    }
    .info-box {
        padding: 1em;
        border-radius: 0.5em;
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        color: #0c5460;
    }
    .warning-box {
        padding: 1em;
        border-radius: 0.5em;
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        color: #856404;
    }
</style>
""", unsafe_allow_html=True)

# Title and description
st.markdown('<div class="main-header">📊 AI Dashboard Generator</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Automatically generate interactive dashboards from your data</div>', unsafe_allow_html=True)

# Sidebar configuration
with st.sidebar:
    st.header("⚙️ Configuration")

    api_key = os.getenv("OPENROUTER_API_KEY", "")
    if not api_key:
        api_key = st.text_input(
            "OpenRouter API Key",
            type="password",
            help="Get your key from https://openrouter.io/keys"
        )

    model = os.getenv("AI_MODEL", "qwen/qwen3-max")
    st.info(f"🤖 Model: **{model}**")

    st.divider()
    st.subheader("📚 Help")
    st.write("""
    - **Upload** your CSV, Excel, or JSON file
    - **Configure** your OpenRouter API key
    - **Generate** your dashboard with one click
    - **Download** the HTML file to share
    """)

# Main content
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📁 Upload Your Data")

    uploaded_file = st.file_uploader(
        "Choose a data file",
        type=["csv", "xlsx", "xls", "json"],
        help="Supported formats: CSV, Excel, JSON"
    )

with col2:
    st.subheader("📊 Dataset Info")
    if uploaded_file:
        try:
            # Load the file
            if uploaded_file.name.endswith('.csv'):
                sample = uploaded_file.read(8192).decode('utf-8', errors='replace')
                uploaded_file.seek(0)
                dialect = csv.Sniffer().sniff(sample, delimiters=',;\t|')
                df = pd.read_csv(uploaded_file, sep=dialect.delimiter)
            elif uploaded_file.name.endswith(('.xlsx', '.xls')):
                df = pd.read_excel(uploaded_file)
            elif uploaded_file.name.endswith('.json'):
                df = pd.read_json(uploaded_file)
            else:
                st.error("Unsupported file format")
                df = None

            if df is not None:
                st.metric("Rows", len(df))
                st.metric("Columns", len(df.columns))

                # Show column preview
                with st.expander("Column Names"):
                    st.write(", ".join(df.columns.tolist()))
        except Exception as e:
            st.error(f"Error loading file: {e}")
            df = None
    else:
        st.info("Upload a file to see dataset info")
        df = None

# Data preview
if uploaded_file and df is not None:
    st.divider()
    st.subheader("👀 Data Preview")

    col1, col2 = st.columns(2)
    with col1:
        st.write("**First few rows:**")
        st.dataframe(df.head(), use_container_width=True)

    with col2:
        st.write("**Data types:**")
        dtype_df = pd.DataFrame({
            "Column": df.columns,
            "Type": [str(dtype) for dtype in df.dtypes]
        })
        st.dataframe(dtype_df, use_container_width=True)

# Generate dashboard
st.divider()
col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    st.subheader("🚀 Generate Dashboard")

with col2:
    generate_button = st.button("Generate Dashboard", type="primary", use_container_width=True)

with col3:
    st.write("")  # Spacing

if generate_button:
    if not uploaded_file:
        st.error("❌ Please upload a file first")
    elif not api_key:
        st.error("❌ Please enter your OpenRouter API key in the sidebar")
    elif df is None:
        st.error("❌ Could not load the file. Please check the format.")
    else:
        # Generate dashboard with streaming log
        try:
            with st.status("🚀 AI Dashboard Generator", expanded=True) as status:
                st.write("─" * 50)

                # Step 1: Load info
                st.write(f"📁 Loading data from: **{uploaded_file.name}**")
                st.write(f"✓ Loaded {len(df)} rows, {len(df.columns)} columns")

                # Step 2: Analyze schema
                st.write("")
                st.write("🔍 Analyzing schema...")
                detector = SchemaDetector(df)
                schema = detector.detect()
                schema_summary = detector.get_summary_for_llm()
                st.write(f"✓ Found {len(schema['dimensions'])} dimensions, {len(schema['metrics'])} metrics")

                # Step 3: LLM Analysis
                st.write("")
                st.write("🤖 Analyzing data with AI...")
                llm = LLMClient(api_key=api_key, model=model)
                schema_analysis = llm.analyze_schema(schema_summary)

                if not schema_analysis or not schema_analysis.get("charts"):
                    st.write("⚠️  LLM returned empty analysis, using defaults")
                    schema_analysis = {
                        "dashboard_title": "Data Dashboard",
                        "kpis": schema['metrics'][:4],
                        "charts": [],
                        "group_by": schema['dimensions'][0] if schema['dimensions'] else None
                    }
                else:
                    st.write(f"✓ Dashboard title: {schema_analysis.get('dashboard_title')}")
                    st.write(f"✓ KPIs: {schema_analysis.get('kpis')}")
                    st.write(f"✓ Charts: {len(schema_analysis.get('charts', []))}")

                # Show full LLM response in a collapsible JSON block
                st.write("")
                st.write("📋 Full LLM schema analysis response:")
                st.json(schema_analysis)

                # Step 4: Data Aggregation
                st.write("")
                st.write("📊 Aggregating data...")
                aggregator = DataAggregator(df)
                kpi_columns = schema_analysis.get("kpis", schema['metrics'][:4])
                kpis = aggregator.process_kpis(kpi_columns)
                charts_config = schema_analysis.get("charts", [])
                chart_data_dict = aggregator.prepare_all_charts(charts_config)
                st.write(f"✓ Calculated {len(kpis)} KPI metrics")
                st.write(f"✓ Prepared {len(chart_data_dict)} charts")

                # Step 5: Generate Charts
                st.write("")
                st.write("📈 Generating charts...")
                charts_json = []
                for idx, (data, metadata) in chart_data_dict.items():
                    try:
                        config = charts_config[idx] if idx < len(charts_config) else {}
                        chart_json = ChartBuilder.build_chart(data, {**metadata, **config})
                        charts_json.append(chart_json)
                        st.write(f"  ✓ Chart {idx + 1}: {config.get('type', 'unknown')}")
                    except Exception as e:
                        st.write(f"  ⚠️  Chart {idx + 1} failed: {e}")

                # Step 6: Generate Narrative
                st.write("")
                st.write("✍️  Generating insights...")
                chart_insights = []
                overall_summary = ""

                try:
                    aggregated_summary = aggregator.get_summary_string()
                    narrative = llm.generate_narrative(aggregated_summary)
                    chart_insights = narrative.get("chart_insights", [])
                    overall_summary = narrative.get("overall_summary", "")
                    st.write(f"✓ Generated {len(chart_insights)} chart insights + overall summary")
                except Exception as e:
                    st.write(f"⚠️  Narrative generation failed: {e}")
                    chart_insights = ["Analysis complete."] * len(charts_json)
                    overall_summary = "Dashboard generated successfully."

                # Step 7: Build HTML
                st.write("")
                st.write("🎨 Building HTML dashboard...")
                html_builder = HTMLBuilder(template_dir="templates")
                html_content = html_builder.build(
                    title=schema_analysis.get("dashboard_title", "Data Dashboard"),
                    kpis=kpis,
                    charts_json=charts_json,
                    chart_insights=chart_insights,
                    overall_summary=overall_summary
                )
                st.write(f"✓ Dashboard built successfully")

                st.write("")
                st.write("=" * 50)
                st.write("✅ Dashboard generation complete!")
                st.write("=" * 50)

                status.update(label="✅ Dashboard generation complete!", state="complete", expanded=False)

            # Display success message
            st.markdown(
                '<div class="success-box">✅ Dashboard generated successfully!</div>',
                unsafe_allow_html=True
            )

            # Show dashboard title
            st.subheader(f"📊 {schema_analysis.get('dashboard_title', 'Data Dashboard')}")

            # Display dashboard preview
            st.write("**Dashboard Preview** (interactive below):")
            st.components.v1.html(html_content, height=1200, scrolling=True)

            # Download button
            st.divider()
            col1, col2, col3 = st.columns([1, 1, 2])

            with col1:
                st.download_button(
                    label="📥 Download HTML",
                    data=html_content,
                    file_name="dashboard.html",
                    mime="text/html",
                    use_container_width=True
                )

            with col2:
                if st.button("🔄 Generate New", use_container_width=True):
                    st.rerun()

            # Show dashboard details
            with st.expander("📋 Dashboard Details"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("KPI Metrics", len(kpis))
                with col2:
                    st.metric("Charts", len(charts_json))
                with col3:
                    st.metric("Data Rows", len(df))

                st.write("**Selected KPIs:**")
                st.write(", ".join(kpi_columns))

                st.write("**Chart Types:**")
                chart_types = [c.get("type", "unknown") for c in charts_config]
                st.write(", ".join(chart_types) if chart_types else "No charts configured")

        except Exception as e:
            st.error(f"❌ Error generating dashboard: {e}")
            st.info("Please check your API key and try again")

# Footer
st.divider()
st.markdown("""
<div style="text-align: center; color: #999; font-size: 0.9em; margin-top: 2em;">
    <p>🚀 <strong>AI Dashboard Generator</strong> | Powered by OpenRouter AI</p>
    <p>Built with Streamlit, Pandas, Plotly, and Jinja2</p>
</div>
""", unsafe_allow_html=True)

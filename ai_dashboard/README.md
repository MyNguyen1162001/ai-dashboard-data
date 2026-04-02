# AI Dashboard Generator

Automatically generate interactive HTML dashboards from any dataset (CSV, Excel, JSON) using AI-powered analysis.

## Features

- 📁 **Auto Data Detection**: Automatically analyze dataset schema
- 🤖 **AI-Powered Analysis**: Use OpenRouter AI to understand your data and select relevant metrics
- 📊 **Interactive Charts**: Generate dynamic Plotly charts (bar, line, pie, scatter, box)
- 📈 **KPI Cards**: Highlight key performance indicators
- ✍️ **AI Insights**: Generate narrative descriptions of findings
- 🎨 **Beautiful HTML**: Professional dashboard with responsive design

## Architecture

```
Input File (CSV/Excel/JSON)
    ↓
Schema Detection (pandas)
    ↓
LLM Analysis (OpenRouter)
    ↓
Data Aggregation (pandas)
    ↓
Chart Generation (Plotly)
    ↓
Narrative Generation (OpenRouter)
    ↓
HTML Assembly (Jinja2)
    ↓
dashboard.html
```

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up OpenRouter API key and AI model:
```bash
export OPENROUTER_API_KEY="your-openrouter-api-key"
export AI_MODEL="qwen/qwen-max"  # Optional: set default model
```

## Usage

### Option 1: Web Interface (Recommended for Non-Technical Users)

Start the Streamlit web app:
```bash
streamlit run app.py
```

Then:
1. Open browser to `http://localhost:8501`
2. Upload your data file
3. Configure API key and model
4. Click "Generate Dashboard"
5. Download the HTML file

See [STREAMLIT_GUIDE.md](STREAMLIT_GUIDE.md) for detailed web UI instructions.

### Option 2: Command Line (For Advanced Users)

Basic usage:
```bash
python main.py data.csv
```

Specify output file (model controlled by AI_MODEL env var):
```bash
python main.py data.csv -o my_dashboard.html
```

To change model, set environment variable:
```bash
export AI_MODEL="qwen/qwen3.5-9b"
python main.py data.csv
```

### Supported Models
- `qwen/qwen3.5-9b` (Recommended - fast and efficient)
- `qwen/qwen-max` (Most capable)
- `meta-llama/llama-2-70b-chat` (Open source)
- Other OpenRouter models available

### Supported File Formats
- CSV (`.csv`)
- Excel (`.xlsx`, `.xls`)
- JSON (`.json`)

## Project Structure

```
ai_dashboard/
├── main.py                    # Entry point
├── schema_detector.py         # Data analysis
├── llm_client.py              # OpenRouter API integration
├── aggregator.py              # Data aggregation
├── chart_builder.py           # Plotly charts
├── html_builder.py            # HTML assembly
├── prompts.py                 # LLM prompts
├── templates/
│   └── dashboard.html         # Jinja2 template
└── requirements.txt
```

## How It Works

### Phase 1: Schema Detection
Analyzes your data to identify:
- Column data types
- Numeric metrics vs. categorical dimensions
- Data quality (nulls, cardinality)
- Sample values

### Phase 2: LLM Analysis
Sends schema summary to AI to decide:
- Dashboard title
- Which columns are KPIs (2-4)
- Which charts to generate (max 3)
- Primary grouping dimension

### Phase 3: Data Aggregation
Prepares data based on LLM decisions:
- Calculates KPI metrics (sum, mean, count)
- Aggregates data for each chart
- Limits to top 20 values for readability

### Phase 4: Chart Generation
Creates interactive Plotly charts:
- Bar charts for comparisons
- Line charts for trends
- Pie charts for distributions
- Scatter plots for relationships
- Box plots for distributions

### Phase 5: Narrative Generation
AI generates insights:
- One insight per chart (2 sentences max)
- Overall summary (3 sentences max)

### Phase 6: HTML Assembly
Combines everything into a beautiful dashboard:
- KPI cards at the top
- Charts in responsive grid
- Insights and summary
- Professional styling

## Example

With `sample_data.csv`:
```bash
python main.py ../sample_data.csv -o sales_dashboard.html
```

Generated dashboard will include:
- Sales, Quantity, and Customer Satisfaction KPIs
- Regional sales comparison (bar chart)
- Trend over time (line chart)
- Product distribution (pie chart)
- AI-generated insights for each chart

## Environment Variables

```bash
OPENROUTER_API_KEY=sk-or-v1-xxxxx  # Required
```

## Troubleshooting

### "OPENROUTER_API_KEY not set"
Set your API key: `export OPENROUTER_API_KEY="your-key"`

### "LLM returned empty analysis"
The model may be overloaded. Try again or switch models with `-m` flag.

### "Chart failed to generate"
Ensure your data has numeric columns for metrics. Add a sample of your data structure.

### "HTML file is blank"
Check that the template file exists in `templates/dashboard.html`

## Performance Tips

- **Large datasets**: Sample rows before running for faster processing
- **Many columns**: LLM will automatically select top metrics
- **Real-time data**: Generate once, or use as part of larger pipeline

## Customization

### Add Custom Chart Types
Edit `chart_builder.py` to add new chart types in the `_build_*` methods.

### Customize HTML Layout
Edit `templates/dashboard.html` to change colors, fonts, or layout.

### Modify Prompts
Edit `prompts.py` to change how AI analyzes your data.

## License

MIT License - feel free to use and modify!

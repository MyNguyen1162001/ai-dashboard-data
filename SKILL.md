# 🎯 AI Dashboard Generator - Skill Reference

## What is it?

Auto-generates beautiful interactive HTML dashboards from any data file (CSV/Excel/JSON) using AI to intelligently select metrics, charts, and generate insights.

## Quick Start (2 min)

### Web UI (Recommended)
```bash
cd ai_dashboard
pip install -r requirements.txt
export OPENROUTER_API_KEY="sk-or-v1-your-key"
streamlit run app.py
# Opens http://localhost:8501
# Upload file → Click generate → Download HTML
```

### CLI
```bash
cd ai_dashboard
python main.py data.csv -o dashboard.html -m qwen/qwen3.5-9b
```

## Setup

### 1. Get API Key
- Visit: https://openrouter.ai/keys
- Copy your key

### 2. Set Environment
```bash
export OPENROUTER_API_KEY="sk-or-v1-your-key"
# OR create ai_dashboard/.env:
# OPENROUTER_API_KEY=sk-or-v1-your-key
```

### 3. Install & Run
```bash
cd ai_dashboard
pip install -r requirements.txt

# Web UI
streamlit run app.py

# Or CLI
python main.py data.csv
```

## Usage

### Web Interface
```
1. streamlit run app.py
2. Upload data file (CSV/Excel/JSON)
3. Enter API key in sidebar (if not in .env)
4. Select AI model
5. Click "Generate Dashboard"
6. Download HTML file
```

### Command Line
```bash
# Basic
python main.py data.csv

# Custom output & model
python main.py data.csv -o report.html -m qwen/qwen-max

# Different formats
python main.py data.xlsx -o dashboard.html
python main.py data.json -o dashboard.html
```

## AI Models Available

| Model | Speed | Quality | Cost |
|-------|-------|---------|------|
| `qwen/qwen3.5-9b` | ⚡⚡⚡ | ⭐⭐⭐⭐ | $ |
| `qwen/qwen-max` | ⚡⚡ | ⭐⭐⭐⭐⭐ | $$ |
| `meta-llama/llama-2-70b-chat` | ⚡ | ⭐⭐⭐⭐ | $ |

## What Gets Generated

Each dashboard includes:
- **Title**: AI-generated based on data
- **KPI Cards**: 4 key metrics highlighted
- **Charts**: Up to 3 interactive Plotly charts
- **Insights**: AI-written analysis per chart
- **Summary**: Overall findings
- **Design**: Responsive, professional styling

## Output

Single self-contained `dashboard.html` file:
- ✓ No dependencies required
- ✓ Works in any browser
- ✓ Interactive charts (zoom, hover, pan)
- ✓ Mobile-responsive
- ✓ Share via email/Slack/Drive

## File Structure

```
ai_dashboard/
├── app.py                    # Web UI (streamlit run app.py)
├── main.py                   # CLI (python main.py data.csv)
├── schema_detector.py        # Analyzes data
├── llm_client.py             # Calls OpenRouter API
├── aggregator.py             # Aggregates data
├── chart_builder.py          # Generates charts
├── html_builder.py           # Builds HTML
├── prompts.py                # AI prompts
├── templates/dashboard.html  # HTML template
├── requirements.txt          # Dependencies
└── README.md                 # Full docs
```

## Supported Formats

- ✓ CSV (`.csv`)
- ✓ Excel (`.xlsx`, `.xls`)
- ✓ JSON (`.json`)

## Troubleshooting

### "OPENROUTER_API_KEY not set"
```bash
export OPENROUTER_API_KEY="your-key"
# Or enter in web UI sidebar
```

### "Module not found"
```bash
cd ai_dashboard
pip install -r requirements.txt
```

### "Port 8501 already in use"
```bash
streamlit run app.py --server.port 8502
```

### "Generation takes too long"
- Use faster model: `qwen/qwen3.5-9b`
- Use smaller dataset
- Check internet connection

### "Dashboard is blank"
- Ensure data has numeric columns
- Check file isn't corrupted
- Try with sample_data.csv first

## Performance

| Dataset Size | Time |
|---|---|
| Small (< 100 rows) | 5-15s |
| Medium (100-1K rows) | 10-20s |
| Large (> 1K rows) | 20-60s |

Times include API calls. Actual processing is < 1 second.

## Customization

### Change AI Behavior
Edit `ai_dashboard/prompts.py` and restart app

### Change Dashboard Colors
Edit CSS in `ai_dashboard/templates/dashboard.html`

### Add Chart Types
Add methods to `ai_dashboard/chart_builder.py`

## Deployment

### Local Network
```bash
streamlit run app.py --server.address 0.0.0.0
# Access from: http://your-ip:8501
```

### Cloud (Free - Streamlit Cloud)
```bash
# 1. Push code to GitHub
# 2. Go to https://share.streamlit.io
# 3. Connect repo and deploy
# 4. Add OPENROUTER_API_KEY in Secrets
```

### Docker
```bash
docker build -t ai-dashboard .
docker run -p 8501:8501 -e OPENROUTER_API_KEY="key" ai-dashboard
```

## Common Commands

```bash
# Install dependencies
pip install -r ai_dashboard/requirements.txt

# Start web UI
streamlit run ai_dashboard/app.py

# Generate from CLI
python ai_dashboard/main.py data.csv

# Custom output
python ai_dashboard/main.py data.csv -o my_dashboard.html

# Custom model
python ai_dashboard/main.py data.csv -m qwen/qwen-max

# Set API key
export OPENROUTER_API_KEY="sk-or-v1-xxx"

# Use different port
streamlit run ai_dashboard/app.py --server.port 9000
```

## Example Workflows

### Workflow 1: Quick Dashboard
```
1. streamlit run app.py
2. Upload CSV
3. Click generate
4. Download HTML
5. Email to team
```
**Time: 2-3 minutes**

### Workflow 2: Batch Processing
```bash
for file in data/*.csv; do
  python main.py "$file" -o "dashboards/${file%.csv}.html"
done
```
**Use for: Multiple files, automation**

### Workflow 3: Team Deployment
```
1. Push to GitHub
2. Deploy to Streamlit Cloud
3. Share URL with team
4. Team uploads their data
5. Instant dashboards
```
**Use for: Non-technical users**

## Key Features

✨ **Automatic Analysis**
- Detects data types & relationships
- Identifies metrics vs dimensions
- Analyzes data quality

🤖 **AI-Powered**
- OpenRouter API integration
- Multiple model options
- Intelligent chart selection

📊 **Beautiful Dashboards**
- 5 chart types (bar, line, pie, scatter, box)
- Professional responsive design
- Interactive Plotly charts

💡 **Smart Insights**
- AI-generated narrative per chart
- Overall summary
- Business-focused analysis

## API Keys

### Getting a Key
1. Go to https://openrouter.io
2. Sign up (free tier available)
3. Get API key from keys page
4. Set environment variable or use in app

### Security
- Never commit API key to git
- Use .env file or environment variables
- Free tier: ~100,000 tokens/month

## Data Requirements

### What Works Well
- CSV, Excel, JSON files
- Mixed numeric/categorical data
- 10+ rows, 2+ columns
- Clear column names

### What to Avoid
- All text columns (need some numbers)
- Deeply nested JSON
- Corrupted/incomplete data
- > 100MB files (slow processing)

## Documentation

| Document | Purpose |
|----------|---------|
| WEB_UI_GUIDE.md | For web UI users |
| QUICKSTART.md | 5-minute setup |
| STREAMLIT_GUIDE.md | Advanced web UI features |
| README.md | Full technical reference |
| SOLUTION_PLAN.md | Architecture & design |

## Support

### Check These First
1. Verify API key is set: `echo $OPENROUTER_API_KEY`
2. Test with sample_data.csv first
3. Read README.md troubleshooting section
4. Check error messages in console

### Common Issues
- **API key**: Make sure it's set and valid
- **Modules**: Run `pip install -r requirements.txt`
- **File format**: Ensure CSV/Excel/JSON
- **Port conflict**: Use different port with `--server.port`

## Quick Reference

```bash
# Install (do once)
cd ai_dashboard && pip install -r requirements.txt

# Set key (do once per terminal)
export OPENROUTER_API_KEY="sk-or-v1-xxx"

# Start web UI (every time you use it)
streamlit run app.py

# Or use CLI
python main.py data.csv
```

## What Happens Behind the Scenes

```
1. Load data with pandas
2. Analyze schema & structure
3. Send to OpenRouter AI for analysis
4. AI suggests metrics & charts
5. Aggregate data based on suggestions
6. Generate Plotly charts
7. Send results to AI for insights
8. Render beautiful HTML
9. Display & download
```

## Tips & Tricks

- **Fast generation**: Use `qwen/qwen3.5-9b`
- **Best quality**: Use `qwen/qwen-max`
- **Batch processing**: Use CLI with shell loop
- **Team access**: Deploy to Streamlit Cloud
- **Custom styling**: Edit HTML template
- **Different models**: Change in app or `-m` flag

## TL;DR

```bash
pip install -r ai_dashboard/requirements.txt
export OPENROUTER_API_KEY="your-key"
streamlit run ai_dashboard/app.py
# Upload file → Generate → Download
```

That's it! You're ready to generate dashboards. 🎉

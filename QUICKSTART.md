# 🚀 Quick Start Guide - AI Dashboard Generator

## 1. Install Dependencies

```bash
cd /Users/tramynguyen/Work/AI_data_analysis/ai_dashboard
pip install -r requirements.txt
```

## 2. Set Up OpenRouter API Key

Get your free API key from [OpenRouter](https://openrouter.io/keys)

Then set it in your environment:

```bash
export OPENROUTER_API_KEY="sk-or-v1-your-key-here"
```

Or create a `.env` file:

```bash
cp .env.example .env
# Edit .env with your API key
```

## 3. Generate Your First Dashboard

Using the sample dataset provided:

```bash
python main.py ../sample_data.csv
```

This will create `dashboard.html` in the current directory.

### Using Your Own Data

```bash
python main.py /path/to/your/data.csv -o my_dashboard.html
```

### Specify AI Model

```bash
python main.py ../sample_data.csv -m qwen/qwen-max -o dashboard.html
```

## 4. View Your Dashboard

Open the generated HTML file in your browser:

```bash
open dashboard.html    # macOS
xdg-open dashboard.html  # Linux
start dashboard.html   # Windows
```

## Features You'll See

✨ **Interactive Dashboard** with:
- 📊 KPI Cards showing key metrics
- 📈 Interactive Plotly charts
- 💡 AI-generated insights for each chart
- 📝 Overall summary of findings
- 🎨 Beautiful, responsive design

## Supported Data Formats

- ✅ CSV files (`.csv`)
- ✅ Excel files (`.xlsx`, `.xls`)
- ✅ JSON files (`.json`)

## Available OpenRouter Models

| Model | Speed | Quality | Cost |
|-------|-------|---------|------|
| qwen/qwen3.5-9b | ⚡⚡⚡ | ⭐⭐⭐⭐ | $ |
| qwen/qwen-max | ⚡⚡ | ⭐⭐⭐⭐⭐ | $$ |
| meta-llama/llama-2-70b | ⚡ | ⭐⭐⭐⭐ | $ |

## Example: Sales Data Dashboard

```bash
python main.py ../sample_data.csv -o sales_dashboard.html -m qwen/qwen3.5-9b
```

This will analyze the sample sales dataset and generate a dashboard showing:
- Total Sales, Average Quantity, Customer Satisfaction metrics
- Sales by Region comparison
- Sales trends over time
- Product performance distribution
- AI insights about the data

## Troubleshooting

### ❌ "OPENROUTER_API_KEY not set"
→ Make sure you've set the environment variable or created .env file

### ❌ "Module not found"
→ Run `pip install -r requirements.txt` from the ai_dashboard directory

### ❌ "File not found"
→ Use absolute paths or run from the ai_dashboard directory

### ❌ "LLM returned empty analysis"
→ Try again - the API might be temporarily busy. Or use a different model.

## Project Structure

```
ai_dashboard/
├── main.py                 # Run this to generate dashboards
├── schema_detector.py      # Analyzes data structure
├── llm_client.py          # Calls OpenRouter API
├── aggregator.py          # Prepares data
├── chart_builder.py       # Creates charts
├── html_builder.py        # Assembles HTML
├── prompts.py             # LLM prompts
├── templates/
│   └── dashboard.html     # HTML template
├── requirements.txt       # Dependencies
├── README.md              # Full documentation
└── .env.example          # Configuration template
```

## How It Works (Overview)

1. 📂 **Load Data** - Reads your CSV/Excel/JSON file
2. 🔍 **Analyze Schema** - Detects columns, types, and relationships
3. 🤖 **AI Analysis** - Asks OpenRouter AI to suggest charts and metrics
4. 📊 **Prepare Data** - Aggregates data based on AI suggestions
5. 📈 **Generate Charts** - Creates interactive Plotly charts
6. ✍️ **Generate Insights** - AI writes descriptions of findings
7. 🎨 **Build Dashboard** - Combines everything into HTML
8. 💾 **Save Output** - Saves beautiful dashboard.html

## Next Steps

- 📖 Read [README.md](ai_dashboard/README.md) for detailed documentation
- 🔧 Customize [templates/dashboard.html](ai_dashboard/templates/dashboard.html) for your brand
- 📝 Modify [prompts.py](ai_dashboard/prompts.py) to change AI behavior
- 🎨 Edit CSS in template for different colors/fonts

## Getting Help

- 📚 Full docs: [README.md](ai_dashboard/README.md)
- 🔍 Explore code files for detailed comments
- 🐛 Check troubleshooting section above
- 💬 Review the SOLUTION_PLAN.md for architecture details

Happy Dashboard Building! 🎉

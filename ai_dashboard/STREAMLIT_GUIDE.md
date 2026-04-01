# 🚀 Streamlit Web UI Guide

## Overview

The Streamlit web interface provides an easy-to-use dashboard for generating AI-powered dashboards without using the command line.

## Installation

```bash
cd ai_dashboard
pip install -r requirements.txt
```

This installs Streamlit along with all other dependencies.

## Quick Start

### 1. Set Up API Key

Option A: Environment variable
```bash
export OPENROUTER_API_KEY="sk-or-v1-your-key"
```

Option B: Enter in the app (sidebar)
- Leave unset in environment
- Enter your key directly in the web interface

### 2. Start the App

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

### 3. Generate Your First Dashboard

1. **Upload File**: Click "Browse files" and select your CSV/Excel/JSON
2. **Configure**: Enter API key in sidebar (if not set in .env)
3. **Choose Model**: Select your preferred AI model
4. **Generate**: Click "Generate Dashboard" button
5. **Download**: Download the HTML file when ready

## Features

### 📁 File Upload
- Supports CSV, Excel (.xlsx, .xls), and JSON files
- Automatic format detection
- Shows file size and column count

### 📊 Data Preview
- Preview first rows of data
- See column names and data types
- Understand your data before generating

### ⚙️ Configuration
- **API Key**: Secure input field (password type)
- **Model Selection**: Choose from multiple OpenRouter models
- **Help**: Quick reference guide in sidebar

### 🚀 Dashboard Generation
- Progress indicator showing each step
- Real-time status updates
- Handles errors gracefully with helpful messages

### 📥 Download
- Download generated HTML as file
- Share dashboards with others
- Fully self-contained (no external dependencies except Plotly CDN)

### 👀 Preview
- View dashboard directly in the browser
- Interactive charts with zoom, pan, hover
- Full dashboard styling and layout

### 📋 Dashboard Details
- View statistics about generated dashboard
- See which metrics were selected
- Check chart types used

## Available AI Models

### Qwen Series (Recommended)
- **qwen/qwen3.5-9b** - Fast, efficient, great quality
- **qwen/qwen-max** - More capable, best quality

### Open Source
- **meta-llama/llama-2-70b-chat** - Powerful open model

### Other
- **deepseek/deepseek-chat** - Chinese AI company model

All models are available through OpenRouter API.

## Workflow

```
Upload File
    ↓
View Preview
    ↓
Configure (API Key, Model)
    ↓
Click "Generate Dashboard"
    ↓
Monitor Progress (15 seconds - 1 minute)
    ↓
View Dashboard Preview
    ↓
Download HTML File
```

## Step-by-Step Tutorial

### Example: Sales Data Analysis

1. **Start the app**:
   ```bash
   streamlit run app.py
   ```

2. **Upload file**:
   - Click "Choose a data file"
   - Select your sales data CSV
   - Wait for preview to load

3. **Configure API**:
   - Scroll to sidebar
   - Paste your OpenRouter API key
   - Keep default model or select preferred one

4. **Review data**:
   - Look at preview section
   - Verify column names and types
   - Check that data looks correct

5. **Generate**:
   - Click blue "Generate Dashboard" button
   - Watch progress bar
   - Wait for "✅ Dashboard generated successfully!"

6. **View results**:
   - Scroll down to see dashboard preview
   - Interact with charts
   - Check insights and KPIs

7. **Download**:
   - Click "📥 Download HTML" button
   - Save dashboard.html to your computer
   - Open in browser to view anytime

## Configuration

### .env File Setup

Create `.env` file in `ai_dashboard/` directory:

```
OPENROUTER_API_KEY=sk-or-v1-your-key-here
```

Then start the app:
```bash
streamlit run app.py
```

The API key will be pre-filled in the sidebar.

### Streamlit Configuration

Create `.streamlit/config.toml` to customize:

```toml
[theme]
primaryColor = "#667eea"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"

[client]
showErrorDetails = true
```

## Troubleshooting

### ❌ "Connection refused" or "Address already in use"
The default port 8501 is busy. Use a different port:
```bash
streamlit run app.py --server.port 8502
```

### ❌ "OPENROUTER_API_KEY not set"
Either:
- Enter key in the sidebar text input, OR
- Set environment variable: `export OPENROUTER_API_KEY="your-key"`

### ❌ "Module not found"
Run from the `ai_dashboard` directory:
```bash
cd ai_dashboard
streamlit run app.py
```

### ❌ "Dashboard not loading/blank"
- Check browser console for errors (F12)
- Ensure file has data with numeric columns
- Try with sample_data.csv first

### ❌ "Generation takes too long"
- Use qwen/qwen3.5-9b model (faster)
- Check internet connection
- OpenRouter API might be busy - try again

### ❌ "Charts not showing in preview"
- Wait for full generation to complete
- Check that data has numeric columns
- Refresh browser page

## Performance Tips

### Faster Generation
- Use `qwen/qwen3.5-9b` model
- Smaller datasets (< 100MB)
- Better internet connection

### Better Results
- Use `qwen/qwen-max` model
- Clean data (no missing values)
- Clear column names

### Optimize Data
```python
# Remove unnecessary columns
df = df[['date', 'region', 'sales', 'quantity']]

# Remove rows with missing values
df = df.dropna()

# Export to CSV
df.to_csv('clean_data.csv', index=False)
```

## Customization

### Change Default Model
Edit `app.py` line ~65:

```python
model = st.selectbox(
    "AI Model",
    [
        "qwen/qwen3.5-9b",        # Default
        "qwen/qwen-max",
        # Add more models here
    ]
)
```

### Change Color Scheme
Edit the CSS section in `app.py` (around line ~40):

```python
st.markdown("""
<style>
    .main-header {
        color: #YOUR-COLOR;  # Change this
    }
</style>
""", unsafe_allow_html=True)
```

### Add More File Formats
Edit line ~115:

```python
uploaded_file = st.file_uploader(
    "Choose a data file",
    type=["csv", "xlsx", "xls", "json", "parquet"],  # Add more
)
```

## Deployment

### Local Network
Share with team on local network:

```bash
streamlit run app.py --server.address 0.0.0.0
```

Access from other computers: `http://your-ip:8501`

### Cloud Deployment (Streamlit Cloud)

1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repo
4. Deploy instantly

Set secrets in Streamlit Cloud dashboard:
```
OPENROUTER_API_KEY = sk-or-v1-xxx
```

### Docker Deployment

Create `Dockerfile`:

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py"]
```

Build and run:
```bash
docker build -t ai-dashboard .
docker run -p 8501:8501 -e OPENROUTER_API_KEY="your-key" ai-dashboard
```

## Comparison: CLI vs Web UI

| Feature | CLI | Web UI |
|---------|-----|--------|
| Setup | Simple | Very simple |
| Learning curve | Steeper | Very gentle |
| Best for | Batch processing | Interactive use |
| Automation | Easy | Harder |
| Sharing | Manual download | Built-in download |
| Team use | Less intuitive | Very intuitive |

## Best Practices

1. **API Key Security**
   - Never commit API key to git
   - Use .env file or environment variables
   - Use .gitignore to exclude .env

2. **Data Handling**
   - Clean data before uploading
   - Test with sample_data.csv first
   - Keep sensitive data out of shared dashboards

3. **Model Selection**
   - Start with qwen3.5-9b (fast)
   - Use qwen-max for important analysis
   - Monitor API costs

4. **Dashboard Sharing**
   - Downloaded HTML is self-contained
   - Share via email, Drive, Slack
   - No special viewer needed

## Advanced Usage

### Batch Processing
For many files, use CLI instead:
```bash
for file in data/*.csv; do
  python main.py "$file" -o "dashboards/${file%.csv}.html"
done
```

### API Integration
Call the generator from your code:
```python
from schema_detector import SchemaDetector
from llm_client import LLMClient
import pandas as pd

df = pd.read_csv('data.csv')
detector = SchemaDetector(df)
schema = detector.detect()
# ... continue processing
```

### Custom Prompts
Modify `prompts.py` to change AI behavior, then reload the app.

## Keyboard Shortcuts

When Streamlit app is running:
- **R**: Rerun the app
- **C**: Clear cache
- **K**: View keyboard shortcuts
- **Q**: Quit

## Monitor & Logs

Streamlit shows detailed logs:
```bash
streamlit run app.py --logger.level=debug
```

## Server Configuration

### Custom Port
```bash
streamlit run app.py --server.port 9000
```

### Public URL
```bash
streamlit run app.py --server.headless true --server.enableXsrfProtection false
```

### Memory Limits
```bash
streamlit run app.py --client.maxMessageSize 2048
```

## Support

- Streamlit docs: https://docs.streamlit.io
- OpenRouter docs: https://openrouter.io/docs
- Report issues: Check Streamlit GitHub issues

## Summary

The Streamlit web UI provides a user-friendly interface for generating dashboards. Key advantages:

✅ **Easy to use** - No command line needed
✅ **Visual feedback** - See progress in real-time
✅ **Instant preview** - View dashboard immediately
✅ **One-click download** - Share easily
✅ **Interactive** - Test different models
✅ **Professional** - Beautiful, polished interface

Start with the web UI for a great user experience!

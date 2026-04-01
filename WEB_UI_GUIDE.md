# 🌐 Web UI Guide - Phase 6

## Overview

Phase 6 introduces a **Streamlit web interface** for the AI Dashboard Generator, making it easy for non-technical users to generate dashboards without the command line.

## Quick Start

### 1. Install Streamlit
```bash
cd ai_dashboard
pip install -r requirements.txt
```

### 2. Set API Key (Optional)
```bash
export OPENROUTER_API_KEY="sk-or-v1-your-key"
```

### 3. Launch the App
```bash
streamlit run app.py
```

The app opens automatically at `http://localhost:8501`

## What You Get

### 🎯 User-Friendly Interface
- **Upload Section**: Drag-and-drop or click to upload files
- **Configuration Panel**: Sidebar for API key and model selection
- **Data Preview**: Automatic preview of your data
- **Progress Indicator**: Real-time feedback during generation
- **Dashboard Preview**: View generated dashboard in the browser
- **Download Button**: One-click download of HTML file

### 📊 Features

```
┌─────────────────────────────────────────────────────────┐
│  📊 AI Dashboard Generator                              │
├─────────────────────────────────────────────────────────┤
│  ⚙️ Configuration (sidebar)                              │
│  - API Key input                                        │
│  - Model selection dropdown                            │
│  - Help/Documentation                                  │
├─────────────────────────────────────────────────────────┤
│  📁 Upload Your Data                                     │
│  - CSV, Excel, JSON support                            │
│  - Automatic file detection                            │
├─────────────────────────────────────────────────────────┤
│  📊 Dataset Info                                         │
│  - Row count                                           │
│  - Column count                                        │
│  - Column names preview                                │
├─────────────────────────────────────────────────────────┤
│  👀 Data Preview                                         │
│  - First few rows                                      │
│  - Data types                                          │
├─────────────────────────────────────────────────────────┤
│  🚀 Generate Dashboard                                   │
│  - Single click to start                               │
│  - Progress indicator                                  │
│  - Step-by-step status                                 │
├─────────────────────────────────────────────────────────┤
│  📥 Download                                             │
│  - Download HTML file                                  │
│  - Generate new dashboard                              │
│  - View dashboard details                              │
└─────────────────────────────────────────────────────────┘
```

## Workflow Comparison

### CLI Approach
```
Command Line → Python Script → Output File → Open Browser
```

### Web UI Approach
```
Web Browser → Upload File → Preview → Generate → Download
```

**Web UI is much more intuitive for non-technical users!**

## Files Added in Phase 6

```
ai_dashboard/
├── app.py                          # Main Streamlit application
├── .streamlit/
│   └── config.toml                 # Streamlit configuration
├── STREAMLIT_GUIDE.md              # Detailed Streamlit guide
├── requirements.txt                # Updated with streamlit
└── ... (all previous files)
```

## Technical Architecture

### Web UI Layer (New)
```
User Browser (Streamlit UI)
        ↓
app.py (Web Interface)
        ↓
Existing Core Modules
  - schema_detector.py
  - llm_client.py
  - aggregator.py
  - chart_builder.py
  - html_builder.py
```

### Data Flow
```
Upload File → Load with pandas → SchemaDetector → LLMClient
    ↓ (AI Analysis) → Aggregator → ChartBuilder → HTMLBuilder
    ↓ (Generate HTML) → Display in Browser & Download
```

## Usage Examples

### Example 1: Sales Team Dashboard
1. Sales manager opens web UI in browser
2. Uploads monthly sales CSV
3. Configures API key in sidebar
4. Clicks "Generate Dashboard"
5. Downloads HTML to share with team

### Example 2: Data Scientist Analysis
1. Data scientist uses web UI for quick exploration
2. Tests different models with same data
3. Compares generated dashboards
4. Exports best version as HTML

### Example 3: Business Intelligence
1. BI team publishes web UI internally
2. Business users upload their datasets
3. Auto-generates dashboards instantly
4. Downloads reports for presentations

## Configuration

### Environment Variables
```bash
# Set API key
export OPENROUTER_API_KEY="sk-or-v1-your-key"

# Optional: Run on custom port
streamlit run app.py --server.port 8502
```

### .env File
Create `ai_dashboard/.env`:
```
OPENROUTER_API_KEY=sk-or-v1-your-key-here
```

### Streamlit Settings
Edit `ai_dashboard/.streamlit/config.toml`:
- Change theme colors
- Configure max file size
- Set log level
- Enable/disable features

## Deployment Options

### Local Machine
```bash
streamlit run app.py
```
Access: `http://localhost:8501`

### Team Network
```bash
streamlit run app.py --server.address 0.0.0.0
```
Access: `http://your-machine-ip:8501` from other computers

### Cloud (Streamlit Cloud)
```bash
# 1. Push to GitHub
git push origin main

# 2. Go to https://share.streamlit.io
# 3. Select your repo
# 4. Add secrets in admin panel

OPENROUTER_API_KEY = sk-or-v1-xxx
```

### Docker
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
EXPOSE 8501
CMD ["streamlit", "run", "app.py"]
```

```bash
docker build -t ai-dashboard .
docker run -p 8501:8501 -e OPENROUTER_API_KEY="your-key" ai-dashboard
```

## Features in Detail

### 📁 File Upload
- Supports CSV, Excel, JSON
- Shows file info (rows, columns)
- Validates file format
- Handles errors gracefully

### 📊 Data Preview
- Shows first rows
- Displays data types
- Lists all column names
- Validates data before processing

### ⚙️ Configuration
- API key input (password field)
- Model selection dropdown
- Help documentation in sidebar
- All options saved in session

### 🚀 Generation
- Multi-step process with progress
- Real-time status messages
- Error handling with helpful messages
- Automatic fallbacks if LLM fails

### 🎨 Dashboard Preview
- Full interactive dashboard in browser
- All charts are clickable/zoomable
- Embedded CSS and JavaScript
- Responsive design

### 📥 Download
- One-click HTML export
- Self-contained file (no external files needed)
- Ready to share via email/Slack/Drive

### 📋 Details Panel
- Show generated dashboard statistics
- List selected KPIs
- Display chart types used
- Expandable/collapsible section

## Advanced Features

### Session Management
Streamlit handles sessions automatically. Each user gets isolated state.

### Caching
Consider adding caching for repeated operations:
```python
@st.cache_data
def load_file(uploaded_file):
    return pd.read_csv(uploaded_file)
```

### Error Handling
App handles:
- Missing API key → helpful message
- Invalid file format → clear error
- LLM failure → fallback to defaults
- Network issues → retry guidance

### State Management
- File upload persists during session
- Configuration settings are retained
- Generated dashboard stays in memory
- Clear visual feedback for all actions

## Performance

### Generation Time
- Small files (< 100 rows): 5-15 seconds
- Medium files (100-1000 rows): 10-20 seconds
- Large files (> 1000 rows): 20-60 seconds

Factors:
- API response time
- File size
- Model selected
- Internet connection

### Optimization Tips
1. Use qwen/qwen3.5-9b for speed
2. Clean data before uploading
3. Keep files reasonably sized
4. Better internet connection = faster generation

## Troubleshooting

### App won't start
```bash
# Check if port 8501 is in use
lsof -i :8501

# Use different port
streamlit run app.py --server.port 8502
```

### API key not working
```bash
# Verify key is valid at https://openrouter.io/keys
# Check if key is set in environment
echo $OPENROUTER_API_KEY

# Or enter directly in the web UI
```

### Dashboard preview is blank
- Wait for full generation to complete
- Check browser console (F12) for errors
- Try with sample_data.csv first
- Refresh page if needed

### File upload fails
- Check file format (CSV, Excel, JSON only)
- Verify file is readable
- Try smaller file first
- Check file isn't corrupted

### Generation takes too long
- Use faster model (qwen3.5-9b)
- Check internet connection
- Try smaller file
- OpenRouter might be busy - try again

## Comparison: CLI vs Web UI

| Aspect | CLI | Web UI |
|--------|-----|--------|
| **Ease of Use** | Moderate | Very Easy |
| **Visual Feedback** | Text output | Real-time UI |
| **File Upload** | Command line | Drag & drop |
| **Team Sharing** | Manual download | Built-in |
| **Automation** | Easy scripting | Manual clicking |
| **Learning Curve** | Steeper | Gentle |
| **Best For** | Power users, automation | Interactive use, non-technical users |

## Next Steps

### Immediate
1. Install dependencies
2. Start the app
3. Test with sample_data.csv
4. Download a generated dashboard

### Short Term
1. Share web UI link with team
2. Let users test with their data
3. Gather feedback
4. Make customizations

### Medium Term
1. Deploy to cloud (Streamlit Cloud)
2. Set up for team access
3. Create user documentation
4. Monitor usage

## Summary

**Phase 6 delivers:**
- ✅ Streamlit web UI
- ✅ Drag-and-drop file upload
- ✅ Real-time progress indication
- ✅ Beautiful dashboard preview
- ✅ One-click download
- ✅ Configuration management
- ✅ Error handling
- ✅ Help documentation

**Benefits:**
- Non-technical users can generate dashboards
- No command line needed
- Beautiful, professional interface
- Real-time feedback
- Easy to share and deploy

**Ready to use!** 

```bash
cd ai_dashboard
streamlit run app.py
```

Then open your browser to `http://localhost:8501`

For detailed information, see [STREAMLIT_GUIDE.md](ai_dashboard/STREAMLIT_GUIDE.md)

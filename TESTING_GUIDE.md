# Testing Guide - AI Dashboard Generator

## Prerequisites

1. Install dependencies:
```bash
cd ai_dashboard
pip install -r requirements.txt
```

2. Set up OpenRouter API key:
```bash
export OPENROUTER_API_KEY="sk-or-v1-your-key-here"
```

---

## Test 1: Basic Functionality with Sample Data

### Step 1: Run Generator
```bash
cd ai_dashboard
python main.py ../sample_data.csv -o test_dashboard.html
```

### Expected Output
```
🚀 AI Dashboard Generator
--------------------------------------------------

📁 Loading data from: ../sample_data.csv
✓ Loaded 40 rows, 6 columns

🔍 Analyzing schema...
✓ Found 2 dimensions, 3 metrics

🤖 Analyzing data with AI...
✓ Dashboard title: Regional Sales Performance
✓ KPIs: ['sales', 'quantity']
✓ Charts: 3

📊 Aggregating data...
✓ Calculated 6 KPI metrics

📈 Generating charts...
  ✓ Chart 1: bar
  ✓ Chart 2: line
  ✓ Chart 3: pie

✍️  Generating insights...
✓ Generated 3 chart insights + overall summary

🎨 Building HTML dashboard...
✓ Dashboard saved to: /Users/tramynguyen/Work/AI_data_analysis/ai_dashboard/test_dashboard.html

==================================================
✅ Dashboard generation complete!
==================================================
```

### Step 2: Verify Output
```bash
# Check file was created
ls -lh test_dashboard.html

# Open in browser
open test_dashboard.html
```

### Expected Dashboard Features
✅ Professional header with gradient background
✅ 4 KPI cards showing Sales, Quantity, Customer Satisfaction metrics
✅ 3 interactive Plotly charts
✅ Chart insights below each chart
✅ Overall summary at bottom
✅ Responsive design (resize browser to test)

---

## Test 2: Test with Different Data Format

### Step 2a: Create Excel Test File
```bash
cd ai_dashboard
python -c "
import pandas as pd
df = pd.read_csv('../sample_data.csv')
df.to_excel('test_data.xlsx', index=False)
print('Created test_data.xlsx')
"
```

### Step 2b: Generate from Excel
```bash
python main.py test_data.xlsx -o excel_dashboard.html
```

### Expected
✅ Same output as CSV test
✅ File successfully loads and processes
✅ Results are identical to CSV version

---

## Test 3: Test with JSON Format

### Step 3a: Create JSON Test File
```bash
cd ai_dashboard
python -c "
import pandas as pd
df = pd.read_csv('../sample_data.csv')
df.to_json('test_data.json', orient='records')
print('Created test_data.json')
"
```

### Step 3b: Generate from JSON
```bash
python main.py test_data.json -o json_dashboard.html
```

### Expected
✅ File loads correctly
✅ Dashboard generates successfully
✅ Results match CSV version

---

## Test 4: Test Different AI Models

### Available Models to Test:
```bash
# Fast model (recommended)
python main.py ../sample_data.csv -m qwen/qwen3.5-9b -o model1.html

# More capable model
python main.py ../sample_data.csv -m qwen/qwen-max -o model2.html

# Open source model
python main.py ../sample_data.csv -m meta-llama/llama-2-70b-chat -o model3.html
```

### Comparison Metrics
- **Generation speed**: qwen3.5-9b should be fastest
- **Insight quality**: Observe chart insights and summary
- **Chart selection**: Check if different models pick different charts
- **KPI selection**: See if models prioritize different metrics

---

## Test 5: Test with Larger Dataset

### Step 5a: Create Larger Dataset
```bash
cd ai_dashboard
python -c "
import pandas as pd
df = pd.read_csv('../sample_data.csv')
# Expand dataset
df = pd.concat([df] * 100, ignore_index=True)
df.to_csv('large_dataset.csv', index=False)
print(f'Created large_dataset.csv with {len(df)} rows')
"
```

### Step 5b: Generate Dashboard
```bash
python main.py large_dataset.csv -o large_dashboard.html
```

### Verify
✅ Completes without errors
✅ Still generates responsive charts
✅ Top 20 items in each chart (for readability)
✅ All KPIs calculated correctly

---

## Test 6: Test Error Handling

### Test 6a: Missing API Key
```bash
unset OPENROUTER_API_KEY
python main.py ../sample_data.csv
```

### Expected
```
❌ Error loading file: OPENROUTER_API_KEY environment variable not set
```

### Fix
```bash
export OPENROUTER_API_KEY="your-key-here"
```

### Test 6b: Invalid File Path
```bash
python main.py nonexistent_file.csv
```

### Expected
```
❌ Error loading file: No such file or directory: 'nonexistent_file.csv'
```

### Test 6c: Unsupported Format
```bash
echo "test" > test.txt
python main.py test.txt
```

### Expected
```
❌ Error loading file: Unsupported file type: .txt
```

---

## Test 7: Validate HTML Output

### Step 7a: Check HTML Structure
```bash
cd ai_dashboard
python -c "
import re
with open('test_dashboard.html', 'r') as f:
    content = f.read()
    
checks = {
    'DOCTYPE': '<!DOCTYPE html>' in content,
    'Plotly Script': 'plotly-latest.min.js' in content,
    'Gradient Background': 'linear-gradient' in content,
    'KPI Cards': 'kpi-card' in content,
    'Chart Containers': 'chart-wrapper' in content,
    'Insights': 'chart-insight' in content,
    'Overall Summary': 'overall_summary' in content
}

for check, result in checks.items():
    status = '✓' if result else '✗'
    print(f'{status} {check}')
"
```

### Expected
```
✓ DOCTYPE
✓ Plotly Script
✓ Gradient Background
✓ KPI Cards
✓ Chart Containers
✓ Insights
✓ Overall Summary
```

### Step 7b: Validate Plotly JSON
```bash
python -c "
import json
import re
with open('test_dashboard.html', 'r') as f:
    content = f.read()

# Extract Plotly data
matches = re.findall(r'const chart_\d+ = ({.*?});', content, re.DOTALL)
print(f'Found {len(matches)} charts')

for i, match in enumerate(matches):
    try:
        chart_data = json.loads(match)
        has_data = 'data' in chart_data
        has_layout = 'layout' in chart_data
        print(f'Chart {i+1}: data={has_data}, layout={has_layout}')
    except:
        print(f'Chart {i+1}: Invalid JSON')
"
```

### Expected
```
Found 3 charts
Chart 1: data=True, layout=True
Chart 2: data=True, layout=True
Chart 3: data=True, layout=True
```

---

## Test 8: Browser Compatibility

### Browsers to Test
- ✅ Chrome/Chromium
- ✅ Firefox
- ✅ Safari
- ✅ Edge
- ✅ Mobile browsers (iPhone Safari, Chrome Mobile)

### What to Check
1. **KPI Cards**: Display correctly in grid
2. **Charts**: Render and respond to hover
3. **Responsiveness**: Resize window - layout adapts
4. **Interactions**: 
   - Hover over charts shows data
   - Click legend items to toggle series
   - Zoom and pan work
   - Download button available

---

## Test 9: Performance Testing

### Measure Generation Time
```bash
time python main.py ../sample_data.csv -o perf_test.html
```

### Expected Timing
- Schema detection: <1s
- LLM analysis: 2-5s (depends on API)
- Data aggregation: <1s
- Chart generation: <1s
- Narrative generation: 2-5s
- HTML assembly: <1s
- **Total: 5-15 seconds**

### Profile by File Size
```bash
# Small (40 rows)
time python main.py ../sample_data.csv

# Medium (4000 rows)
python -c "
import pandas as pd
df = pd.read_csv('../sample_data.csv')
df = pd.concat([df] * 100, ignore_index=True)
df.to_csv('medium.csv', index=False)
"
time python main.py medium.csv

# Large (40000 rows)
python -c "
import pandas as pd
df = pd.read_csv('../sample_data.csv')
df = pd.concat([df] * 1000, ignore_index=True)
df.to_csv('large.csv', index=False)
"
time python main.py large.csv
```

---

## Test 10: Customization Testing

### Test Custom Template Changes
```bash
# Backup original
cp templates/dashboard.html templates/dashboard.html.bak

# Edit template - change color
sed -i 's/#667eea/#00a86b/g' templates/dashboard.html

# Generate and verify new color
python main.py ../sample_data.csv -o color_test.html
open color_test.html

# Restore original
cp templates/dashboard.html.bak templates/dashboard.html
```

### Test Custom Prompt Changes
```bash
# Edit prompts.py to change AI behavior
# For example, modify the dashboard title instruction
# Then regenerate

python main.py ../sample_data.csv -o prompt_test.html
```

---

## Automated Test Script

Create `test_all.py`:

```python
#!/usr/bin/env python3
import os
import sys
from pathlib import Path

def run_test(name, command):
    print(f"\n{'='*60}")
    print(f"Test: {name}")
    print(f"{'='*60}")
    result = os.system(command)
    if result == 0:
        print(f"✅ {name} PASSED")
    else:
        print(f"❌ {name} FAILED")
    return result == 0

def main():
    os.chdir('ai_dashboard')
    
    tests = [
        ("CSV Input", "python main.py ../sample_data.csv -o test1.html"),
        ("Excel Input", "python main.py test_data.xlsx -o test2.html"),
        ("JSON Input", "python main.py test_data.json -o test3.html"),
        ("Custom Model", "python main.py ../sample_data.csv -m qwen/qwen-max -o test4.html"),
    ]
    
    results = []
    for name, cmd in tests:
        results.append(run_test(name, cmd))
    
    print(f"\n{'='*60}")
    print(f"SUMMARY: {sum(results)}/{len(results)} tests passed")
    print(f"{'='*60}")
    
    return 0 if all(results) else 1

if __name__ == "__main__":
    sys.exit(main())
```

Run it:
```bash
python test_all.py
```

---

## Validation Checklist

- [ ] Sample data generates dashboard
- [ ] CSV, Excel, JSON formats all work
- [ ] Different models produce different results
- [ ] Error handling works for invalid inputs
- [ ] HTML output is valid and displays correctly
- [ ] Charts are interactive in browser
- [ ] KPI cards show correct values
- [ ] Insights are generated and displayed
- [ ] Dashboard is responsive on mobile
- [ ] Performance is acceptable
- [ ] Custom changes apply correctly

---

## Troubleshooting Test Failures

| Failure | Debugging Steps |
|---------|-----------------|
| Dashboard not generating | Check API key set, check file format |
| Charts not displaying | Check HTML file exists, open in browser console |
| Insights empty | Check LLM response, try different model |
| Wrong KPI values | Verify data types in source file |
| Slow generation | Check internet connection, try faster model |

---

## Success!

When all tests pass, you have a fully functional AI Dashboard Generator! 🎉

See [QUICKSTART.md](QUICKSTART.md) for how to use it on your own data.

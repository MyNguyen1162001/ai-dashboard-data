# AI Data Analysis — Automated Dashboard Generator

## Overview

A tool that takes raw input data and automatically generates a polished PowerPoint dashboard using AI to handle layout, visualization, and narrative.

## The Problem

Turning raw data into a presentable PowerPoint dashboard is repetitive and time-consuming:
- Manually creating charts and summaries slide by slide
- Reformatting the same insights for different audiences (executives, analysts, stakeholders)
- Keeping dashboards up-to-date as data changes

## The Solution

Provide your data once. Get a ready-to-share PowerPoint dashboard.

```
Input Data  →  AI Analysis  →  PowerPoint Dashboard (.pptx)
(CSV, Excel,
 JSON, DB)
```

## Intended Workflow

1. **Input** — Drop in your data file (CSV, Excel, JSON, or connect a database)
2. **Configure** — Optionally describe the focus or target audience
3. **Generate** — AI analyzes the data, identifies key metrics, and builds the slides
4. **Export** — Receive a finished `.pptx` file ready to share

## Key Features (Planned)

- Automatic chart selection based on data type (bar, line, pie, table, KPI cards)
- AI-generated narrative summaries and insights per slide
- Consistent branding and layout
- Support for multiple data sources
- Re-generation on data refresh

## Project Status

> Early stage — defining scope and architecture.

## Tech Stack (Proposed)

- **AI/LLM** — Claude API for data interpretation and narrative generation
- **Python** — Core processing pipeline
- **python-pptx** — PowerPoint generation
- **pandas** — Data ingestion and transformation

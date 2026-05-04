# Review Insight System 🔍

AI-powered customer review analysis with sentiment classification, aspect detection, and product improvement recommendations.

## Features

- **Sentiment Analysis** — VADER-based classification (positive/negative/neutral)
- **Aspect Detection** — 12 product dimensions (battery, camera, display, etc.)
- **Keyword Extraction** — TF-IDF based important terms
- **Problem Detection** — Recurring issues with severity scoring
- **Recommendations** — Data-driven product improvement suggestions
- **Live Analyzer** — Real-time review analysis
- **Interactive Dashboard** — Charts, metrics, and insights

## Quick Start

### Option 1: Windows Batch Script
```bash
# Double-click start.bat or run:
start.bat
```

### Option 2: Manual Start
```bash
# Terminal 1 - API Server
python api.py

# Terminal 2 - Frontend
cd frontend
npm run dev
```

Then open: **http://localhost:3000**

## Architecture

```
Backend (Flask API)     Frontend (React + Vite)
├── /api/summary       ├── Dashboard (KPIs + Charts)
├── /api/aspects       ├── Aspects (Sentiment by Category)
├── /api/problems      ├── Reviews (Browse + Filter)
├── /api/keywords      ├── Analyzer (Live Text Analysis)
└── /api/analyze       └── Metrics (Model Evaluation)
```

## Tech Stack

**Backend:** Python, Flask, NLTK (VADER), scikit-learn, pandas
**Frontend:** React, Vite, Recharts, Axios
**ML Pipeline:** Preprocessing → Sentiment → Aspects → Keywords → Insights

## Data Flow

1. **Input:** Raw review text + rating
2. **Preprocessing:** Clean, tokenize, lemmatize
3. **Sentiment:** VADER polarity scoring
4. **Aspects:** Keyword taxonomy + window-based sentiment
5. **Insights:** Problem detection + recommendation generation
6. **Output:** JSON reports + interactive visualizations

Built with ❤️ using modern NLP and React
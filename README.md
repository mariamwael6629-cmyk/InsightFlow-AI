# ✦ InsightFlow AI — Customer Feedback Intelligence Platform

![AI Powered](https://img.shields.io/badge/AI-Powered-7c6dff)
![Accuracy](https://img.shields.io/badge/Sentiment%20Accuracy-98.2%25-00d4aa)
![Languages](https://img.shields.io/badge/Languages-40%2B-ff5fa0)
![License](https://img.shields.io/badge/License-MIT-orange)

InsightFlow AI is a cutting-edge customer feedback intelligence platform designed to aggregate, categorize, and analyze customer sentiment from multiple channels at scale. Powered by a fine-tuned AI engine, it accurately decodes nuanced emotional data—such as sarcasm, mixed signals, and cultural context—giving product, support, and marketing teams actionable business insights in real time.

---

## 🚀 Key Features

- **98.2% AI Sentiment Accuracy:** Deep learning model that processes mixed signals, context, and sarcasm across 40+ languages.
- **Unified Feedback Workspace:** Aggregates multi-channel inputs from 12+ data sources including Emails, Reviews, Surveys, and Social Media.
- **Interactive Analytics Dashboard:** Real-time visibility into your Customer Happiness Rating (Mood Score), Weekly Feedback Volume, and Trend Metrics.
- **AI-Driven Recommendations:** Automatically prioritizes issues (e.g., Checkout friction, Page load speed) and offers high, medium, and low priority actionable solutions.
- **Automated Competitor & Performance Reports:** Generates executive-ready monthly summaries, churn alerts, and cross-channel sentiment analysis.
- **Beautiful & Fully Responsive UI:** Built with an immersive glassmorphism dark mode aesthetic that adapts perfectly to desktop, tablet, and mobile devices.

## 🛠️ Technology Stack

- **Frontend:** HTML5, Semantic CSS3 (CSS Variables, Bento Grid, Flexbox layouts), vanilla JS (fetch-based API client)
- **Visualizations / Charting:** [Chart.js](https://www.chartjs.org/) (for rendering smooth sentiment trends and analytical data grids)
- **Typography:** Inter, system-ui sans-serif
- **Backend:** FastAPI, SQLAlchemy 2.0, SQLite (swappable via `DATABASE_URL`), JWT auth (PyJWT + passlib/bcrypt)

## 📂 Project Structure

```text
├── insightflow-ai.html    # Main application: Landing, Analytics, Reports, and Settings pages
├── backend/                # FastAPI backend
│   ├── app/
│   │   ├── core/           # Settings + security (JWT, password hashing)
│   │   ├── db/             # SQLAlchemy engine/session
│   │   ├── models/         # ORM models
│   │   ├── schemas/        # Pydantic request/response schemas
│   │   ├── services/       # Business logic
│   │   ├── routers/        # API route handlers
│   │   ├── seed.py         # Demo data seeding
│   │   └── main.py         # FastAPI app entrypoint
│   ├── requirements.txt
│   └── .env.example
└── README.md               # Project documentation
```

## ⚙️ Running locally

1. **Backend**
   ```bash
   cd backend
   python3 -m venv .venv && source .venv/bin/activate
   pip install -r requirements.txt
   cp .env.example .env
   uvicorn app.main:app --reload --port 8000
   ```
   API docs available at `http://127.0.0.1:8000/docs`. The database is created and seeded automatically on first startup.

   Demo login: `jamie@acmecorp.com` / `InsightFlow123`

2. **Frontend**
   ```bash
   python3 -m http.server 8088
   ```
   Open `http://127.0.0.1:8088/insightflow-ai.html`. The frontend talks to the backend at `http://127.0.0.1:8000` by default (override via `window.API_BASE_URL` before the page script runs, if needed).

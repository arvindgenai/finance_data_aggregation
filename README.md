# 📊 Financial Data Aggregator & GenAI Insight Engine

This project is a Python-based backend system that ingests real-time financial NSE STOCK data (e.g., "RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS", "ICICIBANK.NS"), calculates performance metrics, and generates insights using GenAI (mocked or real). It exposes a set of RESTful API endpoints for interacting with the data and triggering updates.

---

## 🚀 Features

- Real-time data fetching using `yfinance`
- Calculates financial metrics like 24h % change and 7-day average
- Async processing with FastAPI and background tasks
- GenAI-based market summary generation (can be mocked)
- REST API endpoints to access metrics, compare assets, trigger ingestion, and view summary
- Includes unit and integration testing
- Uses clean architecture with modular code

---

## ⚙️ Requirements

Install the required dependencies:

```bash
pip install -r requirements.txt

##  requirements.txt contents:
fastapi
uvicorn
httpx
yfinance
python-dotenv
pytest

Setup Instructions
git clone https://github.com/arvindgenai/finance_data_aggregation.git
cd finance_data_aggregation


Create .env File

GROQ_API_KEY=your_groq_api_key_here


Run the Application
uvicorn main:app --reload

Open in Browser

Base URL: http://localhost:8000

Swagger docs: http://localhost:8000/docs

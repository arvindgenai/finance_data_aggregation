from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import httpx
import asyncio
import os
import yfinance as yf


GROQ_API_KEY = os.getenv("GROQ_API_KEY")  # Or hardcode for testing
print(GROQ_API_KEY)

router = APIRouter()

async def fetch_asset_data_sum(symbol: str) -> list[dict]:
    def get_data():
        return yf.Ticker(symbol).history(period="7d")

    data = await asyncio.to_thread(get_data)

    if data.empty:
        raise HTTPException(status_code=404, detail=f"No data for symbol {symbol}")

    return data.reset_index().to_dict(orient="records")

# ------------------- Calculate Metrics -------------------
def calculate_metrics_data(data: list[dict]) -> dict:
    prices = [row['Close'] for row in data if 'Close' in row]
    change_percent_24h = ((prices[-1] - prices[-2]) / prices[-2]) * 100 if len(prices) >= 2 else 0
    average_price_7d = sum(prices) / len(prices) if prices else 0
    return {
        "change_percent_24h": round(change_percent_24h, 2),
        "average_price_7d": round(average_price_7d, 2)
    }

# ------------------- GenAI Summary Generator -------------------
async def generate_summary(prompt: str) -> str:
    GROQ_API_KEY = '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'
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "messages": [
            {"role": "system", "content": "You are a financial data summarizer."},
            {"role": "user", "content": prompt}
        ],
        "model": "llama-3.3-70b-versatile"
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=payload
        )
        response.raise_for_status()
        result = response.json()
        return result["choices"][0]["message"]["content"]

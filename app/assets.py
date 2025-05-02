# api/assets.py
from fastapi import APIRouter
from models import MetricsResponse
import yfinance as yf

router = APIRouter()

async def fetch_asset_data(symbol: str):
    ticker = yf.Ticker(symbol)
    df = ticker.history(period="7d")
    return df

def calculate_metrics(df):
    latest_price = df['Close'][-1]
    price_24h_ago = df['Close'][-2]
    change_24h = ((latest_price - price_24h_ago) / price_24h_ago) * 100
    avg_7d = df['Close'].mean()

    return {
        "latest_price": latest_price,
        "change_percent_24h": change_24h,
        "average_price_7d": avg_7d
    }

@router.get("/metrics/{symbol}", response_model=MetricsResponse)
async def get_metrics(symbol: str):
    df = await fetch_asset_data(symbol)
    metrics = calculate_metrics(df)
    return {"symbol": symbol, **metrics}

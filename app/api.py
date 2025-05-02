from fastapi import APIRouter
from app.ingestion import fetch_asset_data_sum, calculate_metrics_data,generate_summary
from app.processing import calculate_metrics, fetch_asset_data_compare
from app.models import MetricsResponse , SummaryResponse
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import asyncio
import logging

# api/assets.py
from fastapi import APIRouter
import yfinance as yf

router = APIRouter()

# List of symbols for NSE stocks
symbols = [
    "RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS", "ICICIBANK.NS",
   # "HINDUSTANI.NS", "LT.NS", "BAJFINANCE.NS", "KOTAKBANK.NS", "SBIN.NS"
]


# Fetch stock data and calculate metrics
def fetch_metrics(symbols):
    metrics = {}
    for symbol in symbols:
        ticker = yf.Ticker(symbol)
        df = ticker.history(period="7d")  # Get the last 7 days of data

        latest_price = df['Close'][-1]  # Latest closing price
        price_24h_ago = df['Close'][-2]  # Price 24 hours ago
        change_24h = ((latest_price - price_24h_ago) / price_24h_ago) * 100  # 24h change in percentage

        avg_7d = df['Close'].mean()  # 7-day average price

        metrics[symbol] = {
            "latest_price": latest_price,
            "change_percent_24h": change_24h,
            "average_price_7d": avg_7d
        }
    return metrics


@router.get("/assets")
async def list_assets():
    # Fetch and calculate metrics for each stock
    metrics = fetch_metrics(symbols)

    # Prepare the response with asset names and their metrics
    assets_info = []
    for symbol in symbols:
        assets_info.append({
            "symbol": symbol,
            "latest_price": metrics[symbol]["latest_price"],
            "change_percent_24h": metrics[symbol]["change_percent_24h"],
            "average_price_7d": metrics[symbol]["average_price_7d"]
        })

    return assets_info

@router.get("/metrics/{symbol}", response_model=MetricsResponse)
def get_metrics(symbol: str):
    print("symbol type in get matrix function",type(symbol))
    df =  fetch_asset_data(symbol)
    print("fetch_asset_data type",type(df),"")
    metrics = calculate_metrics(df) # df is dict jo  calculate_metrics pass hai
    return {"symbol": symbol, **metrics}


@router.get("/compare")
async def compare_assets(asset1: str, asset2: str):
    logging.info(f"Comparing assets: {asset1} and {asset2}")

    # Fetch data asynchronously
    data1 = await fetch_asset_data_compare(asset1)
    data2 = await fetch_asset_data_compare(asset2)

    logging.info(f"Data for {asset1}: {data1}")
    logging.info(f"Data for {asset2}: {data2}")

    # Calculate metrics
    metrics1 = calculate_metrics(data1)
    metrics2 = calculate_metrics(data2)

    logging.info(f"Metrics for {asset1}: {metrics1}")
    logging.info(f"Metrics for {asset2}: {metrics2}")

    return {
        "comparison": {
            asset1: metrics1,
            asset2: metrics2
        }
    }

@router.get("/summary", response_model=SummaryResponse)
async def get_market_summary():
    results = await asyncio.gather(*[fetch_asset_data_sum(symbol) for symbol in symbols])
    print("symbol data ",results)
    summaries = []
    for symbol, data in zip(symbols, results):
        metrics = calculate_metrics_data(data)
        summaries.append(
            f"{symbol}: 24h change {metrics['change_percent_24h']}%, "
            f"7d avg price {metrics['average_price_7d']}$"
        )

    prompt = "Summarize the performance of the following Indian stocks:\n" + "\n".join(summaries)
    summary = await generate_summary(prompt)

    return {"summary": summary}


class IngestRequest(BaseModel):
    symbol: str

def fetch_asset_data(symbol: str) -> dict:
    try:
        ticker = yf.Ticker(symbol)
        data = ticker.history(period="7d")
        print("fetch_asset_data ka type", type(data))  # Should be <class 'pandas.DataFrame'>
        print(data)

        if data.empty:
            raise ValueError(f"No data found for {symbol}")

        # Converting DataFrame to a dictionary format that can be passed to calculate_metrics
        data_dict = data.to_dict(orient='records')  # Converts the DataFrame to a list of dicts
        return data_dict  # Return as list of dictionaries

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/ingest")
async def ingest_data(request: IngestRequest):
    result = await fetch_asset_data(request.symbol)
    return result
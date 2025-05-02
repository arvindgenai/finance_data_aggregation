from fastapi import APIRouter
import yfinance as yf
import pandas as pd

router = APIRouter()
def calculate_metrics(data):
    # If input is a list of dicts, convert it to DataFrame
    if isinstance(data, list):
        df = pd.DataFrame(data)
    elif isinstance(data, dict):
        df = pd.DataFrame([data])  # Just in case it's a single dict
    elif isinstance(data, pd.DataFrame):
        df = data
    else:
        raise ValueError("Unsupported data format")

    if df.empty or "Close" not in df.columns:
        return {
            "latest_price": 0.0,
            "change_percent_24h": 0.0,
            "average_price_7d": 0.0,
        }

    # Calculate metrics
    latest_price = df["Close"].iloc[-1]
    previous_price = df["Close"].iloc[-2]
    change_percent_24h = ((latest_price - previous_price) / previous_price) * 100
    average_price_7d = df["Close"].mean()

    return {
        "latest_price": round(latest_price, 2),
        "change_percent_24h": round(change_percent_24h, 2),
        "average_price_7d": round(average_price_7d, 2),
    }



import yfinance as yf
from fastapi import HTTPException

import yfinance as yf
import pandas as pd
from fastapi import HTTPException
import asyncio


async def fetch_asset_data_compare(symbol: str) -> list[dict]:
    print(f"Fetching data for symbol: {symbol}")

    try:
        # Define the function to fetch data from yfinance
        def get_data():
            ticker = yf.Ticker(symbol)
            return ticker.history(period="7d")

        # Run the blocking function in a separate thread
        data = await asyncio.to_thread(get_data)

        # Print the type and contents of the fetched data for debugging
        print(f"Fetched data type: {type(data)}")  # Should be pandas DataFrame
        print(data)

        # Check if the data is empty and raise an error if so
        if data.empty:
            raise ValueError(f"No data found for symbol: {symbol}")

        # Convert DataFrame to list of dictionaries
        data_dict = data.reset_index().to_dict(orient="records")

        return data_dict

    except ValueError as e:
        # Catch specific exception for missing data
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        # Catch all other exceptions
        raise HTTPException(status_code=400, detail=f"Error fetching data for {symbol}: {str(e)}")
# async def fetch_asset_data_compare(symbol: str) -> list[dict]:
#     print('symbol >>>>>>', symbol)
#     try:
#         def get_data():
#             ticker = yf.Ticker(symbol)
#             return ticker.history(period="7d")
#
#         data = await asyncio.to_thread(get_data)
#
#         print("fetch_asset_data ka type:", type(data))  # pandas DataFrame
#         print(data)
#
#         if data.empty:
#             raise ValueError(f"No data found for symbol: {symbol}")
#
#         data_dict = data.reset_index().to_dict(orient="records")
#         return data_dict
#
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))
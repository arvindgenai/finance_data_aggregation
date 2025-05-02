from pydantic import BaseModel

class MetricsResponse(BaseModel):
    symbol: str
    latest_price: float
    change_percent_24h: float
    average_price_7d: float

class SummaryResponse(BaseModel):
    summary: str

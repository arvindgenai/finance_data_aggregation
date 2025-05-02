from app.processing import calculate_metrics

def test_calculate_metrics():
    dummy_data = {'Close': {'2024-04-25': 100, '2024-04-26': 110}}
    metrics = calculate_metrics(dummy_data)
    assert metrics["latest_price"] == 110
    assert round(metrics["change_percent_24h"], 2) == 10.00
    assert metrics["average_price_7d"] == 105.0

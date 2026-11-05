import yfinance as yf
import pandas as pd

def download_data(tickers, index, total_years):
    prezzi = yf.download(tickers, period=total_years, progress=False)["Close"]
    benchmark_raw = yf.download(index, period="20y", progress=False)["Close"]

    # Gestisci MultiIndex di yfinance
    if isinstance(prezzi.columns, pd.MultiIndex):
        prezzi.columns = prezzi.columns.get_level_values(0)

    prezzi = prezzi[tickers]

    # Forza benchmark a Series
    if isinstance(benchmark_raw, pd.DataFrame):
        benchmark = benchmark_raw.squeeze()
    else:
        benchmark = benchmark_raw
    
    return prezzi, benchmark
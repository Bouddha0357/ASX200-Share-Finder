import yfinance as yf
import pandas as pd
import numpy as np

def get_asx200_tickers():
    # Replace or scrape the full ASX200 list
    return ['CBA.AX', 'BHP.AX', 'WES.AX', 'CSL.AX', 'NAB.AX']

def get_ratios(tickers):
    pe_ratios = {}
    pb_ratios = {}

    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            info = stock.info

            pe = info.get('trailingPE')
            pb = info.get('priceToBook')

            if pe is not None and pe > 0:
                pe_ratios[ticker] = pe
            if pb is not None and pb > 0:
                pb_ratios[ticker] = pb

        except Exception as e:
            print(f"Error retrieving data for {ticker}: {e}")

    return pe_ratios, pb_ratios

def calculate_average(ratios):
    values = [v for v in ratios.values() if v is not None and v > 0]
    return np.mean(values) if values else None

def filter_below_average(ratios, average):
    return [ticker for ticker, val in ratios.items() if val < average]

def get_latest_moving_averages(ticker, days=180):
    try:
        data = yf.download(ticker, period=f'{days}d')
        if data.empty

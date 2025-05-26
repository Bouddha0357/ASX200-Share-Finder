import yfinance as yf
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import time

# Step 1: Get ASX200 Tickers from MarketIndex
def get_asx200_tickers():
    print("Fetching ASX200 tickers from Market Index website...")
    url = 'https://www.marketindex.com.au/asx200'
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        tickers = []
        table = soup.find('table', {'class': 'table'})
        if table:
            rows = table.find_all('tr')[1:]  # Skip header row
            for row in rows:
                cols = row.find_all('td')
                if cols:
                    ticker = cols[0].text.strip()
                    tickers.append(f"{ticker}.AX")
        print(f"Found {len(tickers)} tickers.")
        return tickers
    except Exception as e:
        print(f"Failed to fetch tickers: {e}")
        return []

# Step 2: Get P/E and P/B ratios, skip tickers with missing/invalid data
def get_ratios(tickers):
    pe_ratios = {}
    pb_ratios = {}

    for idx, ticker in enumerate(tickers, 1):
        try:
            print(f"Fetching ratios for {ticker} ({idx}/{len(tickers)})...")
            stock = yf.Ticker(ticker)
            info = stock.info

            pe = info.get('trailingPE')
            pb = info.get('priceToBook')

            if pe is None or pe <= 0 or pb is None or pb <= 0:
                print(f"Skipping {ticker} due to missing/invalid P/E or P/B.")
                continue

            pe_ratios[ticker] = pe
            pb_ratios[ticker] = pb

            time.sleep(0.1)  # tiny pause to be polite to Yahoo servers

        except Exception as e:
            print(f"Error retrieving data for {ticker}: {e}")
            time.sleep(1)  # pause a bit on error
            continue

    return pe_ratios, pb_ratios

# Step 3: Average calculation and filtering
def calculate_average(ratios):
    values = [v for v in ratios.values() if v is not None and v > 0]
    return np.mean(values) if values else None

def filter_below_average(ratios, average):
    return [ticker for ticker, val in ratios.items() if val < average]

# Step 4: Get moving averages
def get_latest_moving_averages(ticker, days=180):
    try:
        print(f"Downloading price data for {ticker}...")
        data = yf.download(ticker, period=f'{days}d', progress=False)
        if data.empty:
            print(f"No price data for {ticker}")
            return None, None

        data['MA20'] = data['Close'].rolling(window=20).mean()
        data['MA50'] = data['Close'].rolling(window=50).mean()

        latest = data.dropna().iloc[-1]
        return latest['MA20'], latest['MA50']
    except Exception as e:
        print(f"Failed to download price data for {ticker}: {e}")
        return None, None

# Step 5: Main Logic
def main():
    tickers = get_asx200_tickers()
    if not tickers:
        print("❌ No tickers found! Exiting.")
        return

    pe_ratios, pb_ratios = get_ratios(tickers)

    print(f"P/E ratios found for {len(pe_ratios)} companies.")
    print(f"P/B ratios found for {len(pb_ratios)} companies.")

    avg_pe = calculate_average(pe_ratios)
    avg_pb = calculate_average(pb_ratios)

    if avg_pe is None or avg_pb is None:
        print("⚠️ Unable to calculate averages — no valid P/E or P/B data found.")
        return

    below_avg_pe = filter_below_average(pe_ratios, avg_pe)
    below_avg_pb = filter_below_average(pb_ratios, avg_pb)

    final_tickers = list(set(below_avg_pe) & set(below_avg_pb))
    print(f"\nAverage P/E: {avg_pe:.2f}")
    print(f"Average P/B: {avg_pb:.2f}")
    print(f"Companies with P/E and P/B below average: {len(final_tickers)}")

    if not final_tickers:
        print("❌ No companies matched the criteria. Exiting.")
        return

    print("Calculating moving averages and preparing CSV data...")
    csv_data = []
    for ticker in final_tickers:
        pe = pe_ratios.get(ticker)
        pb = pb_ratios.get(ticker)
        ma20, ma50 = get_latest_moving_averages(ticker)

        csv_data.append({
            'Ticker': ticker,
            'P/E Ratio': pe,
            'P/B Ratio': pb,
            'Latest MA20': ma20,
            'Latest MA50': ma50
        })

    df = pd.DataFrame(csv_data)
    df.to_csv('filtered_asx200_companies.csv', index=False)
    print("\n✅ Results exported to 'filtered_asx200_companies.csv'")

if __name__ == "__main__":
    main()

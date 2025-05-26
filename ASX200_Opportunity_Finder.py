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
        if data.empty:
            return None, None

        data['MA20'] = data['Close'].rolling(window=20).mean()
        data['MA50'] = data['Close'].rolling(window=50).mean()

        latest = data.dropna().iloc[-1]
        return latest['MA20'], latest['MA50']
    except Exception as e:
        print(f"Failed to download price data for {ticker}: {e}")
        return None, None

# === Main Logic ===
tickers = get_asx200_tickers()

pe_ratios, pb_ratios = get_ratios(tickers)

avg_pe = calculate_average(pe_ratios)
avg_pb = calculate_average(pb_ratios)

below_avg_pe = filter_below_average(pe_ratios, avg_pe)
below_avg_pb = filter_below_average(pb_ratios, avg_pb)

final_tickers = list(set(below_avg_pe) & set(below_avg_pb))

print(f"\nAverage P/E: {avg_pe:.2f}")
print(f"Average P/B: {avg_pb:.2f}")
print(f"\nCompanies with P/E and P/B below average: {final_tickers}")

# Prepare CSV data
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

# Export to CSV
df = pd.DataFrame(csv_data)
df.to_csv('filtered_asx200_companies.csv', index=False)

print("\n✅ Results exported to 'filtered_asx200_companies.csv'")

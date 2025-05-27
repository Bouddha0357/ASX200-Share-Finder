import yfinance as yf
import pandas as pd
import time

# ✅ You can replace or extend this with the full ASX 200 list
ASX200_TICKERS = [
    'CBA.AX', 'BHP.AX', 'WBC.AX', 'CSL.AX', 'NAB.AX',
    'WES.AX', 'ANZ.AX', 'MQG.AX', 'WOW.AX', 'TLS.AX'
    # Add more tickers here...
]

def fetch_pe_pb(tickers):
    results = []

    for ticker in tickers:
        try:
            print(f"Fetching {ticker}...")
            stock = yf.Ticker(ticker)
            info = stock.info

            pe = info.get('trailingPE')
            pb = info.get('priceToBook')

            if pe is not None and pb is not None:
                results.append({
                    'Ticker': ticker,
                    'P/E Ratio': pe,
                    'P/B Ratio': pb
                })
            else:
                print(f"Skipping {ticker} (missing data)")

            time.sleep(0.2)

        except Exception as e:
            print(f"Error fetching {ticker}: {e}")
            continue

    return results

def main():
    data = fetch_pe_pb(ASX200_TICKERS)

    if not data:
        print("❌ No data fetched.")
        return

    df = pd.DataFrame(data)
    df.to_csv("asx200_pe_pb.csv", index=False)
    print(f"\n✅ Fetched data for {len(df)} companies. Saved to 'asx200_pe_pb.csv'")

if __name__ == "__main__":
    main()

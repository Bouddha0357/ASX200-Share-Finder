import yfinance as yf
import pandas as pd
import time

TICKERS = [
    'CBA.AX', 'BHP.AX', 'WBC.AX', 'CSL.AX', 'NAB.AX',
    'WES.AX', 'ANZ.AX', 'MQG.AX', 'WOW.AX', 'TLS.AX'
]

def fetch_pe_ratios(tickers):
    data = []
    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            pe = info.get('trailingPE')
            if pe is not None and pe > 0:
                data.append({'Ticker': ticker, 'P/E Ratio': pe})
            time.sleep(0.2)  # brief pause to avoid rate limits
        except:
            continue
    return data

def main():
    results = fetch_pe_ratios(TICKERS)
    if results:
        df = pd.DataFrame(results)
        df.to_csv("asx200_pe_ratios.csv", index=False)

if __name__ == "__main__":
    main()

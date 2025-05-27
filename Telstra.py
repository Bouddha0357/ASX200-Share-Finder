import yfinance as yf

def get_share_price(ticker_symbol):
    ticker = yf.Ticker(ticker_symbol)
    try:
        price = ticker.info.get("regularMarketPrice")
        if price is not None:
            print(f"{ticker_symbol} Current Share Price: ${price:.2f}")
        else:
            print(f"{ticker_symbol}: Share price not available.")
    except Exception as e:
        print(f"Error fetching data for {ticker_symbol}: {e}")

if __name__ == "__main__":
    get_share_price("TLS.AX")  # Telstra

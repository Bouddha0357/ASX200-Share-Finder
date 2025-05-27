import yfinance as yf

ticker = yf.Ticker("TLS.AX")
info = ticker.info

# Print all available keys and values
for key, value in info.items():
    print(f"{key}: {value}")

import yfinance as yf

ticker = yf.Ticker("TLS.AX")
info = ticker.info
pe_ratio = info.get("trailingPE")

if pe_ratio is not None:
    print(f"Telstra (TLS.AX) P/E Ratio: {pe_ratio:.2f}")
else:
    print("P/E Ratio not available.")

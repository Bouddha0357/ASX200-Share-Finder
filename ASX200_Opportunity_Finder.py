import yfinance as yf
import tkinter as tk

def get_pe_ratio():
    try:
        ticker = yf.Ticker("TLS.AX")
        pe = ticker.info.get('trailingPE')
        if pe is not None:
            result_label.config(text=f"P/E Ratio for Telstra (TLS.AX): {pe:.2f}")
        else:
            result_label.config(text="P/E ratio not available.")
    except Exception as e:
        result_label.config(text=f"Error fetching data: {e}")

# GUI setup
root = tk.Tk()
root.title("Telstra P/E Ratio")

root.geometry("300x150")
root.resizable(False, False)

title_label = tk.Label(root, text="Click to get Telstra's P/E Ratio", font=("Arial", 12))
title_label.pack(pady=10)

get_button = tk.Button(root, text="Fetch P/E Ratio", command=get_pe_ratio)
get_button.pack(pady=5)

result_label = tk.Label(root, text="", font=("Arial", 11))
result_label.pack(pady=10)

root.mainloop()

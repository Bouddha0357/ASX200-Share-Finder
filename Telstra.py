import requests
from bs4 import BeautifulSoup
import csv

def get_pb_ratio(ticker):
    url = f"https://finance.yahoo.com/quote/{ticker}/key-statistics"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"Failed to retrieve data for {ticker}")
        return None
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Yahoo's key statistics P/B ratio is in a table, look for "Price/Book (mrq)"
    try:
        rows = soup.find_all('tr')
        for row in rows:
            cells = row.find_all('td')
            if len(cells) == 2 and "Price/Book (mrq)" in cells[0].text:
                pb = cells[1].text.strip()
                return pb
    except Exception as e:
        print(f"Error parsing data for {ticker}: {e}")
        return None
    
    return None

# Example usage for Telstra
ticker = "TLS.AX"
pb_ratio = get_pb_ratio(ticker)
print(f"{ticker} P/B Ratio: {pb_ratio}")

# Save to CSV
with open('pb_ratios.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Ticker', 'P/B Ratio'])
    writer.writerow([ticker, pb_ratio])

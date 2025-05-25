# 1.	Yahoo Finance
import pandas as pd

# Get list of S&P 500 companies from Wikipedia
url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
sp500_table = pd.read_html(url)[0]
symbols = sp500_table['Symbol'].tolist()

# Clean up special cases
symbols = [symbol.replace(".", "-") for symbol in symbols]  # e.g., BRK.B becomes BRK-B

# Step 2: Install and Use yfinance to Pull Minute-Level OHLCV Data

#pip install yfinance

import yfinance as yf

# Example: Download 1-day minute data for AAPL
ticker = yf.Ticker("AAPL")
data = ticker.history(interval="1m", period="1d")

print(data.head())

# Step 3: Loop Through All Symbols (Limited Due to API Restrictions)

#You can’t call all 500 tickers at once — Yahoo Finance throttles. Start with ~5–10 symbols.

from time import sleep

ohlcv_data = {}

for symbol in symbols[:10]:  # Test with first 10 symbols
    try:
        ticker = yf.Ticker(symbol)
        df = ticker.history(interval="1m", period="1d")
        ohlcv_data[symbol] = df
        print(f"Fetched {symbol}")
        sleep(1)  # Be polite to avoid being blocked
    except Exception as e:
        print(f"Failed for {symbol}: {e}")


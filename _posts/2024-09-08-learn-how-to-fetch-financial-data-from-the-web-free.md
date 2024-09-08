---
layout: single
title: "5 Free Python Tools to Fetch Financial Data from the Web (2024 Edition)"
excerpt: "In this post, we’ll explore 5 free Python tools that let you grab financial information right from the web."
type: post
header:
    overlay_color: "#333"
classes: wide
published: true
comments: true
categories:  
    - finance
tags:
    - python
    - english articles
---

# 5 Free Python Tools to Fetch Financial Data from the Web (2024 Edition)

If you’re into finance and Python, you’re probably always on the lookout for ways to fetch financial data efficiently—and preferably, without breaking the bank (or blowing up your API limits). In this post, we’ll explore 5 free Python tools that let you grab financial information right from the web. We’ll cover the pros, cons, and throw in a small type-checked Python snippet for each. Let’s dive in!

## 1. Pandas DataReader
The good old reliable tool for financial data retrieval. [Pandas DataReader](https://pandas-datareader.readthedocs.io/en/latest/) is an extension of the Pandas library. It allows you to pull financial data from multiple online sources like Yahoo Finance, FRED, and more.

**Pros:**
- Easy to use, familiar Pandas syntax.
- Can fetch data from multiple sources.

**Cons:**
- Yahoo Finance API is no longer supported, so some features may break.
- Limited to pre-set data providers.

**Example**
```python
import pandas_datareader as pdr
from datetime import datetime
from typing import Any

def get_stock_data(stock: str, start: str, end: str) -> Any:
    start_date = datetime.strptime(start, "%Y-%m-%d")
    end_date = datetime.strptime(end, "%Y-%m-%d")
    return pdr.get_data_yahoo(stock, start=start_date, end=end_date)

# Example usage
# df = get_stock_data("AAPL", "2022-01-01", "2022-12-31")

```

## 2. Alpha Vantage
A free, API-based service for retrieving real-time and historical financial data. [Alpha Vantage](https://www.alphavantage.co/documentation/) offers free access to stock prices, FX rates, and more. It has a straightforward API you can use in your Python code.

**Pros:**
- Free API with 500 requests per day (enough for small projects).
- Wide range of data: stocks, forex, crypto, and technical indicators.

**Cons:**
- Has a requests limit: 5 requests per minute.
- Requires an API key, so there’s some setup required.

**Example:**

```python
import requests
from typing import Any

def get_alpha_vantage_data(api_key: str, symbol: str) -> Any:
    url = f"https://www.alphavantage.co/query"
    params = {
        'function': 'TIME_SERIES_DAILY',
        'symbol': symbol,
        'apikey': api_key
    }
    response = requests.get(url, params=params)
    return response.json()

# Example usage
# api_key = "YOUR_API_KEY"
# data = get_alpha_vantage_data(api_key, "AAPL")
```

## 4. yFinance
The successor to the now defunct Yahoo Finance API. [yFinance](https://python-yahoofinance.readthedocs.io/en/latest/api.html) is a Python wrapper for Yahoo Finance that provides financial data, stock prices, historical data, and more.

**Pros:**
- No API key required, super simple to use.
- Supports historical and real-time data.
- Convenient with pandas-like DataFrame outputs.

**Cons:**
- Not as fast as API-based services like Alpha Vantage.
- Rate-limited, though it’s not always clear what those limits are.

**Example:**

```python
import yfinance as yf
from typing import Any

def get_yfinance_data(ticker: str) -> Any:
    stock = yf.Ticker(ticker)
    return stock.history(period="1y")

# Example usage
# df = get_yfinance_data("AAPL")

```

## 4. Yahoo_fin
An alternative Yahoo Finance scraper, great for pulling stock prices. [yahoo_fin](https://python-yahoofinance.readthedocs.io/en/latest/api.html) lets you scrape financial data from Yahoo Finance, including stock prices, historical data, and financials.

**Pros:**
- No API key, and no strict request limits.
- Can pull options and historical prices.

**Cons:**
- Slower than API solutions since it scrapes HTML.
- Not as robust for large data sets.

**Example:**

```python
from yahoo_fin import stock_info
from typing import Any

def get_yahoo_fin_data(ticker: str) -> Any:
    return stock_info.get_data(ticker)

# Example usage
# df = get_yahoo_fin_data("AAPL")
```

## 5. Nasdaq Data Link (formerly Quandl)

[Nasdaq Data Link](https://docs.data.nasdaq.com/docs/python-installation) is the successor to Quandl, offering access to a wide range of financial, economic, and alternative datasets. You can still access historical stock prices, commodities, economic indicators, and more, just like you could with Quandl, but under the new branding.

**Pros:**
- Extensive dataset library: Includes stock data, commodities, alternative datasets, and economic indicators.
- API remains simple and familiar if you’ve used Quandl before.
- Free tier available with access to many datasets.

**Cons:**
- Requires API key for all requests.
- Limited free API requests (50 per day on the free tier, more for paid).
- Some premium datasets are behind a paywall.

**Example:**

```python
import nasdaqdatalink
from typing import Any

def get_nasdaq_data(api_key: str, dataset: str) -> Any:
    """
    Fetches financial or economic data from Nasdaq Data Link.

    Args:
    api_key (str): Your Nasdaq Data Link API key.
    dataset (str): The dataset code to fetch (e.g., 'WIKI/AAPL').

    Returns:
    pd.DataFrame: A DataFrame containing the requested dataset.
    """
    nasdaqdatalink.ApiConfig.api_key = api_key
    return nasdaqdatalink.get(dataset)

# Example usage
# api_key = "YOUR_API_KEY"
# data = get_nasdaq_data(api_key, "WIKI/AAPL")

```

## Bonus: Yahoo Finance API Changes - No More CSV Downloads 😔
For years, many of us have relied on downloading CSV files directly from Yahoo Finance's website to get historical stock data with ease. Unfortunately, Yahoo Finance recently changed its API, and downloading CSV files directly from the site is no longer an option.

This means that the good old "download as CSV" trick is gone, and you’ll have to rely on tools like yFinance or other APIs to fetch this data programmatically.

While yFinance does a great job of fetching data in Python, if you were used to working with raw CSV files, you might need to rework your process.

I know, it’s a bummer. But don’t worry! I’ve got your back. I created these functions to take care of that job for you, so you don’t have to worry about downloading those files manually anymore. You can now fetch the same data with just a few lines of Python!

```python 
from time import sleep
import requests
from datetime import datetime as dt
from dateutil.relativedelta import relativedelta
import pandas as pd
from tqdm import tqdm


def get_range(range_from, end_date):

    accepted_values = ['3m', '9m', '1y', '5y', '10y']
    if range_from not in accepted_values:
        raise Exception('Invalid from value')
    
    if range_from == '3m':
        start_date = end_date - relativedelta(months=3)
    if range_from == '9m':
        start_date = end_date - relativedelta(months=9)
    if range_from == '1y':
        start_date = end_date - relativedelta(years=1)
    if range_from == '5y':
        start_date = end_date - relativedelta(years=5)
    if range_from == '10y':
        start_date = end_date - relativedelta(years=10)
    
    return str(start_date), str(end_date)


def get_range_timestamps(start_date, end_date):

    start_date = str(dt.strptime(start_date, "%Y-%m-%d")
        .timestamp()) \
        .replace('.0', '')

    end_date = str(dt.strptime(end_date, "%Y-%m-%d")
        .timestamp()) \
        .replace('.0', '')

    return start_date, end_date


def get_portfolio(assets, from_='3m', start_date=None, end_date=dt.now().date()):

    portfolio = pd.DataFrame()

    for i, asset in tqdm(enumerate(assets), total = len(assets)):
        ticker_data = get_one_ticker(asset, from_=from_, start_date=start_date, end_date=end_date)
        close_data = prepare_data(ticker_data, asset).reset_index()
        if i == 0:
            portfolio = close_data[['Date', asset]]
            continue
        elif asset in portfolio.columns:
            continue
        portfolio = pd.concat([portfolio, close_data[asset]], axis=1)
        sleep(1)

    portfolio = portfolio.set_index('Date')
    portfolio.index = pd.to_datetime(portfolio.index)
    portfolio = portfolio.round(3)
    return portfolio


def get_one_ticker(asset, from_='3m', start_date=None, end_date=dt.now().date()):
    
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) \
           AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'}
    if start_date:
        end_date = str(end_date)
        start, end = get_range_timestamps(start_date, end_date)
    else:
        start, end = get_range(range_from=from_, end_date=end_date)
        start, end = get_range_timestamps(start, end)

    url = f"https://query2.finance.yahoo.com/v8/finance/chart/{asset}?" \
          f"period1={start}&period2={end}&interval=1d&events=history"
    
    try:
        response = requests.get(url, headers=headers)
    except Exception as e:
        raise 
    if response.ok:
        data = pd.DataFrame.from_dict(response.json()['chart']['result'][0]['indicators']['quote'][0])
        data['Date'] = response.json()['chart']['result'][0]['timestamp']
        data['Date'] = data['Date'].apply(dt.fromtimestamp)
        data = data.set_index('Date', drop=True)
        data.index = data.index.normalize()
        return data.round(2)
    else:
        print(response.text)
        raise Exception(f'Could not retrieve data:{response.status_code}')
    
def prepare_data(data, ticker):
    data = data.drop(['open', 'high', 'low', 'volume'], axis=1)
    data = data.rename(columns={"close": ticker})
    return data.round(2)

## Usage
ticker_data = get_one_ticker('AAPL', from_='5y')
ticker_data.to_csv('your_file_name.csv')

portfolio_data = get_portfolio(['AAPL', 'AMZN', 'QQQ', 'SPY', 'TSLA'], from_='10y')
portfolio_data.to_csv('your_file_name.csv')

```
## Conclusions

So, which tool is best for you? It depends on your needs! Here’s a quick comparison:

- **Pandas DataReader:** Great for ease of use but losing support for Yahoo Finance.
- **Alpha Vantage:** Great free API but with request limits.
- **yFinance:** No API key required, but has some rate limitations.
- **Yahoo_fin:** Scraping-based, so no API hassles, but slower.
- **Nasdaq Data Link:** Reliable, easy-to-use replacement for Quandl, offering wide data access with a familiar API.
- **Custom code:** Fully tailored to match very specific needs and flavors. 

All of these tools are perfect for small to medium-sized projects, but be mindful of request limits if you're fetching a lot of data!

Let me know your thoughts in the comments

**Happy investing!**
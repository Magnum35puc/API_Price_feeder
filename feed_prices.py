import schedule
import time
import requests
import json

from Utils import APIUtils 


Alpha_Vantage_API_Key =""

def get_fr_stock_prices(ticker:str):
    symbol = f"{ticker}.PAR"
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={Alpha_Vantage_API_Key}"
    response = requests.get(url)
    data = json.loads(response.text)
    price = float(data["Global Quote"]["05. price"])
    print(f"The latest price of {ticker} is {price:.2f}")
    time.sleep(30)
    return price


def get_us_stock_prices(ticker:str):
    symbol = f"{ticker}"
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={Alpha_Vantage_API_Key}"
    response = requests.get(url)
    data = json.loads(response.text)
    price = float(data["Global Quote"]["05. price"])
    print(f"The latest price of {ticker} is {price:.2f}")
    time.sleep(30)
    return price


def get_de_stock_prices(ticker:str):
    symbol = f"{ticker}.FRK"
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={Alpha_Vantage_API_Key}"
    response = requests.get(url)
    data = json.loads(response.text)
    price = float(data["Global Quote"]["05. price"])
    print(f"The latest price of {ticker} is {price:.2f}")
    time.sleep(30)
    return price

# Function that updates the price of the assets
def get_crypto_price(ticker:str):
    print(f"Getting price of {ticker}")
    url = "https://min-api.cryptocompare.com/data/price"
    params = {
        "fsym": ticker,
        "tsyms": "USD"
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        price = data["USD"]
        print(price)
        return price



api = "https://asset-vision-api-zznkesfula-oa.a.run.app/"
token = APIUtils.get_login(f"{api}login")

all_crypto = APIUtils.get_all_assets_by_cat(api,'Cryptocurrency', token )
all_fr_stocks = APIUtils.get_all_assets_by_cat(api,'Stock FR', token)
all_us_stocks = APIUtils.get_all_assets_by_cat(api,'Stock US', token)
all_de_stocks = APIUtils.get_all_assets_by_cat(api,'Stock DE', token)

# Schedule the price update to run every hour
schedule.every().hour.do(APIUtils.update_price,tickers = all_crypto, api= api, get_pricefunc = get_crypto_price)
schedule.every().hour.do(APIUtils.update_price,tickers = all_fr_stocks, api= api, get_pricefunc = get_fr_stock_prices)
schedule.every().hour.do(APIUtils.update_price,tickers = all_us_stocks, api= api, get_pricefunc = get_us_stock_prices)
schedule.every().hour.do(APIUtils.update_price,tickers = all_de_stocks, api= api, get_pricefunc = get_de_stock_prices)

while True:
   schedule.run_pending()
   time.sleep(1)
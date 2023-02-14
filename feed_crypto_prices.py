import schedule
import time
import requests
import ast
import json


def get_login(api_url):
    headers = {
        "accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "username": "admin",
        "password": "1234"
    }

    response = requests.post(api_url, headers=headers, data=data)
    return ast.literal_eval(response.content.decode('utf-8'))["access_token"]

def get_all_assets(api,asset_class):
    token = get_login(api+ "login/")
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer "+ token
    }

    response = requests.get(api+ "assets/", headers=headers)
    if response.status_code == 200:
        assets = response.json()
        types = set([asset['symbol'] for asset in  assets if asset['asset_class']==asset_class])
        return types
    else:
        print("Request failed with status code:", response.status_code)


# Function that updates the price of the assets
def get_price(ticker):
    url = "https://min-api.cryptocompare.com/data/price"
    params = {
        "fsym": ticker,
        "tsyms": "USD"
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        price = data["USD"]
        return price

def update_price(tickers, api ):
    token = get_login(api+ "login/")
    for ticker in tickers : 
        price = get_price(ticker)
        details = {
            "last_price":price
        }
        url = f"{api}asset/{ticker}?asset_details={json.dumps(details) }"

        header = {
            "accept": "application/json",
            "Authorization": "Bearer "+ token
        }
        response = requests.put(url, headers=header)

        print(response.content)

api = "http://localhost:8000/"

all_crypto = get_all_assets(api,'Cryptocurrency' )
# Schedule the price update to run every hour
schedule.every().hour.do(update_price, all_crypto, api)

while True:
   schedule.run_pending()
   time.sleep(1)
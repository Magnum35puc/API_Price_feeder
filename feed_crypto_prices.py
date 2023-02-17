import schedule
import time
import requests
import ast
from datetime import datetime
import json


def get_login(login_url):
    headers = {
        "accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    payload = 'grant_type=&username=admin&password=1234&scope=&client_id=&client_secret='

    response = requests.request("POST", login_url, headers=headers, data=payload)
    token = ast.literal_eval(response.content.decode('utf-8'))["access_token"]
    print("Logged in")
    return token

def get_all_assets(api,asset_class):
    token = get_login(api+ "login")
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer "+ token
    }

    response = requests.get(api+ "assets/", headers=headers)
    if response.status_code == 200:
        assets = response.json()
        types = set([asset['symbol'] for asset in  assets if asset['asset_class']==asset_class])
        print("All selected assets are " + str(types))
        return types
    else:
        print("Request failed with status code:", response.status_code)


# Function that updates the price of the assets
def get_price(ticker):
    print("Getting price of " + ticker)
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

def update_price(tickers, api):
    print(str(datetime.now())+" - Starting updating prices")
    token = get_login(api+ "login")
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


api = "https://asset-vision-api-zznkesfula-oa.a.run.app/"

all_crypto = get_all_assets(api,'Cryptocurrency' )

# Schedule the price update to run every hour
schedule.every().hour.do(update_price,tickers = all_crypto, api= api)

while True:
   schedule.run_pending()
   time.sleep(1)
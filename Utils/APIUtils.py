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
    payload = 'grant_type=&username=admin&password=1111&scope=&client_id=&client_secret='

    response = requests.request("POST", login_url, headers=headers, data=payload)
    token = ast.literal_eval(response.content.decode('utf-8'))["access_token"]
    print(f"Logged in {datetime.now()}")
    return token

def get_all_assets_by_cat(api,asset_class, token):
    headers = {"accept": "application/json", "Authorization": f"Bearer {token}"}
    response = requests.get(f"{api}assets/", headers=headers)
    if response.status_code == 200:
        assets = response.json()
        types = {
            asset['symbol']
            for asset in assets 
            if asset['asset_class'] == asset_class
        }
        print(f"All selected assets are {types}")
        return types
    else:
        print("Request failed with status code:", response.status_code)

def update_price(tickers, api, get_pricefunc):
    print(f"{str(datetime.now())} - Starting updating prices")
    try:
        token = get_login(f"{api}login")
        for ticker in tickers: 
            price = get_pricefunc(ticker)
            details = {
                "last_price":price
            }
            url = f"{api}asset/{ticker}?asset_details={json.dumps(details) }"

            header = {"accept": "application/json", "Authorization": f"Bearer {token}"}
            response = requests.put(url, headers=header)
    except Exception:
        print("Something went wrong")

def update_rate(tickers, api, get_pricefunc):
    print(f"{str(datetime.now())} - Starting updating prices")
    try:
        token = get_login(f"{api}login")
        for ticker in tickers: 
            price = get_pricefunc(ticker)
            details = {
                "last_rate":price
            }
            url = f"{api}rate/{ticker}?rate_details={json.dumps(details) }"

            header = {"accept": "application/json", "Authorization": f"Bearer {token}"}
            response = requests.put(url, headers=header)
    except Exception:
        print("Something went wrong")
import requests
import json

def get_crypto_prices():
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
    params = {
        "symbol": "BTC,ETH,LTC,BCH,ADA,XLM",
        "convert": "USD"
    }
    headers = {
        "Accepts": "application/json",
        "X-CMC_PRO_API_KEY": "877fff13-5b22-441c-8ba9-f0cf19ea69a5"
    }
    response = requests.get(url, params=params, headers=headers)

    if response.status_code == 200:
        data = response.json()
        if 'data' in data:
            btc_info = data["data"]["BTC"]
            eth_info = data["data"]["ETH"]
            ltc_info = data["data"]["LTC"]
            bch_info = data["data"]["BCH"]
            ada_info = data["data"]["ADA"]
            xlm_info = data["data"]["XLM"]

            btc_price = round(float(btc_info["quote"]["USD"]["price"]), 2)
            eth_price = round(float(eth_info["quote"]["USD"]["price"]), 2)
            ltc_price = round(float(ltc_info["quote"]["USD"]["price"]), 2)
            bch_price = round(float(bch_info["quote"]["USD"]["price"]), 2)
            ada_price = round(float(ada_info["quote"]["USD"]["price"]), 2)
            xlm_price = round(float(xlm_info["quote"]["USD"]["price"]), 2)

            return btc_price, eth_price, ltc_price, bch_price, ada_price, xlm_price
        else:
            return None  # or some default value
    else:
        return None  # or some default value


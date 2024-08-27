import requests
import json

def payment(usd_amount, crypto):
    url = "https://api.nowpayments.io/v1/payment"

    payload = json.dumps({
                    "price_amount": usd_amount,
                    "price_currency": "usd",
                    "pay_currency": f"{crypto}",
                    "ipn_callback_url": "https://nowpayments.io",
                    "order_id": "BEC",
                    "order_description": f"{crypto} deposit"
                })
    headers = {
                    'x-api-key': 'ZP1SH6F-F39M03R-P0BD136-JS0WPCZ',
                    'Content-Type': 'application/json'
                }
    response = requests.post(url, headers=headers, data=payload)
    response.raise_for_status()     
    data = json.loads(response.text)
    payment_id = data.get("payment_id")    
    payment_status = data.get("payment_status")
    pay_address = data.get("pay_address")
    print(pay_address)

    return payment_id, payment_status, pay_address

def confirm_payment(payment_id):
        url = f"https://api.nowpayments.io/v1/payment/{payment_id}"

        payload={}
        headers = {
        'x-api-key': 'ZP1SH6F-F39M03R-P0BD136-JS0WPCZ'
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        data = json.loads(response.text)
        return data.get("payment_status")



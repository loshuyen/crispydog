import os
import requests
import json

def tappay_direct_pay(prime, amount, order_number, phone_number, name, email):
    url = "https://sandbox.tappaysdk.com/tpc/payment/pay-by-prime"
    headers = {
        "Content-Type": "application/json",
        "x-api-key": os.getenv("TAPPAY_PARTNER_KEY")
    }
    data = {
            "prime": prime,
            "partner_key": os.getenv("TAPPAY_PARTNER_KEY"),
            "merchant_id": os.getenv("TAPPAY_MERCHANT_ID"),
            "amount": amount,
            "order_number": order_number,
            "details": "digital content",
            "cardholder": {
                "phone_number": phone_number,
                "name": name,
                "email": email,
            }
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    result = response.json()
    response_data = {
            "number": result["order_number"],
            "payment": {
                "pay_method": "credit card",
                "status": result["status"],
                "message": result["msg"],
                "rec_trade_id": result["rec_trade_id"],
                "auth_code": result["auth_code"],
                "amount": result["amount"],
                "currency": result["currency"],
                "transaction_time": result["transaction_time_millis"],
            }
        }
    return response_data
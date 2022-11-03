import requests
import hashlib
import hmac
import os
from datetime import datetime
from dotenv import load_dotenv
import json

load_dotenv()

secret_key = os.getenv('secret_key')
x_login = os.getenv('x_login')
x_trans_key = os.getenv('x_trans_key')


# dumps_result = json.dumps(payload)


# print('Secret key encoded: ', secret_key_encoded)
# print('Data encoded: ', data_encoded)


# signature = hmac.new(secret_key_encoded, data_encoded,
#                      hashlib.sha256).hexdigest()


# SIG = "V2-HMAC-SHA256, Signature: " + signature


def make_test_payment():

    utd_dt = datetime.utcnow()

    utd_dt_string = utd_dt.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    utd_dt_string = utd_dt_string[:-4]+'Z'

    payload = {
        "amount": 10,
        "currency": "KES",
        "country": "KE",
        "payment_method_id": "CARD",
        "payment_method_flow": "REDIRECT",
        "payer": {
            "name": "Leo Messi",
            "email": "leo@messi.com",
            "document": "12345678",
            "user_reference": "12345",
            "address": {
                    "state": "Rio de Janeiro",
                    "city": "Volta Redonda",
                    "zip_code": "27275-595",
                    "street": "Servidao B-1",
                    "number": "1106"
            }
        },
        "order_id": "61713113412",
        "notification_url": "http://merchant.com/notifications"
    }

    SIG = "V2-HMAC-SHA256, Signature: " + \
        generate_signature(utd_dt_string, json.dumps(payload))

    print('SIG:: ', SIG)

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "X-Date": utd_dt_string,
        "X-Login": x_login,
        "X-Trans-Key": x_trans_key,
        "Content-Type": "application/json",
        "X-Version": "2.1",
        "User-Agent": "MerchantTest / 1.0",
        "Authorization": SIG,
        "Accept": 'application/json'
    }

    url = "https://sandbox.dlocal.com/payments"

    response = requests.post(url, json=payload, headers=headers)
    print(response.text)


def generate_signature(string_timestamp, string_payload):

    secret_key_encoded = bytes(secret_key, 'UTF-8')
    data_encoded = bytes((x_login+string_timestamp +
                          string_payload), 'UTF-8')

    signature = hmac.new(secret_key_encoded, data_encoded,
                         hashlib.sha256).hexdigest()

    return signature


def main():
    make_test_payment()


if __name__ == "__main__":
    main()

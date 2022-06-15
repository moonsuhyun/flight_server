import models.Secret
import base64
import hmac
import time
import json
import hashlib
import requests


def send_sms(number, text):
    service_id = models.Secret.get_secret("service_id")
    url = f"https://sens.apigw.ntruss.com/sms/v2/services/{service_id}/messages"
    timestamp = str(int(time.time() * 1000))
    secret_key = bytes(models.Secret.get_secret('auth_secret_key'), 'utf-8')
    method = 'POST'
    uri = f'/sms/v2/services/{service_id}/messages'
    message = bytes(f'{method} {uri}\n{timestamp}\n{models.Secret.get_secret("access_key_id")}', 'utf-8')
    signing_key = base64.b64encode(hmac.new(secret_key, message, digestmod=hashlib.sha256).digest())

    headers = {
        'Content-Type': 'application/json; charset=utf-8',
        'x-ncp-apigw-timestamp': timestamp,
        'x-ncp-iam-access-key': models.Secret.get_secret('access_key_id'),
        'x-ncp-apigw-signature-v2': signing_key,
    }
    body = {
        'type': 'SMS',
        'contentType': 'COMM',
        'countryCode': '82',
        'from': f'{models.Secret.get_secret("send_number")}',
        'content': f'{text}',
        'messages': [
            {
                'to': f'{number}'
            }
        ]
    }
    encoded_data = json.dumps(body)

    res = requests.post(url, headers=headers, data=encoded_data)
    return res.status_code

import hashlib
import hmac
import base64
import requests
import time, json
from rest_framework.views import APIView
from django.conf import settings


def send_message(name, phone_num):
    timestamp = int(time.time() * 1000)
    timestamp = str(timestamp)

    url = "https://sens.apigw.ntruss.com"
    requestUrl1 = "/sms/v2/services/"
    requestUrl2 = "/messages"

    serviceId = settings.NCP_SERVICE_ID
    access_key = settings.NCP_ACCESS_KEY_ID

    uri = requestUrl1 + serviceId + requestUrl2
    apiUrl = url + uri

    secret_key = settings.NCP_SECRET_KEY
    secret_key = bytes(secret_key, 'UTF-8')

    method = "POST"
    message = method + " " + uri + timestamp + "\n" + access_key
    message = bytes(message, 'UTF-8')

    signingkey = base64.b64encode(hmac.new(secret_key, message, digestmod=hashlib.sha256).digest())

    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'x-ncp-apigw-timestamp': timestamp,
        'x-ncp-iam-access-key': access_key,
        'x-ncp-apigw-signature-v2': signingkey,
    }

    message = name+"님, 테스트 내용입니다."		# 메세지 내용을 저장
    phone = phone_num			# 핸드폰 번호를 저장
    
    body = {
        "type": "SMS",
        "contentType": "COMM",
        "from": settings.SENDER_PHONE_NUM,
        "content": message,
        "messages": [{"to": phone}]
    }
    body = json.dumps(body)

    res = requests.post(apiUrl, headers=headers, data=body)

    res.request
    res.status_code
    res.raise_for_status()

    print(res.json())
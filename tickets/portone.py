import requests

from django.conf import settings

#포트원 서버와 통신하기 위한 토큰을 받아오는 함수
def get_token():
    access_data = {
        'ptn_key': settings.PORTONE_KEY,
        'ptn_secret': settings.PORTONE_SECRET,
    }

    url = "https://api.iamport.kr/users/getToken"

    req = requests.post(url, data=access_data)
    access_res = req.json()
    print('access_res', access_res)

    if access_res['code'] == 0:
        return access_res['response']['access_token']
    else:
        return None

#결제 준비 함수
#포트원에 미리 정보를 전달하여 어떤 주문 번호로 얼마를 결제할 지 미리 전달하는 역할
def payments_prepare(order_id, amount, *args, **kwargs):
    access_token = get_token()
    if access_token:        #token이 존재하는 경우
        access_data = {
            'merchant_uid': order_id,
            'amount': amount,
        }

    url = "https://api.iamport.kr/payments/prepare"
    headers = {
        'Authorization': access_token
    }

    req = requests.post(url, data=access_data, headers=headers)
    res = req.json()

    if res['code'] != 0:
        raise ValueError("API 통신 오류")
    else:
        raise ValueError("토큰 오류")
    
#결제가 완료된 후에 실제 결제가 이뤄진 것이 맞는지 확인할 때 사용
def find_transaction(order_id, *args, **kwargs):
    access_token = get_token()
    if access_token:
        url = "https://api.iamport.kr/payments/find/" + order_id
        headers = {
            'Authorization': access_token
        }

        req = requests.post(url, headers=headers)
        res = req.json()
        if res['code'] == 0:
            context = {
                'ptn_id': res['response']['ptn_uid'],
                'merchant_order_id': res['response']['merchant_uid'],
                'amount': res['response']['amount'],
                'status': res['response']['status'],
                'type': res['response']['pay_method'],
                'receipt_url': res['response']['receipt_url'],
            }
            return context
        else:
            return None
    else:
        raise ValueError("토큰 오류")
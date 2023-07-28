import hashlib
from django.db import models
from core.models import TimeStampedModel
from .portone import payments_prepare, find_transaction

class Category(models.Model):
    name = models.CharField(max_length=30)   # 티켓 종류 구분 (일반/신입생)

    def __str__(self):
        return self.name

#구매 전 정보 저장
class Ticketing(TimeStampedModel):
    category = models.ForeignKey('Category', related_name='tickets', on_delete=models.CASCADE)
    buyer = models.CharField(max_length=20)   # 결제자 이름
    phone_num = models.CharField(max_length=20)   # 핸드폰 번호
    email = models.EmailField()
    member = models.PositiveIntegerField(default=1)   # 결제 인원
    available_ticket = models.BooleanField(default=True)   # 티켓 구매 가능 여부
    meeting = models.BooleanField(default=False)   # 소모임 참석 가능 여부 확인
    qrcode = models.ImageField(upload_to='qr_codes', blank=True)

    def __str__(self):
        return 'Order {}.{}'.format(self.buyer, self.id)
    
    # def get_total_price(self):
    #     total


class OrderTransactionManager(models.Manager):
    def create_new(self, order, amount, success=None, transaction_status=None):
        if not order:
            raise ValueError("주문 오류")
        #.encode('utf-8')을 이용하여 유니코드 문자열을 UTF-8형식의 바이트 문자열로 변환
        # 문자열을 해싱한 다음 hexidigest() 함수를 사용하여 바이트 문자열을 16진수로 변환한 문자열을 반환
        order_hash = hashlib.sha1(str(order.id).encode('utf-8')).hexdigest()
        phone_hash = str(order.phone_num)
        final_hash = hashlib.sha1((order_hash + phone_hash).encode('utf-8')).hexdigest()[:10]
        merchant_order_id = "%s"%(final_hash)

        payments_prepare(merchant_order_id, amount)
        transaction = self.model(
            order=order,
            merchant_order_id=merchant_order_id,
            amount=amount,
        )
        if success is not None:
            transaction.success = success
            transaction.transaction_status = transaction_status
        try:
            transaction.save()
        except Exception as e:
            print('save error', e)
        return transaction.merchant_order_id
    
    def get_transaction(self, merchant_order_id):
        result = find_transaction(merchant_order_id)
        if result['status'] == 'paid':
            return result
        else:
            return None

#결제 정보 저장
#TODO: 결제 정보를 엑셀로 이동 필요
class OrderTransaction(models.Model):
    order = models.ForeignKey('Ticketing', on_delete=models.CASCADE)
    merchant_order_id = models.CharField(max_length=120, null=True, blank=True)
    transaction_id = models.CharField(max_length=120, null=True, blank=True)
    transaction_status = models.CharField(max_length=220, null=True, blank=True)

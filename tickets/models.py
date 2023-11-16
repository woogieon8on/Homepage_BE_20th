import hashlib
from django.db import models
from django.db.models.signals import post_save
from django.core.validators import MinValueValidator, MaxValueValidator
from core.models import TimeStampedModel
from .iamport import payments_prepare, find_transaction

# class Category(models.Model):
#     name = models.CharField(max_length=30)   # 티켓 종류 구분 (일반/신입생)

#     def __str__(self):
#         return self.name
    

# 신입생 참석자의 경우 FreshmanTicket DB에 저장되므로 추가로 참석자란에 저장할 필요 없다고 판단
class Participant(models.Model):
    name = models.CharField(max_length=5)
    phone_num = models.CharField(max_length=11)
    general_ticket = models.ForeignKey(
        "GeneralTicket", related_name='participants', on_delete=models.CASCADE)

    def __str__(self):
        return '{}/{}/{}'.format(self.general_ticket.buyer, self.name, self.id)

#구매 전 정보 저장
class GeneralTicket(TimeStampedModel):  #일반 티켓
    buyer = models.CharField(max_length=20)   # 결제자 이름
    phone_num = models.CharField(max_length=20, unique=True)   # 핸드폰 번호
    member = models.PositiveIntegerField(default=1)   # 예매 인원
    price = models.PositiveIntegerField(default=0)

    def __str__(self):
        return 'Order {}/{}'.format(self.buyer, self.id)
    
    class Meta:
        ordering = ['-created']

class FreshmanTicket(TimeStampedModel):  #신입생 티켓
    buyer = models.CharField(max_length=30)
    phone_num = models.CharField(max_length=20, unique=True)
    major = models.CharField(max_length=30)
    student_id = models.CharField(max_length=10, unique=True)
    meeting = models.BooleanField(default=False)
    reservation_id = models.CharField(max_length=10, unique=True, null=True)   # 주문번호(예약번호)

    def __str__(self):
        return 'Order {}.{}'.format(self.buyer, self.id)


class OrderTransactionManager(models.Manager):
    use_for_related_fields = True

    def create_new(self, order, amount, success=None, transaction_status=None):
        if not order:
            raise ValueError("주문 오류")
        #.encode('utf-8')을 이용하여 유니코드 문자열을 UTF-8형식의 바이트 문자열로 변환
        # 문자열을 해싱한 다음 hexidigest() 함수를 사용하여 바이트 문자열을 16진수로 변환한 문자열을 반환
        order_hash = hashlib.sha1(str(order.id).encode('utf-8')).hexdigest()
        phone_hash = str(order.phone_num)
        final_hash = hashlib.sha1((order_hash + phone_hash).encode('utf-8')).hexdigest()[:10]
        merchant_order_id = "%s"%(final_hash)   # 예약 번호(결제 번호)
        
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
    
    #필요한 지 논의 필요
    def get_transaction(self, merchant_order_id):
        result = find_transaction(merchant_order_id)
        # if result['status'] == 'paid':
        return result
        # else:
        #     return None

#결제 정보 저장
#TODO: 결제 정보를 엑셀로 이동 필요
class OrderTransaction(TimeStampedModel):
    order = models.ForeignKey(GeneralTicket, on_delete=models.CASCADE)
    merchant_order_id = models.CharField(max_length=120, null=True, blank=True)
    transaction_id = models.CharField(max_length=120, null=True, blank=True)
    amount = models.PositiveIntegerField(default=0)
    transaction_status = models.CharField(max_length=220, null=True, blank=True)

    objects = OrderTransactionManager()

    def __str__(self):
        return str(self.order.id)
    
    class Meta:
        ordering = ['-created']

def order_payment_validation(sender, instance, created, *args, **kwargs):
    if instance.transaction_id:
        import_transaction = OrderTransaction.objects.get_transaction(
        merchant_order_id = instance.merchant_order_id)
        merchant_order_id = import_transaction['merchant_order_id']
        imp_id = import_transaction['imp_id']
        amount = import_transaction['amount']
        local_transaction = OrderTransaction.objects.filter(
            merchant_order_id=merchant_order_id,
            transaction_id=imp_id,
            amount=amount,
        ).exists()
        if not import_transaction or not local_transaction:
            raise ValueError("비정상 거래입니다.")
        
post_save.connect(order_payment_validation, sender=OrderTransaction)

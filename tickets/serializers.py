import random
import string

from rest_framework import serializers

from .models import GeneralTicket, FreshmanTicket

class GeneralTicketDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = GeneralTicket
        ordering = ['-id']
        fields = [
            'id',
            'buyer',
            'phone_num',
            'member',
            'price',
        ]

    def create(self, validated_data):
        member = validated_data.get('member', 1)
        price = member * int(5000)
        validated_data['price'] = price

        ticket = GeneralTicket.objects.create(**validated_data)

        return ticket
    

class FreshmanTicketDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = FreshmanTicket
        ordering = ['-id']
        fields = '__all__'

    def create(self, validated_data):

        #TODO:view나 model로 옮기기
        # 예약번호 랜덤 생성 (최대 10번 시도)
        for _ in range(10):
            reservation_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
            if not FreshmanTicket.objects.filter(reservation_id=reservation_id).exists():
                validated_data['reservation_id'] = reservation_id
                break

        if not reservation_id:
            raise ValueError("유효한 예약번호를 생성하지 못했습니다.")

        return FreshmanTicket.objects.create(**validated_data)
    
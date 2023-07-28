
from rest_framework import serializers

from .models import Ticketing

class TicketDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticketing
        ordering = ['-id']
        fields = [
            'category',
            'buyer',
            'phone_num',
            'email',
            'member',
        ]

    def create(self, validated_data):
        return super().create(validated_data)
    
class QRCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticketing
        fields = [
            'category',
            'buyer',
            'phone_num',
            'member',
            'qrcode',
        ]
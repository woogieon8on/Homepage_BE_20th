
from rest_framework import serializers

from .models import GeneralTicket, FreshmanTicket

class GeneralTicketDetailSerializer(serializers.ModelSerializer):
    # price = serializers.SerializerMethodField()

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
        ticket = GeneralTicket.objects.create(**validated_data)

        return ticket
    

class FreshmanTicketDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = FreshmanTicket
        ordering = ['-id']
        fields = '__all__'

    def create(self, validated_data):
        return FreshmanTicket.objects.create(**validated_data)
    
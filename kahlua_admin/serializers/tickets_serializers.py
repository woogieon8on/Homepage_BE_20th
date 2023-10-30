from django.shortcuts import get_object_or_404
from rest_framework import serializers
from tickets.models import FreshmanTicket

class FreshmanSerializer(serializers.ModelSerializer):
    class Meta:
        model = FreshmanTicket
        ordering = ['-id']  # 최신순으로 정렬
        fields = [
            'id',
            'buyer',
            'phone_num',
            'major',
            'student_id',
            'meeting',
        ]
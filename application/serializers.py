from rest_framework import serializers

from .models import ApplyForm


class ApplyFormCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplyForm
        ordering = ['-id']
        fields = '__all__'

    def create(self, validated_data):
        return ApplyForm.objects.create(**validated_data)


class ApplyFormCompleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplyForm
        fields = '__all__'
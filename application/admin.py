from django.contrib import admin
from . import models
from import_export.admin import ExportActionMixin

# Register your models here.

@admin.register(models.ApplyForm)
class ApplyFormAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ('name','phone_num','birthdate','gender','address','first_preference',
                    'second_preference','play_instrument','motive')
    #pass
    
"""
    name = models.CharField(max_length=20)   # 지원자 이름
    phone_num = models.CharField(max_length=13, null=True)   # 전화번호('-'없는 상태로 입력받기)
    birthdate = models.DateField(blank=True)   # 생년월일
    gender = models.CharField(choices=GENDER_CHOICES, max_length=20, blank=True)   # 성별
    address = models.CharField(max_length=200)   # 거주지
    first_preference = models.CharField(choices=PREFERENCE_CHOICES, max_length=20)   # 1지망
    second_preference = models.CharField(choices=PREFERENCE_CHOICES, max_length=20)   # 2지망
    play_instrument = models.CharField(max_length=200, blank=True)   # 다룰 줄 아는 악기
    motive = models.TextField()   # 지원 동기
"""
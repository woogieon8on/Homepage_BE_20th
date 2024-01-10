from django.db import models
from core.models import TimeStampedModel

class ApplyForm(TimeStampedModel):
    """GENER CHOICE"""
    MALE = '남성'
    FEMALE = '여성'
    GENDER_CHOICES = [
        (MALE, '남성'),
        (FEMALE, '여성'),
    ]
    """PREFERENCE_CHOICES"""
    VOCAL = '보컬'
    DRUM = '드럼'
    GUITAR = '기타'
    BASS = '베이스'
    SYNTHESIZER = '신디'
    PREFERENCE_CHOICES = [
        (VOCAL, '보컬'),
        (DRUM, '드럼'),
        (GUITAR, '기타'),
        (BASS, '베이스'),
        (SYNTHESIZER, '신디'),
    ]

    name = models.CharField(max_length=20)   # 지원자 이름
    phone_num = models.CharField(max_length=13, null=True)   # 전화번호('-'없는 상태로 입력받기)
    birthdate = models.CharField(max_length=8, blank=True)   # 생년월일d('-'없는 상태로 입력받기)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=20)   # 성별
    address = models.CharField(max_length=200)   # 거주지
    first_preference = models.CharField(choices=PREFERENCE_CHOICES, max_length=20)   # 1지망
    second_preference = models.CharField(choices=PREFERENCE_CHOICES, max_length=20)   # 2지망
    play_instrument = models.CharField(max_length=200, blank=True)   # 다룰 줄 아는 악기
    motive = models.TextField()   # 지원 동기

    def __str__(self):
        return self.name
    
from django.db import models
from core.models import TimeStampedModel

class ApplyForm(TimeStampedModel):

    MALE = '남성'
    FEMALE = '여성'
    GENDER_CHOICES = [
        (MALE, '남성'),
        (FEMALE, '여성'),
    ]

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
    birthdate = models.DateField(blank=True)   # 생년월일
    gender = models.CharField(choices=GENDER_CHOICES, max_length=20, blank=True)   # 성별
    address = models.CharField(max_length=200)   # 거주지
    first_preference = models.CharField(choices=PREFERENCE_CHOICES, max_length=20)   # 1지망
    second_preference = models.CharField(choices=PREFERENCE_CHOICES, max_length=20)   # 2지망
    play_instrument = models.CharField(max_length=200, blank=True)   # 다룰 줄 아는 악기
    motive = models.TextField()   # 지원 동기

    def __str__(self):
        return self.name
    
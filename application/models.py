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
    """MAJOR CHOICE"""
    COMPUTER = '컴퓨터공학과'
    FREE = '자율전공학과'
    MAJOR_CHOICES = [
        (COMPUTER, '컴퓨터공학과'),
        (FREE, '자율전공학과'),
    ]
    """PREFERENCE_CHOICES"""
    VOCAL = '보컬'
    DRUM = '드럼'
    GUITAR = '기타'
    BASS = '베이스'
    SYNTHESIZER = '신디(피아노)'
    PREFERENCE_CHOICES = [
        (VOCAL, '보컬'),
        (DRUM, '드럼'),
        (GUITAR, '기타'),
        (BASS, '베이스'),
        (SYNTHESIZER, '신디(피아노)'),
    ]

    name = models.CharField(max_length=20)   # 지원자 이름
    phone_num = models.CharField(max_length=13, null=True)   # 전화번호('-'없는 상태로 입력받기)
    birthdate = models.CharField(max_length=8, blank=True)   # 생년월일d('-'없는 상태로 입력받기)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=20)   # 성별
    address = models.CharField(max_length=200)   # 거주지
    major = models.CharField(choices=MAJOR_CHOICES, max_length=6, default='')   # 전공학과
    first_preference = models.CharField(choices=PREFERENCE_CHOICES, max_length=20)   # 1지망
    second_preference = models.CharField(choices=PREFERENCE_CHOICES, max_length=20)   # 2지망
    exprience_and_reason = models.TextField(default='')   # 지원세션의 경력과 이유
    play_instrument = models.TextField()   # 다룰 줄 아는 악기
    motive = models.TextField()   # 지원 동기
    finish_time = models.TextField(default='')   # 끝나는 시간
    meeting = models.BooleanField(default=False)   # 뒷풀이 참석 여부
    readiness = models.TextField(default='')   # 면접 전 각오

    def __str__(self):
        return self.name
    
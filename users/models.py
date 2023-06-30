import re
from email.policy import default
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import UserManager, BaseUserManager, AbstractBaseUser, PermissionsMixin

# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        """
            주어진 이메일, 비밀번호 등 개인정보로 인스턴스 생성
        """
        if not email:
            raise ValueError(('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(('Superuser nust have is_superuser=True.'))
        
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=100, unique=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    nickname = models.CharField(max_length=30, blank=True)

    #소셜 계정인 경우, 소셜 ID 프로바이더 값 저장(ex. kakao, naver, goole)
    social_provider = models.CharField(max_length=30, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
    
    def email_isvalid(value):
        try:
            validation = re.compile(
                r'^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
            if not re.match(validation, value):
                raise Exception('올바른 메일 형식이 아닙니다.')
            return value
        except Exception as e:
            print('예외가 발생했습니다.', e)

    def clean(self):
        if not self.email_isvalid(self.email):
            raise ValidationError('메일 형식이 올바르지 않습니다.')
# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    name = models.CharField(max_length=100)
    birth_date = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)


class FinancialProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    saving_style = models.CharField(max_length=10)  # '공격적', '중립적', '보수적'
    spending_style = models.CharField(max_length=10)
    title = models.CharField(max_length=30)         # 예: '절제된 야망가'
    checklist_submitted = models.BooleanField(default=False)  # 첫 진입 여부


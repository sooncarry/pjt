from django.db import models

class FinanceTerm(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)  # 예: 휴면예금
    eng_title = models.CharField(max_length=100)  # Dormant Deposit
    content = models.TextField()

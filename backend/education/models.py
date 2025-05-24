from django.db import models

class FinanceTerm(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)  # 예: 휴면예금
    eng_title = models.CharField(max_length=100)  # Dormant Deposit
    content = models.TextField()
from django.db import models

class NewsItem(models.Model):
    title = models.CharField(max_length=255)
    summary = models.TextField(blank=True)
    url = models.URLField()
    published_at = models.DateField(null=True, blank=True)
    source = models.CharField(max_length=100)
    thumbnail = models.URLField(blank=True)
    category = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.source} - {self.title[:30]}"

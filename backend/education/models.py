from django.db import models

class FinanceTerm(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)       # 예: 휴면예금
    eng_title = models.CharField(max_length=100)   # 예: Dormant Deposit
    content = models.TextField()

class NewsItem(models.Model):
    title        = models.CharField(max_length=255)
    summary      = models.TextField(blank=True)              # API의 description
    url          = models.URLField()                         # API의 originallink
    published_at = models.DateTimeField(null=True, blank=True)  # API의 pubDate (시간 포함)
    source       = models.CharField(
        max_length=100,
        blank=True,
        default=""
    )                                                       # 언론사(도메인 등), 없으면 빈 문자열
    thumbnail    = models.URLField(blank=True)               # 미제공 시 빈값
    category     = models.CharField(
        max_length=100,
        blank=True,
        default="금융"
    )                                                       # 기본 카테고리: 금융

    def __str__(self):
        return f"{self.source} - {self.title[:30]}"
# backend/education/models.py

from django.db import models

class FinanceTerm(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)       # 예: 휴면예금
    eng_title = models.CharField(max_length=100)   # 예: Dormant Deposit
    content = models.TextField()

    def __str__(self):
        return self.title


class NewsItem(models.Model):
    title = models.CharField(max_length=255)
    url = models.URLField(unique=True)
    thumbnail = models.URLField(blank=True, null=True)  # 썸네일 이미지 URL
    lede = models.TextField(blank=True)
    press = models.CharField(max_length=50, blank=True)
    published_at = models.DateTimeField(null=True, blank=True)  # 기사 게시 시각
    crawled_at = models.DateTimeField(auto_now_add=True)        # 크롤링 시각(서버 기준)

    def __str__(self):
        return self.title


class QuizQuestion(models.Model):
    question = models.CharField(max_length=255)
    option1 = models.CharField(max_length=100)
    option2 = models.CharField(max_length=100)
    option3 = models.CharField(max_length=100)
    option4 = models.CharField(max_length=100)
    answer = models.IntegerField()  # 0~3
    explanation = models.TextField()

    def options(self):
        return [self.option1, self.option2, self.option3, self.option4]

    def __str__(self):
        return self.question

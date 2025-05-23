from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class ChallengeTemplate(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    default_goal_amount = models.PositiveIntegerField()
    default_total_units = models.PositiveIntegerField()  # 주 or 월 수
    default_unit = models.CharField(max_length=10, choices=[('day', '일'),('week', '주'), ('month', '월')])

    def __str__(self):
        return self.name


class UserChallenge(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='challenges')
    template = models.ForeignKey(ChallengeTemplate, on_delete=models.SET_NULL, null=True)
    goal_amount = models.PositiveIntegerField()
    total_units = models.PositiveIntegerField()
    unit = models.CharField(max_length=10, choices=[('day', '일'),('week', '주'), ('month', '월')])
    is_active = models.BooleanField(default=True)
    started_at = models.DateField(auto_now_add=True)
    completed_at = models.DateField(null=True, blank=True)


    def __str__(self):
        return f"{self.user.username}의 챌린지: {self.template.name}"


class ChallengeProgress(models.Model):
    user_challenge = models.ForeignKey(UserChallenge, on_delete=models.CASCADE, related_name='progresses')
    unit_index = models.PositiveIntegerField()  # 0부터 시작하는 주차 or 월차
    is_saved = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user_challenge', 'unit_index')
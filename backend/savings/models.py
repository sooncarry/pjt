from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class ChallengeTemplate(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

class SavingChallenge(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    template = models.ForeignKey(ChallengeTemplate, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=100)
    income = models.IntegerField()
    fixed_expenses = models.IntegerField()
    luxury_budget = models.IntegerField()
    goal_amount = models.IntegerField()
    weekly_saving = models.IntegerField()
    total_weeks = models.IntegerField()
    start_date = models.DateField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)

class SavingCheck(models.Model):
    challenge = models.ForeignKey(SavingChallenge, on_delete=models.CASCADE, related_name='checks')
    date = models.DateField()
    is_saved = models.BooleanField(default=False)

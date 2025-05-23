from django.db import models

# Create your models here.
class DepositProduct(models.Model):
    name = models.CharField(max_length=100)
    interest_rate = models.FloatField()
    min_amount = models.PositiveIntegerField()

    def __str__(self):
        return self.name
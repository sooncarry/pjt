# stock/models.py
from django.db import models

class StockKnowledge(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    content = models.TextField()
    image = models.URLField()
    
    def __str__(self):
        return self.title

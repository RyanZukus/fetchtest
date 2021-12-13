from django.db import models

# Create your models here.
class PointRecord(models.Model):
    payer = models.CharField(max_length=200)
    points = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)
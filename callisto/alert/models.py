from django.db import models

class savedAlert(models.Model):
    name = models.CharField(max_length=255)
    component = models.CharField(max_length=255)
    alert_value = models.IntegerField()

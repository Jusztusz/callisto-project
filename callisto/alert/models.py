from django.db import models
import hashlib

class savedAlert(models.Model):
    name = models.CharField(max_length=255)
    component = models.CharField(max_length=255)
    alert_value = models.IntegerField()
    chatID = models.CharField(max_length=255)
    
class TelegramCredentials(models.Model):
    api_key = models.CharField(max_length=256)
    chat_id = models.CharField(max_length=50)

    def save(self, *args, **kwargs):
        self.api_key = hashlib.sha256(self.api_key.encode()).hexdigest()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Telegram Chat ID: {self.chat_id}"

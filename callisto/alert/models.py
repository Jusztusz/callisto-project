from django.db import models
from cryptography.fernet import Fernet
import base64
from django.conf import settings

class savedAlert(models.Model):
    name = models.CharField(max_length=255)
    component = models.CharField(max_length=255)
    alert_value = models.IntegerField()
    chatID = models.CharField(max_length=255)
    alertMessage = models.TextField()
    
class TelegramCredentials(models.Model):
    chat_id = models.CharField(max_length=50)
    encrypted_api_key = models.TextField()  # Titkosított API kulcs tárolása
    

    @staticmethod
    def encrypt_api_key(api_key):
        key = settings.SECRET_KEY[:32]
        fernet = Fernet(base64.urlsafe_b64encode(key.encode()))
        return fernet.encrypt(api_key.encode()).decode()

    @staticmethod
    def decrypt_api_key(encrypted_api_key):
        key = settings.SECRET_KEY[:32]
        fernet = Fernet(base64.urlsafe_b64encode(key.encode()))
        return fernet.decrypt(encrypted_api_key.encode()).decode()

    def save(self, *args, **kwargs):
        if not self.encrypted_api_key:
            self.encrypted_api_key = self.encrypt_api_key(self.api_key)
        super().save(*args, **kwargs)

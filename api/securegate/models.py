from django.db import models
from phone_field import PhoneField

# Create your models here.

class TelegramUser(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    phone = PhoneField(help_text='Contact phone number')
    active_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.username

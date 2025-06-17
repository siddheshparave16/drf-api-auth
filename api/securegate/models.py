from django.db import models
from phone_field import PhoneField

# Create your models here.

from django.db import models
from phone_field import PhoneField

class TelegramUser(models.Model):
    """
    Stores Telegram user information. Maintains exact behavior for existing APIs.
    """
    first_name = models.CharField(
        max_length=50,
        help_text="User's first name (max 50 characters)"
    )
    
    last_name = models.CharField(
        max_length=50,
        help_text="User's last name (max 50 characters, optional)",
        blank=True
    )
    
    username = models.CharField(
        max_length=50,
        unique=True,  # Ensures no duplicate usernames
        help_text="Unique Telegram username (@handle, max 50 chars)"
    )
    
    phone = PhoneField(
        unique=True,  # Prevents duplicate phone numbers
        help_text='Unique contact phone number in international format (+CountryCode)'
    )
    
    active_at = models.DateTimeField(
        auto_now=True,
        help_text="Automatically updated to current time on each save"
    )

    def __str__(self) -> str:
        return self.username

    class Meta:
        verbose_name = "Telegram User"
        verbose_name_plural = "Telegram Users"
        ordering = ['-active_at']  # Newest users first
        indexes = [
            models.Index(fields=['username']),  # Optimizes username lookups
            models.Index(fields=['phone']),     # Optimizes phone lookups
        ]
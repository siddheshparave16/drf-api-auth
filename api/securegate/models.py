from django.db import models

class TelegramUser(models.Model):
    """
    Stores Telegram user information collected from the bot.
    """
    first_name = models.CharField(
        max_length=50,
        help_text="User's first name (max 50 characters)"
    )
    
    last_name = models.CharField(
        max_length=50,
        help_text="User's last name (max 50 characters, optional)",
        blank=True,
        null=True
    )
    
    username = models.CharField(
        max_length=50,
        unique=True,
        help_text="Unique Telegram username (@handle, max 50 chars)",
        blank=True,
        null=True
    )
    
    telegram_id = models.BigIntegerField(
        unique=True,
        help_text="Telegram's unique user ID"
    )
    
    active_at = models.DateTimeField(
        auto_now=True,
        help_text="Last interaction timestamp"
    )

    def __str__(self) -> str:
        return f"{self.username} (ID: {self.telegram_id})"

    class Meta:
        verbose_name = "Telegram User"
        verbose_name_plural = "Telegram Users"
        ordering = ['-active_at']
        indexes = [
            models.Index(fields=['username']),
            models.Index(fields=['telegram_id']),
        ]

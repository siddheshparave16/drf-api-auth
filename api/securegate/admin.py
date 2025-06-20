from django.contrib import admin
from .models import TelegramUser

# Register your models here.

class TelegramUserAdmin(admin.ModelAdmin):
    model = TelegramUser
    list_display = ['username', 'telegram_id', 'first_name', 'last_name', 'active_at']
    ordering = ["active_at"]
    search_fields = ["username", "first_name", "telegram_id", "last_name"]

admin.site.register(TelegramUser, TelegramUserAdmin)


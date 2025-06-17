from rest_framework import serializers
from securegate.models import TelegramUser

class TelegramUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TelegramUser
        fields = ['id', 'first_name', 'last_name', 'username', 'phone']

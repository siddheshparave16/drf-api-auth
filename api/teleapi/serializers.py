from rest_framework import serializers
from securegate.models import TelegramUser

class TelegramUserSerializer(serializers.ModelSerializer):
    """
    Serializer for TelegramUser model
    
    Handles serialization/deserialization of Telegram user data
    Includes fields: id, first_name, last_name, username, phone
    """
    class Meta:
        model = TelegramUser
        fields = ['id', 'first_name', 'last_name', 'username', 'phone']
import datetime
from django.utils import timezone
from securegate.models import TelegramUser
from django.http import HttpResponse
from teleapi.serializers import TelegramUserSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

@api_view(['GET'])
def telegram_user_list(request):
    """Get list of all Telegram users (no auth required)"""
    teleusers = TelegramUser.objects.all()
    serializer = TelegramUserSerializer(teleusers, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
def create_telegram_user(request):
    """
    GET: Show expected user fields
    POST: Create new Telegram user
    """
    if request.method == 'GET':
        return Response({
            "first_name": "string",
            "last_name": "string",
            "username": "string",
            "phone": "string",
        }, status=status.HTTP_200_OK)

    if request.method == 'POST':
        serializer = TelegramUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_telegram_user(request, pk):
    """
    Get/update user details (requires auth)
    - GET: Get user by ID
    - PUT: Full update
    - PATCH: Partial update
    """
    try:
        teleuser = TelegramUser.objects.get(pk=pk)
    except TelegramUser.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = TelegramUserSerializer(teleuser)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = TelegramUserSerializer(teleuser, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'PATCH':
        serializer = TelegramUserSerializer(teleuser, data=request.data, partial=True) 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'DELETE'])
@permission_classes([IsAuthenticated])
def delete_telegram_user(request, pk):
    """Get or delete a user (requires auth)"""
    try:
        teleuser = TelegramUser.objects.get(pk=pk)
    except TelegramUser.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = TelegramUserSerializer(teleuser)
        return Response(serializer.data)

    elif request.method == 'DELETE':
        teleuser.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def active_users_today(request):
    """Get users active in last 24 hours (requires auth)"""
    if request.method == 'GET':
        current_time = timezone.now()
        time_before_twenty_four_ago = current_time - datetime.timedelta(hours=24)
        
        active_users = TelegramUser.objects.filter(active_at__gte=time_before_twenty_four_ago)

        serializer = TelegramUserSerializer(active_users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
from django.urls import path
from .views import (telegram_user_list, create_telegram_user,
                    update_telegram_user, delete_telegram_user, active_users_today)

urlpatterns = [
    path('telegramuser/', telegram_user_list),
    path('telegramuser/create/', create_telegram_user),
    path('telegramuser/update/<int:pk>/', update_telegram_user),
    path('telegramuser/delete/<int:pk>/', delete_telegram_user),
    path('telegramuser/active/today/', active_users_today),
]

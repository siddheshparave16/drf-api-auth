from django.urls import path, reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from .views import register, home, telegram_userView, wrapped_token_auth
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


app_name="securegate"

urlpatterns = [
    path('', home, name='home'),
    path('register/', register, name='register'),
    path('login/', LoginView.as_view(template_name='securegate/login.html', success_url=reverse_lazy('securegate:home')), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('teleusers/', telegram_userView, name='telegram_users'),
    path('api-token-auth/', wrapped_token_auth, name='api_token_auth'),
    path('api/token-jwt/', TokenObtainPairView.as_view(), name='jwt_token_obtain_pair'),
    path('api/token-jwt/refresh/', TokenRefreshView.as_view(), name='jwt_token_refresh'),
]

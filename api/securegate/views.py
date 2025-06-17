from datetime import timedelta
from django.utils import timezone
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import redirect
from .models import TelegramUser
from .forms import CustomUserCreationForm
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework.authtoken.models import Token
from django.contrib.auth import login
from .tasks import send_email

def register(request):
    """
    Handles user registration with email verification.
    Processes POST requests to create new users and GET requests to display the form.
    """
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')

            # Check for existing email before saving
            if User.objects.filter(email=email).exists():
                messages.error(request, "This email is already in use.")
                return redirect('securegate:register')

            # Create and authenticate new user
            user = form.save()
            
            # Trigger async welcome email via Celery
            send_email.delay(user.pk)
            
            # Authenticate user immediately after registration
            login(request, user)
            messages.success(request, f"Welcome {username}, You are successfully logged in.")
            return redirect('securegate:home')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'securegate/register.html', {'form': form})

@login_required
def home(request):
    """Protected home view that requires authentication"""
    return render(request, 'securegate/home.html')

@login_required
def telegram_userView(request):
    """
    Returns JSON list of all Telegram users.
    Requires authentication.
    """
    tele_users_data = TelegramUser.objects.all()
    user_list = list(tele_users_data.values())
    return HttpResponse(content=user_list)

@login_required
@csrf_exempt
def wrapped_token_auth(request):
    """
    Generates or retrieves an API token for authenticated users.
    - Automatically deletes tokens older than 1 day
    - Returns JSON with token key and expiration info
    - CSRF exempt for API access
    """
    # Clean up old tokens for this user
    Token.objects.filter(
        user=request.user, 
        created__lt=timezone.now()-timedelta(days=1)
    ).delete()
    
    # Get or create new token
    token, created = Token.objects.get_or_create(user=request.user)
    return JsonResponse({
        'token': token.key, 
        'expires_in': '1 day'
    })
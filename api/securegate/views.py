from datetime import timedelta
from django.utils import timezone
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.shortcuts import redirect
from .models import TelegramUser
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework.authtoken.models import Token
from django.contrib.auth import login


# Create your views here.

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()

            # Log in the user after successful registration
            login(request, user)

            username = form.cleaned_data.get('username')
            messages.success(request, f"Welcome {username}, You are successfully loged in.")
            return redirect('securegate:home')
    else:
        form = UserCreationForm()
    
    return render(request, 'securegate/register.html', {'form': form})


@login_required
def home(request):
    return render(request, 'securegate/home.html')


@login_required
def telegram_userView(request):
    tele_users_data = TelegramUser.objects.all()
    user_list = list(tele_users_data.values())
    return HttpResponse(content=user_list)


@login_required
@csrf_exempt
def wrapped_token_auth(request):
    """Wrapper that forces authentication for the current user"""
    # Delete tokens older than 1 days
    Token.objects.filter(user=request.user, 
                       created__lt=timezone.now()-timedelta(days=1)).delete()
    token, created = Token.objects.get_or_create(user=request.user)
    return JsonResponse({'token': token.key, 'expires_in': '1 day'})

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def login_signup_view(request):
    return render(request, 'auth.html')

from django.contrib.auth import get_user_model
User = get_user_model()

def signup_user(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        contact = request.POST.get('email_or_phone')
        password = request.POST.get('password')
        account_type = request.POST.get('account_type')

        if User.objects.filter(username=contact).exists():
            messages.error(request, "User already exists")
            return redirect('accounts')

        user = User.objects.create_user(
            username=contact,
            email=contact,
            password=password,
            first_name=first_name,
            last_name=last_name,
            contact=contact,
            account_type=account_type
        )

        messages.success(request, "Account created! Please log in.")
        return redirect('accounts')

    return redirect('accounts')


def login_user(request):
    if request.method == 'POST':
        email = request.POST.get('login_email')
        password = request.POST.get('login_password')
        user = authenticate(request, username=email, password=password)

        if user:
            login(request, user)
            messages.success(request, f"Welcome {user.first_name}")
            return redirect('home')
        else:
            messages.error(request, "Invalid credentials")
            return redirect('accounts')

def logout_user(request):
    logout(request)
    messages.info(request, "Logged out successfully")
    return redirect('auth')
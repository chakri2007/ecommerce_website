from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

User = get_user_model()

def login_signup_view(request):
    return render(request, 'auth.html')


def signup_user(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        contact = request.POST.get('email_or_phone')
        password = request.POST.get('password')
        user_type = request.POST.get('account_type')  # should match your model field: `type`

        if User.objects.filter(email=contact).exists() or User.objects.filter(phone=contact).exists():
            messages.error(request, "User already exists")
            return redirect('accounts')

        user = User.objects.create_user(
            email=contact if "@" in contact else None,
            phone=contact if "@" not in contact else None,
            password=password,
            first_name=first_name,
            last_name=last_name,
            type=user_type  # match your model field name
        )

        messages.success(request, "Account created! Please log in.")
        return redirect('accounts')

    return redirect('accounts')


def login_user(request):
    if request.method == 'POST':
        contact = request.POST.get('login_email')
        password = request.POST.get('login_password')
        user = authenticate(request, username=contact, password=password)  # works with custom backend

        if user:
            login(request, user)
            messages.success(request, f"Welcome {user.first_name}")
            return redirect('home')
        else:
            messages.error(request, "Invalid credentials")
            return redirect('accounts')
    messages.error(request, "Login first")
    return redirect('accounts')

def logout_user(request):
    logout(request)
    messages.info(request, "Logged out successfully")
    return redirect('accounts')


@login_required
def home_view(request):
    return render(request, 'home.html')

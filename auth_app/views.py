from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from .forms import UpdateProfileForm
from django.utils.translation import gettext as _

def my_view(request):
    greeting = _("Welcome to your income and expense tracker.")
    return HttpResponse(greeting)


User = get_user_model()

def login_user(request):
    if request.method == "POST":
        identifier = request.POST.get('identifier')
        password = request.POST.get('password')

        user = None
        if identifier:
            try:
                if '@' in identifier:
                    user = User.objects.get(email=identifier)
                else:
                    user = User.objects.get(phone=identifier)
            except User.DoesNotExist:
                user = None

        if user and user.check_password(password) and user.is_active:
            login(request, user)
            return redirect("index")
        else:
            return render(request, "login.html", {'error': 'Login yoki parol xato'})
    return render(request, "login.html")


def logout_user(request):
    logout(request)
    return redirect("auth_app:login")


def register_user(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if not (email or phone):
            return render(request, "register.html", {'error': 'Email yoki telefon raqamini kiriting'})

        if password1 != password2:
            return render(request, "register.html", {'error': 'Parollar mos kelmayapti'})

        user = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
        )
        user.set_password(password1)
        user.save()

        return redirect("auth_app:login")

    return render(request, "register.html")

@login_required
def profile(request):
    return render(request, 'profile.html', {'user': request.user})

@login_required
def update_profile(request):
    if request.method == "POST":
        form = UpdateProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('auth_app:profile')
    else:
        form = UpdateProfileForm(instance=request.user)

    return render(request, 'update_profile.html', {'form': form})


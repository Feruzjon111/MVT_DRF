from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.http import HttpResponse
from django.utils.translation import gettext as _

def my_view(request):
    greeting = _("Welcome to your income and expense tracker.")
    return HttpResponse(greeting)



class CustomUserManager(BaseUserManager):
    def create_user(self, phone, email=None, password=None, **extra_fields):
        if not phone and not email:
            raise ValueError('Telefon raqam yoki email kiriting')

        if email:
            email = self.normalize_email(email)
        user = self.model(phone=phone, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(phone=phone, email=email, password=password, **extra_fields)



class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, null=True, blank=True)
    phone = models.CharField(max_length=12, unique=True, null=True, blank=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone']

    objects = CustomUserManager()

    def __str__(self):
        return self.email or self.phone or "No ID"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        return self.first_name


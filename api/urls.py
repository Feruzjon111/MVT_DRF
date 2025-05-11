from django.urls import path
from .views import RegisterAPIView, LoginAPIView, LogoutAPIView, ProfileAPIView, ProfileDeleteAPIView ,ProfileUpdateAPIView, ChangePasswordView, Email_or_Phone, Auth

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('profile/', ProfileAPIView.as_view(), name='profile'),
    path('profile/update/', ProfileUpdateAPIView.as_view(), name='profile_update'),
    path('profile/delete/', ProfileDeleteAPIView.as_view(), name='profile_delete'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('Email_or_Phone/', Email_or_Phone.as_view(), name='Email_or_Phone'),
    path('auth_one/', Auth.as_view(), name='auth_one'),
]
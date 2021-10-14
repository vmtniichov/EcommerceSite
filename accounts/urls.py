from django import urls
from django.contrib.messages.api import success
from django.urls import path, include
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordResetView, 
    PasswordResetDoneView, 
    PasswordResetConfirmView, 
    PasswordResetCompleteView
)
from .views import UserCreateView, UserDetailView, UserUpdateView,PwdChangeView,PwdResetView

app_name = "accounts"

urlpatterns = [
    path('login/', LoginView.as_view(template_name = 'accounts/login.html', redirect_authenticated_user=True), name = "login"),
    path('logout/', LogoutView.as_view(), name = 'logout'),
    path('signup/', UserCreateView.as_view(), name = "signup"),
    path('profile/<pk>', UserDetailView.as_view(), name = "profile"),
    path('update/<pk>', UserUpdateView.as_view(), name = "update"),
    path('password-change/<pk>', PwdChangeView.as_view(), name = "pwd-change"),
    #enter Email 
    path('password-reset/<pk>', PwdResetView.as_view(template_name="accounts/password_reset.html"), name = "pwd-reset"),

    #Email sent success message
    path('password-reset-sent/', PasswordResetDoneView.as_view(template_name="accounts/password_reset_done.html.html"), name = "pwd-reset-done"),

    #link to password reset page
    path('password-reset/<pk>', PasswordResetConfirmView.as_view(template_name="accounts/password_reset.html"), name = "pwd"),

    #Pwd changed successfully message
    path('password-reset/<pk>', PasswordResetCompleteView.as_view(template_name="accounts/password_reset.html"), name = "pwd-reset"),
]
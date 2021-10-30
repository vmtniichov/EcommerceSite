from django import urls
from django.contrib.messages.api import success
from django.urls import path, include
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
)
from .views import UserCreateView, UserDetailView, UserUpdateView,PwdChangeView, CreateAddressView, UpdateAddressView,CheckoutView ,remove_address, load_district, load_ward

app_name = "accounts"

urlpatterns = [
    path('login/', LoginView.as_view(template_name = 'registration/login.html', redirect_authenticated_user=True), name = "login"),
    path('logout/', LogoutView.as_view(), name = 'logout'),
    path('signup/', UserCreateView.as_view(), name = "signup"),
    path('profile/', UserDetailView.as_view(), name = "profile"),
    path('update/<pk>', UserUpdateView.as_view(), name = "update"),
    path('password-change/', PwdChangeView.as_view(), name = "pwd-change"),

    path('new-address/', CreateAddressView.as_view(), name = "new-address"),
    path('update-address/<pk>', UpdateAddressView.as_view(), name = "update-address"),
    path('remove-address/<pk>', remove_address, name = "remove-address"),
    path('ajax/load-districts/', load_district, name = "ajax-load-districts"),
    path('ajax/load-wards/', load_ward, name = "ajax-load-wards"),

    path('process-to-checkout/', CheckoutView.as_view(), name = "checkout"),


]
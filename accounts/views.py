from django.shortcuts import render, redirect
from django.urls.base import reverse
from django.urls import  reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (
    PasswordChangeView, 

    PasswordResetView, 
    PasswordResetDoneView, 
    PasswordResetConfirmView, 
    PasswordResetCompleteView
)
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth import get_user_model
from django.contrib import messages

from .forms import CreateUserForm, UserUpdateForm, UserPasswordChangeForm


User = get_user_model()

class UserCreateView(CreateView):
    form_class = CreateUserForm
    success_url = reverse_lazy("accounts:login")
    template_name = 'accounts/signup.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('items:home')
        return super(UserCreateView, self).get(request, *args, **kwargs)

class UserDetailView(LoginRequiredMixin,DetailView):
    model = User
    context_object_name = "user"
    template_name = "accounts/user_profile.html"

    def get_object(self, *args, **kwargs):
        return self.request.user

class UserUpdateView(LoginRequiredMixin, UpdateView):
    form_class = UserUpdateForm
    template_name = "accounts/user_info_update.html"

    def get_object(self, *args, **kwargs):
        return self.request.user

    def get_success_url(self):
        messages.info(self.request, "Updated")
        return reverse("accounts:profile", kwargs={'pk':self.object.pk})

class PwdChangeView(LoginRequiredMixin,PasswordChangeView):
    form_class = UserPasswordChangeForm
    template_name = "accounts/password_change.html"

    def get_success_url(self) -> str:
        messages.info(self.request, "Password Changed!")
        return reverse("accounts:profile", kwargs={'pk':self.request.user.pk})

class PwdResetView(PasswordResetView):
    
    form_class = PasswordResetForm

    def get_success_url(self) -> str:
        return redirect("accounts:pwd-reset-done")



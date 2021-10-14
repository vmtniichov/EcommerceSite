from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth import  get_user_model
from django import forms
User = get_user_model()

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password1', 'password2')

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['username'].help_text = None
        self.fields['password2'].label = 'Confirm your password'
        self.fields['email'].help_text = None

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')

class UserPasswordChangeForm(PasswordChangeForm):
    class Meta():
        fields=('old_password','new_password1','new_password2')


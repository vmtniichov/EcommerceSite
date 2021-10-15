from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth import  get_user_model
from django import forms
User = get_user_model()

class CreateUserForm(UserCreationForm):
    error_messages = {
        'password_mismatch': "Mật khẩu không khớp.",
    }
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password1', 'password2')

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['username'].help_text = None
        self.fields['password2'].help_text = None
        self.fields['email'].help_text = None
        # self.fields['password1'].help_text = "<ul><li>{0}</li><li>{1}</li><li>{2}</li><li>{3}</li></ul>".format(
        #     "Mật khẩu không được bao gồm các thông tin cá nhân bên trên.",
        #     "Mật khẩu phải có ít nhất 8 ký tự.",
        #     "Mật khẩu không được là các mật khẩu thường dùng(Ví dụ:12345678).",
        #     "Mật khẩu phải bao gồm cả ký tự và số.",
        # )
        
        
        # self.fields['first_name'].label = 'Họ'
        # self.fields['last_name'].label = 'Tên'
        # self.fields['email'].label = 'Email'
        # self.fields['password1'].label = 'Mật khẩu'
        # self.fields['password2'].label = 'Nhập lại mật khẩu'

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')

class UserPasswordChangeForm(PasswordChangeForm):
    class Meta():
        fields=('old_password','new_password1','new_password2')


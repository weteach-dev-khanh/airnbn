from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User


class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        max_length=254,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-black focus:border-transparent transition-all',
            'placeholder': 'Email hoặc tên đăng nhập',
            'autofocus': True,
        })
    )
    password = forms.CharField(
        label="Mật khẩu",
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-black focus:border-transparent transition-all',
            'placeholder': 'Mật khẩu',
            'autocomplete': 'current-password',
        })
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Email hoặc tên đăng nhập'
        
    class Meta:
        model = User
        fields = ['username', 'password']

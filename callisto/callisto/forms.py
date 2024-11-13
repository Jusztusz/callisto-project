from django import forms
from django.contrib.auth.forms import AuthenticationForm

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(label="Felhasználónév", max_length=30, widget=forms.TextInput(attrs={'class':
        'form-control rounded-xl'}))
    password = forms.CharField(label="Jelszó", widget=forms.PasswordInput(attrs={'class':
        'form-control rounded-xl'}))

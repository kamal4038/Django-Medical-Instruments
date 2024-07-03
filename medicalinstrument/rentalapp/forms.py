from django import forms
from .models import *



class RegisterForm(forms.ModelForm):
    class Meta:
        models=Register

        fields=['username','password','confirm_password','dob','mobile_number','email_address','gender','address','photo']


class LoginForm(forms.Form):
    email=forms.EmailField(label="Email")
    password=forms.CharField(widget=forms.PasswordInput)


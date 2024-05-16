from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import get_user_model

class UserAuthForm(AuthenticationForm):
    username = forms.CharField()
    password = forms.CharField()
    class Meta:
        model = get_user_model()
        fields = ['username', 'password']
  
        
class UserRegForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
        
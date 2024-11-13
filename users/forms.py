from django.contrib.auth.forms import (AuthenticationForm,
                                       UserCreationForm,
                                       UserChangeForm,
                                       PasswordChangeForm,
                                       )
from django.contrib.auth import get_user_model
from django import forms

from phonenumber_field.widgets import PhoneNumberPrefixWidget
from phonenumber_field.formfields import PhoneNumberField
from django_countries.widgets import CountrySelectWidget


class UserLoginForm(AuthenticationForm):

    username = forms.CharField()
    password = forms.CharField(label='Пароль')

    class Meta:
        model = get_user_model
        fields = ['username', 'password']
        widgets = {
            'phone': PhoneNumberPrefixWidget(),
        }


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Имя пользователя')
    password1 = forms.CharField(label='Пароль')
    password2 = forms.CharField(label='Повтор пароля')

    class Meta:
        model = get_user_model()
        fields = ['username',
                  'email',
                  'phone',
                  'first_name',
                  'last_name',
                  'password1',
                  'password2',
                  ]
        labels = {
            'email': 'E-mail',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
        }
        widgets = {
            'phone': PhoneNumberPrefixWidget(
                country_attrs={
                    'class': "form-select input-group-text",
                    'style': 'font-size:10px',
                    },
                number_attrs={'class': "form-control",
                              'style': 'width:230px',
                              },
                attrs={'style': 'font-size:12px'},
                ),
        }

    def clean_email(self):
        email = self.cleaned_data['email']

        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError("Такой E-mail уже существует!")

        return email

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if get_user_model().objects.filter(phone=phone).exists():
            raise forms.ValidationError(
                "Такой номер телефона уже зарегистрирован в системе!",
                )

        return phone


class UserUpdateForm(UserChangeForm):
    username = forms.CharField(disabled=True)
    email = forms.EmailField(disabled=True)
    phone = PhoneNumberField(disabled=True, required=False)
    image = forms.ImageField(required=False)

    class Meta:
        model = get_user_model()
        fields = ['username',
                  'image',
                  'email',
                  'phone',
                  'gender',
                  'country',
                  'first_name',
                  'last_name',
                  ]
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
        }
        widgets = {
            'country': CountrySelectWidget()
        }


class UserChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField()
    new_password1 = forms.CharField()
    new_password2 = forms.CharField()

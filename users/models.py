from django.db import models
from django.contrib.auth.models import AbstractUser

from django.urls import reverse
from phonenumber_field.modelfields import PhoneNumberField
from django_countries.fields import CountryField


class User(AbstractUser):
    """Модель пользователя
    """
    image = models.ImageField(upload_to='users/',
                              blank=True, null=True,
                              verbose_name='аватар'
                              )
    email = models.EmailField(max_length=254,
                              unique=True,
                              verbose_name='эмеил'
                              )
    is_verify_email = models.BooleanField(default=False,
                                          verbose_name='подтвержденный эмеил'
                                          )
    phone = PhoneNumberField(null=True,
                             blank=False,
                             verbose_name='номер телефона'
                             )
    country = CountryField(verbose_name='страна',
                           null=True,
                           blank=True,
                           blank_label='(select country)'
                           )
    gender = models.CharField(verbose_name='пол',
                              choices=(('men', 'Мужчина'),
                                       ('women', 'Женщина'),
                                       (None, 'Не выбрано')),
                              null=True,
                              blank=True,
                              default=None
                              )

    class Meta:
        db_table = 'user'
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

    def get_absolute_url(self):
        return reverse("users:user", kwargs={"username": self.username})

from django.urls import path
from users.apps import UsersConfig
from users.views import LoginUser, RegUser
from django.contrib.auth.views import LogoutView

app_name = UsersConfig.name

urlpatterns = [
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('registration/', RegUser.as_view(), name='reg'),
]
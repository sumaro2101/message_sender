from django.urls import path

from main_page.apps import MainPageConfig
from . import views


app_name = MainPageConfig.name


urlpatterns = [
    path('', views.MainPageView.as_view(), name='main'),
]

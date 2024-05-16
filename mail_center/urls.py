from django.urls import path
from mail_center.apps import MailCenterConfig
from mail_center.views import mail_center

app_name = MailCenterConfig.name

urlpatterns = [
    path('mails/', mail_center, name='mails'),
    
]
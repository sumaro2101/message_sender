from django.urls import path
from mail_center.apps import MailCenterConfig
from mail_center.views import ListSendMessages

app_name = MailCenterConfig.name

urlpatterns = [
    path('mails/', ListSendMessages.as_view(), name='mails'),
    
]
from django.urls import path
from mail_center.apps import MailCenterConfig
from mail_center.views import ListSendMessages, CreateSend

app_name = MailCenterConfig.name

urlpatterns = [
    path('mails/', ListSendMessages.as_view(), name='mails'),
    path('mails/create/<slug:slug>/', CreateSend.as_view(), name='mail_create'),
]
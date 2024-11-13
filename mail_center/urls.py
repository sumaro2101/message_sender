from django.urls import path
from mail_center.apps import MailCenterConfig
from mail_center.views import (ListSendMessages,
                               CreateSend,
                               UpdateSend,
                               ViewSend,
                               DeleteSend,
                               )


app_name = MailCenterConfig.name


urlpatterns = [
    path('mails/',
         ListSendMessages.as_view(),
         name='mails',
         ),
    path('mails/detail/<slug:slug>/',
         ViewSend.as_view(),
         name='mail_detail',
         ),
    path('mails/create/<slug:slug>/',
         CreateSend.as_view(),
         name='mail_create',
         ),
    path('mails/update/<slug:slug>/',
         UpdateSend.as_view(),
         name='mail_update',
         ),
    path('mails/delete/<slug:slug>/',
         DeleteSend.as_view(),
         name='mail_delete',
         ),
]

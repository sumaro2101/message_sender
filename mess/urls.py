from django.urls import path
from mess.apps import MessConfig
from mess.views import MessagesListView, main_list, MessageCreateView, MessageUpdateView, MessageDeleteView

app_name = MessConfig.name

urlpatterns = [
    path('', main_list, name='main'),
    path('messages/', MessagesListView.as_view(), name='list'),
    path('messages/create/', MessageCreateView.as_view(), name='create_mess'),
    path('messages/update/<slug:slug>', MessageUpdateView.as_view(), name='update_mess'),
    path('messages/delete/<slug:slug>', MessageDeleteView.as_view(), name='delete_mess'),
]
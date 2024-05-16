from django.urls import path
from our_clients.apps import OurClientsConfig
from our_clients.views import client_list

app_name = OurClientsConfig.name

urlpatterns = [
    path('clients/', client_list, name='clients'),
    
]
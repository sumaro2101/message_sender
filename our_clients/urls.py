from django.urls import path
from our_clients.apps import OurClientsConfig
from .views import (ClientCreateView,
                    ClientToggleActivityView,
                    ClientUpdateView,
                    ClientsListView,
                    )


app_name = OurClientsConfig.name


urlpatterns = [
    path('clients/',
         ClientsListView.as_view(),
         name='clients',
         ),
    path('clients/create/',
         ClientCreateView.as_view(),
         name='create_client',
         ),
    path('clietns/update/<int:pk>',
         ClientUpdateView.as_view(),
         name='update_client',
         ),
    path('clietns/delete/<int:pk>',
         ClientToggleActivityView.as_view(),
         name='delete_client',
         ),
]

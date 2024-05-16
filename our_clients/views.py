from django.shortcuts import render

# Create your views here.

def client_list(request):
    return render(request, 'our_clients/clients_list.html', {'catg_selected': 3,
                                                             'title': 'Клиенты'})
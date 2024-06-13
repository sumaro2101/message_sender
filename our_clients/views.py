from django.shortcuts import render
from django.urls import reverse_lazy
from .models import ClientServise
from .forms import AddClientForm
from django.views.generic import CreateView, DeleteView, UpdateView, ListView
from django.contrib.auth import mixins
from pytils.translit import slugify
# Create your views here.

    
class ClientsListView(mixins.LoginRequiredMixin, ListView):
    template_name = 'our_clients/clients_list.html'
    model = ClientServise
    context_object_name = 'clients'
    paginate_by = 21
    extra_context = {'title': 'clients', 'catg_selected': 3}
    
    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            return queryset.select_related('employee').filter(employee=self.request.user)
        return queryset.select_related('employee')
    
    
class ClientCreateView(mixins.LoginRequiredMixin, CreateView):
    model = ClientServise
    form_class = AddClientForm
    template_name = 'our_clients/cliendinfo_form.html'
    success_url = reverse_lazy('our_clients:clients')
    extra_context = {'title': 'create', 'catg_selected': 3}


class ClientUpdateView(mixins.LoginRequiredMixin, UpdateView):
    model = ClientServise
    form_class = AddClientForm
    template_name = 'our_clients/cliendinfo_form.html'
    context_object_name = 'client_p'
    success_url = reverse_lazy('our_clients:clients')
    extra_context = {'title': 'update', 'catg_selected': 3}
    
    def form_valid(self, form):
        form.instance.slug = f'{slugify(form.instance.employee.pk)}-{slugify(form.instance.title_message)}'
        return super().form_valid(form)


class ClientDeleteView(mixins.LoginRequiredMixin, DeleteView):
    model = ClientServise
    template_name = 'our_clients/client_delete.html'
    context_object_name = 'client_p'
    success_url = reverse_lazy('our_clients:clients')
    extra_context = {'title': 'update', 'catg_selected': 3}
    
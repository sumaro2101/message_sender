from typing import Any
from django.forms import BaseModelForm
from django.http import HttpRequest, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView, ListView
from django.contrib.auth import mixins
from django.db.models import Q

from pytils.translit import slugify

from .models import ClientServise
from .forms import AddClientForm
from .mixins import OwnerOrStaffPermissionMixin, CheckModeratorMixin
# Create your views here.

    
class ClientsListView(mixins.LoginRequiredMixin, CheckModeratorMixin, ListView):
    template_name = 'our_clients/clients_list.html'
    model = ClientServise
    context_object_name = 'clients'
    paginate_by = 21
    extra_context = {'title': 'Clients', 'catg_selected': 3}
    
    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_staff and not self.request.user.is_superuser:
            return queryset.filter(Q(employee=self.request.user)).order_by('client_first_name').select_related('employee')
        return queryset.order_by('client_first_name').select_related('employee')
    
    
class ClientCreateView(mixins.LoginRequiredMixin, mixins.UserPassesTestMixin, CreateView):
    model = ClientServise
    form_class = AddClientForm
    template_name = 'our_clients/cliendinfo_form.html'
    success_url = reverse_lazy('our_clients:clients')
    extra_context = {'title': 'ClientCreate', 'catg_selected': 3}
    
    def form_valid(self, form: BaseModelForm):
        form.instance.employee = self.request.user
        return super().form_valid(form)
    
    def test_func(self) -> bool | None:
        return not self.request.user.groups.filter(name='moderator').exists()


class ClientUpdateView(mixins.LoginRequiredMixin, OwnerOrStaffPermissionMixin, UpdateView):
    model = ClientServise
    form_class = AddClientForm
    template_name = 'our_clients/cliendinfo_form.html'
    context_object_name = 'client_p'
    success_url = reverse_lazy('our_clients:clients')
    extra_context = {'title': 'ClientUpdate', 'catg_selected': 3}
    
    def form_valid(self, form):
        form.instance.slug = f'{slugify(form.instance.employee.pk)}-{slugify(form.instance.client_last_name)}'
        return super().form_valid(form)
    
    def test_func(self) -> bool | None:
        return self.request.user.is_superuser or\
                self.request.user == self.get_object().employee


class ClientToggleActivityView(mixins.LoginRequiredMixin ,OwnerOrStaffPermissionMixin, DeleteView):
    model = ClientServise
    template_name = 'our_clients/client_delete.html'
    context_object_name = 'client_p'
    success_url = reverse_lazy('our_clients:clients')
    extra_context = {'title': 'update', 'catg_selected': 3}
    
    def form_valid(self, form):
        if self.object.actual:
            self.object.actual = False
        else:
            self.object.actual = True
        self.object.save(update_fields=['actual'])
        return HttpResponseRedirect(self.get_success_url())
    
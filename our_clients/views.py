from django.forms import BaseModelForm
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView, ListView
from django.contrib.auth import mixins
from django.db.models import Q

from pytils.translit import slugify

from .models import ClientServise
from .forms import AddClientForm
from .mixins import OwnerOrStaffPermissionMixin
# Create your views here.

    
class ClientsListView(mixins.LoginRequiredMixin, ListView):
    template_name = 'our_clients/clients_list.html'
    model = ClientServise
    context_object_name = 'clients'
    paginate_by = 21
    extra_context = {'title': 'clients', 'catg_selected': 3}
    
    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_staff and not self.request.user.is_superuser:
            return queryset.filter(Q(employee=self.request.user)).order_by('client_first_name').select_related('employee')
        return queryset.order_by('client_first_name').select_related('employee')
    
    
class ClientCreateView(mixins.LoginRequiredMixin, CreateView):
    model = ClientServise
    form_class = AddClientForm
    template_name = 'our_clients/cliendinfo_form.html'
    success_url = reverse_lazy('our_clients:clients')
    extra_context = {'title': 'create', 'catg_selected': 3}
    
    def form_valid(self, form: BaseModelForm):
        form.instance.employee = self.request.user
        return super().form_valid(form)


class ClientUpdateView(mixins.LoginRequiredMixin, OwnerOrStaffPermissionMixin, UpdateView):
    model = ClientServise
    form_class = AddClientForm
    template_name = 'our_clients/cliendinfo_form.html'
    context_object_name = 'client_p'
    success_url = reverse_lazy('our_clients:clients')
    extra_context = {'title': 'update', 'catg_selected': 3}
    
    def form_valid(self, form):
        form.instance.slug = f'{slugify(form.instance.employee.pk)}-{slugify(form.instance.client_last_name)}'
        return super().form_valid(form)
    
    def test_func(self) -> bool | None:
        return self.request.user.is_staff or\
            self.request.user.is_superuser or\
                self.request.user == self.get_object().employee


class ClientDeleteView(OwnerOrStaffPermissionMixin, DeleteView):
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
    
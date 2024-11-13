from typing import Any
from django.forms import BaseModelForm
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import (CreateView,
                                  DeleteView,
                                  UpdateView,
                                  ListView,
                                  )
from django.contrib.auth import mixins
from django.db.models import Q

from pytils.translit import slugify

from .models import ClientServise
from .forms import AddClientForm
from .mixins import OwnerOrStaffPermissionMixin, CheckModeratorMixin
from mail_center.cache import get_or_set_cache, delete_cache


class ClientsListView(mixins.LoginRequiredMixin,
                      CheckModeratorMixin,
                      ListView):
    template_name = 'our_clients/clients_list.html'
    model = ClientServise
    context_object_name = 'clients'
    paginate_by = 21
    extra_context = {'title': 'Clients', 'catg_selected': 3}

    def get_queryset(self):
        queryset = get_or_set_cache(ClientServise, is_queryset_all=True)
        if not queryset:
            queryset = super().get_queryset()

        if (not self.request.user.is_staff and
            not self.request.user.is_superuser):
            return (queryset.filter(Q(employee=self.request.user))
                    .order_by('client_first_name')
                    .select_related('employee'))

        return (queryset
                .order_by('client_first_name')
                .select_related('employee'))

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['content_manager'] = get_or_set_cache(
            self.request.user.groups,
            slug='content-manager',
            type_field='name',
            )
        context['title'] = 'Clients'
        context['catg_selected'] = 3
        return context


class ClientCreateView(mixins.LoginRequiredMixin,
                       CheckModeratorMixin,
                       mixins.UserPassesTestMixin,
                       CreateView):
    model = ClientServise
    form_class = AddClientForm
    template_name = 'our_clients/cliendinfo_form.html'
    success_url = reverse_lazy('our_clients:clients')
    extra_context = {'title': 'ClientCreate', 'catg_selected': 3}

    def form_valid(self, form: BaseModelForm):
        form.instance.employee = self.request.user
        delete_cache(ClientServise, is_queryset_all=True)
        return super().form_valid(form)

    def test_func(self) -> bool | None:
        return (not self.moderator and
                not self.request.user.is_staff or
                self.request.user.is_superuser)


class ClientUpdateView(mixins.LoginRequiredMixin,
                       OwnerOrStaffPermissionMixin,
                       UpdateView):
    model = ClientServise
    form_class = AddClientForm
    template_name = 'our_clients/cliendinfo_form.html'
    context_object_name = 'client_p'
    success_url = reverse_lazy('our_clients:clients')
    extra_context = {'title': 'ClientUpdate', 'catg_selected': 3}

    def form_valid(self, form):
        slug_employee = slugify(form.instance.employee.pk)
        slug_client = slugify(form.instance.client_last_name)
        form.instance.slug = f'{slug_employee}-{slug_client}'
        delete_cache(ClientServise, is_queryset_all=True)
        return super().form_valid(form)

    def test_func(self) -> bool | None:
        return self.request.user.is_superuser or\
                self.request.user == self.get_object().employee


class ClientToggleActivityView(mixins.LoginRequiredMixin,
                               OwnerOrStaffPermissionMixin,
                               DeleteView):
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
        delete_cache(ClientServise, is_queryset_all=True)
        return HttpResponseRedirect(self.get_success_url())

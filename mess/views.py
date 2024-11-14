from typing import Any
from django.db.models.query import Q
from django.http import HttpResponseRedirect
from django.contrib.auth import mixins
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.db import transaction

from pytils.translit import slugify

from .models import MessageInfo
from .forms import CreateMessageForm
from .mixins import OwnerOrStaffPermissionMixin, CheckModeratorMixin
from mail_center.models import SendingMessage
from mail_center.core.scheduler_core import update_task_interval
from mail_center.cache import get_or_set_cache, delete_cache


class MessagesListView(mixins.LoginRequiredMixin,
                       CheckModeratorMixin,
                       ListView):
    model = MessageInfo
    paginate_by = 4
    context_object_name = 'messages'
    template_name = 'messages/messages_list.html'

    def get_queryset(self):
        queryset = get_or_set_cache(MessageInfo, is_queryset_all=True)
        if not queryset:
            queryset = super().get_queryset()
        if not self.request.user.is_staff:
            return (queryset.select_related('employee')
                    .filter(employee=self.request.user)
                    .order_by('-actual', '-time_edit'))
        return (queryset.select_related('employee')
                .order_by('-actual', '-time_edit'))

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        content_manager = get_or_set_cache(self.request.user.groups,
                                           slug='content-manager',
                                           type_field='name',
                                           )
        context['content_manager'] = content_manager
        context['title'] = 'Messages'
        context['catg_selected'] = 2
        return context


class MessageCreateView(mixins.LoginRequiredMixin,
                        mixins.UserPassesTestMixin,
                        CreateView):
    model = MessageInfo
    form_class = CreateMessageForm
    template_name = 'messages/messageinfo_form.html'
    success_url = reverse_lazy('mess:list')
    extra_context = {'title': 'create', 'catg_selected': 2}

    def form_valid(self, form):
        form.instance.employee = self.request.user
        slug_employee = slugify(form.instance.employee.pk)
        slug_message = slugify(form.instance.title_message)
        form.instance.slug = f'{slug_employee}-{slug_message}'
        delete_cache(MessageInfo, is_queryset_all=True)
        return super().form_valid(form)

    def test_func(self) -> bool | None:
        return (not self.request.user.is_staff or
                self.request.user.is_superuser)


class MessageUpdateView(mixins.LoginRequiredMixin,
                        OwnerOrStaffPermissionMixin,
                        UpdateView):
    model = MessageInfo
    form_class = CreateMessageForm
    template_name = 'messages/messageinfo_form.html'
    context_object_name = 'message'
    success_url = reverse_lazy('mess:list')

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = 'MessageUpdate'
        context['catg_selected'] = 2
        return context

    def form_valid(self, form):
        slug_employee = slugify(form.instance.employee.pk)
        slug_message = slugify(form.instance.title_message)
        form.instance.slug = f'{slug_employee}-{slug_message}'
        delete_cache(MessageInfo, is_queryset_all=True)
        return super().form_valid(form)

    def test_func(self) -> bool | None:
        return self.request.user.is_superuser or\
                self.request.user == self.get_object().employee


class MessageChangeActivityView(mixins.LoginRequiredMixin,
                                OwnerOrStaffPermissionMixin,
                                DeleteView):
    model = MessageInfo
    template_name = 'messages/message_delete.html'
    context_object_name = 'message'
    success_url = reverse_lazy('mess:list')
    extra_context = {'title': 'update', 'catg_selected': 2}

    def form_valid(self, form):
        newsletter = SendingMessage.objects.filter(Q(message=self.object))
        objects = []
        fields = []

        if self.object.actual:
            self.object.actual = False
            for news in newsletter:
                news.status = 'end'
                news.date_first_send = None
                objects.append(news)
            fields.extend(['status', 'date_first_send',])
        else:
            self.object.actual = True
            for news in newsletter:
                news.status = 'freeze'
                objects.append(news)
            fields.append('status')

        with transaction.atomic():
            self.object.save(update_fields=['actual'])
            if objects:
                SendingMessage.objects.bulk_update(
                    objs=objects,
                    fields=fields,
                    )
                [update_task_interval(new,
                                      interval=None,
                                      start_time=new.date_first_send,
                                      changed_data=fields,
                                      )
                 for new
                 in objects]
                [delete_cache(SendingMessage, new.slug)
                 for new
                 in objects]
        delete_cache(SendingMessage, is_queryset_all=True)
        return HttpResponseRedirect(self.get_success_url())

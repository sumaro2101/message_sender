from typing import Any
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.contrib.auth import mixins

from pytils.translit import slugify

from .models import SendingMessage
from .forms import FormSendMesssage
from .services import (check_message, create_task_interval, update_task_interval,
                       delete_task_interval,
                       get_task, get_procent_interval_time)
from .mixins import OwnerOrStaffPermissionMixin
from mess.models import MessageInfo
# Create your views here.


class ViewSend(mixins.LoginRequiredMixin, OwnerOrStaffPermissionMixin, DetailView):
    queryset = SendingMessage.objects.select_related('message', 'owner_send')
    context_object_name = 'mail'
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        task = get_task(self.object)
        context['task'] = task
        context['clients'] = self.object.clients.filter(actual=True)
        
        if self.object.status in ['freeze', 'create'] or not self.object.clients.filter(actual=True).exists():
            context['next_send'] = None
            context['procent_to_send'] = None
        elif not task.last_run_at and task.start_time or task.last_run_at < task.start_time:
            next_send = task.start_time + self.object.periodicity
            procent_to_send = get_procent_interval_time(self.object.periodicity, next_send)
            context['procent_to_send'] =  procent_to_send
            context['next_send'] = next_send
        elif task.last_run_at > task.start_time:
            next_send = task.last_run_at + self.object.periodicity
            procent_to_send = get_procent_interval_time(self.object.periodicity, next_send)
            context['procent_to_send'] =  procent_to_send
            context['next_send'] = next_send
        else:
            context['next_send'] = None
            context['procent_to_send'] = None   
        
        return context
    
    
class ListSendMessages(mixins.LoginRequiredMixin, ListView):
    model = SendingMessage
    context_object_name = 'messages'
    paginate_by = 4
    template_name = 'mail_center/mail_list.html'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_staff and not self.request.user.is_superuser:
            queryset = queryset.filter(owner_send=self.request.user).order_by('-pk').select_related('message')
        else:
            queryset = queryset.order_by('-pk').select_related('message')
        return queryset
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Send'
        context['catg_selected'] = 5
        return context
    
    
class CreateSend(mixins.LoginRequiredMixin, mixins.UserPassesTestMixin, CreateView):
    model = SendingMessage
    form_class = FormSendMesssage
    
    def dispatch(self, request, *args, **kwargs):
        self.message = check_message(MessageInfo, self.kwargs.get('slug'))
        return super().dispatch(request, *args, **kwargs)
        
    def form_valid(self, form):
        form.instance.owner_send = self.request.user
        form.instance.message = self.message
        periodicity = form.cleaned_data['periodicity']
        start_time = form.cleaned_data['date_first_send']
        
        if start_time:
            form.instance.status = 'run'
        form.slug = None
        form = form.save()
        
        form.slug = f'{self.request.user.id}-{slugify(self.request.user.username)}-{form.pk}-{slugify(self.message.title_message)}'
        form.save()
        
        self.object = form
        create_task_interval(object_=form, task='mail_center.tasks.send', interval=periodicity, start_time=start_time)
        return HttpResponseRedirect(self.get_success_url())
    
    def get_initial(self) -> dict[str, Any]:
        initial = super().get_initial()
        initial['message'] = self.message.pk
        return initial
    
    def get_form_kwargs(self) -> dict[str, Any]:
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def get_success_url(self) -> str:
        return reverse_lazy('mail_center:mail_detail', kwargs={'slug': self.object.slug})
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['message'] = self.message
        return context
      
    def test_func(self) -> bool | None:
        return self.message.employee == self.request.user or self.request.user.is_superuser
    

class UpdateSend(mixins.LoginRequiredMixin, OwnerOrStaffPermissionMixin, UpdateView):
    model = SendingMessage
    form_class = FormSendMesssage
    context_object_name = 'mail_up'
    
    def get_form_kwargs(self) -> dict[str, Any]:
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        if form.changed_data:
            periodicity = form.cleaned_data['periodicity']
            start_time = form.cleaned_data['date_first_send']
            if not start_time and not form.instance.status == 'create':
                form.changed_data.append('status')
                form.instance.status = 'freeze'
            elif start_time and form.instance.status in ('create', 'freeze'):
                form.changed_data.append('status')
                form.instance.status = 'run'
            self.object = form.save()
            update_task_interval(object_=self.object,
                                interval=periodicity,
                                start_time=start_time,
                                changed_data=form.changed_data)
        
        return HttpResponseRedirect(self.get_success_url())
    
    
class DeleteSend(mixins.PermissionRequiredMixin, DeleteView):
    model = SendingMessage
    permission_required = 'mail_center.delete_sendingmessage'
    context_object_name = 'send_delete'
    
    def get_success_url(self) -> str:
        return reverse_lazy('mail_center:mails')
    
    def form_valid(self, form):
        delete_task_interval(self.object)
        return super().form_valid(form)
    
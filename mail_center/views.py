from typing import Any
from django.db.models.base import Model as Model
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.contrib.auth import mixins
from django.core.exceptions import PermissionDenied

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
    
    def get_context_data(self, *, object_list=None, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        task = get_task(self.object)
        context['task'] = task
        context['clients'] = self.object.clients.filter(actual=True)
        context['title'] = 'Send'
        context['catg_selected'] = 5
        
        if self.object.status in ['freeze', 'create', 'end'] or not self.object.clients.filter(actual=True).exists():
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
    
    def post(self, request, *args, **kwargs):
        update_fields = []
        if status := request.POST.get('change_status'):
            if not self.object.slug == status:
                raise PermissionDenied()
            if not self.object.status == 'freeze':
                self.object.status = 'freeze'
                update_fields.append('status')
            else:
                self.object.status = 'run'
                update_fields.append('status')
        
        if end_task := request.POST.get('end_task'):
            if not self.object.slug == end_task:
                raise PermissionDenied()
            if not self.object.status == 'end':
                self.object.status = 'end'
                self.object.date_first_send = None
                update_fields.extend(['status', 'date_first_send', ])
        
        self.object.save(update_fields=update_fields)
        update_task_interval(self.object, interval=None, changed_data=update_fields)
        return redirect('mail_center:mail_detail', **{'slug': self.object.slug})
    
    
class ListSendMessages(mixins.LoginRequiredMixin, ListView):
    model = SendingMessage
    context_object_name = 'messages'
    paginate_by = 4
    template_name = 'mail_center/mail_list.html'
    
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any):
        return super().dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
        queryset = super().get_queryset()
        request_get = self.request.GET
        match request_get.get('status'):
            case 'run':
                queryset = queryset.filter(status='run')
                self.filter_select = '2'
            case 'create':
                queryset = queryset.filter(status='create')
                self.filter_select = '3'
            case 'freeze':
                queryset = queryset.filter(status='freeze')
                self.filter_select = '4'
            case 'end':
                queryset = queryset.filter(status='end')
                self.filter_select = '5'
            case _:
                self.filter_select = '1'
            
        if not self.request.user.is_staff and not self.request.user.is_superuser:
            queryset = queryset.filter(owner_send=self.request.user).order_by('-status').select_related('message')
        else:
            queryset = queryset.order_by('-status').select_related('message')
        return queryset
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Send'
        context['catg_selected'] = 5
        context['filter_select'] = self.filter_select
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
        kwargs = {'template_render': 'mail_form/mail_send_form.html'}
        create_task_interval(object_=form, task='mail_center.tasks.send', interval=periodicity, start_time=start_time, **kwargs)
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
        context['title'] = 'Send'
        context['catg_selected'] = 5
        return context
      
    def test_func(self) -> bool | None:
        return self.message.employee == self.request.user or self.request.user.is_superuser
    

class UpdateSend(mixins.LoginRequiredMixin, OwnerOrStaffPermissionMixin, UpdateView):
    model = SendingMessage
    form_class = FormSendMesssage
    context_object_name = 'mail_up'
    
    def get(self, request: HttpRequest, *args: str, **kwargs: Any):
        if self.object.status == 'end':
            raise PermissionDenied()
        return super().get(request, *args, **kwargs)    
    
    def get_form_kwargs(self) -> dict[str, Any]:
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        if form.changed_data:
            periodicity = form.cleaned_data['periodicity'] if 'periodicity' in form.changed_data else None
            start_time = form.cleaned_data['date_first_send']
            
            if not form.enabled:
                form.instance.status = 'end'
                form.instance.date_first_send = None
                form.changed_data.extend('status', 'date_first_send',)
                
            elif not start_time and not form.instance.status == 'create':
                form.changed_data.append('status')
                form.instance.status = 'freeze'
                
            elif start_time and form.instance.status in ('create', 'freeze'):
                form.changed_data.append('status')
                form.instance.status = 'run'
                
            self.object = form.save()
            
            kwargs = {'template_render': 'mail_form/mail_send_form.html'}
            update_task_interval(object_=self.object,
                                interval=periodicity,
                                start_time=start_time,
                                changed_data=form.changed_data,
                                **kwargs)
        
        return HttpResponseRedirect(self.get_success_url())
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = 'Send'
        context['catg_selected'] = 5
        return context
    
    
class DeleteSend(mixins.PermissionRequiredMixin, DeleteView):
    model = SendingMessage
    permission_required = 'mail_center.delete_sendingmessage'
    context_object_name = 'send_delete'
    
    def get_success_url(self) -> str:
        return reverse_lazy('mail_center:mails')
    
    def form_valid(self, form):
        delete_task_interval(self.object)
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = 'Send'
        context['catg_selected'] = 5
        return context
    
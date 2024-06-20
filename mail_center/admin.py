from django.contrib import admin
from django.contrib.admin.models import LogEntry
from django.db.models.query import QuerySet
from django.http import HttpRequest
from django.forms import ModelForm

from pytils.translit import slugify

from typing import Any

from .models import SendingMessage, ResultsSendMessages
from mail_center.services import create_task_interval, update_task_interval, delete_task_interval

# Register your models here.

@admin.register(SendingMessage)
class SendingMessageAdmin(admin.ModelAdmin):
    model = SendingMessage
    list_display = ('pk', 'message', 'clients', 'date_first_send', 'periodicity', 'status')

    fieldsets = (
        (('Информация о письме'), {
            'fields': ('message', 'clients',),
            'classes': ('extrapretty', 'wide'),
        }),
        (('Временые интервалы'), {
            'fields': ('date_first_send', 'periodicity'),
            'classes': ('extrapretty', 'wide'),
        }),
        (('Статус'), {
            'fields': ('status',),
            'classes': ('extrapretty', 'wide'),
        })
    )
    
    def clients(self, obj):
        return [client for client in obj.clients.get_queryset()]
    
    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        queryset = super().get_queryset(request)
        return queryset.select_related('message')
    
    def get_readonly_fields(self, request: HttpRequest, obj: Any | None = ...) -> list[str] | tuple[Any, ...]:
        if not request.user.is_superuser:
            self.readonly_fields = ('status')
        return super().get_readonly_fields(request, obj)
    
    def _change_status(self, obj):
        obj = obj
        update_fields = []
        if not obj.date_first_send and not obj.status == 'create':
                obj.status = 'freeze'
                update_fields.append('status')
        elif obj.date_first_send and obj.status in ('create', 'freeze'):
            obj.status = 'run'
            update_fields.append('status')
            
        return update_fields, obj
    
    def log_addition(self, request: HttpRequest, obj: Any, message: Any) -> LogEntry: 
        update_fields, obj = self._change_status(obj) 
        obj.slug = f'{request.user.id}-{slugify(request.user.username)}-{obj.pk}-{slugify(obj.message.title_message)}'
        update_fields.append('slug')
        obj.save(update_fields=update_fields)
        
        kwargs = {'template_render': 'mail_form/mail_send_form.html'}
        create_task_interval(object_=obj, task='mail_center.tasks.send', interval=obj.periodicity, start_time=obj.date_first_send, **kwargs)
        return super().log_addition(request, obj, message)
    
    def log_change(self, request: HttpRequest, obj: Any, message: Any) -> LogEntry:
        change_data = ['periodicity', 'date_first_send', 'status']
        _, obj = self._change_status(obj)
        obj.save(update_fields=change_data)
        
        update_task_interval(object_=obj, interval=obj.periodicity, start_time=obj.date_first_send, changed_data=change_data)
        return super().log_change(request, obj, message)
    
    
@admin.register(ResultsSendMessages)
class ResultsSendMessagesAdmin(admin.ModelAdmin):
    model = ResultsSendMessages
    list_display = ('send_task', 'sheduler_task', 'date_done', 'result')
    
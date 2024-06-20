from typing import Any
from django.contrib import admin
from django.contrib.admin.models import LogEntry
from django.db.models.query import QuerySet
from django.http import HttpRequest

from pytils.translit import slugify

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
    
    
@admin.register(ResultsSendMessages)
class ResultsSendMessagesAdmin(admin.ModelAdmin):
    model = ResultsSendMessages
    list_display = ('send_task', 'sheduler_task', 'date_done', 'result')
    
from django.contrib import admin
from django.contrib.admin.models import LogEntry
from django.db.models.query import QuerySet
from django.http import HttpRequest
from django.db.models import Model

from pytils.translit import slugify

from typing import Any

from .models import SendingMessage, ResultsSendMessages
from mail_center.core.scheduler_core import (create_task_interval,
                                             update_task_interval,
                                             delete_task_interval,
                                             )


@admin.register(SendingMessage)
class SendingMessageAdmin(admin.ModelAdmin):
    model = SendingMessage
    list_display = ('pk',
                    'message',
                    'clients',
                    'date_first_send',
                    'periodicity',
                    'enabled',
                    'status',
                    )

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
            'fields': ('status', 'enabled'),
            'classes': ('extrapretty', 'wide'),
        })
    )

    def clients(self, obj: Model) -> list[Model]:
        """Поле ManyToMany для вывода клиетов
        """
        return [client
                for client
                in obj.clients.get_queryset()]

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        queryset = super().get_queryset(request)
        return queryset.select_related('message')

    def get_readonly_fields(self,
                            request: HttpRequest,
                            obj: Any | None = ...,
                            ) -> list[str] | tuple[Any, ...]:
        if (not request.user.is_superuser or
            request.user.groups.filter(name='moderator').exists()):
            self.readonly_fields = ('status',
                                    'message',
                                    'clients',
                                    'date_first_send',
                                    'periodicity',
                                    )
        return super().get_readonly_fields(request, obj)

    def _change_status(self, obj: Model) -> tuple[list[str], Model]:
        """Логика автоматизированного изменения статуса исходя
        из атрибутов

        Args:
            obj (Model): Целевая модель

        Returns:
            tuple(list(str), Model): Возвращает готовый список
            и измененую модель
        """
        obj: Model = obj
        if not isinstance(obj, Model):
            raise TypeError(f'{obj} должен быть классом модели')
        update_fields: list[str] = []
        if not obj.enabled:
            obj.status = 'end'
            obj.date_first_send = None
            update_fields.extend(['status', 'date_first_send',])
        elif not obj.date_first_send and not obj.status == 'create':
            obj.status = 'freeze'
            update_fields.append('status')
        elif (obj.date_first_send and
              obj.status in ('create', 'freeze', 'end')):
            obj.status = 'run'
            update_fields.append('status')
        return update_fields, obj

    # CRUD система по редактированию рассписания в
    # зависимости от изменения целевого объекта
    def log_addition(self,
                     request: HttpRequest,
                     obj: Any,
                     message: Any,
                     ) -> LogEntry:
        """Создание рассписания
        """
        update_fields, obj = self._change_status(obj)
        slug_username = slugify(request.user.username)
        slug_message = slugify(obj.message.title_message)
        obj.slug = f'{request.user.id}-{slug_username}-{obj.pk}-{slug_message}'
        update_fields.append('slug')
        obj.save(update_fields=update_fields)

        kwargs = {'template_render': 'mail_form/mail_send_form.html'}
        create_task_interval(object_=obj,
                             task='mail_center.tasks.send',
                             interval=obj.periodicity,
                             start_time=obj.date_first_send,
                             **kwargs,
                             )
        return super().log_addition(request, obj, message)

    def log_change(self,
                   request: HttpRequest,
                   obj: Any,
                   message: Any,
                   ) -> LogEntry:
        """Изменения рассписания
        """
        change_data = ['periodicity',
                       'date_first_send',
                       'status']
        _, obj = self._change_status(obj)
        obj.save(update_fields=change_data)

        update_task_interval(object_=obj,
                             interval=obj.periodicity,
                             start_time=obj.date_first_send,
                             changed_data=change_data,
                             )
        return super().log_change(request, obj, message)

    def log_deletion(self,
                     request: HttpRequest,
                     obj: Any,
                     object_repr: str,
                     ) -> LogEntry:
        """Удаление рассписания
        """
        delete_task_interval(obj)
        return super().log_deletion(request, obj, object_repr)


@admin.register(ResultsSendMessages)
class ResultsSendMessagesAdmin(admin.ModelAdmin):
    model = ResultsSendMessages
    list_display = ('send_task',
                    'sheduler_task',
                    'date_done',
                    'result',
                    )

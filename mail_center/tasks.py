from django_celery_beat.models import PeriodicTask

from typing import Union
from smtplib import SMTPException

from .services import send_mails, _convert_unique_name_to_id
from .models import SendingMessage, ResultsSendMessages
from mail_center.celery import app


@app.task
def send(object_unique_name: Union[str, None] = None,
         template_render: Union[str, None] = None,
         ) -> None:
    """Задание для события и рассписания, оправка писем пользователям

    Args:
        object_unique_name (str|None): Уникальное имя обекта
    """
    pk = _convert_unique_name_to_id(object_unique_name)
    sheduler_task = (PeriodicTask._default_manager
                     .get(name=object_unique_name))
    model_check = (SendingMessage._default_manager
                   .select_related('message')
                   .get(pk=pk))
    user_email = [client.client_mail
                  for client
                  in model_check.clients.get_queryset()
                  if client.actual]

    try:
        send_mails(model_check.message, user_email, template_render)
        (ResultsSendMessages.objects
         .create(send_task=model_check,
                 sheduler_task=sheduler_task,
                 result='success',
                 ))
    except SMTPException:
        (ResultsSendMessages.objects
         .create(send_task=model_check,
                 sheduler_task=sheduler_task,
                 result='failed',
                 ))

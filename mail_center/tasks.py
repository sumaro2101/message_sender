from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist

from typing import List, Union

from .services import send_mails, _convert_unique_name_to_id
from .models import SendingMessage
from mail_center.celery import app


@app.task
def send(object_unique_name: Union[str, None]= None) -> None:
    """Задание для события и рассписания, оправка писем пользователям

    Args:
        object_unique_name (str|None): Уникальное имя обекта_
    """    
    _, pk = _convert_unique_name_to_id(object_unique_name)
    model_check = SendingMessage._default_manager.get(pk=pk)
    user_email = [client.client_mail for client in model_check.clients.get_queryset() if client.actual]
    
    return send_mails(user_email)

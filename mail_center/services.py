from django.http.request import HttpRequest
from django.http.response import Http404, HttpResponseForbidden
from django.db.models import Model, Q
from django_celery_beat.models import IntervalSchedule, PeriodicTask
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from typing import Any, Union, Tuple, List
from datetime import timedelta, datetime
import json


choise_period_time: Tuple[Tuple[timedelta, str]] = (
    (timedelta(seconds=60), 'Каждые 1 минуту'),
    (timedelta(minutes=15), 'Каждые 15 минут'),
    (timedelta(minutes=30), 'Каждый 30 минут'),
    (timedelta(hours=1), 'Каждый 1 час'),
    (timedelta(hours=2), 'Каждые 2 часа'),
    (timedelta(hours=3), 'Каждые 3 часа'),
    (timedelta(hours=4), 'Каждые 4 часа'),
    (timedelta(hours=5), 'Каждые 5 часов'),
    (timedelta(hours=6), 'Каждые 6 часов'),
    (timedelta(hours=12), 'Каждые 12 часов'),
    (timedelta(days=1), 'Каждые 1 сутки'),
    (timedelta(days=2), 'Каждые 2 суток'),
    (timedelta(days=3), 'Каждые 3 суток'),
    (timedelta(days=4), 'Каждые 4 суток'),
    (timedelta(days=5), 'Каждые 5 суток'),
    (timedelta(days=6), 'Каждые 6 суток'),
    (timedelta(weeks=1), 'Каждую 1 неделю'),
    (timedelta(weeks=2), 'Каждые 2 недели'),
    (timedelta(weeks=3), 'Каждые 3 недели'),
    (timedelta(days=30), 'Каждый 1 месяц'),
    (timedelta(days=60), 'Каждые 2 месяца'),
    (timedelta(days=90), 'Каждые 3 месяца'),
    (timedelta(days=120), 'Каждые 4 месяца'),
    (timedelta(days=150), 'Каждые 5 месяцев'),
    (timedelta(days=180), 'Каждые 6 месяцев'),
    (timedelta(days=360), 'Каждый 12 месяцев'),
)

def check_message(request: HttpRequest, model_message: Model, message_id: str) -> Union[Http404, Model]:
    """Проверяет существование письма и возвращает

    Args:
        message_id (str): Может быть любым значение ссылающимся на обьект
    """    
    
    if not isinstance(message_id, str):
        raise TypeError(f'{message_id} аргумент не является значением, необходима строка')
    if issubclass(model_message, Model):
        message = get_object_or_404(model_message, **{'slug': message_id})
        if not message.employee == request.user:
            raise HttpResponseForbidden('Доступ к обьекту сообщения запрещен')
        return message
    raise TypeError(f'{model_message} не является моделью')


def send_mails(emails: List[str]) -> None:
    """Функция для оправки письма, является внутренней начинкой другой функции TASK

    Args:
        emails (List[str]): Список целевых эмеилов для оправки
     """  
       
    subject: str = 'test send mail'
    body: str = 'this test mail'
    server_mail: str = settings.EMAIL_HOST_USER
    users: List[str] = emails
    
    send_mail(subject=subject,
              message=body,
              from_email=server_mail,
              recipient_list=users,
              fail_silently=False)


def _unique_name_task(model: Model) -> Union[str, TypeError]:
    """Создание уникального имени для обьекта

    Args:
        model (Model): Модель базы данных на основе которой будет построенно имя

    Raises:
        TypeError: Исключение в случае если целевой объект не является подклассом Model

    Returns:
        Union[str, TypeError]: Возвращает готовое имя либо исключение
    """    
    
    if isinstance(model, Model):
        object_meta: Model = model._meta
        name: str = f'{object_meta.app_label}.{object_meta.model_name}_{model.pk}'
    else:
        raise TypeError('аргумент model должен быть подклассом Model')
    return name
    

def create_task_interval(object_: Model,
                         task,
                         interval: timedelta,
                         start_time: Union[datetime, None],
                         *args,
                         **kwargs: Any) -> None:
    """Создание события по рассписанию

    Args:
        object_ (Model): обьект для построения уникального имени
        task (_type_): Обьект события который будет вызыватся
        interval (timedelta): Интервал обязательно должен быть timedelta()
        start_time: (datetime | None): Время старта события по рассписанию

    Raises:
        ValueError: Будет в случае если интервал не является timedelta()
    """    
    
    name = _unique_name_task(object_)
    
    interval_parse = False
    
    if interval.seconds:
        every, period = (interval.seconds, 'seconds')
        interval_parse = True
        
    if interval.days:
        every, period = (interval.days, 'days')
        interval_parse = True
     
    if not interval_parse:
        raise ValueError('interval должен быть timedelta значением')
    
    args = json.dumps(args) if args else []
    kwargs = json.dumps(kwargs['kwargs']) if kwargs else {}
      
    PeriodicTask.objects.create(name=name,
                                task=task,
                                interval=IntervalSchedule.objects.get(Q(every=every, period=period)),
                                start_time=start_time,
                                args=args,
                                kwargs=kwargs
                                )
    
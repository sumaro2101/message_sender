from django.http.response import Http404
from django.db.models import Model, Q
from django_celery_beat.models import IntervalSchedule, PeriodicTask
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned, PermissionDenied
from django.template.exceptions import TemplateDoesNotExist
from django.urls import NoReverseMatch
from django.conf import settings
from django.template import loader
from django.core.mail import EmailMultiAlternatives

from typing import Any, Union, Tuple, List, Literal, Callable
from datetime import timedelta, datetime, timezone
import json

from .exeptions import BadArgumentsProcessingTask


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


def check_message(model_message: Model, message_id: str) -> Union[Http404, Model]:
    """Проверяет существование письма и возвращает

    Args:
        message_id (str): Может быть любым значение ссылающимся на обьект
    """    
    
    if not isinstance(message_id, str):
        raise TypeError(f'{message_id} аргумент не является строкой')
    if issubclass(model_message, Model):
        message = get_object_or_404(model_message, **{'slug': message_id})
        if not message.actual:
            raise PermissionDenied()
        return message
    raise TypeError(f'{model_message} не является моделью')


def send_mails(model_subject: Model, emails: List[str], template_render: Union[str, None]= None) -> None:
    """Функция для оправки письма, является внутренней начинкой другой функции TASK

    Args:
        model_subject (Model): Модель которая имеет ссылку на сообщение
        emails (List[str]): Список целевых эмеилов для оправки
        template_render (str, None): Ссылка на html для отправки письма
     """  
    email_template_name = template_render
    subject_template_name = "mail_form/mail_send_subject.txt"
    subject: str = model_subject.title_message
    body: str = model_subject.text_message
    server_mail: str = settings.EMAIL_HOST_USER
    users: List[str] = emails
    
    if email_template_name:
        
        context = {
        "name": model_subject.employee,
        "title": subject,
        "body": body,
        }

        try:
            subject = loader.render_to_string(subject_template_name, context=context)
            subject = "".join(subject.splitlines())
        except TemplateDoesNotExist:
            raise TemplateDoesNotExist(f'По заданному пути: {subject_template_name} - шаблон не был найден')
        except NoReverseMatch:
            raise NoReverseMatch('Ошибка при постоении пути')
        
        try:
            body = loader.render_to_string(email_template_name, context=context)
        except TemplateDoesNotExist:
            raise TemplateDoesNotExist(f'По заданному пути: {email_template_name} - шаблон не был найден')
        except NoReverseMatch:
            raise NoReverseMatch('Ошибка при постоении пути')
        

    email_message = EmailMultiAlternatives(subject, body, server_mail, users)
    email_message.send()


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
        raise TypeError(f'аргумент {model} должен быть подклассом Model')
    return name
    

def _convert_unique_name_to_id(unique_name: str) -> Tuple[str]:
    """Конвертация уникального имени события в id рассылки

    Args:
        unique_name (str): Уникальное имя события
    """    
    if not isinstance(unique_name, str):
        raise TypeError(f'{unique_name} должен быть сторокой')
    try:
        pk = unique_name.split('_')[-1]
        if not len(pk):
            raise
    except:
        raise ValueError(f'{unique_name} не является именем события')
    
    return pk
    
    
def _check_task(name_task: str) -> PeriodicTask:
    """Проверяет существование события в Базе Данных

    Args:
        name_task (str): Уникальное имя которое будет ключем

    Returns:
        PeriodicTask: Возвращает событие
    """    
    
    try:
        task_object = PeriodicTask.objects.get(name=name_task)
    except (ObjectDoesNotExist, MultipleObjectsReturned):
        return None
    return task_object


def _core_task(name: str,
               object_: Model,
                task: Union[Callable, None]= None,
                interval: Union[timedelta, None]= None,
                start_time: Union[datetime, None]= None,
                type_processing: Literal['create', 'update', 'delete']= 'update',
                changed_data: Union[None, List[str]]= [],
                *args,
                **kwargs: Any) -> None:
    """Ядро обработки события по рассписанию

    Args:
        name (str): Уникальное имя
        object_ (Model): Обьект для построения уникального имени
        task (_type_): Обьект события который будет вызыватся
        interval (timedelta): Интервал обязательно должен быть timedelta()
        start_time: (datetime | None): Время старта события по рассписанию
        type_processing ('create', 'update', 'delete'): Тип обработки объекта
        changed_data (None, Dict) = None: Словарь с изменяемыми полями

    Raises:
        ValueError: Будет в случае если интервал не является timedelta()
    """ 
       
    if interval:
        
        if not isinstance(interval, timedelta):
            raise TypeError(f'interval должен быть timedelta значением')
        else:
            if interval.seconds:
                every, period = (interval.seconds, 'seconds')   
            elif interval.days:
                every, period = (interval.days, 'days')
            
        schedule = IntervalSchedule.objects.filter(Q(every=every, period=period))
        if schedule.exists():
            try:
                interval = schedule.get()
            except MultipleObjectsReturned:
                raise MultipleObjectsReturned(f'{interval} вернул больше одного значения, необходимо проверить объекты интервалов')
        else:
            raise ObjectDoesNotExist(f'Не было найдено не одного интервала по значению {interval}')
    
    args = json.dumps(args) if args else []
    kwargs = kwargs['kwargs'] if kwargs.get('kwargs') else kwargs
    kwargs = json.dumps(kwargs) if kwargs else {}
      
    match type_processing:
        case 'create':
            if not task:
                raise BadArgumentsProcessingTask('Для создания события необходим целевой обьект для работы')
            
            PeriodicTask.objects.create(name=name,
                                        task=task,
                                        interval=interval,
                                        start_time=start_time,
                                        args=args,
                                        kwargs=kwargs
                                        )
            
        case 'update':
            task_object = _check_task(name_task=name)
            update_fields = []
            
            if 'periodicity' in changed_data:
                update_fields.append('interval')
                task_object.interval = interval
                
            if 'date_first_send' in changed_data:
                update_fields.append('start_time')
                task_object.start_time = start_time
            
            if 'status' in changed_data:
                update_fields.append('enabled')
                status = object_.status
                match status:
                    case 'run':
                        task_object.enabled = True
                    case 'freeze' | 'end':
                        task_object.enabled = False
                    case _:
                        raise ValueError(f'Статус для обновления события может быть "run", "freeze", "end" было полученно {status}')
                    
            task_object.save(update_fields=update_fields)
            
        case 'delete':
            # В случае если событие не будет найдено, будет пропуск
            # Это возможно если по ошибке было удалено событие раньше чем рассылка
            task_object = _check_task(name)
            if task_object:
                task_object.delete()
            else:
                print(f'По {name} событие не было найдено, целевой объект был удален')
        case _:
            raise ValueError(f'type_processing должен быть только "create", "update", "delete". Было полученно значение {type_processing}')
                
            
def create_task_interval(object_: Model,
                         task,
                         interval: timedelta,
                         start_time: Union[datetime, None]= None,
                         changed_data: Union[None, List[str]] = [],
                         *args,
                         **kwargs: Any) -> None:
    """Создает событие которое работает по рассписанию

   Args:
        object_ (Model): Обьект для построения уникального имени
        task (_type_): Обьект события который будет вызыватся
        interval (timedelta): Интервал обязательно должен быть timedelta()
        start_time: (datetime | None): Время старта события по рассписанию
        changed_data (None, Dict) = None: Словарь с изменяемыми полями
    """
     
    type_processing = 'create'
    name = _unique_name_task(object_)
    kwargs.update(**{'object_unique_name': name})
    
    _core_task(name=name,
               object_=object_,
               task=task,
               interval=interval,
               start_time=start_time,
               type_processing=type_processing,
               changed_data=changed_data,
               *args,
               **kwargs)
 
    
def update_task_interval(object_: Model,
                         interval: timedelta,
                         start_time: Union[datetime, None] = None,
                         changed_data: Union[None, List[str]] = [],
                         *args,
                         **kwargs: Any) -> None:
    """Обновляет событие которое работает по рассписанию

   Args:
        object_ (Model): Обьект для построения уникального имени
        task (_type_): Обьект события который будет вызыватся
        interval (timedelta): Интервал обязательно должен быть timedelta()
        start_time: (datetime | None): Время старта события по рассписанию
        changed_data (None, List) = None: Словарь с изменяемыми полями
    """
    type_processing = 'update'
    name = _unique_name_task(object_)
    kwargs.update(**{'object_unique_name': name})
    
    _core_task(name=name,
               object_=object_,
               interval=interval,
               start_time=start_time,
               type_processing=type_processing,
               changed_data=changed_data,
               *args,
               **kwargs)


def delete_task_interval(object_: Model) -> None:
    """Удаляет событие из Базы Данных

   Args:
        object_ (Model): Обьект для построения уникального имени
    """
    type_processing = 'delete'
    name = _unique_name_task(object_)
    _core_task(name=name,
               object_=object_,
               type_processing=type_processing)
    
    
def get_procent_interval_time(interval: timedelta, next_send: datetime) -> str:
    """Вычисление процента исходя из пересечении двух интервалов на плоскости

    Args:
        interval (timedelta): Интервал
        next_send (datetime): Точка B

    Returns:
        str: Возвращает процент
    """
    if not isinstance(interval, timedelta):
        raise TypeError(f'{interval} не является классом timedelta')
    if not isinstance(next_send, datetime):
        raise TypeError(f'{next_send} не является классом datetime')
    
    interval = interval.total_seconds()
    remaining_interval = next_send - datetime.now(timezone.utc)

    treveled_interval = interval - remaining_interval.total_seconds()
    
    total_procent = (treveled_interval / interval) * 100
    procent_correct = round(total_procent, 2)
    
    if procent_correct < 0:
        procent_correct = 0
        
    if procent_correct > 100:
        procent_correct = 100
    return str(procent_correct)
    
    
def get_task(model: Model) -> PeriodicTask:
    """Получение обьекта события

    Args:
        model (Model): Обьект модели для поиска события привязанного к обьекту

    Returns:
        PeriodicTask: Обьект события
    """    
    name = _unique_name_task(model=model)
    task = _check_task(name_task=name)
    
    return task

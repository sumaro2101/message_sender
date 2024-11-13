from django.db.models import Model, Q
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

from django_celery_beat.models import IntervalSchedule, PeriodicTask

from datetime import datetime, timedelta
import json
from typing import Any, Callable, Literal

from mail_center.exeptions import BadArgumentsProcessingTask
from mail_center.services import _check_task, _unique_name_task
from mail_center.cache import delete_cache


def _parse_interval_to_intervalschedule(
    interval: timedelta,
    ) -> IntervalSchedule:
    """Разбирает на части timedelta и выводит необходимые параметры.

    Args:
        interval (timedelta): Интервал времени timedelta

    Raises:
        TypeError: Исключение в случае если аргумент не является timedelta.
        MultipleObjectsReturned: Исключение если по какой то причине
        по результатам парсинга вывелось несколько объектов рассписания.
        ObjectDoesNotExist: Исключение если не получилось
        получить не одного рассписания

    Returns:
        IntervalSchedule: Возращает объект рассписания
    """
    if not isinstance(interval, timedelta):
        raise TypeError('interval должен быть timedelta значением')
    else:
        if interval.seconds:
            every, period = (interval.seconds, 'seconds')
        elif interval.days:
            every, period = (interval.days, 'days')

    schedule = (IntervalSchedule.objects
                .filter(Q(every=every, period=period)))
    if schedule.exists():
        try:
            interval = schedule.get()
        except MultipleObjectsReturned:
            raise MultipleObjectsReturned(
                f'{interval} вернул больше одного значения, '
                'необходимо проверить объекты интервалов',
                )
    else:
        raise ObjectDoesNotExist(
            f'Не было найдено не одного интервала по значению {interval}',
            )
    return interval


def _core_task(name: str,
               object_: Model,
               task: Callable | None = None,
               interval: timedelta | None = None,
               start_time: datetime | None = None,
               type_processing: Literal['create',
                                        'update',
                                        'delete',
                                        ] = 'update',
               changed_data: list[str] | None = [],
               *args,
               **kwargs: Any,
               ) -> None:
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
        interval: IntervalSchedule = _parse_interval_to_intervalschedule(
            interval,
            )
    args = json.dumps(args) if args else []
    kwargs = kwargs['kwargs'] if kwargs.get('kwargs') else kwargs
    kwargs = json.dumps(kwargs) if kwargs else {}
    match type_processing:
        case 'create':
            if not task:
                raise BadArgumentsProcessingTask(
                    'Для создания события необходим целевой '
                    'обьект для работы',
                    )
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
                        raise ValueError(
                            'Статус для обновления события может быть '
                            f'"run", "freeze", "end" было полученно {status}',
                            )
            task_object.save(update_fields=update_fields)
            delete_cache(PeriodicTask, name)

        case 'delete':
            # В случае если событие не будет найдено, будет пропуск
            # Это возможно если по ошибке было удалено событие
            # раньше чем рассылка
            task_object = _check_task(name)
            if task_object:
                task_object.delete()
                delete_cache(PeriodicTask, name)
            else:
                print(
                    f'По {name} событие не было найдено,'
                    ' целевой объект был удален',
                    )
        case _:
            raise ValueError(
                'type_processing должен быть только'
                ' "create", "update", "delete".'
                f' Было полученно значение {type_processing}',
                )


def create_task_interval(object_: Model,
                         task,
                         interval: timedelta,
                         start_time: datetime | None = None,
                         changed_data: list[str] | None = [],
                         *args,
                         **kwargs: Any,
                         ) -> None:
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
                         start_time: datetime | None = None,
                         changed_data: list[str] | None = [],
                         *args,
                         **kwargs: Any,
                         ) -> None:
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

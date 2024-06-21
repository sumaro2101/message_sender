from django.db.models import QuerySet, Model
from django.conf import settings
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

from django_celery_beat.models import IntervalSchedule, PeriodicTask

from typing import Type, Union, Literal


def _get_single_name_item(object_: Model, slug: Union[str, None] = None) -> str:
    """Вывод уникального имени для Model

    Args:
        object_ (Model): Объект типа Model

    Returns:
        str: Возращает готовое уникальное имя
    """    
    if slug:
        if isinstance(object_, QuerySet):
            obj_meta = object_.model._meta
            return f'{obj_meta.app_label}_{obj_meta.model_name}_{slug}'
        
        obj_meta = object_._meta
        return f'{obj_meta.app_label}_{obj_meta.model_name}_{slug}'
    raise ValueError(f'slug атрибут - {slug}, нужно указать значение для класса Model')


def _get_multiple_name_items(objects_: QuerySet[Type[Model]],
                             slug: Union[str, None] = None) -> str:
    """Вывод уникального имени для Queryset

    Args:
        objects_ (QuerySet[Type[Model]]): Объект типа Queryset

    Returns:
        str: Возращает готовое уникальное имя
    """
    if slug:
        return _get_single_name_item(object_=objects_, slug=slug)
    
    if not isinstance(objects_, list):
        obj_meta = objects_._meta
    elif isinstance(objects_, list):
        obj_meta = objects_[0]._meta
        
    return f'{obj_meta.app_label}_{obj_meta.model_name}_list'
    
        
def _make_name_object_cache(target_object: Union[QuerySet[Type[Model]], Model],
                            slug: Union[str, None] = None,
                            is_queryset_all: bool = False) -> str:
    """Точка входа и опеределение объекта для формирования уникального именя для кэша

    Args:
        target_object (Queryset, Model): Целевой объект для постороения уникального имени

    Raises:
        ValueError: Исключение в случае если целевой объект не принадлежит не к одному требуемых классов

    Returns:
        str: Возвращает готовое уникальное имя
    """    
    if isinstance(target_object, QuerySet) or is_queryset_all:
        name = _get_multiple_name_items(target_object, slug)
        
    elif issubclass(target_object, Model):
        name = _get_single_name_item(target_object, slug)
        
    else:
        raise ValueError(f'{target_object} не является подклассом Model или Queryset')
    
    return name


def get_or_set_cache(model: Union[Model, QuerySet[Model]],
                     slug: Union[str, None] = None,
                     type_field: Union[Literal['name', 'slug'], None] = 'slug',
                     is_queryset_all: bool = False) -> Union[Model, QuerySet[Model], None]:
    """
    Получение или сохранение кэша
    
    !!!ОСТОРОЖНО для получения Queryset не указывайте slug и type_field.
    Данный кэш возвращает только все объекты Queryset, дальнейшая обработка ложится на вас!!!
    
    Если вам необходимо вывести один объект из Queryset, укажите slug. Если есть неоходимость поиска по name, в type_field укажите "name"
    
    Args:
        model (Union[QuerySet[Type[Model]], Type[Model]]): Целевой объект для сохранения и получения кэша,
        так же на основе объекта строится имя.
        slug (Union[str, None] = None): Атрибут для поиска, так же является уникальным именем
        type_field (Union[str, None] = None): Тип поля для вывода объекта

    Returns:
        Union[QuerySet[Type[Model]], Type[Model], None]: Возращает объект или группу объектов из кэша
    """    
                                 
    if not settings.CACHE_ENABLE:
        return None
    if slug:
        if not isinstance(slug, str):
            raise TypeError(f'slug атрибут - {slug}, необходима строка')
    
    name_object = _make_name_object_cache(model, slug, is_queryset_all)
    
    cache_obj = cache.get(name_object)
    
    if not cache_obj:
        if isinstance(model, QuerySet) or is_queryset_all:
            # В случае если из QuerySet необходимо вытащить определенный объект по slug или name
            if slug and type_field:
                try:
                    match type_field:
                        case 'name':
                            cache_obj = model.get(name=slug)
                        case 'slug':
                            cache_obj = model.get(slug=slug)
                        case _:
                            cache_obj = model.all()
                except (ObjectDoesNotExist, MultipleObjectsReturned):
                    raise(f'Произошла ошибка на уровне поиска объекта по "{type_field}={slug}" из Queryset')      
            else:
                cache_obj = model.objects.all()
        elif issubclass(model, (Model, PeriodicTask)):
            try:
                match type_field:
                    case 'name':
                        cache_obj = model.objects.get(name=slug)
                    case 'slug':
                        cache_obj = model.objects.get(slug=slug)
                    case _:
                        raise
            except (ObjectDoesNotExist, MultipleObjectsReturned):
                raise (f'Произошла ошибка на уровне вывода объекта по "{type_field}={slug}" из Queryset')
        else:
            raise TypeError(f'{model} атрибут не является подклассом Model или Queryset')
        cache.set(name_object, cache_obj)
        
    return cache_obj


def delete_cache(model: Union[Model, QuerySet[Type[Model]]], slug: Union[str, None] = None, is_queryset_all: bool = False) -> None:
    """Удаление кэша из Базы данных оперeделенного объекта,
    по задумке все что нужно это построить ключ из этих аргументов для удаления

    Args:
        model (Union[Model, QuerySet[Type[Model]]]): Модель или Queryset так же на основе объекта строится имя
        slug (str): Уникальное имя для поиска
    """
    
    if not settings.CACHE_ENABLE:
        return None

    if slug:
        if not isinstance(slug, str):
            raise TypeError(f'slug атрибут - {slug}, необходима строка')
    
    name_object = _make_name_object_cache(model, slug, is_queryset_all)
    
    cache.delete(key=name_object)
    
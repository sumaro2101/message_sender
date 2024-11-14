# Title
Данный проект выполняет функцию по рассылке сообщений клиентам.
## View
### Scheduler
Реализована своё ядро по обработке данных
для задач по рассписанию.
1. create_task_interval
2. update_task_interval
3. delete_task_interval

create_task_interval
```python
# Создание задачи по рассписанию
# Описанный ниже  пример в окружении метода
# form_valid
form = form.save()
periodicity = form.cleaned_data['periodicity']
start_time = form.cleaned_data['date_first_send']
kwargs = {'template_render': 'mail_form/mail_send_form.html'}
create_task_interval(object_=form, # Сущность типа <Item> Model.
                     task='mail_center.tasks.send', # Ссылка на задачу.
                     interval=periodicity, # Интервал.
                     start_time=start_time, # Время начала.
                     **kwargs, # Доп. Данные. Обычно ссылка на HTML.
                     )
```

update_task_interval
```python
# Обновление задачи по рассписанию
# Описанный ниже  пример в окружении метода
# form_valid
form = form.save()
periodicity = form.cleaned_data['periodicity']
start_time = form.cleaned_data['date_first_send']
kwargs = {'template_render': 'mail_form/mail_send_form.html'}
update_task_interval(object_=form, # Сущность типа <Item> Model.
                     interval=periodicity, # Интервал.
                     start_time=start_time, # Время начала.
                     changed_data=form.changed_data, # Измененые данные.
                     **kwargs, # Доп. Данные. Обычно ссылка на HTML.
                     )
```

delete_task_interval
```python
# Удаление задачи по рассписанию
# Описанный ниже пример в окружении метода
# form_valid
delete_task_interval(object_=self.object)
```

### Cache
Реализован ручной Кэш, для этого описанны специализированные
функции.
1. get_or_set_cache
2. delete_cache

get_or_set_cache
```python
from .models import SendingMessage

# Получение всего QuerySet
queryset = get_or_set_cache(SendingMessage, is_queryset_all=True) # -> QuerySet
# Получение определенной сущности
slug = 'some_slug_id_item'
self.object = get_or_set_cache(model=queryset, slug=slug) # -> <Item>
# Получение сущности по полю name
name = 'some_name_item'
self.object = get_or_set_cache(
    model=queryset,
    type_field='name',
    slug=slug,
    ) # -> <Item>
```

delete_cache
```python
# Удаление из Кэша всего QuerySet
delete_cache(SendingMessage, is_queryset_all=True)
# Удаление из Кэша опеределенной сущности
queryset = QuerySet(<Item:1>, <Item:2>)
slug = 'some_slug_id_item'
delete_cache(
    model=queryset,
    slug=slug,
    )
```

### Backend Authentication
Реализован класс для Backend аутентификации по Email
1. EmailAuthBackend

```python
# settings.py
AUTHENTICATION_BACKENDS = [
    'users.authentication.EmailAuthBackend',
]
```

## RabbitMQ, Celery
Используется Брокер сообщений RabbitMQ и Worker Celery
### Docker RabbitMQ
```yaml
rabbitmq:
    hostname: rabbitmq
    image: rabbitmq:4.0.3-management
    env_file:
      - .env
    ports:
      - 5672:5672
      - 15672:15672
    volumes:
      - rabbitmq-data:/var/lib/rabbitmq

volumes:
  rabbitmq-data:
```

### Настройка RabbitMQ
```python
# .env
RABBITMQ_DEFAULT_USER=guest # Логин RabbitMQ
RABBITMQ_DEFAULT_PASS=guest # Пароль RabbitMQ
```

### Docker Celery Worker
```yaml
celery_worker:
    build: 
      context: .
      dockerfile: ./docker/django/Dockerfile
    command: /start-celeryworker
    volumes:
      - .:/app
    env_file:
      - .env
```

### Настройка Celery
```python
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
app = Celery('mail_center')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
```

### Использование
После настройки RabbitMQ и Celery
Вам необходимо запустить проект (инструкции ниже)
а затем перейти по адрессу:
http://localhost:15672/
Это будет страница RabbitMQ для просмотра всех каналов, очередей,
обмеников, пользователей, и.т.д.
Вам нужно будет ввести логин и пароль для аутентификации который вы указали в .env

## Redis
Redis NoSQL база данных которая может играть роль как
брокера сообщений так и базой данных для Cache.
### Docker Redis
```yaml
  redis:
    image: redis:7.2.5-alpine
    expose:
      - 6379
```

### Настройка
Предварительная настройка не требуется для
стандартного объема задач.


## Flower
Flower это мощное приложение для отслеживания всех
задач на стороне Worker.
### Docker Flower
```yaml
dashboard:
    build: 
      context: .
      dockerfile: ./docker/django/Dockerfile
    command: /start-flower
    volumes:
      - .:/app
    ports:
      - 5555:5555
    env_file:
      - .env
```

### Настройка
Предварительная настройка не требуется, все настройки подтягиваются
автоматически из RabbitMQ.

### Использование
Для использования Flower вам нужно перейти по адрессу:
http://localhost:5555/
У вас откроется страница Flower с полной информацией о Worker и Tasks.

## Dependencies
### Зависимости необхомые проекту:
1. django
2. psycopg2-binary
3. pillow
4. pytils
5. redis
6. hiredis
7. celery
8. django-celery-beat
9. python-crontab
10. flower
11. gunicorn
12. django-phonenumbers
13. django-phonenumber-field
14. django-countries

## Install
Для успешной установки следующие инструкции:
1. Настройте .env.sample, а затем переменуйте его в .env
```python
# .env.sample
POSTGRES_PASSWORD=password # Пароль для Базы Данных (настройка)
DB_PASSWORD=password # Пароль для Базы Данных (использование)
RABBITMQ_DEFAULT_USER=user # Логин RabbitMQ
RABBITMQ_DEFAULT_PASS=password # Пароль RabbitMQ
# Email настройки можете не указывать если "DEBAG=True" в settings.py
HOST_USER=user@yandex.ru # Хост почты для рассылки (Если установлен режим DEBAG=False)
PASS_USER=password # Пароль от почты для рассыки (Если установлен режим DEBAG=False)
```

2. Docker
В проекте присутствует Docker. Если у вас нет Docker вы можете установить его через официальный сайт.
Оф. сайт: [link](https://www.docker.com)

Неоходимо сделать билд образов и контейнеров
```bash
docker compose build
```

Затем запустить образы
```bash
docker compose up
```

## Using
Инструкции использования:
- После запуска в Docker проекта вы можете открывать 
его в вашем Web Браузере http://localhost/
- Вы попадаете на главную страницу с описанием о сайте и краткой
информацией о сайте. Вам доступны только вкладки
"Главная страница", "Центр рассылок", "Блог", "Войти".
- Вы можете перейти во вкладку "Блог" и увидеть все статьи которые есть.
- Нажмите на кнопку "Войти" и попадаете на форму аутентификации.
- Нажмите на кнопку "Регистрация".
- Введите все обязательные поля. Если все данные верные вам будет отправлено на
почту сообщение о подтверждении регистрации.
!!!ВАЖНО!!!
Если стоит DEBAG=True уведомление о регистрации прийдет в консоль
от Worker, оно не чем не отличается от обычного за исключением того что оно не отправится
на реальный Эмеил. 
!!!ВАЖНО!!!
- Перейдите по полученной ссылке из Эмеила и вы верифицируете вашу почту.
- Затем вы можете снова нажать на кнопку Войти и ввести данные в форму аутентификации.
- Вы попадаете на "Центр рассылок", пока что рассылок у вас нет.
- Для создания сообщения для рассылки перейдите на вкладку "Центр сообщений".
- В центре сообщений нажмите на кнопку "Создать сообщение".
- Введите заголовок и содержимое сообщения и нажмите на кнопку "Создать".
- В списке сообщений вы увидете только что созданное вами сообщение,
вы можете Редактировать (изменять) его или Деактивировать - Активировать.
При изменения статуса по центру будет изменяться напись.
- Теперь нужно добавить клиентов для рассылки. Перейдите на вкладку "Центр клиентов".
- Ваш список клиентов будет пуст, нажмите "Добавить клиента".
- Введите данные клиента и нажмите кнопку "Создать".
- В списке клиентов вы увидете только что созданного клиента. Вы можете Изменить его данные или
Деактивировать - Активировать его. Исходя из статуса будет меняться надпись на карточке клиента.
- Теперь можно создать рассылку, перейдите на вкладку "Центр рассылок".
- В Центре рассылок у вас не будет не каких рассылок, нажмите "Добавить рассылку".
- Вас перекинет в "Центр сообщений" для выбора сообщения для рассылки.
- Нажмите на зеленую кнопку "Начать рассылку" которая расположена на карточке сообщения.
- Вы попадаете в форму создания рассылки.
У вас отображается "Выбранное сообщение" с контекстом сообщения,
"Настройки сообщения" с выбором времени начала рассылки и интервала,
а так же "Выбор клиентов" там где отображается список активных клиентов.
- Выберете клиентов и настройки для рассылки и нажмите кнопку "Принять".
- Начинается рассылка клиентам.
!!! ВАЖНО !!!
Если DEBAG=True все сообщения из рассылки будут приходить только в консоль
от Worker, если вы хотите создать реальную рассылку, вам нужно установить DEBAG=False,
заполнить соотвествующие Эмеил поля, если вы их не заполняли и тогда рассыка пойдет на
реальные Эмеилы.
!!! ВАЖНО !!!
- После создания рассылки вы попадаете на страницу текущей созданной рассылки
со всеми данными о ней. Так же имеется шкала которая визуализирует сколько
времени осталось до следующей итерации отправки сообщения.
Вы можете "Изменить" рассылку,
"Заморозить", в этом случае статус рассылки изменится на "Заморожена" и рассылка остановится,
"Завершить" - завершает рассылку без возможности ее возобновить, статус будет "Завершена".
- !!! АДМИНИСТРАТОР !!!
- Если зайти с правами доспута Администратора появляются дополнительные возможности.
- Открывается новая вкладка "Для администратора" с возмоностями
"Добавить пользователя", "Список пользователей", "Панель администратора".
- Так же у администратора есть возможность изменять данные любого пользователя,
а так же удалять рассылки.
- В панели администратора есть возможность совершить любые действия.

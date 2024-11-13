from django.template import loader
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.contrib.auth import get_user_model

from typing import Union, Dict

from celery import shared_task

from mail_center.celery import app


@app.task
def send_verify_email(
    email: str,
    context: Union[Dict, str],
    subject_template_name: Union[str, None] =
    'registration/password_reset_subject.txt',
    email_template_name: Union[str, None] =
    'passwords/password_reset_email.html',
    ) -> None:
    """Отправка письма для верификации почты.
    Так же может быть использована для других целей.
    В силу секретности данных результат этой отправки не где не сохраняется.

    Args:
        email (str): Эмеил пользователю которому будет отправлено письмо
        context (Union[Dict[str], str]): Основные данные которые будут
        фигурировать в письме
        subject_template_name (optional): Предмет заголовка.
        email_template_name (optional): Путь к html который будет базой
        для отправки (есть возмонжость отправки произвольной формы,
        так же обычным message отправкой).
        Если хотите отправить обычное письмо к
        текстом вам нужно email_template_name выставить в None.
    """
    if not email_template_name:
        subject = subject_template_name
        body = context
    else:
        subject = loader.render_to_string(subject_template_name, context)
        subject = "".join(subject.splitlines())
        body = loader.render_to_string(email_template_name, context)

    server_email = settings.EMAIL_HOST_USER

    email_message = EmailMultiAlternatives(
        subject,
        body,
        server_email,
        [email],
        )
    email_message.send()


@shared_task
def delete_non_verify_users():
    """Удаляет не верефицированых пользователей,
    если они какое то время не подтверждали почту
    """
    get_user_model().objects.filter(is_verify_email=False).delete()

from django.db import models
from django.contrib.auth import get_user_model


class MessageInfo(models.Model):
    """Модель сообщения которое будет частью рассылки
    """
    employee = models.ForeignKey(get_user_model(),
                                 verbose_name='cоздатель',
                                 related_name='employeers',
                                 blank=True,
                                 null=True,
                                 on_delete=models.SET_NULL
                                 )
    title_message = models.CharField(max_length=100,
                                     verbose_name='заголовок сообщения'
                                     )
    text_message = models.TextField(verbose_name='содержимое сообщения')
    slug = models.SlugField(max_length=256,
                            unique=True,
                            blank=True,
                            null=True
                            )
    time_create = models.DateTimeField(auto_now_add=True,
                                       verbose_name='время создания'
                                       )
    time_edit = models.DateTimeField(auto_now=True,
                                     blank=True,
                                     null=True,
                                     verbose_name='время редактирования'
                                     )
    actual = models.BooleanField(default=True,
                                 verbose_name='актуальность'
                                 )

    class Meta:
        verbose_name = 'сообщение'
        verbose_name_plural = 'сообщения'
        ordering = ['-time_edit']

    def __str__(self):
        return self.title_message

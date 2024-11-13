from django.db import models
from django.contrib.auth import get_user_model


class ClientServise(models.Model):
    """Модель клиента для рассылок
    Имеет поля: ФИО, эмеил, описание

    Отношение: our_clients:ClientServise
    """
    employee = models.ForeignKey(get_user_model(),
                                 verbose_name='кем добавлено',
                                 on_delete=models.SET_NULL,
                                 blank=True,
                                 null=True
                                 )
    client_mail = models.EmailField(verbose_name='эмеил клиента',)
    client_first_name = models.CharField(max_length=80,
                                         verbose_name='имя клиента'
                                         )
    client_last_name = models.CharField(max_length=120,
                                        verbose_name='фамилия клиента'
                                        )
    client_middle_name = models.CharField(max_length=120,
                                          verbose_name='отчество клиента',
                                          default=None,
                                          blank=True,
                                          null=True
                                          )
    client_info = models.TextField(blank=True,
                                   null=True,
                                   verbose_name='информания о клиенте'
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
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'
        ordering = ['-time_edit']

    def __str__(self):
        return self.client_mail

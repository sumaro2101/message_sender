from django.db import models
from django.contrib.auth import get_user_model
from mail_center.services import choise_period_time
# Create your models here.


class SendingMessage(models.Model):
    
    owner_send = models.ForeignKey(get_user_model(), verbose_name='пользователь', null=True, on_delete=models.CASCADE)
    message = models.ForeignKey("mess.MessageInfo", verbose_name='сообщения для рассылки', on_delete=models.CASCADE)
    clients = models.ManyToManyField("our_clients.ClientServise", verbose_name='клиенты для рассылки')
    date_first_send = models.DateTimeField(verbose_name='время первой отправки', default=None, blank=True, null=True)
    date_last_send = models.DateTimeField(verbose_name='время последней отправки', default=None, blank=True, null=True)
    periodicity = models.DurationField(verbose_name='переодичность отправки', choices=choise_period_time, default=choise_period_time[9])
    status = models.CharField(max_length=50, choices=[('end', 'Завершено'), ('create', 'Созданно'), ('run', 'Запущено')], default='create')

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки сообщений'
        ordering = ['-date_first_send', '-status']

    def __str__(self):
        return self.status


class ResultsSendMessages(models.Model):
    result = models.CharField(max_length=50, null=True, blank=True)
    
    class Meta:
        verbose_name = 'Результаты рассылки'
        verbose_name_plural = 'Результаты Рассылки сообщений'

    def __str__(self):
        return self.result
    
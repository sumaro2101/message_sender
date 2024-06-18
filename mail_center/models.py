from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

from mail_center.services import choise_period_time
# Create your models here.


class SendingMessage(models.Model):
    
    owner_send = models.ForeignKey(get_user_model(), verbose_name='пользователь', null=True, on_delete=models.CASCADE)
    message = models.ForeignKey("mess.MessageInfo", verbose_name='сообщения для рассылки', on_delete=models.CASCADE)
    clients = models.ManyToManyField("our_clients.ClientServise", verbose_name='клиенты для рассылки')
    date_first_send = models.DateTimeField(verbose_name='время первой отправки', default=None, blank=True, null=True)
    periodicity = models.DurationField(verbose_name='периодичность отправки', choices=choise_period_time, default=choise_period_time[9])
    slug = models.SlugField(max_length=256, null=True)
    status = models.CharField(max_length=50, choices=[('end', 'Завершено'), ('create', 'Созданно'), ('freeze', 'Заморожено'), ('run', 'Запущено')], default='create')

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки сообщений'
        ordering = ['-date_first_send', '-status']

    def __str__(self):
        return self.status

    def get_absolute_url(self):
        return reverse("mail_center:mail_detail", kwargs={"slug": self.slug})


class ResultsSendMessages(models.Model):
    send_task = models.ForeignKey("mail_center.SendingMessage", verbose_name='ссылка на объект рассылки', null=True, on_delete=models.SET_NULL)
    sheduler_task = models.ForeignKey("django_celery_beat.PeriodicTask", verbose_name='ссылка на объект события', null=True, on_delete=models.SET_NULL)
    date_done = models.DateTimeField(auto_now=True, verbose_name='Дата окончания задачи')
    result = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        
        ordering = ['-date_done']
        verbose_name = 'Результаты рассылки'
        verbose_name_plural = 'Результаты Рассылки сообщений'

    def __str__(self):
        return self.result
    
from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

class SendingMessage(models.Model):
    message = models.ForeignKey("mess.MessageInfo", verbose_name='сообщения для рассылки', on_delete=models.CASCADE)
    clients = models.ManyToManyField("our_clients.ClientServise", verbose_name='клиенты для рассылки')
    date_first_send = models.DateTimeField(verbose_name='время первой отправки', default=None, blank=True, null=True)
    date_last_send = models.DateTimeField(verbose_name='время последней отправки', default=None, blank=True, null=True)
    periodicity = models.DateTimeField(verbose_name='периодичность отправок', default=None, blank=True, null=True)
    status = models.CharField(max_length=50, choices=[('end', 'Завершено'), ('create', 'Созданно'), ('run', 'Запущено')])

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки сообщений'
        ordering = ['-date_first_send', '-status']

    def __str__(self):
        return self.status

    # def get_absolute_url(self):
    #     return reverse("_detail", kwargs={"pk": self.pk})

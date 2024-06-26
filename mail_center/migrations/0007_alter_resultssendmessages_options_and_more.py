# Generated by Django 5.0.6 on 2024-06-18 21:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_celery_beat', '0018_improve_crontab_helptext'),
        ('mail_center', '0006_alter_sendingmessage_status'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='resultssendmessages',
            options={'ordering': ['-date_done'], 'verbose_name': 'Результаты рассылки', 'verbose_name_plural': 'Результаты Рассылки сообщений'},
        ),
        migrations.RemoveField(
            model_name='sendingmessage',
            name='date_last_send',
        ),
        migrations.AddField(
            model_name='resultssendmessages',
            name='date_done',
            field=models.DateTimeField(auto_now=True, verbose_name='Дата окончания задачи'),
        ),
        migrations.AddField(
            model_name='resultssendmessages',
            name='send_task',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='mail_center.sendingmessage', verbose_name='ссылка на объект рассылки'),
        ),
        migrations.AddField(
            model_name='resultssendmessages',
            name='sheduler_task',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='django_celery_beat.periodictask', verbose_name='ссылка на объект события'),
        ),
    ]

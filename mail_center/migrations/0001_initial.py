# Generated by Django 5.0.6 on 2024-05-16 19:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('mess', '0003_alter_messageinfo_options'),
        ('our_clients', '0003_clientservise_employee'),
    ]

    operations = [
        migrations.CreateModel(
            name='SendingMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_first_send', models.DateTimeField(default=None, verbose_name='время первой отправки')),
                ('periodicity', models.DateTimeField(default=None, verbose_name='периодичность отправок')),
                ('status', models.CharField(choices=[('завершена', 'завершена'), ('создана', 'создана'), ('запущена', 'запущена')], max_length=50)),
                ('clients', models.ManyToManyField(to='our_clients.clientservise', verbose_name='клиенты для рассылки')),
                ('message', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mess.messageinfo', verbose_name='сообщения для рассылки')),
            ],
            options={
                'verbose_name': 'Рассылка',
                'verbose_name_plural': 'Рассылки сообщений',
            },
        ),
    ]

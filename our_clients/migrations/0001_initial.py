# Generated by Django 5.0.6 on 2024-05-16 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ClientServise',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_mail', models.EmailField(max_length=254, unique=True, verbose_name='эмеил клиента')),
                ('client_first_name', models.CharField(max_length=80, verbose_name='имя клиента')),
                ('client_last_name', models.CharField(max_length=120, verbose_name='фамилия клиента')),
                ('client_middle_name', models.CharField(default=None, max_length=120, verbose_name='отчество клиента')),
                ('client_info', models.TextField(blank=True, null=True, verbose_name='информания о клиенте')),
                ('time_create', models.DateTimeField(auto_now_add=True, verbose_name='время создания')),
                ('time_edit', models.DateTimeField(auto_now=True, null=True, verbose_name='время редактирования')),
                ('actual', models.BooleanField(default=True, verbose_name='актуальность')),
            ],
            options={
                'verbose_name': 'клиент',
                'verbose_name_plural': 'клиенты',
                'ordering': ['-time_edit'],
            },
        ),
    ]

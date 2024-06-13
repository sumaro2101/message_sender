# Generated by Django 5.0.6 on 2024-05-16 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mail_center', '0004_sendingmessage_date_last_send'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sendingmessage',
            name='status',
            field=models.CharField(choices=[('end', 'завершена'), ('create', 'создана'), ('run', 'запущена')], max_length=50),
        ),
    ]
# Generated by Django 5.0.6 on 2024-06-20 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mail_center', '0009_sendingmessage_enabled_alter_sendingmessage_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sendingmessage',
            name='enabled',
            field=models.BooleanField(default=True, verbose_name='активность рассылки'),
        ),
    ]

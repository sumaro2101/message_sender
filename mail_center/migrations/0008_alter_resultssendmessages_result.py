# Generated by Django 5.0.6 on 2024-06-18 21:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mail_center', '0007_alter_resultssendmessages_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resultssendmessages',
            name='result',
            field=models.CharField(choices=[('success', 'Успешно'), ('failed', 'Провалено')], max_length=50),
        ),
    ]

# Generated by Django 4.2 on 2024-02-19 15:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_payments'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name': 'пользователь', 'verbose_name_plural': 'пользователи'},
        ),
        migrations.DeleteModel(
            name='Payments',
        ),
    ]

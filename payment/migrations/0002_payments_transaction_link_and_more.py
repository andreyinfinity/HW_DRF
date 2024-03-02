# Generated by Django 4.2 on 2024-02-26 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='payments',
            name='transaction_link',
            field=models.URLField(blank=True, max_length=400, null=True, verbose_name='ссылка на оплату'),
        ),
        migrations.AlterField(
            model_name='payments',
            name='transaction_id',
            field=models.CharField(blank=True, default='', max_length=500, null=True, verbose_name='id сессии оплаты'),
        ),
    ]
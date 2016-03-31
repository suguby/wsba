# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-01 20:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('presentations', '0006_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='answers_type',
            field=models.CharField(choices=[('multi', 'Множественный выбор'), ('single', 'Единичный выбор')], default='multi', max_length=8, verbose_name='Тип ответов'),
        ),
    ]

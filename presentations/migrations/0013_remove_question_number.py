# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-21 11:21
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('presentations', '0012_auto_20160321_1104'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='number',
        ),
    ]

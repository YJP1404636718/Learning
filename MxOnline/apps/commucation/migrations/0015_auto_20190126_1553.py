# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2019-01-26 15:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commucation', '0014_auto_20181221_1923'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='desc',
            field=models.CharField(max_length=200, verbose_name='文章描述'),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-12-21 18:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commucation', '0012_auto_20181129_1345'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='content',
            field=models.CharField(blank=True, max_length=1000, null=True, verbose_name='文章内容'),
        ),
    ]

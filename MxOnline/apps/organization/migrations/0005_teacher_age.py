# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-06-16 13:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0004_teacher_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='age',
            field=models.IntegerField(default=0, verbose_name='年龄'),
        ),
    ]

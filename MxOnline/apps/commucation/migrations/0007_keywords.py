# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-11-22 12:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commucation', '0006_comment_date_publish'),
    ]

    operations = [
        migrations.CreateModel(
            name='Keywords',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word', models.CharField(max_length=30, verbose_name='违禁关键字')),
            ],
            options={
                'verbose_name': '违禁关键字',
                'verbose_name_plural': '违禁关键字',
            },
        ),
    ]

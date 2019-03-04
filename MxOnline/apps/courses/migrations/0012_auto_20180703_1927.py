# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-07-03 19:27
from __future__ import unicode_literals

import DjangoUeditor.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0011_course_is_banner'),
    ]

    operations = [
        migrations.CreateModel(
            name='BannerCourse',
            fields=[
            ],
            options={
                'verbose_name_plural': '轮播课程',
                'proxy': True,
                'verbose_name': '轮播课程',
            },
            bases=('courses.course',),
        ),
        migrations.AddField(
            model_name='course',
            name='course_direction',
            field=models.CharField(default='', max_length=100, verbose_name='课程方向'),
        ),
        migrations.AlterField(
            model_name='course',
            name='detail',
            field=DjangoUeditor.models.UEditorField(default='', verbose_name='课程详情'),
        ),
    ]
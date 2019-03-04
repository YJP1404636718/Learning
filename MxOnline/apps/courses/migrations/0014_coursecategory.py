# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-07-04 13:21
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0013_auto_20180703_1939'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_category', models.CharField(default='', max_length=100, verbose_name='课程类别')),
                ('direction', models.ForeignKey(blank=True, max_length=100, null=True, on_delete=django.db.models.deletion.CASCADE, to='courses.CourseDirection', verbose_name='课程方向')),
            ],
            options={
                'verbose_name': '课程类别',
                'verbose_name_plural': '课程类别',
            },
        ),
    ]

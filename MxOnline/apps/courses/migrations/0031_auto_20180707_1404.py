# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-07-07 14:04
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0030_auto_20180707_1404'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='coursedirection',
            unique_together=set([('course_direction', 'course_category')]),
        ),
    ]

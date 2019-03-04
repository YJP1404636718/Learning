# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-06-16 19:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20180613_1527'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailverifyrecord',
            name='send_type',
            field=models.CharField(choices=[('register', '注册'), ('forget', '找回密码'), ('update_email', '修改密码')], max_length=10, verbose_name='验证码类型'),
        ),
    ]

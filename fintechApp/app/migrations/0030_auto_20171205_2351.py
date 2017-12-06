# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-05 23:51
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0029_auto_20171205_0326'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='userName',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
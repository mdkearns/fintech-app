# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-01 20:19
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0018_report_stars'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='report',
            name='stars',
        ),
    ]

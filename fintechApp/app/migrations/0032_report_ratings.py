# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-06 00:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0031_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='ratings',
            field=models.ManyToManyField(blank=True, to='app.Rating'),
        ),
    ]

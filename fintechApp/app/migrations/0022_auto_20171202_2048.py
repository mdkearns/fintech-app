# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-02 20:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0021_merge_20171202_0045'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='encrypted_message_text',
            field=models.BinaryField(),
        ),
    ]
# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-19 15:43
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_merge_20171119_1543'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReportFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='NO_NAME', max_length=50)),
                ('file', models.FileField(upload_to='files/')),
            ],
        ),
        migrations.AddField(
            model_name='report',
            name='files',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.ReportFile'),
        ),
    ]

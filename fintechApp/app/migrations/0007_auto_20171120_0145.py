# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-20 01:45
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0006_auto_20171113_2203'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReportFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='NO_NAME', max_length=50)),
                ('file', models.FileField(upload_to='files/')),
                ('encrypted', models.BooleanField(default=False)),
                ('companyUser', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='report',
            name='timeStamp',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='report',
            name='files',
            field=models.ManyToManyField(null=True, to='app.ReportFile'),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-02-08 14:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Life', '0010_video_silenced'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(default='No description', max_length=500)),
                ('name', models.CharField(max_length=50)),
                ('silenced', models.CharField(default='N', max_length=1)),
                ('article', models.CharField(default='Go to link', max_length=6000)),
                ('link', models.CharField(default='None', max_length=500)),
            ],
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-02-06 08:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Welcome_phrase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=140)),
                ('part_of_day', models.IntegerField()),
            ],
        ),
    ]
# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-02-23 00:17
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Life', '0017_auto_20170223_0115'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ddnegative',
            old_name='Doption2',
            new_name='Doption',
        ),
    ]
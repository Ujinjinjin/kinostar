# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-11 18:46
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0003_auto_20170311_2144'),
    ]

    operations = [
        migrations.RenameField(
            model_name='album',
            old_name='movie_trailer',
            new_name='trailer',
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-03 19:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oauth', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='oauthtoken',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]

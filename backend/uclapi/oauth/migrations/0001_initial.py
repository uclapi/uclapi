# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-01 16:26
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import oauth.app_helpers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('dashboard', '0008_auto_20170701_1626'),
    ]

    operations = [
        migrations.CreateModel(
            name='OAuthScope',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('scope_number', models.BigIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='OAuthToken',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                (
                    'token',
                    models.CharField(
                        default=oauth.app_helpers.generate_user_token,
                        max_length=75,
                        unique=True
                    )
                ),
                (
                    'app',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to='dashboard.App'
                    )
                ),
                (
                    'scope',
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to='oauth.OAuthScope'
                    )
                ),
                (
                    'user',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to='dashboard.User'
                    )
                ),
            ],
        ),
    ]

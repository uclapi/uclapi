# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-15 20:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('roombookings', '0005_auto_20170215_1908'),
    ]

    operations = [
        migrations.CreateModel(
            name='CmisUclapiVEquipFeatures',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('setid', models.CharField(blank=True, max_length=40, null=True)),
                ('roomid', models.CharField(blank=True, max_length=40, null=True)),
                ('units', models.FloatField(blank=True, null=True)),
                ('description', models.CharField(blank=True, max_length=320, null=True)),
                ('siteid', models.CharField(blank=True, max_length=40, null=True)),
                ('type', models.CharField(blank=True, max_length=8, null=True)),
            ],
            options={
                'managed': False,
                'db_table': 'CMIS_UCLAPI_V_EQUIP_FEATURES',
            },
        ),
    ]

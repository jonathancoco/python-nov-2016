# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-18 19:44
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('property_search_app', '0002_property'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='property',
            options={'managed': False},
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-07 11:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interaction', '0005_created_modified_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='interaction',
            name='created_on',
            field=models.DateTimeField(auto_now_add=True, db_index=True, null=True),
        ),
        migrations.AlterField(
            model_name='servicedelivery',
            name='created_on',
            field=models.DateTimeField(auto_now_add=True, db_index=True, null=True),
        ),
    ]
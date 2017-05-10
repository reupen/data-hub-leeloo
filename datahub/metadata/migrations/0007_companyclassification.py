# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-08 11:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('metadata', '0006_headquartertype'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyClassification',
            fields=[
                ('id', models.UUIDField(primary_key=True, serialize=False)),
                ('name', models.TextField(blank=True)),
                ('selectable', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
                'ordering': ('name',),
            },
        ),
    ]
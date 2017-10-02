# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-26 14:59
from __future__ import unicode_literals

import django.contrib.postgres.fields.citext
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0011_add_adviser_tel_num'),
    ]

    operations = [
        migrations.AddField(
            model_name='advisor',
            name='contact_email',
            field=models.EmailField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='advisor',
            name='email',
            field=django.contrib.postgres.fields.citext.CICharField(max_length=255, unique=True, verbose_name='username'),
        ),
    ]
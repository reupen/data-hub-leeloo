# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-27 10:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('investment', '0001_squashed_0013_add_quotable_as_case_study'),
    ]

    operations = [
        migrations.AddField(
            model_name='investmentproject',
            name='other_business_activity',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
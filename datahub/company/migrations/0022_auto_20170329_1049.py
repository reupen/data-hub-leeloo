# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-29 10:49
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0021_auto_20170308_1157'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='one_list_account_owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='one_list_owned_companies', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='company',
            name='parent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subsidiaries', to='company.Company'),
        ),
    ]
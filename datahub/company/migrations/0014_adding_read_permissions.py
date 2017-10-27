# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-27 09:34
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0013_update_marketing_fields'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='advisor',
            options={'permissions': (('read_advisor', 'Can read advisor'),), 'verbose_name': 'adviser'},
        ),
        migrations.AlterModelOptions(
            name='companieshousecompany',
            options={'permissions': (('read_companieshousecompany', 'Can read company house company'),), 'verbose_name_plural': 'Companies House companies'},
        ),
        migrations.AlterModelOptions(
            name='company',
            options={'permissions': (('read_company', 'Can read company'),), 'verbose_name_plural': 'companies'},
        ),
        migrations.AlterModelOptions(
            name='contact',
            options={'permissions': (('read_contact', 'Can read contact'),)},
        ),
    ]

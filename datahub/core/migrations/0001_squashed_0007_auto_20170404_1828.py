# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-25 10:20
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    replaces = [('core', '0001_initial'), ('core', '0002_auto_20170117_1007'), ('core', '0003_auto_20170118_1600'), ('core', '0004_remove_taskinfo_name'), ('core', '0005_auto_20170124_1141'), ('core', '0006_taskinfo_manual_rerun_task'), ('core', '0007_auto_20170404_1828')]

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
    ]
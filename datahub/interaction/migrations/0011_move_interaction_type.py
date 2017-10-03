# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-02 10:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interaction', '0010_ren_interaction_type_comm_channel'),
        ('metadata', '0005_auto_20171002_0950'),
    ]

    state_operations = [
        migrations.CreateModel(
            name='CommunicationChannel',
            fields=[
                ('id', models.UUIDField(primary_key=True, serialize=False)),
                ('name', models.TextField(blank=True)),
                ('disabled_on', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'ordering': ('name',),
                'abstract': False,
                'db_table': 'metadata_interactiontype'
            },
        ),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(state_operations=state_operations)
    ]

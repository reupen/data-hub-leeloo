# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-07 13:55
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('omis-quote', '0005_adding_read_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='TermsAndConditions',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('created_on', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('name', models.CharField(help_text='Only used internally.', max_length=100)),
                ('content', models.TextField()),
            ],
            options={
                'ordering': ('-created_on',),
            },
        ),
        migrations.AddField(
            model_name='quote',
            name='terms_and_conditions',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='omis-quote.TermsAndConditions'),
        ),
    ]

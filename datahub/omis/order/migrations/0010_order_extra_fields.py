# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-11 09:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0009_order_service_types'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='contacts_not_to_approach',
            field=models.TextField(blank=True, help_text='Are there contacts that DIT should not approach?'),
        ),
        migrations.AddField(
            model_name='order',
            name='description',
            field=models.TextField(blank=True, help_text='Description of the work needed.'),
        ),
        migrations.AddField(
            model_name='order',
            name='existing_agents',
            field=models.TextField(blank=True, editable=False, help_text='Legacy field. Details of any existing agents.'),
        ),
        migrations.AddField(
            model_name='order',
            name='further_info',
            field=models.TextField(blank=True, editable=False, help_text='Legacy field. Further information.'),
        ),
        migrations.AddField(
            model_name='order',
            name='permission_to_approach_contacts',
            field=models.TextField(blank=True, editable=False, help_text='Legacy field. Can DIT speak to the contacts?'),
        ),
        migrations.AddField(
            model_name='order',
            name='product_info',
            field=models.TextField(blank=True, editable=False, help_text='Legacy field. What is the product?'),
        ),
    ]
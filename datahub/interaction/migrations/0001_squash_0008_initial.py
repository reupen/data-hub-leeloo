# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-25 11:55
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('metadata', '0001_squashed_0012_auto_20170523_0940'),
        ('company', '0001_squash_0030_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Interaction',
            fields=[
                ('created_on', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified_on', models.DateTimeField(auto_now=True, null=True)),
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('date', models.DateTimeField()),
                ('subject', models.TextField()),
                ('notes', models.TextField(max_length=4000)),
                ('company', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='interactions', to='company.Company')),
                ('contact', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='interactions', to='company.Contact')),
                ('dit_advisor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='interactions', to=settings.AUTH_USER_MODEL)),
                ('dit_team', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='metadata.Team')),
                ('interaction_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='metadata.InteractionType')),
                ('service', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='metadata.Service')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ServiceDelivery',
            fields=[
                ('created_on', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified_on', models.DateTimeField(auto_now=True, null=True)),
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('date', models.DateTimeField()),
                ('subject', models.TextField()),
                ('notes', models.TextField(max_length=4000)),
                ('feedback', models.TextField(max_length=4000, null=True)),
                ('company', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='servicedeliverys', to='company.Company')),
                ('contact', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='servicedeliverys', to='company.Contact')),
                ('country_of_interest', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='metadata.Country')),
                ('dit_advisor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='servicedeliverys', to=settings.AUTH_USER_MODEL)),
                ('dit_team', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='metadata.Team')),
                ('event', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='metadata.Event')),
                ('sector', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='metadata.Sector')),
                ('service', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='metadata.Service')),
            ],
            options={
                'verbose_name_plural': 'service deliveries',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ServiceOffer',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('dit_team', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='metadata.Team')),
                ('event', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='metadata.Event')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='metadata.Service')),
            ],
        ),
        migrations.AddField(
            model_name='servicedelivery',
            name='service_offer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='interaction.ServiceOffer'),
        ),
        migrations.AddField(
            model_name='servicedelivery',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='metadata.ServiceDeliveryStatus'),
        ),
        migrations.AddField(
            model_name='servicedelivery',
            name='uk_region',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='metadata.UKRegion'),
        ),
    ]

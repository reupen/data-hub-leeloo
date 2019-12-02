# Generated by Django 2.2.3 on 2019-07-28 19:24

from django.db import migrations
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0014_update_permissions_django_21'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='service',
            field=mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='metadata.Service'),
        ),
    ]

# Generated by Django 2.1 on 2018-08-21 10:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0030_update_permissions_django_21'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='company',
            options={'permissions': (('view_company_document', 'Can view company document'), ('view_company_timeline', 'Can view company timeline'), ('export_company', 'Can export company')), 'verbose_name_plural': 'companies'},
        ),
    ]
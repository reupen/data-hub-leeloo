# Generated by Django 2.2.4 on 2019-11-05 20:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('company_list', '0008_allow_is_legacy_default_to_be_false'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.RemoveField(
                    model_name='companylistitem',
                    name='adviser',
                ),
            ],
        ),
    ]
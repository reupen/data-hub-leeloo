# Generated by Django 2.0.4 on 2018-05-14 15:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('interaction', '0025_initial_communication_channels'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='interaction',
            options={'default_permissions': ('add_all', 'change_all', 'delete'), 'permissions': (('read_all_interaction', 'Can read all interaction'), ('read_associated_investmentproject_interaction', 'Can read interaction for associated investment projects'), ('add_associated_investmentproject_interaction', 'Can add interaction for associated investment projects'), ('change_associated_investmentproject_interaction', 'Can change interaction for associated investment projects'), ('read_policy_feedback_interaction', 'Can read policy feedback interaction'), ('add_policy_feedback_interaction', 'Can add policy feedback interaction'), ('change_policy_feedback_interaction', 'Can change policy feedback interaction'))},
        ),
    ]

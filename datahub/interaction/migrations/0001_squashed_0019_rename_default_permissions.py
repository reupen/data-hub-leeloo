# Generated by Django 2.0.2 on 2018-02-09 15:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    replaces = [('interaction', '0001_squash_0008_initial'), ('interaction', '0002_add_investment_project_to_interactions'), ('interaction', '0003_fix_blank_fields'), ('interaction', '0004_rename_advsor_fkeys_to_adviser'), ('interaction', '0005_created_modified_by'), ('interaction', '0006_auto_20170807_1124'), ('interaction', '0007_add_date_index'), ('interaction', '0008_add_interaction_kind'), ('interaction', '0009_add_interaction_event'), ('interaction', '0010_ren_interaction_type_comm_channel'), ('interaction', '0011_move_interaction_type'), ('interaction', '0012_update_interaction_type_fkeys'), ('interaction', '0013_rename_interaction_type_table'), ('interaction', '0014_remove_service_delivery'), ('interaction', '0015_adding_read_permissions'), ('interaction', '0016_add_archived_documents_url_path'), ('interaction', '0017_add_default_id_for_metadata'), ('interaction', '0018_add_assoc_permissions'), ('interaction', '0019_rename_default_permissions')]

    initial = True

    dependencies = [
        ('metadata', '0011_add_default_id_for_metadata'),
        ('event', '0008_add_service'),
        ('company', '0001_squashed_0010_auto_20170807_1124'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('investment', '0001_squashed_0013_add_quotable_as_case_study'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommunicationChannel',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('name', models.TextField(blank=True)),
                ('disabled_on', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'ordering': ('name',),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Interaction',
            fields=[
                ('created_on', models.DateTimeField(auto_now_add=True, db_index=True, null=True)),
                ('modified_on', models.DateTimeField(auto_now=True, null=True)),
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('date', models.DateTimeField()),
                ('subject', models.TextField()),
                ('notes', models.TextField(max_length=4000)),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='interactions', to='company.Company')),
                ('contact', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='interactions', to='company.Contact')),
                ('dit_adviser', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='interactions', to=settings.AUTH_USER_MODEL)),
                ('dit_team', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='metadata.Team')),
                ('communication_channel', models.ForeignKey(blank=True, help_text='For interactions only.', null=True, on_delete=django.db.models.deletion.SET_NULL, to='interaction.CommunicationChannel')),
                ('service', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='metadata.Service')),
                ('investment_project', models.ForeignKey(blank=True, help_text='For interactions only.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='interactions', to='investment.InvestmentProject')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('kind', models.CharField(choices=[('interaction', 'Interaction'), ('service_delivery', 'Service delivery'), ('policy', 'Policy interaction')], max_length=255)),
                ('event', models.ForeignKey(blank=True, help_text='For service deliveries only.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='interactions', to='event.Event')),
                ('archived_documents_url_path', models.CharField(blank=True, help_text='Legacy field. File browser path to the archived documents for this interaction.', max_length=255)),

            ],
            options={
                'abstract': False,
                'indexes': [models.Index(fields=['-date', '-created_on'], name='interaction_date_06c266_idx')],
                'default_permissions': ('add_all', 'change_all', 'delete'),
                'permissions': (('read_all_interaction', 'Can read all interaction'), ('read_associated_investmentproject_interaction', 'Can read interaction for associated investment projects'), ('add_associated_investmentproject_interaction', 'Can add interaction for associated investment projects'), ('change_associated_investmentproject_interaction', 'Can change interaction for associated investment projects'))
            },
        ),
    ]

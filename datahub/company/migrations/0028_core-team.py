# Generated by Django 2.0.7 on 2018-07-27 14:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0027_add_timeline_permission'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyCoreTeamMember',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('adviser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='core_team_memberships', to=settings.AUTH_USER_MODEL)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='core_team_members', to='company.Company')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='companycoreteammember',
            unique_together={('company', 'adviser')},
        ),
    ]

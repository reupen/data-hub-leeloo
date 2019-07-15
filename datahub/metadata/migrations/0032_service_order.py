from pathlib import PurePath

from django.db import migrations, models

from datahub.core.migration_utils import load_yaml_data_in_migration


def load_services(apps, schema_editor):
    load_yaml_data_in_migration(
        apps,
        PurePath(__file__).parent / '0032_service_order.yaml',
    )


class Migration(migrations.Migration):

    dependencies = [
        ('metadata', '0031_update_services'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='order',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterModelOptions(
            name='service',
            options={
                'ordering': ('order',)
                },
        ),
        migrations.RunPython(load_services, migrations.RunPython.noop),
    ]
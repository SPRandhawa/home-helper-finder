from django.db import migrations


def sync_approval_status(apps, schema_editor):
    Helper = apps.get_model('helpers', 'Helper')
    database = schema_editor.connection.alias
    Helper.objects.using(database).filter(
        verification_status='verified',
    ).update(approved=True)
    Helper.objects.using(database).filter(
        verification_status='rejected',
    ).update(approved=False)


class Migration(migrations.Migration):

    dependencies = [
        ('helpers', '0003_helper_verification_notes_helper_verification_status_and_more'),
    ]

    operations = [
        migrations.RunPython(sync_approval_status, migrations.RunPython.noop),
    ]

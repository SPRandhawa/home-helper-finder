from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('helpers', '0004_sync_approved_with_verification'),
    ]

    operations = [
        migrations.AddField(
            model_name='helper',
            name='working_days',
            field=models.JSONField(blank=True, default=list),
        ),
    ]

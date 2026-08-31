from django.db import migrations
from django.contrib.auth.models import User


def create_admin(apps, schema_editor):
    """Create a superuser admin account"""
    if not User.objects.filter(username='home-finder').exists():
        User.objects.create_superuser(
            username='home-finder',
            email='admin@example.com',
            password='Home@123Finder'
        )


def delete_admin(apps, schema_editor):
    """Delete the admin user on rollback"""
    User.objects.filter(username='home-finder').delete()


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.RunPython(create_admin, delete_admin),
    ]

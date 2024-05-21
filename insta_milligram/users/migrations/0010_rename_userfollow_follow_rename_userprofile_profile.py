# Generated by Django 5.0.4 on 2024-05-21 07:05

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_userfollow_at'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name='UserFollow',
            new_name='Follow',
        ),
        migrations.RenameModel(
            old_name='UserProfile',
            new_name='Profile',
        ),
    ]

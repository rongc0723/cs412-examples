# Generated by Django 5.1.1 on 2024-10-13 20:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mini_fb', '0005_alter_profile_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='name',
        ),
    ]

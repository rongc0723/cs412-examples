# Generated by Django 5.1.3 on 2024-12-05 06:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0008_rename_profile_image_url_profile_profile_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='buyer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='buyer', to='project.profile'),
        ),
    ]

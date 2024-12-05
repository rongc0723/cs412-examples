# Generated by Django 5.1.3 on 2024-12-05 06:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0009_alter_item_buyer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='buyer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='buyer', to='project.profile'),
        ),
    ]

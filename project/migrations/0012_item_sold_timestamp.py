# Generated by Django 5.1.3 on 2024-12-07 02:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0011_alter_profile_profile_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='sold_timestamp',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]

# Generated by Django 5.1.1 on 2024-10-13 20:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mini_fb', '0004_profile_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='name',
            field=models.TextField(blank=True, null=True),
        ),
    ]
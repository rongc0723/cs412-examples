# Generated by Django 5.1.3 on 2024-11-09 01:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voter_analytics', '0003_voter_year_of_birth_alter_voter_dob'),
    ]

    operations = [
        migrations.AlterField(
            model_name='voter',
            name='precinct_number',
            field=models.CharField(max_length=6),
        ),
    ]

# Generated by Django 5.1.3 on 2024-11-20 02:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0002_profile_phone_number_item_image_review'),
    ]

    operations = [
        migrations.RenameField(
            model_name='item',
            old_name='name',
            new_name='item_name',
        ),
    ]

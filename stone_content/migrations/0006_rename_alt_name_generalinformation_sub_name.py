# Generated by Django 3.2.22 on 2024-01-08 16:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stone_content', '0005_emergence'),
    ]

    operations = [
        migrations.RenameField(
            model_name='generalinformation',
            old_name='alt_name',
            new_name='sub_name',
        ),
    ]

# Generated by Django 3.2.22 on 2024-01-08 13:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('geomat_content', '0022_rename_trivial_name_generalinformation_sub_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='generalinformation',
            old_name='variety',
            new_name='variety_name',
        ),
    ]

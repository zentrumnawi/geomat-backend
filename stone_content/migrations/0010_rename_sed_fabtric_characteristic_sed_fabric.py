# Generated by Django 3.2.22 on 2024-01-25 09:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stone_content', '0009_rename_sub_name_generalinformation_alt_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='characteristic',
            old_name='sed_fabtric',
            new_name='sed_fabric',
        ),
    ]

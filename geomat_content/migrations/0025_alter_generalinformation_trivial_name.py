# Generated by Django 3.2.22 on 2024-01-11 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geomat_content', '0024_rename_sub_name_generalinformation_trivial_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='generalinformation',
            name='trivial_name',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='trivial name'),
        ),
    ]

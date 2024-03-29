# Generated by Django 3.0.7 on 2021-10-14 15:23

from django.db import migrations, models


def add_temp_pressure_units(apps, schema_editor):

    CrystalSystem = apps.get_model("geomat_content", "CrystalSystem")

    for system in CrystalSystem.objects.all():
        if system.temperature:
            system.temperature += " °C"
        if system.pressure:
            system.pressure += " kbar"
        system.save()


class Migration(migrations.Migration):

    dependencies = [
        ('geomat_content', '0012_auto_20211014_1655'),
    ]

    operations = [
        migrations.AlterField(
            model_name='crystalsystem',
            name='pressure',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='pressure'),
        ),
        migrations.AlterField(
            model_name='crystalsystem',
            name='temperature',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='temperature'),
        ),
        migrations.RunPython(add_temp_pressure_units, migrations.RunPython.noop)
    ]

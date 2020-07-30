# Generated by Django 3.0.7 on 2020-07-29 13:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("geomat_content", "0002_cleavage_model"),
    ]

    operations = [
        migrations.CreateModel(
            name="CrystalSystem",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "crystal_system",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("TC", "Triclinic"),
                            ("MC", "Monoclinic"),
                            ("OR", "Orthorhombic"),
                            ("TT", "Tetragonal"),
                            ("TR", "Trigonal"),
                            ("HG", "Hexagonal"),
                            ("CB", "Cubic"),
                            ("AM", "Amorph"),
                        ],
                        max_length=2,
                        verbose_name="crystal system",
                    ),
                ),
                (
                    "temperature",
                    models.IntegerField(
                        blank=True, null=True, verbose_name="temperature"
                    ),
                ),
                (
                    "pressure",
                    models.IntegerField(blank=True, null=True, verbose_name="pressure"),
                ),
                (
                    "mineral_type",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="crystal_system",
                        to="geomat_content.MineralType",
                        verbose_name="mineral type",
                    ),
                ),
            ],
            options={
                "verbose_name": "Crystal System",
                "verbose_name_plural": "Crystal Systems",
            },
        ),
    ]
# Generated by Django 3.0.7 on 2021-10-14 14:23

from django.db import migrations, models


def populate_cleavage_text(apps, schema_editor):

    Property = apps.get_model("geomat_content", "Property")

    for prop in Property.objects.all():
        cleav_text = ""
        CLEAVAGE_CHOICES = {
            "PE": "perfekt",
            "LP": "vollkommen",
            "GO": "good",
            "DI": "distinct",
            "ID": "indistinct",
            "NO": "none",
        }
        for cleav in prop.cleavage.all():
            coord_str = ""
            if cleav.coordinates:
                coord_str = f"in {cleav.coordinates}"
            cleav_text += f"{CLEAVAGE_CHOICES[cleav.cleavage]} {coord_str} \n"

        prop.cleavage_text = cleav_text
        prop.save()


class Migration(migrations.Migration):

    dependencies = [
        ('geomat_content', '0010_auto_20211010_2106'),
    ]

    operations = [
        migrations.AddField(
            model_name='property',
            name='cleavage_text',
            field=models.TextField(null=True, verbose_name='Cleavages'),
        ),
        migrations.RunPython(populate_cleavage_text, migrations.RunPython.noop)
    ]

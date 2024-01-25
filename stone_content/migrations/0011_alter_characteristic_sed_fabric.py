# Generated by Django 3.2.22 on 2024-01-25 09:45

from django.db import migrations, models
import stone_content.models


class Migration(migrations.Migration):

    dependencies = [
        ('stone_content', '0010_rename_sed_fabtric_characteristic_sed_fabric'),
    ]

    operations = [
        migrations.AlterField(
            model_name='characteristic',
            name='sed_fabric',
            field=stone_content.models.ChoiceArrayField(base_field=models.CharField(blank=True, choices=[('1', 'homogen'), ('2', 'inhomogen'), ('3', 'matrixgestützt'), ('4', 'komponentengestützt'), ('5', 'hohe Rauigkeit'), ('6', 'mittlere Rauigkeit'), ('7', 'geringe Rauigkeit'), ('8', 'sehr geringe Rauigkeit'), ('9', 'gute Sortierung'), ('10', 'mittlere Sortierung'), ('11', 'schlechte Sortierung'), ('12', 'unreif'), ('13', 'mittelreif'), ('14', 'reif'), ('15', 'hochreif'), ('16', 'feine Schichtung'), ('17', 'mittlere Schichtung'), ('18', 'grobe Schichtung'), ('19', 'undeutliche Schichtung'), ('20', 'keine Schichtung'), ('21', 'Schrägschichtung'), ('22', 'Kreuzschichtung'), ('23', 'Rippelschichtung'), ('24', 'mit Hohlräumen'), ('25', 'mit Poren'), ('26', 'Lockergestein'), ('27', 'Festgestein')], max_length=2), blank=True, null=True, size=None, verbose_name='Gefüge (Sediment)'),
        ),
    ]

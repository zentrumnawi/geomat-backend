# Generated by Django 3.2.22 on 2024-01-11 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stone_content', '0007_auto_20240111_1130'),
    ]

    operations = [
        migrations.AlterField(
            model_name='composition',
            name='cementation',
            field=models.CharField(blank=True, choices=[('1', 'kalkig'), ('2', 'kieselig')], max_length=1, null=True, verbose_name='Zement'),
        ),
    ]

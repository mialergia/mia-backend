# Generated by Django 3.0 on 2020-10-13 20:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pollens', '0003_auto_20201013_0206'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='polen',
            options={'verbose_name': 'Polen', 'verbose_name_plural': 'Polen'},
        ),
        migrations.AlterModelOptions(
            name='reporteconcentracion',
            options={'verbose_name': 'Reporte', 'verbose_name_plural': 'Reportes'},
        ),
    ]

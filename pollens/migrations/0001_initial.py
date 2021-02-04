# Generated by Django 3.0 on 2020-09-08 03:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GrupoPolinico',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('unidad_medida', models.CharField(max_length=12)),
                ('nivel_alto', models.IntegerField()),
                ('nivel_medio', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Polen',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(max_length=50)),
                ('nombre_cientifico', models.CharField(blank=True, max_length=50)),
                ('nombre_comun', models.CharField(blank=True, max_length=50)),
                ('familia', models.CharField(max_length=50)),
                ('picks_presente', models.BooleanField()),
                ('alergenicidad', models.CharField(max_length=50)),
                ('grupo_polinico', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='polenes', to='pollens.GrupoPolinico')),
            ],
        ),
        migrations.CreateModel(
            name='ReporteConcentracion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nivel', models.IntegerField()),
                ('fecha', models.DateTimeField()),
                ('grupo_polinico', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='niveles', to='pollens.GrupoPolinico')),
                ('tipo_polinico', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='niveles', to='pollens.Polen')),
            ],
        ),
    ]

# Generated by Django 3.0 on 2020-09-06 23:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('symptoms', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='entradadiario',
            old_name='pregunta_diario',
            new_name='preguntas',
        ),
        migrations.RenameField(
            model_name='valorrespuesta',
            old_name='pregunta_diario',
            new_name='pregunta',
        ),
    ]

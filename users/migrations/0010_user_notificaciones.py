# Generated by Django 3.0 on 2020-10-21 00:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('information', '0002_notificacion'),
        ('users', '0009_user_onesignal_player_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='notificaciones',
            field=models.ManyToManyField(blank=True, to='information.Notificacion'),
        ),
    ]

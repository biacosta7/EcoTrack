# Generated by Django 5.1.1 on 2024-11-07 22:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('centros', '0006_alter_centrocoleta_telefone'),
    ]

    operations = [
        migrations.AddField(
            model_name='centrocoleta',
            name='latitude',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='centrocoleta',
            name='longitude',
            field=models.FloatField(blank=True, null=True),
        ),
    ]

# Generated by Django 5.1.1 on 2024-09-25 21:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('centros', '0004_alter_centrocoleta_tipos'),
    ]

    operations = [
        migrations.AlterField(
            model_name='centrocoleta',
            name='tipos',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]

# Generated by Django 5.1.1 on 2024-09-25 21:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('centros', '0005_alter_centrocoleta_tipos'),
    ]

    operations = [
        migrations.AlterField(
            model_name='centrocoleta',
            name='telefone',
            field=models.CharField(help_text='Telefone do centro.', max_length=20),
        ),
    ]

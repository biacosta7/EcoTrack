# Generated by Django 5.1.1 on 2024-09-30 21:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agendamentos', '0002_empresa'),
    ]

    operations = [
        migrations.AddField(
            model_name='agendamento',
            name='empresa',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='agendamentos.empresa'),
            preserve_default=False,
        ),
    ]
# Generated by Django 5.1.1 on 2024-09-29 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0016_user_cep'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='nome',
            field=models.CharField(help_text='Nome do usuário.', max_length=30, null=True),
        ),
    ]

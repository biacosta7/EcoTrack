# Generated by Django 5.1.1 on 2024-11-04 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0017_alter_user_nome'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='pontuacao',
            field=models.IntegerField(default=0, help_text='Pontuação acumulada por reciclagem de resíduos.'),
        ),
    ]
# Generated by Django 5.1.1 on 2024-09-29 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0015_user_first_name_user_last_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='cep',
            field=models.CharField(blank=True, help_text='CEP do usuário ou da empresa.', max_length=20, null=True),
        ),
    ]
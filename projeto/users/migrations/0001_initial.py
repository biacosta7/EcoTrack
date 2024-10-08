# Generated by Django 5.1 on 2024-09-21 23:53

import django.contrib.auth.models
import django.contrib.auth.validators
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ('auth', '0011_update_proxy_permissions'),  # ou a última migração disponível para o app auth
]


    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('is_company', models.BooleanField(default=False, help_text='Designa se o usuário é uma empresa.')),
                ('nome_empresa', models.CharField(blank=True, help_text='Nome da empresa.', max_length=255, null=True)),
                ('endereco_empresa', models.CharField(blank=True, help_text='Endereço da empresa.', max_length=500, null=True)),
                ('telefone_empresa', models.CharField(blank=True, help_text='Telefone da empresa.', max_length=20, null=True)),
                ('company_website', models.URLField(blank=True, help_text='Website da empresa.', null=True)),
                ('nome', models.CharField(help_text='Nome do usuário.', max_length=30)),
                ('sobrenome', models.CharField(help_text='Sobrenome do usuário.', max_length=30)),
                ('telefone', models.CharField(blank=True, help_text='Telefone do usuário.', max_length=20, null=True)),
                ('email', models.EmailField(help_text='Endereco de e-mail do usuário.', max_length=254, unique=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='Os grupos aos quais este usuário pertence.', related_name='custom_user_set', to='auth.group')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Permissões específicas para este usuário.', related_name='custom_user_permissions_set', to='auth.permission')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]

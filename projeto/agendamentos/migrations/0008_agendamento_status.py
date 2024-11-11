# Generated by Django 5.1.1 on 2024-11-11 22:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agendamentos', '0007_agendamento_pontuacao_alter_agendamento_empresa_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='agendamento',
            name='status',
            field=models.CharField(choices=[('solicitacao', 'Solicitação de Agendamento'), ('coleta', 'Coleta'), ('triagem', 'Triagem'), ('transformacao', 'Transformação'), ('realocacao', 'Realocação')], default='solicitacao', max_length=20),
        ),
    ]
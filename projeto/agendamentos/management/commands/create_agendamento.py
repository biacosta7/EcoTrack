from django.core.management.base import BaseCommand
from agendamentos.models import Agendamento  # Ajuste conforme necessário

class Command(BaseCommand):
    help = 'Cria um agendamento'

    def add_arguments(self, parser):
        parser.add_argument('empresa_id', type=int)
        parser.add_argument('nome', type=str)
        parser.add_argument('data', type=str) 
        parser.add_argument('hora', type=str)
        parser.add_argument('endereco', type=str)
        parser.add_argument('tipos_residuos', nargs='+')  # Aceita múltiplos tipos

    def handle(self, *args, **kwargs):
        empresa_id = kwargs['empresa_id']
        nome = kwargs['nome']
        data = kwargs['data']
        hora = kwargs['hora']
        endereco = kwargs['endereco']
        tipos_residuos = kwargs['tipos_residuos']

        # Criação do agendamento
        agendamento = Agendamento.objects.create(
            empresa_id=empresa_id,
            nome=nome,
            data=data,
            hora=hora,
            endereco=endereco,
            tipos_residuos=', '.join(tipos_residuos)
        )
        self.stdout.write(self.style.SUCCESS(f'Agendamento criado: {agendamento}'))

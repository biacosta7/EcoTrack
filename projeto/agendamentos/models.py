from django.db import models
from users.models import User

class Agendamento(models.Model):
    nome = models.CharField(max_length=100)
    data = models.DateField()
    hora = models.TimeField()
    endereco = models.CharField(max_length=255)
    tipos_residuos = models.TextField(max_length=150)
    empresa = models.ForeignKey(User, limit_choices_to={'is_company': True}, related_name='agendamentos', on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, related_name='agendamentos_usuario', on_delete=models.CASCADE)  # Novo campo para associar o agendamento ao usuário

    def __str__(self):
        return f'{self.nome} - {self.data} às {self.hora}'

from django.db import models
from users.models import User

class Agendamento(models.Model):
    nome = models.CharField(max_length=100)
    data = models.DateField()
    hora = models.TimeField()
    endereco = models.CharField(max_length=255)
    tipos_residuos = models.TextField()  # Armazena os tipos de resíduos
    empresa = models.ForeignKey(User, on_delete=models.CASCADE, related_name='agendamentos')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='meus_agendamentos')
    pontuacao = models.IntegerField(default=0)  # Adicionando o campo pontuacao

    def __str__(self):
        return f'Agendamento de {self.nome} para {self.data} às {self.hora}'

from django.db import models
from users.models import User

class Agendamento(models.Model):
    # Definindo as etapas possíveis do agendamento
    ETAPA_CHOICES = [
        ('solicitacao', 'Solicitação de Agendamento'),
        ('coleta', 'Coleta'),
        ('triagem', 'Triagem'),
        ('transformacao', 'Transformação'),
        ('realocacao', 'Realocação'),
    ]
    
    # Etapa atual, com opções predefinidas
    etapa_atual = models.CharField(
        max_length=100,
        choices=ETAPA_CHOICES,
        default='solicitacao'
    )

    # Outros campos
    nome = models.CharField(max_length=100)
    data = models.DateField()
    hora = models.TimeField()
    endereco = models.CharField(max_length=255)
    tipos_residuos = models.TextField()
    
    # Relacionamento com o usuário (empresa e usuário do agendamento)
    empresa = models.ForeignKey(User, on_delete=models.CASCADE, related_name='agendamentos')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='meus_agendamentos')
    
    # Pontuação do agendamento
    pontuacao = models.IntegerField(default=0)

    # Status do agendamento (se necessário)
    STATUS_CHOICES = [
        ('solicitacao', 'Solicitação'),
        ('confirmado', 'Confirmado'),
        ('cancelado', 'Cancelado'),
    ]
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='solicitacao'
    )

    def __str__(self):
        return f'Agendamento de {self.nome} para {self.data} às {self.hora}'

    # Método para exibir a etapa de forma legível no template
    def get_etapa_display(self):
        return dict(self.ETAPA_CHOICES).get(self.etapa_atual, 'Etapa não definida')

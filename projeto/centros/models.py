from django.db import models
from users.models import User
#nome', 'telefone', 'endereco', 'numero', 
# 'complemento', 'cep', 'tipos', 
# 'horario_abertura', 'horario_fechamento'
class CentroColeta(models.Model):
    TIPOS_CHOICES = [
        ('metal', 'Metal'),
        ('papel', 'Papel'),
        ('plastico', 'Plástico'),
        ('organico', 'Orgânico'),
        ('perigoso', 'Perigoso'),
        ('vidro', 'Vidro')
    ]

    nome = models.CharField(max_length=255, help_text="Nome do centro de coleta.")
    telefone = models.CharField(max_length=20, help_text="Telefone do centro.")
    endereco = models.CharField(max_length=500, help_text="Endereço do centro de coleta.")
    numero = models.CharField(max_length=10, help_text="Número do endereço do centro", blank=True, null=True)
    complemento = models.CharField(max_length=50, help_text="Complemento do endereço", blank=True, null=True)
    cep = models.CharField(max_length=9, help_text="Número do CEP", blank=True, null=True)
    tipos = models.CharField(max_length=255,blank=True, null=True)
    horario_abertura = models.CharField(max_length=100, help_text="Horário de abertura.", blank=True, null=True)
    horario_fechamento = models.CharField(max_length=100, help_text="Horário de fechamento.", blank=True, null=True)
    usuario_responsavel = models.ForeignKey(User, related_name='centros_responsaveis', on_delete=models.CASCADE, help_text="Usuário responsável pelo centro.")

    def __str__(self):
        return self.nome
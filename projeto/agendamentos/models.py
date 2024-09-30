from django.db import models

class Empresa(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

class Agendamento(models.Model):
    nome = models.CharField(max_length=100)
    data = models.DateField()
    hora = models.TimeField()
    tipos_residuos = models.TextField()  # Múltiplos tipos de resíduos salvos como uma string separada por vírgulas
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)  # Adicione esta linha

    def __str__(self):
        return f'{self.nome} - {self.data} às {self.hora}'


from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Recompensa

@receiver(post_migrate)
def create_recompensas(sender, **kwargs):
    if sender.name == 'users':  # Substitua 'users' pelo nome do seu aplicativo
        recompensas = [
            {"nome": "Sementes de árvores", "descricao": "Troque por sementes de árvores para plantar no seu bairro.", "custo": 100},
            {"nome": "Desconto em lojas de produtos ecológicos", "descricao": "Desconto de 10% em sua próxima compra.", "custo": 200},
            {"nome": "Lixeiras ecológicas", "descricao": "Troque por uma lixeira ecológica para a sua casa.", "custo": 250},
            {"nome": "Oficina de reciclagem", "descricao": "Participe de uma oficina de reciclagem e aprenda mais sobre o meio ambiente.", "custo": 400},
            {"nome": "Cesta de produtos orgânicos", "descricao": "Receba uma cesta com produtos orgânicos de agricultores locais.", "custo": 650},
            {"nome": "Kits de jardinagem", "descricao": "Receba um kit de jardinagem para cultivar suas próprias plantas.", "custo": 800},
            {"nome": "Experiência em ecoturismo", "descricao": "Ganhe uma experiência em ecoturismo em uma reserva ambiental.", "custo": 1000},
        ]
        
        for recompensa in recompensas:
            Recompensa.objects.get_or_create(**recompensa)

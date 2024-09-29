from django.urls import path
from .views import cadastrar_centro, lista_centros, atualizar_centro, remover_centro

app_name = 'centros'

urlpatterns = [
    path('cadastrar/', cadastrar_centro, name='cadastrar_centro'),
    path('lista/', lista_centros, name='lista_centros'),  # URL para listar os centros
    path('atualizar/<int:centro_id>/', atualizar_centro, name='atualizar_centro'),
    path('remover/<int:centro_id>/', remover_centro, name='remover_centro')
]

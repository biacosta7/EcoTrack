from django.urls import path
from .views import cadastrar_centro, lista_centros

app_name = 'centros'

urlpatterns = [
    path('cadastrar/', cadastrar_centro, name='cadastrar_centro'),
    path('lista/', lista_centros, name='lista_centros'),  # URL para listar os centros
]

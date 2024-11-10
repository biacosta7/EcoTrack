from django.urls import path
from . import views

app_name = 'centros'

urlpatterns = [
    path('cadastrar/', views.cadastrar_centro, name='cadastrar_centro'),
    path('lista/', views.lista_centros, name='lista_centros'),  # URL para listar os centros
    path('atualizar/<int:centro_id>/', views.atualizar_centro, name='atualizar_centro'),
    path('remover/<int:centro_id>/', views.remover_centro, name='remover_centro'),
    path('mapa/', views.localizar_centros, name='localizar_centros'),
    path('pontos-de-coleta/', views.pontos_de_coleta, name='pontos_de_coleta'),  # Nova URL para retornar JSON dos pontos
    path('calcular_distancia/', views.calcular_distancia, name='calcular_distancia'),

]

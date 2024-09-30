from django.urls import path
from . import views

app_name = 'agendamentos'

urlpatterns = [
    path('', views.agendar, name='agendamentos_coleta'),  # View para o formulário de agendamento
    path('confirmacao/<str:data_agendamento>/<str:horario_agendamento>/<str:empresa_nome>/', views.confirmacao_view, name='confirmacao'),  # View de confirmação com parâmetros
    path('lista/', views.lista_agendamentos, name='lista_agendamentos'),  # View para listar agendamentos
]

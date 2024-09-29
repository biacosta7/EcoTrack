from django.urls import path
from . import views

app_name = 'agendamentos'

urlpatterns = [
    path('', views.agendar, name='agendamentos_coleta'),  # View para o formulário de agendamento
    path('confirmacao/', views.confirmacao_view, name='confirmacao'),  # View de confirmação
]

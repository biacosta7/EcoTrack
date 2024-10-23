from django.urls import path
from . import views

app_name = 'agendamentos'

urlpatterns = [
    path('', views.agendar, name='agendamentos_coleta'),  # View para o formulário de agendamento
    path('confirmacao/<str:data_agendamento>/<str:horario_agendamento>/<str:empresa_nome>/', views.confirmacao_view, name='confirmacao'),
    path('lista/', views.lista_agendamentos, name='lista_agendamentos'),  # View para listar agendamentos
    path('visualizar/<int:id>/', views.ver_agendamentos, name='ver_agendamentos'),
    path('delete/<int:agendamento_id>/', views.delete_appointment, name='delete_appointment'),
    path('meus-agendamentos/', views.ver_agendamentos_usuario, name='ver_agendamentos_usuario'),  # Nova rota para visualizar agendamentos do usuário
    path('meus-agendamentos/delete/<int:agendamento_id>/', views.delete_user_appointment, name='delete_user_appointment'),  # Nova rota para deletar agendamento do usuário
    path('editar_agendamento/<int:agendamento_id>/', views.editar_agendamento, name='editar_agendamento'),
]



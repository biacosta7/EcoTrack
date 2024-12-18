from django.urls import path
from . import views

app_name = 'agendamentos'

urlpatterns = [
    path('', views.agendar, name='agendamentos_coleta'),
    path('confirmacao/<str:data_agendamento>/<str:horario_agendamento>/<str:empresa_nome>/', views.confirmacao_view, name='confirmacao'),
    path('lista/', views.lista_agendamentos, name='lista_agendamentos'),
    path('visualizar/<int:id>/', views.ver_agendamentos_empresa, name='ver_agendamentos'),
    path('delete/<int:agendamento_id>/', views.delete_user_appointment, name='delete_user_appointment'),
    path('meus-agendamentos/', views.ver_agendamentos, name='ver_agendamentos_usuario'),
    path('editar_agendamento/<int:agendamento_id>/', views.editar_agendamento, name='editar_agendamento'),
    path('editar_etapa/<int:agendamento_id>/', views.editar_etapa_agendamento, name='editar_etapa_agendamento'),
    path('agendamentos/empresa/<int:id>/', views.ver_agendamentos_empresa, name='ver_agendamentos_empresa'),

]

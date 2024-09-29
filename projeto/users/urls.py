from django.urls import path
from django.contrib.auth import views as auth_views
from users.views import (
    user_detail_view,
    user_list_view,
    CustomLoginView,
    user_delete_view,
    empresa_dashboard_view,
    usuario_dashboard_view,
    register_view,
    confirmacao_view,

)

app_name = 'user'

urlpatterns = [
    path('', user_list_view, name='listar_user'), 
    #path('criar-centro/', criar_centro, name='criar-centro'),  # Nova rota para criar centro, se aplicável
    path('<int:id>/', user_detail_view, name='user-detail'), 
    #path('<int:id>/update/', user_update_view, name='user-update'),  # Rota para atualizar usuário
    path('<int:id>/delete/', user_delete_view, name='user-delete'),  # Rota para deletar usuário
    path('login/', CustomLoginView.as_view(), name='login'),
    path('registrar/', register_view, name='register'),
    path('empresa/dashboard/', empresa_dashboard_view, name='empresa_dashboard'),
    path('usuario/dashboard/', usuario_dashboard_view, name='usuario_dashboard'),
    path('confirmacao/', confirmacao_view, name='confirmacao'),

]

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
    recompensas_view,
    trocar_recompensa_view,  # Importa a nova view
)

app_name = 'user'

urlpatterns = [
    path('', user_list_view, name='listar_user'), 
    path('<int:id>/', user_detail_view, name='user-detail'), 
    path('<int:id>/delete/', user_delete_view, name='user-delete'),  
    path('login/', CustomLoginView.as_view(), name='login'),
    path('registrar/', register_view, name='register'),
    path('empresa/dashboard/', empresa_dashboard_view, name='empresa_dashboard'),
    path('usuario/dashboard/', usuario_dashboard_view, name='usuario_dashboard'),
    path('confirmacao/', confirmacao_view, name='confirmacao'),
    
    # Adiciona as novas rotas para recompensas
    path('recompensas/', recompensas_view, name='recompensas'),  # Rota para a página de recompensas
    path('trocar-recompensa/<int:recompensa_id>/', trocar_recompensa_view, name='trocar_recompensa'),  # Rota para trocar recompensa
]

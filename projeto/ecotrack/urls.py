from django.contrib import admin
from django.urls import include, path
from users.views import home_view

urlpatterns = [
    path('', home_view, name='home'),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls', namespace='user')),
    path('centros/', include('centros.urls')),  # Inclui as URLs do app 'centros'
    path('agendamento/', include('agendamentos.urls')),  # Inclui as URLs do app 'agendamentos'
    path('rastreamentos/', include('rastreamentos.urls', namespace='rastreamentos')),  # Inclui as URLs do app 'rastreamentos' com o namespace
]

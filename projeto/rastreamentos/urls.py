from django.urls import path
from . import views

app_name = 'rastreamentos'  # Define o namespace para o app

urlpatterns = [
    path('rastrear/', views.rastrear_usuario_view, name='rastrear_usuario'),
]

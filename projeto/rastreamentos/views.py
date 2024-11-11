from django.shortcuts import render

def rastrear_usuario_view(request):
    return render(request, 'rastreamentos/rastrear_usuario.html')

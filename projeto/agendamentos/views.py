from django.shortcuts import render, redirect
from .models import Agendamento, Empresa
from django.core.exceptions import ValidationError 

def agendar(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        data = request.POST.get('data')
        hora = request.POST.get('hora')
        tipos_residuos = request.POST.getlist('tipos_residuos')  # Lista de resíduos selecionados

        # Concatena os resíduos selecionados em uma string separada por vírgulas
        tipos_residuos_str = ', '.join(tipos_residuos)  
        
        try:
            # Cria o objeto Agendamento com os dados enviados
            agendamento = Agendamento(
                nome=nome,
                data=data,
                hora=hora,
                tipos_residuos=tipos_residuos_str
            )
            agendamento.full_clean()  # Valida os dados
            agendamento.save()  # Salva o agendamento no banco de dados
            
            # Redireciona para a página de confirmação
            return redirect('agendamentos:confirmacao')  
        
        except ValidationError as e:
            # Captura erros de validação
            print(f"Erro de validação: {e}")
    
    return render(request, 'agendamentos/agendamentos_coleta.html')

def confirmacao_view(request):
    return render(request, 'agendamentos/confirmacao.html')  # Página de confirmação

def agendar_view(request):
    empresas = Empresa.objects.all()  # Obtendo todas as empresas
    if request.method == 'POST':
        # Aqui você pode processar o formulário
        pass

    return render(request, 'seu_template.html', {'empresas': empresas})

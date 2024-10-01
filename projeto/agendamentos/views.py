from django.shortcuts import render, redirect
from django.contrib import messages  # Importando para exibir mensagens
from .models import Agendamento, Empresa
from users.models import User
from django.core.exceptions import ValidationError

def agendar(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        data = request.POST.get('data')
        hora = request.POST.get('hora')
        empresa_id = request.POST.get('empresa')  # Captura a empresa selecionada
        tipos_residuos = request.POST.getlist('tipos_residuos')  # Lista de resíduos selecionados

        # Concatena os resíduos selecionados em uma string separada por vírgulas
        tipos_residuos_str = ', '.join(tipos_residuos)

        # Verificação de conflitos
        if Agendamento.objects.filter(data=data, hora=hora, empresa_id=empresa_id).exists():
            messages.error(request, 'Já existe um agendamento para esta data, hora e empresa. Por favor, escolha outro horário.')
            empresas = User.objects.filter(is_company=True)  # Obtém todas as empresas cadastradas
            return render(request, 'agendamentos/agendamentos_coleta.html', {'empresas': empresas})

        try:
            # Cria o objeto Agendamento com os dados enviados
            agendamento = Agendamento(
                nome=nome,
                data=data,
                hora=hora,
                tipos_residuos=tipos_residuos_str,
                empresa_id=empresa_id  # Define a empresa selecionada
            )
            agendamento.full_clean()  # Valida os dados
            agendamento.save()  # Salva o agendamento no banco de dados
            
            # Redireciona para a página de confirmação com os dados do agendamento
            return redirect('agendamentos:confirmacao', data_agendamento=data, horario_agendamento=hora, empresa_nome=User.objects.get(id=empresa_id).nome_empresa)
        
        except ValidationError as e:
            print(f"Erro de validação: {e}")

    empresas = User.objects.filter(is_company=True)  # Obtém todas as empresas cadastradas
    return render(request, 'agendamentos/agendamentos_coleta.html', {'empresas': empresas})

def confirmacao_view(request, data_agendamento, horario_agendamento, empresa_nome):
    return render(request, 'agendamentos/confirmacao.html', {
        'data_agendamento': data_agendamento,
        'horario_agendamento': horario_agendamento,
        'empresa_nome': empresa_nome
    })  # Passando os dados para a página de confirmação

def lista_agendamentos(request):
    agendamentos = Agendamento.objects.all()  # Obtém todos os agendamentos
    return render(request, 'agendamentos/lista_agendamentos.html', {'agendamentos': agendamentos})

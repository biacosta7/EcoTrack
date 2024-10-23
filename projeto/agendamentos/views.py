from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages  # Importando para exibir mensagens
from .models import Agendamento
from users.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required

@login_required
def agendar(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        data = request.POST.get('data')
        hora = request.POST.get('hora')
        endereco = request.POST.get('endereco')
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
                empresa_id=empresa_id,  # Define a empresa selecionada
                endereco=endereco
            )
            
            agendamento.full_clean()  # Valida os dados
            agendamento.save()  # Salva o agendamento no banco de dados
            
            # Redireciona para a página de confirmação com os dados do agendamento
            return redirect('agendamentos:confirmacao', data_agendamento=data, horario_agendamento=hora, empresa_nome=User.objects.get(id=empresa_id).nome_empresa)
        
        except ValidationError as e:
            print(f"Erro de validação: {e}")

    empresas = User.objects.filter(is_company=True)  # Obtém todas as empresas cadastradas
    return render(request, 'agendamentos/agendamentos_coleta.html', {'empresas': empresas})

@login_required
def confirmacao_view(request, data_agendamento, horario_agendamento, empresa_nome):
    return render(request, 'agendamentos/confirmacao.html', {
        'data_agendamento': data_agendamento,
        'horario_agendamento': horario_agendamento,
        'empresa_nome': empresa_nome
    })  # Passando os dados para a página de confirmação

@login_required
def lista_agendamentos(request):
    agendamentos = Agendamento.objects.all()  # Obtém todos os agendamentos
    return render(request, 'agendamentos/lista_agendamentos.html', {'agendamentos': agendamentos})

@login_required
def ver_agendamentos(request, id):
    empresa = get_object_or_404(User, id=id, is_company=True)
    agendamentos = Agendamento.objects.filter(empresa=empresa)

    context = {
        'agendamentos': agendamentos, 
        'empresa': empresa,
    }

    return render(request, 'agendamentos/ver_agendamentos.html', context)




@login_required
def delete_appointment(request, agendamento_id):
    try:
        # Tenta obter o agendamento pelo ID ou gera um erro se não for encontrado
        agendamento = Agendamento.objects.get(id=agendamento_id)

        # Verifica se o usuário logado é a empresa associada ao agendamento
        if agendamento.empresa == request.user:
            agendamento.delete()  # Exclui o agendamento
            messages.success(request, 'Agendamento excluído com sucesso.')
        else:
            # Se o usuário logado não for a empresa do agendamento
            messages.error(request, 'Você não tem permissão para excluir este agendamento.')
    except Agendamento.DoesNotExist:
        # Se o agendamento não existir, exibe uma mensagem de erro
        messages.error(request, 'Agendamento não disponível para exclusão.')

    # Redireciona de volta para a página de visualização de agendamentos
    agendamentos = Agendamento.objects.filter(empresa=request.user)
    return render(request, 'agendamentos/ver_agendamentos.html', {
        'agendamentos': agendamentos,
        'empresa': request.user 
    })

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages  # Importando para exibir mensagens
from .models import Agendamento
from users.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from centros.models import CentroColeta


@login_required
def agendar(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        data = request.POST.get('data')
        hora = request.POST.get('hora')
        endereco = request.POST.get('endereco')
        empresa_id = request.POST.get('empresa')  # Captura a empresa selecionada
        tipos_residuos = request.POST.getlist('tipos_residuos')  # Lista de resíduos selecionados

        tipos_residuos_str = ', '.join(tipos_residuos)

        # Verificação de conflitos
        if Agendamento.objects.filter(data=data, hora=hora, empresa_id=empresa_id).exists():
            messages.error(request, 'Já existe um agendamento para esta data, hora e empresa. Por favor, escolha outro horário.')
            empresas = User.objects.filter(is_company=True)
            return render(request, 'agendamentos/agendamentos_coleta.html', {'empresas': empresas})

        try:
            # Criando o agendamento com os dados do POST e o usuário logado
            agendamento = Agendamento(
                nome=nome,
                data=data,
                hora=hora,
                tipos_residuos=tipos_residuos_str,
                empresa_id=empresa_id,
                endereco=endereco,
                usuario=request.user  # Associando o agendamento ao usuário logado
            )
            agendamento.full_clean()  # Valida os dados
            agendamento.save()  # Salva no banco

            return redirect('agendamentos:confirmacao', data_agendamento=data, horario_agendamento=hora, empresa_nome=User.objects.get(id=empresa_id).nome_empresa)

        except ValidationError as e:
            print(f"Erro de validação: {e}")

    empresas = User.objects.filter(is_company=True)
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
    # Obtém a empresa específica pelo ID ou retorna 404 se não existir
    empresa = get_object_or_404(User, id=id, is_company=True)
    # Filtra os agendamentos associados à empresa
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
        if request.user.is_company and agendamento.empresa == request.user:
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
    return redirect('agendamentos:ver_agendamentos', id=request.user.id)

@login_required
def ver_agendamentos_usuario(request, id):
    """View para visualizar agendamentos de uma empresa específica"""
    try:
        # Obtém a empresa específica pelo ID ou lança uma exceção se não existir
        empresa = User.objects.get(id=id, is_company=True)

        # Filtra os agendamentos associados à empresa
        agendamentos = Agendamento.objects.filter(empresa=empresa)

        context = {
            'agendamentos': agendamentos, 
            'empresa': empresa,
        }
        return render(request, 'agendamentos/ver_agendamentos.html', context)

    except User.DoesNotExist:
        # Se a empresa não existir, exibe uma mensagem de erro
        messages.error(request, 'A empresa solicitada não existe.')
        return redirect('agendamentos:lista_agendamentos')  # Redireciona para uma lista geral ou outra página relevante

@login_required
def delete_user_appointment(request, agendamento_id):
    """View para deletar um agendamento"""
    try:
        # Tenta obter o agendamento pelo ID ou gera um erro se não for encontrado
        agendamento = Agendamento.objects.get(id=agendamento_id)

        # Verifica se o usuário logado é a empresa associada ao agendamento
        if request.user.is_company and agendamento.empresa == request.user:
            agendamento.delete()  # Exclui o agendamento
            messages.success(request, 'Agendamento excluído com sucesso.')
        else:
            # Se o usuário logado não for a empresa do agendamento
            messages.error(request, 'Você não tem permissão para excluir este agendamento.')

    except Agendamento.DoesNotExist:
        # Se o agendamento não existir, exibe uma mensagem de erro
        messages.error(request, 'Agendamento não disponível para exclusão.')

    # Redireciona para a página de visualização de agendamentos
    return redirect('agendamentos:ver_agendamentos', id=request.user.id)


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Agendamento

def editar_agendamento(request, agendamento_id):
    agendamento = get_object_or_404(Agendamento, id=agendamento_id)

    if request.method == 'POST':
        nome = request.POST['nome']
        data = request.POST['data']
        hora = request.POST['hora']
        endereco = request.POST['endereco']
        tipos_residuos = request.POST.getlist('tipos_residuos')

        # Verificar se o horário está sendo alterado
        if agendamento.hora != hora:
            # Verificar se já existe um agendamento para a mesma data e hora
            if Agendamento.objects.filter(data=data, hora=hora).exists():
                messages.error(request, 'Este horário já está indisponível.')
                return render(request, 'agendamentos/editar_agendamento.html', {
                    'agendamento': agendamento,
                })

        # Atualizar agendamento
        agendamento.nome = nome
        agendamento.data = data
        agendamento.hora = hora
        agendamento.endereco = endereco
        agendamento.tipos_residuos = tipos_residuos
        agendamento.save()
        messages.success(request, 'Agendamento atualizado com sucesso!')
        return redirect('user:usuario_dashboard')  # Redirecionar após atualização

    return render(request, 'agendamentos/editar_agendamento.html', {
        'agendamento': agendamento,
    })













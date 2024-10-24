from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
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
        empresa_id = request.POST.get('empresa')
        tipos_residuos = request.POST.getlist('tipos_residuos')
        tipos_residuos_str = ', '.join(tipos_residuos)

        # Verificação de conflitos
        if Agendamento.objects.filter(data=data, hora=hora, empresa_id=empresa_id).exists():
            messages.error(request, 'Já existe um agendamento para esta data, hora e empresa. Por favor, escolha outro horário.')
            empresas = User.objects.filter(is_company=True)
            return render(request, 'agendamentos/agendamentos_coleta.html', {'empresas': empresas})

        try:
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
    })

@login_required
def lista_agendamentos(request):
    agendamentos = Agendamento.objects.all()
    return render(request, 'agendamentos/lista_agendamentos.html', {'agendamentos': agendamentos})

@login_required
def ver_agendamentos(request):
    """View para visualizar agendamentos do usuário logado"""
    agendamentos = Agendamento.objects.filter(usuario=request.user)
    return render(request, 'agendamentos/ver_agendamentos_usuario.html', {'agendamentos': agendamentos})

def ver_agendamentos_empresa(request, id):
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
def delete_user_appointment(request, agendamento_id):
    try:
        agendamento = Agendamento.objects.get(id=agendamento_id)

        # Verifica se o usuário logado é o dono do agendamento
        if agendamento.usuario == request.user:
            agendamento.delete()
            messages.success(request, 'Agendamento excluído com sucesso.')
        else:
            messages.error(request, 'Você não tem permissão para excluir este agendamento.')
    except Agendamento.DoesNotExist:
        messages.error(request, 'Agendamento não disponível para exclusão.')

    return redirect('agendamentos:ver_agendamentos_usuario')  # Redireciona para a lista de agendamentos do usuário

@login_required
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
            if Agendamento.objects.filter(data=data, hora=hora, empresa=agendamento.empresa).exists():
                messages.error(request, 'Este horário já está indisponível.')
                return render(request, 'agendamentos/editar_agendamento.html', {
                    'agendamento': agendamento,
                })

        # Atualizar agendamento
        agendamento.nome = nome
        agendamento.data = data
        agendamento.hora = hora
        agendamento.endereco = endereco
        agendamento.tipos_residuos = ', '.join(tipos_residuos)
        agendamento.save()
        messages.success(request, 'Agendamento atualizado com sucesso!')
        return redirect('agendamentos:ver_agendamentos_usuario')  # Redirecionar após atualização

    return render(request, 'agendamentos/editar_agendamento.html', {
        'agendamento': agendamento,
    })

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Agendamento
from users.models import User
from django.contrib.auth.decorators import login_required

# Dicionário para mapear tipos de resíduos a suas pontuações
PONTUACAO_RESIDUOS = {
    'Metal': 7,
    'Papel': 5,
    'Plástico': 6,
    'Orgânico': 3,
    'Perigoso': 10,
    'Vidro': 4,
}

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

        pontuacao_total = sum(PONTUACAO_RESIDUOS.get(residuo, 0) for residuo in tipos_residuos)

        # Verificação de conflitos
        if Agendamento.objects.filter(data=data, hora=hora, empresa_id=empresa_id).exists():
            messages.error(request, 'Já existe um agendamento para esta data, hora e empresa.')
            return redirect('agendamentos:agendamentos_coleta')

        agendamento = Agendamento(
            nome=nome,
            data=data,
            hora=hora,
            tipos_residuos=tipos_residuos_str,
            empresa_id=empresa_id,
            endereco=endereco,
            usuario=request.user,
            pontuacao=pontuacao_total
        )
        agendamento.save()
        request.user.pontuacao += pontuacao_total
        request.user.save()

        return redirect('agendamentos:confirmacao', data_agendamento=data, horario_agendamento=hora, empresa_nome=User.objects.get(id=empresa_id).nome_empresa)

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
    agendamentos = Agendamento.objects.filter(usuario=request.user)
    return render(request, 'agendamentos/ver_agendamentos_usuario.html', {'agendamentos': agendamentos})

@login_required
def ver_agendamentos_empresa(request, id):
    empresa = get_object_or_404(User, id=id, is_company=True)
    agendamentos = Agendamento.objects.filter(empresa=empresa)
    return render(request, 'agendamentos/ver_agendamentos.html', {'agendamentos': agendamentos, 'empresa': empresa})

@login_required
def delete_user_appointment(request, agendamento_id):
    agendamento = get_object_or_404(Agendamento, id=agendamento_id, usuario=request.user)
    agendamento.delete()
    messages.success(request, 'Agendamento excluído com sucesso.')
    return redirect('agendamentos:ver_agendamentos_usuario')

@login_required
def editar_agendamento(request, agendamento_id):
    agendamento = get_object_or_404(Agendamento, id=agendamento_id, usuario=request.user)
    
    if request.method == 'POST':
        nome = request.POST['nome']
        data = request.POST['data']
        hora = request.POST['hora']
        endereco = request.POST['endereco']
        tipos_residuos = request.POST.getlist('tipos_residuos')

        if Agendamento.objects.filter(data=data, hora=hora, empresa=agendamento.empresa).exclude(id=agendamento.id).exists():
            messages.error(request, 'Este horário já está indisponível.')
            return redirect('agendamentos:editar_agendamento', agendamento_id=agendamento_id)

        agendamento.nome = nome
        agendamento.data = data
        agendamento.hora = hora
        agendamento.endereco = endereco
        agendamento.tipos_residuos = ', '.join(tipos_residuos)
        agendamento.save()
        messages.success(request, 'Agendamento atualizado com sucesso!')
        return redirect('agendamentos:ver_agendamentos_usuario')

    return render(request, 'agendamentos/editar_agendamento.html', {'agendamento': agendamento})

@login_required
def editar_etapa_agendamento(request, agendamento_id):
    agendamento = get_object_or_404(Agendamento, id=agendamento_id)

    # Verificar se o usuário é dono da empresa do agendamento
    if agendamento.empresa != request.user:
        messages.error(request, 'Você não tem permissão para editar a etapa deste agendamento.')
        return redirect('agendamentos:ver_agendamentos_empresa', id=agendamento.empresa.id)

    if request.method == 'POST':
        nova_etapa = request.POST.get('etapa')

        # Validar se a etapa está entre as permitidas
        if nova_etapa in ['solicitacao', 'coleta', 'triagem', 'transformacao', 'realocacao']:
            agendamento.etapa = nova_etapa
            agendamento.save()
            messages.success(request, 'Etapa do agendamento atualizada com sucesso!')
        else:
            messages.error(request, 'Etapa inválida.')

        # Redireciona para a lista de agendamentos da empresa, usando o ID correto da empresa
        return redirect('agendamentos:ver_agendamentos_empresa', id=agendamento.empresa.id)

    return render(request, 'agendamentos/editar_etapa_agendamento.html', {'agendamento': agendamento})




from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from .models import CentroColeta

@login_required
def cadastrar_centro(request):
    if request.method == 'POST':
        nome = request.POST.get('nome', '').strip()
        telefone = request.POST.get('telefone', '').strip()
        endereco = request.POST.get('endereco', '').strip()
        numero = request.POST.get('numero', '').strip()
        complemento = request.POST.get('complemento', '').strip()
        cep = request.POST.get('cep', '').strip()
        tipos = request.POST.getlist('tipos')
        horario_abertura = request.POST.get('horario_abertura', '').strip()
        horario_fechamento = request.POST.get('horario_fechamento', '').strip()

        # Validações básicas
        errors = []

        if not nome:
            errors.append("O campo 'Nome' é obrigatório.")
        if not telefone:
            errors.append("O campo 'Telefone' é obrigatório.")
        if not endereco:
            errors.append("O campo 'Endereço' é obrigatório.")
        if not cep:
            errors.append("O campo 'CEP' é obrigatório.")
        if not tipos:
            errors.append("Selecione ao menos um tipo de material.")
        if not horario_abertura or not horario_fechamento:
            errors.append("Os campos 'Horário de Abertura' e 'Horário de Fechamento' são obrigatórios.")

        # Caso não haja erros, salvar o centro
        if not errors:
            try:
                centro = CentroColeta(
                    nome=nome,
                    telefone=telefone,
                    endereco=endereco,
                    numero=numero,
                    complemento=complemento,
                    cep=cep,
                    tipos=','.join(tipos),  # Verifique se o modelo aceita string de tipos
                    horario_abertura=horario_abertura,
                    horario_fechamento=horario_fechamento,
                    usuario_responsavel=request.user
                )
                centro.full_clean()  # Verifica a validade dos campos
                centro.save()
                return redirect('centros:lista_centros')  # Redirecionar para a lista de centros
            except ValidationError as e:
                errors.extend(e.messages)
                print(e.messages)  # Exibe os erros de validação

        return render(request, 'centros/cadastrar_centro.html', {
            'errors': errors,
            'form_data': request.POST  # Repassa os dados inseridos pelo usuário
        })

    return render(request, 'centros/cadastrar_centro.html')

@login_required
def lista_centros(request):
    centros = CentroColeta.objects.all()
    # Processar os tipos para cada centro
    for centro in centros:
        centro.tipos_lista = [tipo.strip() for tipo in centro.tipos.split(",")] if centro.tipos else []
    return render(request, 'centros/lista_centros.html', {'centros': centros})


@login_required
def remover_centro(request, centro_id):
    try:
        centro = CentroColeta.objects.get(id=centro_id, usuario_responsavel=request.user)
        if request.method == 'POST':
            centro.delete()
            return redirect('centros:lista_centros')
    except CentroColeta.DoesNotExist:
        return render(request, 'centros/centro_nao_cadastrado.html')
    return render(request, 'centros/remover_centro.html', {'centro': centro})

@login_required
def atualizar_centro(request, centro_id):
    # Obtendo o centro de coleta específico
    centro = get_object_or_404(CentroColeta, id=centro_id, usuario_responsavel=request.user)

    if request.method == 'POST':
        # Obter os dados enviados pelo formulário
        nome = request.POST.get('nome')
        endereco = request.POST.get('endereco')
        telefone = request.POST.get('telefone')

        # Validar se os campos não estão vazios
        if nome and endereco and telefone:
            # Atualizar os dados do centro de coleta
            centro.nome = nome
            centro.endereco = endereco
            centro.telefone = telefone
            centro.save()

            # Redirecionar para a página de lista de centros após salvar
            return redirect('centros:lista_centros')
        else:
            # Adicionar uma mensagem de erro, se necessário
            error_message = "Todos os campos são obrigatórios."
            return render(request, 'centros/atualizar_centro.html', {'centro': centro, 'error_message': error_message})

    return render(request, 'centros/atualizar_centro.html', {'centro': centro})
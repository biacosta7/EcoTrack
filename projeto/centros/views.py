from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from .models import CentroColeta
from django.contrib import messages
from django.http import JsonResponse

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
        latitude = request.POST.get('latitude', '').strip()
        longitude = request.POST.get('longitude', '').strip()

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
        if not latitude:
            errors.append('O campo latitude é obrigatório')
        if not longitude:
            errors.append('O campo longitude é obrigatório')
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
                    usuario_responsavel=request.user,
                    latitude = latitude,
                    longitude = longitude,
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
    """View para atualizar um Centro de Coleta."""
    try:
        # Tenta obter o Centro de Coleta ou retorna None se não existir
        centro = CentroColeta.objects.get(id=centro_id)

        if request.method == 'POST':
            # Aqui ficaria o código para processar o formulário de atualização (se necessário)
            centro.nome = request.POST.get('nome')
            centro.endereco = request.POST.get('endereco')
            # Suponha que você atualiza outros campos como necessário
            centro.save()
            messages.success(request, 'Ponto de coleta atualizado com sucesso.')
            return redirect('centros:lista_centros')

        return render(request, 'centros/atualizar_centro.html', {'centro': centro})

    except CentroColeta.DoesNotExist:
        # Adiciona uma mensagem de erro se o Centro não for encontrado
        messages.error(request, 'Ponto de coleta não existente.')
        return redirect('centros:lista_centros')

def localizar_centros(request):
    centros = CentroColeta.objects.all() 
    return render(request, 'centros/localizar_centros.html', {'centros': centros})

def pontos_de_coleta(request):
    # Consulta todos os centros de coleta registrados
    centros = CentroColeta.objects.all()

    # Cria uma lista com os dados que serão enviados ao frontend
    pontos_data = [
        {
            'nome': centro.nome,
            'latitude': centro.latitude,  # Certifique-se de ter campos de latitude e longitude no seu modelo
            'longitude': centro.longitude,  # Se não tiver, você pode precisar adicionar essas coordenadas no modelo
            'endereco': centro.endereco,
        }
        for centro in centros
    ]

    # Retorna a lista como uma resposta JSON
    return JsonResponse({'pontos': pontos_data})
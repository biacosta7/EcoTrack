from django.shortcuts import render, redirect, get_object_or_404
from math import radians, sin, cos, sqrt, atan2
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from .models import CentroColeta
from django.contrib import messages
from django.http import JsonResponse
import requests
from django.conf import settings
from decimal import Decimal


OPENCAGE_API_KEY = settings.OPENCAGE_API_KEY
def geocode_address(address):
    url = "https://api.opencagedata.com/geocode/v1/json"
    params = {
        'q': address,
        'key': OPENCAGE_API_KEY,
        'language': 'pt',
        'countrycode': 'br'
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        if data['results']:
            location = data['results'][0]['geometry']
            lat = round(location['lat'], 6)
            lng = round(location['lng'], 6)
            lat = Decimal(f"{lat:.6f}")
            lng = Decimal(f"{lng:.6f}")
            return lat, lng
            
        else:
            print(f"No results found for address: {address}")
            return None, None
    except requests.RequestException as e:
        print(f"Error during geocoding request: {e}")
        return None, None
    except (KeyError, IndexError) as e:
        print(f"Error parsing geocoding response: {e}")
        return None, None

@login_required
def cadastrar_centro(request):
    if not hasattr(request.user, 'is_company') or not request.user.is_company:
        return HttpResponseForbidden("Apenas usuários do tipo 'Empresa' podem cadastrar centros de coleta.")

    if request.method == 'POST':
        form_data = {
            'nome': request.POST.get('nome', '').strip(),
            'telefone': request.POST.get('telefone', '').strip(),
            'endereco': request.POST.get('endereco', '').strip(),
            'numero': request.POST.get('numero', '').strip(),
            'complemento': request.POST.get('complemento', '').strip(),
            'cep': request.POST.get('cep', '').strip(),
            'tipos': request.POST.getlist('tipos'),
            'horario_abertura': request.POST.get('horario_abertura', '').strip(),
            'horario_fechamento': request.POST.get('horario_fechamento', '').strip(),
        }

        errors = []

        # Validate required fields
        required_fields = [
            ('nome', "O campo 'Nome' é obrigatório."),
            ('telefone', "O campo 'Telefone' é obrigatório."),
            ('endereco', "O campo 'Endereço' é obrigatório."),
            ('cep', "O campo 'CEP' é obrigatório."),
            ('horario_abertura', "O campo 'Horário de Abertura' é obrigatório."),
            ('horario_fechamento', "O campo 'Horário de Fechamento' é obrigatório."),
        ]
        
        for field, error_message in required_fields:
            if not form_data[field]:
                errors.append(error_message)

        if not form_data['tipos']:
            errors.append("Selecione ao menos um tipo de material.")

        # Geocode address only if there are no errors in required fields
        if not errors:
            full_address = f"{form_data['endereco']}, {form_data['numero']}, {form_data['cep']}"
            latitude, longitude = geocode_address(full_address)
            if latitude is None or longitude is None:
                errors.append("Não foi possível obter as coordenadas para o endereço fornecido.")
            else:
                form_data['latitude'] = round(latitude, 6)
                form_data['longitude'] = round(longitude, 6)

        # If there are no errors, try to save the center
        if not errors:
            try:
                centro = CentroColeta(
                    nome=form_data['nome'],
                    telefone=form_data['telefone'],
                    endereco=form_data['endereco'],
                    numero=form_data['numero'],
                    complemento=form_data['complemento'],
                    cep=form_data['cep'],
                    tipos=','.join(form_data['tipos']),
                    horario_abertura=form_data['horario_abertura'],
                    horario_fechamento=form_data['horario_fechamento'],
                    usuario_responsavel=request.user,
                    latitude=form_data['latitude'],  # Já em Decimal com 6 casas
                    longitude=form_data['longitude'],  # Já em Decimal com 6 casas
                )
                print(f"Latitude após arredondamento: {form_data['latitude']}")
                print(f"Longitude após arredondamento: {form_data['longitude']}")

                centro.full_clean()
                centro.save()
                return redirect('centros:lista_centros')
            except ValidationError as e:
                errors.extend(e.messages)
                print(f"Validation errors: {e.messages}")

        # If there are errors, render the form again with error messages
        return render(request, 'centros/cadastrar_centro.html', {
            'errors': errors,
            'form_data': form_data
        })

    # If it's a GET request, just render the empty form
    return render(request, 'centros/cadastrar_centro.html')

@login_required
def lista_centros(request):
    if not hasattr(request.user, 'is_company') or not request.user.is_company:
        return HttpResponseForbidden("Apenas usuários do tipo 'Empresa' podem visualizar centros de coleta.")
    # Filtra centros para mostrar apenas os criados pelo usuário logado
    centros = CentroColeta.objects.filter(usuario_responsavel=request.user)
    for centro in centros:
        centro.tipos_lista = [tipo.strip() for tipo in centro.tipos.split(",")] if centro.tipos else []
    return render(request, 'centros/lista_centros.html', {'centros': centros})

@login_required
def remover_centro(request, centro_id):
    if not hasattr(request.user, 'is_company') or not request.user.is_company:
        return HttpResponseForbidden("Apenas usuários do tipo 'Empresa' podem deletar centros de coleta.")
    try:
        # Verifica se o centro pertence ao usuário logado
        centro = CentroColeta.objects.get(id=centro_id, usuario_responsavel=request.user)
        if request.method == 'POST':
            centro.delete()
            return redirect('centros:lista_centros')
    except CentroColeta.DoesNotExist:
        return render(request, 'centros/centro_nao_cadastrado.html')
    return render(request, 'centros/remover_centro.html', {'centro': centro})

@login_required
def atualizar_centro(request, centro_id):
    if not hasattr(request.user, 'is_company') or not request.user.is_company:
        return HttpResponseForbidden("Apenas usuários do tipo 'Empresa' podem editar centros de coleta.")
    try:
        # Verifica se o centro pertence ao usuário logado
        centro = CentroColeta.objects.get(id=centro_id, usuario_responsavel=request.user)
        if request.method == 'POST':
            centro.nome = request.POST.get('nome')
            centro.endereco = request.POST.get('endereco')
            centro.numero = request.POST.get('numero')
            centro.complemento = request.POST.get('complemento')
            centro.cep = request.POST.get('cep')
            centro.telefone = request.POST.get('telefone')
            centro.tipos = ','.join(request.POST.getlist('tipos'))
            centro.horario_abertura = request.POST.get('horario_abertura')
            centro.horario_fechamento = request.POST.get('horario_fechamento')
            full_address = f"{centro.endereco}, {centro.numero}, {centro.cep}"
            latitude, longitude = geocode_address(full_address)
            if latitude is not None and longitude is not None:
                centro.latitude = round(latitude, 6)
                centro.longitude = round(longitude, 6)

            centro.save()
            messages.success(request, 'Ponto de coleta atualizado com sucesso.')
            return redirect('centros:lista_centros')

        return render(request, 'centros/atualizar_centro.html', {'centro': centro})

    except CentroColeta.DoesNotExist:
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

def haversine_distance(lat1, lon1, lat2, lon2):
    """Calcula a distância entre duas coordenadas (em quilômetros) usando a fórmula de Haversine."""
    R = 6371.0  # Raio da Terra em quilômetros
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c

@login_required
def calcular_distancia(request):
    if request.method == 'POST':
        user_address = request.POST.get('user_address')
        user_coords = geocode_address(user_address)

        if user_coords == (None, None):
            messages.error(request, "Endereço não encontrado. Tente novamente.")
            return render(request, 'centros/localizar_centros.html', {'user_address': user_address})

        user_lat, user_lon = user_coords
        centros = CentroColeta.objects.all()

        # Calcule a distância entre o endereço do usuário e cada centro
        centros_com_distancia = []
        for centro in centros:
            # Verifique se as coordenadas do centro são válidas
            if centro.latitude is not None and centro.longitude is not None:
                distancia = haversine_distance(user_lat, user_lon, Decimal(centro.latitude), Decimal(centro.longitude))
                centros_com_distancia.append({
                    'centro': centro,
                    'distancia': round(distancia, 2)  # Arredonda para 2 casas decimais
                })
            else:
                # Se as coordenadas não são válidas, adicione uma mensagem ou apenas ignore o centro
                centros_com_distancia.append({
                    'centro': centro,
                    'distancia': 'Coordenadas inválidas'
                })

        # Ordene os centros pela distância
        centros_com_distancia.sort(key=lambda x: x['distancia'] if isinstance(x['distancia'], float) else float('inf'))

        return render(request, 'centros/localizar_centros.html', {
            'centros_com_distancia': centros_com_distancia,
            'user_address': user_address
        })
    return render(request, 'centros/localizar_centros.html')

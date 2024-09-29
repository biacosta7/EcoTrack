from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.views import LoginView
from django.contrib import messages
from .models import User
from django.core.exceptions import ValidationError
from django.urls import reverse

def home_view(request):
    return render(request, 'home.html')

def is_admin(user):
    """
    Verifica se o usuário é um administrador.
    """
    return user.is_staff

@login_required
@user_passes_test(is_admin)
def user_list_view(request):
    """
    View para listar todos os usuários.
    Apenas administradores podem acessar.
    """
    users = User.objects.all()
    return render(request, 'users/user_list.html', {'users': users})

@login_required
@user_passes_test(is_admin)
def user_detail_view(request, id):
    """
    View para detalhar um usuário específico.
    Apenas administradores podem acessar.
    """
    user = get_object_or_404(User, id=id)
    return render(request, 'users/user_detail.html', {'user_detail': user})

@login_required
@user_passes_test(is_admin)
def user_delete_view(request, id):
    """
    View para deletar um usuário existente.
    Apenas administradores podem acessar.
    """
    user_obj = get_object_or_404(User, id=id)
    if request.method == 'POST':
        user_obj.delete()
        messages.success(request, "Usuário deletado com sucesso.")
        return redirect('user:listar_user')
    return render(request, 'users/user_confirm_delete.html', {'user_obj': user_obj})

def register_view(request):
    user_type = request.GET.get('type')
    if request.method == 'POST':
        nome_empresa = request.POST.get('nome_empresa')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        username = request.POST.get('username')
        endereco = request.POST.get('endereco')
        cep = request.POST.get('cep')
        errors = {}

        # Verificação de campos obrigatórios
        if user_type == 'company':
            if not nome_empresa:
                errors['nome_empresa'] = "O campo Nome da Empresa é obrigatório."
            if not email:
                errors['email'] = "O campo Email é obrigatório."
            if not password1:
                errors['password1'] = "O campo Senha é obrigatório."
            if not endereco:
                errors['endereco'] = "O campo Endereço é obrigatório."
            if not cep:
                errors['cep'] = "O campo CEP é obrigatório."
        else:
            if not username:
                errors['username'] = "O campo Nome de Usuário é obrigatório."
            if not email:
                errors['email'] = "O campo Email é obrigatório."
            if not password1:
                errors['password1'] = "O campo Senha é obrigatório."

        # Verificação se o email já está em uso
        if email and User.objects.filter(email=email).exists():
            errors['email'] = "Este e-mail já está em uso."

        # Verificação de senhas coincidentes
        if password1 and password2 and password1 != password2:
            errors['password'] = "As senhas não coincidem."

        # Se houver erros, renderizar novamente o template com as mensagens
        if errors:
            template_name = 'users/criar_empresa.html' if user_type == 'company' else 'users/criar_user.html'
            context = {
                'errors': errors,
                'nome_empresa_value': nome_empresa if user_type == 'company' else '',
                'username_value': username if user_type != 'company' else '',
                'email_value': email,
                'endereco_value': endereco,
                'cep_value': cep,
                'form_action': request.path,
                'csrf_token': request.COOKIES.get('csrftoken'),
            }
            return render(request, template_name, context)

        # Criar o usuário
        user = User(
            email=email,
            is_company=True if user_type == 'company' else False,
            nome_empresa=nome_empresa if user_type == 'company' else None,
            username=username if user_type != 'company' else None,
            endereco=endereco if user_type == 'company' else None,
            cep=cep if user_type == 'company' else None,
        )
        user.set_password(password1)
        user.save()

        messages.success(request, "Registro realizado com sucesso.")

        # Redirecionar com base no tipo de usuário
        if user_type == 'company':
            return redirect('user:empresa_dashboard')  # Redireciona para o dashboard da empresa
        else:
            return redirect('user:usuario_dashboard')  # Redireciona para o dashboard do usuário comum

    # Renderiza o formulário de registro
    else:
        template_name = 'users/criar_empresa.html' if user_type == 'company' else 'users/criar_user.html'
        context = {
            'form_action': request.path,
            'csrf_token': request.COOKIES.get('csrftoken'),
            'title': 'Registrar como Empresa' if user_type == 'company' else 'Registrar como Usuário Comum',
        }
        return render(request, template_name, context)

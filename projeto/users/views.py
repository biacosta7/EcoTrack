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
    return render(request, 'users/listar_user.html', {'users': users})

@login_required
def user_detail_view(request, id):
    """
    View para detalhar um usuário específico.
    Apenas administradores podem acessar.
    """
    # Obtém o usuário específico pelo ID, ou retorna 404 se não existir
    user_detail = get_object_or_404(User, id=id)

    # Contexto a ser passado para o template
    context = {
        'user': request.user,  # O usuário que está autenticado
        'user_detail': user_detail  # O usuário que está sendo detalhado
    }
    print(f"User: {request.user}, ID: {id}")
    return render(request, 'users/detail_user.html', context)

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
        user_type = request.POST.get('user_type')  # Obter o tipo de usuário do POST também
        nome_empresa = request.POST.get('nome_empresa')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        nome = request.POST.get('nome')
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
            if not nome:
                errors['nome'] = "O campo Nome de Usuário é obrigatório."
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
                'user_type': user_type,
                'nome_empresa_value': nome_empresa if user_type == 'company' else '',
                'nome_value': nome if user_type != 'company' else '',
                'email_value': email,
                'endereco_value': endereco if user_type == 'company' else '',
                'cep_value': cep if user_type == 'company' else '',
                'form_action': request.path,
                'csrf_token': request.COOKIES.get('csrftoken'),
            }
            return render(request, template_name, context)

        # Criar o usuário
        user = User(
            email=email,
            is_company=(user_type == 'company'),
            nome_empresa=nome_empresa if user_type == 'company' else None,
            nome=nome if user_type != 'company' else None,
            endereco_empresa=endereco if user_type == 'company' else None,
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
            'user_type': user_type,
        }
        return render(request, template_name, context)

class CustomLoginView(LoginView):
    template_name = 'users/login.html'

    def get_redirect_url(self):
        user = self.request.user
        if user.is_authenticated:
            if hasattr(user, 'is_company') and user.is_company:
                return reverse('user:empresa_dashboard')
            else:
                return reverse('user:usuario_dashboard')
        return super().get_redirect_url()
    

@login_required
def usuario_dashboard_view(request):
    """
    Dashboard para o usuário comum.
    Apenas usuários autenticados podem acessar.
    """
    context = {
        'user': request.user,
        'user_id': request.user.id,
    }
    return render(request, 'users/dashboard_user.html', context)

@login_required
def empresa_dashboard_view(request):
    """
    Dashboard para empresas.
    Apenas usuários autenticados podem acessar.
    """

    context = {
        'user': request.user,
        'user_id': request.user.id,
    }
    return render(request, 'users/dashboard_empresa.html', context)

def confirmacao_view(request):
    return render(request, 'agendamentos/confirmacao.html')


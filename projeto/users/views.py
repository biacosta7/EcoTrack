from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.views import LoginView
from django.contrib import messages
from .models import User, Recompensa
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
        'user_detail': user_detail,  # O usuário que está sendo detalhado
        'pontuacao': user_detail.pontuacao  # Inclui a pontuação
    }
    print(f"User: {request.user}, ID: {id}, Pontuação: {user_detail.pontuacao}")
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
        try:
            user.save()
            messages.success(request, "Registro realizado com sucesso.")
        except Exception as e:
            messages.error(request, "Erro ao realizar registro.")

        # Redirecionar com base no tipo de usuário
        # if user_type == 'company':
        #     return redirect('user:empresa_dashboard')  # Redireciona para o dashboard da empresa
        # else:
        #     return redirect('user:usuario_dashboard')  # Redireciona para o dashboard do usuário comum
        return redirect('user:login')

    # Renderiza o formulário de registro
    else:
        template_name = 'users/criar_empresa.html' if user_type == 'company' else 'users/criar_user.html'
        context = {
            'form_action': request.path,
            'csrf_token': request.COOKIES.get('csrftoken'),
            'title': 'Registrar como Empresa' if user_type == 'company' else 'Registrar como Usuário',
            'user_type': user_type,
        }
        return render(request, template_name, context)

class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    
    # def get(self, request, *args, **kwargs):
    #     if 'next' in request.GET:
    #         messages.error(request, "Você precisa estar autenticado para acessar esta página.")
    #     return super().get(request, *args, **kwargs)
    
    def form_invalid(self, form):
        # Quando o formulário de login for inválido, exibe uma mensagem de erro.
        messages.error(self.request, "Email ou senha inválidos.")
        return super().form_invalid(form)

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
        'empresa': request.user,
        'user_id': request.user.id,
    }
    return render(request, 'users/dashboard_empresa.html', context)

@login_required
def recompensas_view(request):
    """
    View para exibir recompensas e ranking de usuários.
    Apenas usuários autenticados podem acessar.
    """
    user = request.user

    # Verifica se o usuário tem mais de 0 pontos
    if user.pontuacao <= 0:
        messages.warning(request, "Você não possui pontos suficientes para acessar recompensas.")
        return redirect('user:usuario_dashboard')

    # Obtém todas as recompensas disponíveis
    recompensas = Recompensa.objects.filter(disponivel=True)

    # Obtém o ranking dos usuários comuns com mais pontos
    ranking = User.objects.filter(is_company=False).order_by('-pontuacao')[:10]

    context = {
        'recompensas': recompensas,
        'ranking': ranking,
        'pontuacao': user.pontuacao,
    }
    return render(request, 'users/recompensas.html', context)
@login_required
def trocar_recompensa_view(request, recompensa_id):
    """
    View para processar a troca de recompensa.
    Apenas usuários autenticados podem acessar.
    """
    user = request.user
    recompensa = get_object_or_404(Recompensa, id=recompensa_id)

    # Verifica se o usuário tem pontos suficientes
    if user.pontuacao >= recompensa.custo:
        user.pontuacao -= recompensa.custo
        user.save()
        messages.success(request, f"Você trocou {recompensa.nome} com sucesso!")
    else:
        messages.warning(request, "Você não possui pontos suficientes para esta recompensa.")

    return redirect('user:recompensas')


def confirmacao_view(request):
    return render(request, 'agendamentos/confirmacao.html')

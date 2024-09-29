from django.contrib.auth.models import AbstractUser, UserManager as BaseUserManager
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("O email deve ser fornecido.")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    """
    Modelo de usuario personalizado para diferenciar entre usuarios comuns e empresas.
    """
    username = None  # Remove o campo username
    email = models.EmailField(unique=True, blank=False, help_text="Endereço de e-mail do usuário.")

    is_company = models.BooleanField(default=False, help_text="Designa se o usuário é uma empresa.")
    
    # Campos adicionais para empresas
    nome_empresa = models.CharField(max_length=255, blank=True, null=True, help_text="Nome da empresa.")
    endereco_empresa = models.CharField(max_length=500, blank=True, null=True, help_text="Endereço da empresa.")
    telefone_empresa = models.CharField(max_length=20, blank=True, null=True, help_text="Telefone da empresa.")
    cep = models.CharField(max_length=20, blank=True, null=True, help_text="CEP do usuário ou da empresa.")
    # Campos obrigatorios para usuarios comuns
    nome = models.CharField(max_length=30, help_text="Nome do usuário.", null=True)  # Nome obrigatorio
    sobrenome = models.CharField(max_length=30, blank=False, help_text="Sobrenome do usuário.")  # Nome obrigatorio
    telefone = models.CharField(max_length=20, blank=True, null=True, help_text="Telefone do usuário.")


    # Solução do erro: adicionar related_name nos campos de grupos e permissões
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',  # Adicionando related_name para evitar conflito
        blank=True,
        help_text='Os grupos aos quais este usuário pertence.'
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions_set',  # Adicionando related_name para evitar conflito
        blank=True,
        help_text='Permissões específicas para este usuário.'
    )

    objects = UserManager()

    # Definindo o e-mail como campo de login
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        if self.is_company:
            return f"Empresa: {self.nome_empresa} ({self.email})"
        return self.email

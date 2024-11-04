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
    username = None  # Remove o campo username
    email = models.EmailField(unique=True, blank=False, help_text="Endereço de e-mail do usuário.")
    is_company = models.BooleanField(default=False, help_text="Designa se o usuário é uma empresa.")
    pontuacao = models.IntegerField(default=0, help_text="Pontuação acumulada por reciclagem de resíduos.")
    nome_empresa = models.CharField(max_length=255, blank=True, null=True, help_text="Nome da empresa.")
    endereco_empresa = models.CharField(max_length=500, blank=True, null=True, help_text="Endereço da empresa.")
    telefone_empresa = models.CharField(max_length=20, blank=True, null=True, help_text="Telefone da empresa.")
    cep = models.CharField(max_length=20, blank=True, null=True, help_text="CEP do usuário ou da empresa.")
    nome = models.CharField(max_length=30, help_text="Nome do usuário.", null=True)  # Nome obrigatório
    sobrenome = models.CharField(max_length=30, blank=False, help_text="Sobrenome do usuário.")  # Nome obrigatório
    telefone = models.CharField(max_length=20, blank=True, null=True, help_text="Telefone do usuário.")

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True,
        help_text='Os grupos aos quais este usuário pertence.'
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions_set',
        blank=True,
        help_text='Permissões específicas para este usuário.'
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        if self.is_company:
            return f"Empresa: {self.nome_empresa} ({self.email})"
        return self.email

class Recompensa(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    custo = models.PositiveIntegerField()  # Custo em pontos
    disponivel = models.BooleanField(default=True)

    def __str__(self):
        return self.nome

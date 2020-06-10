#-*- coding: utf-8 -*-
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import ugettext_lazy as _
from config.settings import MEDIA_URL, STATIC_URL

# Create your models here.

GENERO_CHOICES = (
    (0, "Masculino"),
    (1, "Femenino"),
)

class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

#User
class User(AbstractUser):
    """User model."""
    username = None
    email = models.EmailField(_('email address'), unique=True)
    image = models.ImageField("Foto", upload_to='miembros/%Y/%m/%d', help_text="Foto del usuario. Opcional.", null=True, blank=True)

    # Foto - obtener ruta absoluta
    def get_image(self):
        if self.image:
            return '{}{}'.format(MEDIA_URL, self.image)
        return '{}{}'.format(STATIC_URL, 'img/empty.png')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

#Profile del User
class UserProfile(models.Model):
    class Meta:
        db_table = 'user_profile'
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    nota = models.TextField(max_length=500, blank=True)
    sexo = models.IntegerField(choices=GENERO_CHOICES)



    #Función Saludo
    def greet(self):
        if self.sexo == 'Masculino':
            return 'Hola, Chico'
        else:
            return 'Hola, Chica'

    def __str__(self):
        return self.user.first_name

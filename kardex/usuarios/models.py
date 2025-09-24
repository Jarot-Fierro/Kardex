from django.contrib.auth.models import AbstractUser
from django.db import models

from kardex.choices import TIPO_PERFIL
from kardex.models import Comuna


class UsuarioPersonalizado(AbstractUser):
    rut = models.CharField(max_length=100, unique=True, null=False, verbose_name='Rut')
    tipo_perfil = models.CharField(max_length=50, choices=TIPO_PERFIL, default='DERIVA', null=True, blank=True)

    comuna = models.ForeignKey(Comuna, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.username

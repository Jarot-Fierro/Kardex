from django.contrib.auth.models import AbstractUser
from django.db import models

from kardex.choices import TIPO_PERFIL
from kardex.models import Comuna, Establecimiento


class UsuarioPersonalizado(AbstractUser):
    comuna = models.ForeignKey(Comuna, on_delete=models.SET_NULL, null=True, blank=True)
    establecimiento = models.ForeignKey(Establecimiento, on_delete=models.SET_NULL, null=True, blank=True)

    tipo_perfil = models.CharField(max_length=50, choices=TIPO_PERFIL, default='DERIVA', null=True, blank=True)

    def __str__(self):
        return self.username

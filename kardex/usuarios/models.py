from django.contrib.auth.models import AbstractUser
from django.db import models

from kardex.choices import TIPO_PERFIL


class UsuarioPersonalizado(AbstractUser):
    rut = models.CharField(max_length=100, unique=True, null=False, verbose_name='Rut')
    tipo_perfil = models.CharField(max_length=50, choices=TIPO_PERFIL, default='DERIVA', null=True, blank=True)

    establecimiento = models.ForeignKey('kardex.Establecimiento', on_delete=models.PROTECT, null=True, blank=True,
                                        verbose_name='Establecimiento'
                                        )

    def __str__(self):
        return self.username

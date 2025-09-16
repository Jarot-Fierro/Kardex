from django.db import models

from config.abstract import StandardModel
from kardex.choices import TIPO_USUARIO


class Profesional(StandardModel):
    rut = models.CharField(max_length=100, unique=True, null=False, verbose_name='R.U.T.')
    nombres = models.CharField(max_length=100, unique=True, null=False, verbose_name='Nombre')
    correo = models.EmailField(max_length=100, unique=True, null=False, verbose_name='Correo')
    telefono = models.CharField(max_length=15, unique=True, verbose_name='Teléfono')
    tipo_usuario = models.CharField(max_length=100, choices=TIPO_USUARIO, default='ADMINISTRATIVE',
                                    verbose_name='Tipo de Usuario')

    establecimiento = models.ForeignKey('kardex.Establecimiento', null=True, blank=True, on_delete=models.DO_NOTHING,
                                        verbose_name='Establecimiento')

    def __str__(self):
        return self.nombres

    class Meta:
        verbose_name = 'Profesional'
        verbose_name_plural = 'Profesionales'

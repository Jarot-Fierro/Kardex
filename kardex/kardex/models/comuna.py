from django.db import models

from config.abstract import StandardModel


class Comuna(StandardModel):
    nombre = models.CharField(max_length=100, unique=True, null=False, verbose_name='Nombre')
    codigo = models.CharField(max_length=200, verbose_name='Código de Comuna')

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Comuna'
        verbose_name_plural = 'Comunas'

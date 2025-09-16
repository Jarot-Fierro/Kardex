from django.db import models

from config.abstract import StandardModel


class Prevision(StandardModel):
    nombre = models.CharField(max_length=100, unique=True, null=False, verbose_name='Nombre')

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Prevision'
        verbose_name_plural = 'Previsiones'

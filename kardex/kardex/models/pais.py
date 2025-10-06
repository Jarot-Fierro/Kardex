from django.db import models
from simple_history.models import HistoricalRecords

from config.abstract import StandardModel


class Pais(StandardModel):
    nombre = models.CharField(max_length=100, unique=True, null=False, verbose_name='Nombre del País')
    cod_pais = models.CharField(max_length=10, unique=True, null=False, verbose_name='Código del País')

    history = HistoricalRecords()

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'País'
        verbose_name_plural = 'Países'

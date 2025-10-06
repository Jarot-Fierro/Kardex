from django.db import models
from simple_history.models import HistoricalRecords

from config.abstract import StandardModel


class Profesion(StandardModel):
    nombre = models.CharField(max_length=100, unique=True, null=False, verbose_name='Nombre')

    history = HistoricalRecords()

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Profesion'
        verbose_name_plural = 'Profesiones'

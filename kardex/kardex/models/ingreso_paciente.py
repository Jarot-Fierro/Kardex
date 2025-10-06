from django.db import models
from simple_history.models import HistoricalRecords

from config.abstract import StandardModel


class IngresoPaciente(StandardModel):
    paciente = models.ForeignKey('kardex.Paciente', on_delete=models.PROTECT, null=False,
                                 verbose_name='Paciente')

    establecimiento = models.ForeignKey('kardex.Establecimiento', on_delete=models.PROTECT, null=False,
                                        verbose_name='Establecimiento')

    history = HistoricalRecords()

    def __str__(self):
        return self.paciente.codigo

    class Meta:
        verbose_name = 'Ingreso de Paciente'
        verbose_name_plural = 'Ingresos de Pacientes'

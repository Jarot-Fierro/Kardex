from django.db import models

from config.abstract import StandardModel


class IngresoPaciente(StandardModel):
    fecha_ingreso = models.DateField(auto_now_add=True, verbose_name='Fecha de Ingreso')
    motivo_ingreso = models.TextField(null=True, blank=True, verbose_name='Motivo de Ingreso')
    diagnostico_ingreso = models.TextField(null=True, blank=True, verbose_name='Diagnóstico de Ingreso')
    estado_actual = models.TextField(null=True, blank=True, verbose_name='Estado Actual')
    fecha_egreso = models.DateField(null=True, blank=True, verbose_name='Fecha de Egreso')

    paciente = models.ForeignKey('kardex.Paciente', on_delete=models.PROTECT, null=False,
                                 verbose_name='Paciente')

    def __str__(self):
        return self.paciente.rut

    class Meta:
        verbose_name = 'Ingreso de Paciente'
        verbose_name_plural = 'Ingresos de Pacientes'

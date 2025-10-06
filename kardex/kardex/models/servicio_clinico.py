from django.db import models
from simple_history.models import HistoricalRecords

from config.abstract import StandardModel


class ServicioClinico(StandardModel):
    nombre = models.CharField(max_length=100, unique=True, null=False, verbose_name='Nombre')
    tiempo_horas = models.IntegerField(null=False, verbose_name='Tiempo en horas')
    correo_jefe = models.EmailField(max_length=100, null=False, verbose_name='Correo del jefe a cargo')
    telefono = models.CharField(max_length=15, verbose_name='Teléfono')

    establecimiento = models.ForeignKey('kardex.Establecimiento', null=True, blank=True, on_delete=models.SET_NULL,
                                        verbose_name='Establecimiento')

    history = HistoricalRecords()

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Servicio Clínico'
        verbose_name_plural = 'Servicios Clínicos'

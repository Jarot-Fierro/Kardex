from django.db import models

from config.abstract import StandardModel


class ClinicalService(StandardModel):
    name = models.CharField(max_length=100, unique=True, null=False, verbose_name='Nombre')
    time_hours = models.IntegerField(null=False, verbose_name='Tiempo en horas')
    email = models.EmailField(max_length=100, unique=True, null=False, verbose_name='Correo del jefe a cargo')
    phone = models.CharField(max_length=15, unique=True, verbose_name='Teléfono')

    establishment = models.ForeignKey('kardex.Establishment', null=True, blank=True, on_delete=models.DO_NOTHING,
                                      verbose_name='Establecimiento')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Servicio Clínico'
        verbose_name_plural = 'Servicios Clínicos'

from django.db import models

from config.abstract import StandardModel


class Establishment(StandardModel):
    name = models.CharField(max_length=100, unique=True, null=False, verbose_name='Nombre')
    address = models.CharField(max_length=200, verbose_name='Dirección')
    phone = models.CharField(max_length=15, verbose_name='Teléfono')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Establecimiento'
        verbose_name_plural = 'Establecimientos'

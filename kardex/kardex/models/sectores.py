from django.db import models
from simple_history.models import HistoricalRecords

from config.abstract import StandardModel
from kardex.choices import SECTOR_COLORS


class Sector(StandardModel):
    codigo = models.CharField(null=True, blank=True, verbose_name='Código del Sector', max_length=100)
    color = models.CharField(null=True, blank=True, verbose_name='Color del Sector', max_length=100)
    observacion = models.TextField(null=True, blank=True, choices=SECTOR_COLORS, verbose_name='Observaciones')
    establecimiento = models.ForeignKey('kardex.Establecimiento', on_delete=models.PROTECT, null=False,
                                        verbose_name='Establecimiento', related_name='sector_establecimiento')

    history = HistoricalRecords()

    def __str__(self):
        return self.codigo

    class Meta:
        verbose_name = 'Sector'
        verbose_name_plural = 'Sectores'

from django.db import models

from config.abstract import StandardModel


class Label(StandardModel):
    name = models.CharField(max_length=100, unique=True, null=False, verbose_name='Nombre')
    rut = models.CharField(max_length=100, unique=True, null=False, verbose_name='R.U.T.')
    rut2 = models.CharField(max_length=100, null=False, verbose_name='R.U.T. Provisorio')
    commune = models.ForeignKey('kardex.Commune', null=True, blank=True, on_delete=models.DO_NOTHING,
                                verbose_name='Comuna')
    establishment = models.ForeignKey('kardex.Establishment', null=True, blank=True, on_delete=models.DO_NOTHING,
                                      verbose_name='Establecimiento')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Etiqueta'
        verbose_name_plural = 'Etiquetas'

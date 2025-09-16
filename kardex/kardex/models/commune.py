from django.db import models

from config.abstract import StandardModel


class Commune(StandardModel):
    name = models.CharField(max_length=100, unique=True, null=False, verbose_name='Nombre')
    code = models.CharField(max_length=200, verbose_name='Código de Comuna')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Comuna'
        verbose_name_plural = 'Comunas'

from django.db import models

from config.abstract import StandardModel


class Profesional(StandardModel):
    rut = models.CharField(max_length=100, unique=True, null=False, verbose_name='R.U.T.')
    nombres = models.CharField(max_length=100, null=False, verbose_name='Nombre')
    correo = models.EmailField(max_length=100, unique=True, null=False, verbose_name='Correo')
    telefono = models.CharField(max_length=15, verbose_name='Teléfono')
    profesion = models.ForeignKey('kardex.Profesion', null=True, blank=True, on_delete=models.SET_NULL,
                                  verbose_name='Profesión')

    establecimiento = models.ForeignKey('kardex.Establecimiento', null=True, blank=True, on_delete=models.SET_NULL,
                                        verbose_name='Establecimiento')

    def __str__(self):
        return self.nombres

    class Meta:
        verbose_name = 'Profesional'
        verbose_name_plural = 'Profesionales'

from django.db import models

from config.abstract import StandardModel


class Ficha(StandardModel):
    rut2 = models.CharField(max_length=100, null=False, verbose_name='R.U.T. Provisorio')
    comuna = models.ForeignKey('kardex.Comuna', null=True, blank=True, on_delete=models.DO_NOTHING,
                               verbose_name='Comuna')
    establecimiento = models.ForeignKey('kardex.Establecimiento', null=True, blank=True, on_delete=models.DO_NOTHING,
                                        verbose_name='Establecimiento')

    usuario = models.ForeignKey('usuarios.UsuarioPersonalizado', on_delete=models.CASCADE, null=False,
                                verbose_name='Usuario')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Ficha'
        verbose_name_plural = 'Fichas'

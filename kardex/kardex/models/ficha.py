from django.db import models

from config.abstract import StandardModel


class Ficha(StandardModel):
    numero_ficha = models.IntegerField(verbose_name='Número de Ficha')
    observacion = models.TextField(null=True, blank=True, verbose_name='Observación')
    fecha_creacion = models.DateField(auto_now_add=True, verbose_name='Fecha de Creación')
    fecha_mov = models.DateField(null=True, blank=True, verbose_name='Fecha de Movimiento')

    establecimiento = models.ForeignKey('kardex.Establecimiento', null=True, blank=True, on_delete=models.DO_NOTHING,
                                        verbose_name='Establecimiento')

    usuario = models.ForeignKey('usuarios.UsuarioPersonalizado', on_delete=models.DO_NOTHING, null=False,
                                verbose_name='Usuario')
    profesional = models.ForeignKey('kardex.Profesional', on_delete=models.DO_NOTHING, null=True, blank=True,
                                    verbose_name='Profesional')

    paciente = models.ForeignKey('kardex.Paciente', on_delete=models.DO_NOTHING, null=True, blank=True,
                                 verbose_name='Paciente')

    def __str__(self):
        return self.numero_ficha

    class Meta:
        verbose_name = 'Ficha'
        verbose_name_plural = 'Fichas'

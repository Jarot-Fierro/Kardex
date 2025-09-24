from django.db import models

from config.abstract import StandardModel
from kardex.choices import ESTADO_RESPUESTA


class MovimientoFicha(StandardModel):
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creación')
    fecha_mov = models.DateTimeField(verbose_name='Fecha de Movimiento')
    fecha_salida = models.DateTimeField(null=True, blank=True, verbose_name='Fecha de Salida')
    fecha_entrada = models.DateTimeField(null=True, blank=True, verbose_name='Fecha de Entrada')
    observacion_entrada = models.TextField(null=True, blank=True, verbose_name='Observación de Entrada')
    observacion_salida = models.TextField(null=True, blank=True, verbose_name='Observación de Salida')
    usuario_entrega = models.CharField(max_length=100, null=True, blank=True, verbose_name='Usuario que Entrega')
    usuario_entrada = models.CharField(max_length=100, null=True, blank=True, verbose_name='Usuario que Entrada')
    estado_respuesta = models.CharField(max_length=50, choices=ESTADO_RESPUESTA,
                                        default='EN ESPERA', null=False, verbose_name='Estado de Respuesta')

    servicio_clinico = models.ForeignKey('kardex.ServicioClinico', null=False, on_delete=models.PROTECT,
                                         verbose_name='Servicio Clínico')
    ficha = models.ForeignKey('kardex.Ficha', null=True, blank=True, on_delete=models.PROTECT,
                              verbose_name='Ficha')
    usuario = models.ForeignKey('usuarios.UsuarioPersonalizado', null=True, blank=True, on_delete=models.PROTECT,
                                verbose_name='Usuario')

    def __str__(self):
        return f"Movimiento de Ficha #{self.ficha.id if self.ficha else 'N/A'}"

    class Meta:
        verbose_name = 'Movimiento Ficha'
        verbose_name_plural = 'Movimientos Fichas'

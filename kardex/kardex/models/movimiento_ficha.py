from django.db import models
from simple_history.models import HistoricalRecords

from config.abstract import StandardModel
from kardex.choices import ESTADO_RESPUESTA


class MovimientoFicha(StandardModel):
    fecha_envio = models.DateTimeField(null=True, blank=True, verbose_name='Fecha de Envío')
    fecha_recepcion = models.DateTimeField(null=True, blank=True, verbose_name='Fecha de Recepción')

    observacion_envio = models.TextField(null=True, blank=True, verbose_name='Observación de Envío')
    observacion_recepcion = models.TextField(null=True, blank=True, verbose_name='Observación de Recepción')

    estado_envio = models.CharField(max_length=50, choices=ESTADO_RESPUESTA,
                                    default='EN ESPERA', null=False, verbose_name='Estado de Envío')

    estado_recepcion = models.CharField(max_length=50, choices=ESTADO_RESPUESTA,
                                        default='EN ESPERA', null=False, verbose_name='Estado de Recepción')

    servicio_clinico_envio = models.ForeignKey('kardex.ServicioClinico', on_delete=models.PROTECT,
                                               verbose_name='Servicio Clínico de Envío',
                                               related_name='envios_desde_este_servicio',
                                               default=1
                                               )

    servicio_clinico_recepcion = models.ForeignKey('kardex.ServicioClinico', on_delete=models.PROTECT,
                                                   verbose_name='Servicio Clínico de Recepción',
                                                   related_name='recepciones_en_este_servicio',
                                                   default=1
                                                   )
    usuario_envio = models.ForeignKey('usuarios.UsuarioPersonalizado', null=True, blank=True, on_delete=models.PROTECT,
                                      verbose_name='Usuario', related_name='movimientos_enviados',
                                      default=1)

    usuario_recepcion = models.ForeignKey('usuarios.UsuarioPersonalizado', null=True, blank=True,
                                          on_delete=models.PROTECT,
                                          verbose_name='Usuario', related_name='movimientos_recepcionados',
                                          default=1)

    profesional_envio = models.ForeignKey('kardex.Profesional', null=True, blank=True, on_delete=models.PROTECT,
                                          verbose_name='Profesional', related_name='movimientos_enviados_profesionales',
                                          default=1)

    profesional_recepcion = models.ForeignKey('kardex.Profesional', null=True, blank=True, on_delete=models.PROTECT,
                                              verbose_name='Profesional',
                                              related_name='movimientos_recepcionados_profesionales',
                                              default=1)

    ficha = models.ForeignKey('kardex.Ficha', null=True, blank=True, on_delete=models.PROTECT,
                              verbose_name='Ficha')

    history = HistoricalRecords()

    def __str__(self):
        return f"Movimiento de Ficha #{self.ficha.id if self.ficha else 'N/A'}"

    class Meta:
        verbose_name = 'Movimiento Ficha'
        verbose_name_plural = 'Movimientos Fichas'

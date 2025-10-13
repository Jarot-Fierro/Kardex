from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from simple_history.models import HistoricalRecords

from config.abstract import StandardModel
from kardex.choices import ESTADO_RESPUESTA


class MovimientoFicha(StandardModel):
    fecha_envio = models.DateTimeField(null=True, blank=True, verbose_name='Fecha de Envío')
    fecha_recepcion = models.DateTimeField(null=True, blank=True, verbose_name='Fecha de Recepción')

    observacion_envio = models.TextField(null=True, blank=True, verbose_name='Observación de Envío')
    observacion_recepcion = models.TextField(null=True, blank=True, verbose_name='Observación de Recepción')

    estado_envio = models.CharField(max_length=50, choices=ESTADO_RESPUESTA,
                                    default='ENVIADO', null=True, blank=True, verbose_name='Estado de Envío')

    estado_recepcion = models.CharField(max_length=50, choices=ESTADO_RESPUESTA,
                                        default='EN ESPERA', null=True, blank=True, verbose_name='Estado de Recepción')

    servicio_clinico_envio = models.ForeignKey('kardex.ServicioClinico', on_delete=models.PROTECT,
                                               verbose_name='Servicio Clínico de Envío',
                                               related_name='envios_desde_este_servicio',
                                               null=True, blank=True,
                                               )

    servicio_clinico_recepcion = models.ForeignKey('kardex.ServicioClinico', on_delete=models.PROTECT,
                                                   verbose_name='Servicio Clínico de Recepción',
                                                   related_name='recepciones_en_este_servicio',
                                                   null=True, blank=True,
                                                   )
    usuario_envio = models.ForeignKey('usuarios.UsuarioPersonalizado', null=True, blank=True, on_delete=models.PROTECT,
                                      verbose_name='Usuario Envio', related_name='movimientos_enviados',
                                      )

    usuario_recepcion = models.ForeignKey('usuarios.UsuarioPersonalizado', null=True, blank=True,
                                          on_delete=models.PROTECT,
                                          verbose_name='Usuario Recepcion', related_name='movimientos_recepcionados',
                                          )

    profesional_envio = models.ForeignKey('kardex.Profesional', null=True, blank=True, on_delete=models.PROTECT,
                                          verbose_name='Profesional Envio',
                                          related_name='movimientos_enviados_profesionales',
                                          )

    profesional_recepcion = models.ForeignKey('kardex.Profesional', null=True, blank=True, on_delete=models.PROTECT,
                                              verbose_name='Profesional Recepcion',
                                              related_name='movimientos_recepcionados_profesionales',
                                              )

    ficha = models.ForeignKey('kardex.Ficha', null=True, blank=True, on_delete=models.PROTECT,
                              verbose_name='Ficha')

    history = HistoricalRecords()

    def clean(self):
        # servicios distintos
        if self.servicio_clinico_envio_id and self.servicio_clinico_recepcion_id and \
                self.servicio_clinico_envio_id == self.servicio_clinico_recepcion_id:
            raise ValidationError(
                {'servicio_clinico_recepcion': 'El servicio de recepción no puede ser igual al de envío.'})
        # no editar si ya está recibido
        if self.pk and self.estado_recepcion == 'RECIBIDO':
            # Permitir idempotencia al marcar recibido: si lo único que cambia es establecer precisamente
            # los campos de recepción desde vacío a sus valores definitivos, no bloquear.
            changed = []
            try:
                old = type(self).objects.get(pk=self.pk)
                tracked = ['fecha_envio', 'observacion_envio', 'estado_envio', 'servicio_clinico_envio',
                           'usuario_envio', 'profesional_envio',
                           'ficha', 'servicio_clinico_recepcion', 'observacion_recepcion', 'profesional_recepcion',
                           'fecha_recepcion', 'estado_recepcion', 'usuario_recepcion']
                for f in tracked:
                    if getattr(old, f) != getattr(self, f):
                        changed.append(f)
            except type(self).DoesNotExist:
                pass
            # Si el estado previo no era RECIBIDO, estamos marcando recepción ahora; no bloquear
            try:
                old_estado = type(self).objects.get(pk=self.pk).estado_recepcion
            except type(self).DoesNotExist:
                old_estado = None
            if changed and old_estado == 'RECIBIDO':
                raise ValidationError('No se puede editar un movimiento ya recibido.')

    def save(self, *args, **kwargs):
        creating = self.pk is None
        # Envío: set defaults and fecha_envio if missing
        if creating:
            if not self.estado_envio:
                self.estado_envio = 'ENVIADO'
            if not self.estado_recepcion:
                self.estado_recepcion = 'EN ESPERA'
            if self.fecha_envio is None:
                self.fecha_envio = timezone.now()
        else:
            # Si se completa recepción, actualizar estado
            if self.fecha_recepcion and self.estado_recepcion != 'RECIBIDO':
                self.estado_recepcion = 'RECIBIDO'
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Movimiento de Ficha #{self.ficha.id if self.ficha else 'N/A'}"

    class Meta:
        verbose_name = 'Movimiento Ficha'
        verbose_name_plural = 'Movimientos Fichas'

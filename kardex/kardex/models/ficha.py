from django.db import models
from simple_history.models import HistoricalRecords

from config.abstract import StandardModel


class Ficha(StandardModel):
    numero_ficha = models.IntegerField(unique=True, null=True, blank=True, verbose_name='Número de Ficha')
    observacion = models.TextField(null=True, blank=True, verbose_name='Observación')
    # fecha_mov = models.DateField(null=True, blank=True, verbose_name='Fecha de Movimiento')

    usuario = models.ForeignKey('usuarios.UsuarioPersonalizado', on_delete=models.PROTECT, null=True, blank=True,
                                verbose_name='Usuario')
    profesional = models.ForeignKey('kardex.Profesional', on_delete=models.PROTECT, null=True, blank=True,
                                    verbose_name='Profesional')

    ingreso_paciente = models.ForeignKey('kardex.IngresoPaciente', on_delete=models.PROTECT, null=True, blank=True,
                                         verbose_name='Paciente')

    history = HistoricalRecords()

    def __str__(self):
        # Retorna siempre una cadena segura para evitar errores en admin/renderizados
        num = self.numero_ficha
        try:
            num_str = str(int(num)).zfill(4) if num is not None else '(sin número)'
        except Exception:
            num_str = str(num) if num is not None else '(sin número)'
        try:
            ingreso = self.ingreso_paciente
            paciente = getattr(ingreso, 'paciente', None)
            establecimiento = getattr(ingreso, 'establecimiento', None)
            paciente_str = str(paciente) if paciente is not None else '(sin paciente)'
            est_str = str(establecimiento) if establecimiento is not None else '(sin establecimiento)'
            return f'Ficha {num_str} - {paciente_str} @ {est_str}'
        except Exception:
            return f'Ficha {num_str}'

    def save(self, *args, **kwargs):
        creating = self.pk is None
        super().save(*args, **kwargs)
        # Asignar número de ficha basado en el ID si aún no se ha asignado
        if creating and not self.numero_ficha:
            self.numero_ficha = self.pk
            super().save(update_fields=['numero_ficha'])

    class Meta:
        verbose_name = 'Ficha'
        verbose_name_plural = 'Fichas'

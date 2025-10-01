from django.db import models

from config.abstract import StandardModel


class Ficha(StandardModel):
    numero_ficha = models.IntegerField(unique=True, null=True, blank=True, verbose_name='Número de Ficha')
    observacion = models.TextField(null=True, blank=True, verbose_name='Observación')
    # fecha_mov = models.DateField(null=True, blank=True, verbose_name='Fecha de Movimiento')

    usuario = models.ForeignKey('usuarios.UsuarioPersonalizado', on_delete=models.PROTECT, null=False,
                                verbose_name='Usuario')
    profesional = models.ForeignKey('kardex.Profesional', on_delete=models.PROTECT, null=True, blank=True,
                                    verbose_name='Profesional')

    ingreso_paciente = models.ForeignKey('kardex.IngresoPaciente', on_delete=models.PROTECT, null=False,
                                         unique=True, verbose_name='Paciente')

    def save(self, *args, **kwargs):
        creating = self.pk is None
        super().save(*args, **kwargs)
        # Asignar número de ficha basado en el ID si aún no se ha asignado
        if creating and not self.numero_ficha:
            self.numero_ficha = self.pk
            super().save(update_fields=['numero_ficha'])

    def __str__(self):
        return str(self.numero_ficha).zfill(4)

    class Meta:
        verbose_name = 'Ficha'
        verbose_name_plural = 'Fichas'

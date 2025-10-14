from django.db import models
from simple_history.models import HistoricalRecords

from config.abstract import StandardModel


class Ficha(StandardModel):
    numero_ficha_sistema = models.IntegerField(unique=True, null=True, blank=True, verbose_name='Número de Ficha')
    numero_ficha_tarjeta = models.IntegerField(unique=True, null=True, blank=True,
                                               verbose_name='Número de Ficha Tarjeta')
    observacion = models.TextField(null=True, blank=True, verbose_name='Observación')

    usuario = models.ForeignKey('usuarios.UsuarioPersonalizado', on_delete=models.PROTECT, null=True, blank=True,
                                verbose_name='Usuario', related_name='fichas_usuarios')
    profesional = models.ForeignKey('kardex.Profesional', on_delete=models.PROTECT, null=True, blank=True,
                                    verbose_name='Profesional', related_name='fichas_profesionales')

    paciente = models.ForeignKey('kardex.Paciente', on_delete=models.PROTECT, null=True, blank=True,
                                 verbose_name='Paciente', related_name='fichas_pacientes')

    establecimiento = models.ForeignKey('kardex.Establecimiento', on_delete=models.PROTECT, null=True, blank=True,
                                        verbose_name='Establecimiento', related_name='fichas_establecimientos')

    history = HistoricalRecords()

    def __str__(self):
        num = self.numero_ficha_sistema

        numero = f"{num:04d}" if num is not None else "----"

        if self.paciente:
            nombre = self.paciente.nombre or ""
            ap_paterno = self.paciente.apellido_paterno or ""
            ap_materno = self.paciente.apellido_materno or ""
            codigo = self.paciente.codigo or ""

            nombre_completo = f"{nombre} {ap_paterno} {ap_materno}".strip()

            if nombre_completo.strip():
                return f"Ficha #{numero} - {nombre_completo}"
            else:
                return f"Ficha #{numero} - Código paciente: {codigo}"
        else:
            return f"Ficha #{numero} - Sin paciente"

    def save(self, *args, **kwargs):
        if self.pk is None:
            super().save(*args, **kwargs)
            if not self.numero_ficha:
                self.numero_ficha = self.pk
                super().save(update_fields=['numero_ficha'])
        else:
            super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Ficha'
        verbose_name_plural = 'Fichas'

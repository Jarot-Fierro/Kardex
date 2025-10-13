from django.core.exceptions import ValidationError
from django.db import models
from simple_history.models import HistoricalRecords

from config.abstract import StandardModel


class IngresoPaciente(StandardModel):
    paciente = models.ForeignKey('kardex.Paciente', on_delete=models.PROTECT, null=False,
                                 verbose_name='Paciente')

    establecimiento = models.ForeignKey('kardex.Establecimiento', on_delete=models.PROTECT, null=False,
                                        verbose_name='Establecimiento')

    history = HistoricalRecords()

    def clean(self):
        # Validar que no haya más de 5 registros para el paciente
        existing_records = IngresoPaciente.objects.filter(paciente=self.paciente)
        if self.pk:
            # Excluir el registro actual si es edición
            existing_records = existing_records.exclude(pk=self.pk)

        if existing_records.count() >= 5:
            raise ValidationError("Este paciente ya tiene el máximo de 5 ingresos.")

        # Validar que no exista un ingreso para el mismo establecimiento
        if existing_records.filter(establecimiento=self.establecimiento).exists():
            raise ValidationError(f"Este paciente ya tiene un ingreso registrado para {self.establecimiento}.")

    def save(self, *args, **kwargs):
        self.full_clean()  # Llama a clean antes de guardar
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Ingreso de Paciente'
        verbose_name_plural = 'Ingresos de Pacientes'
        unique_together = ('paciente', 'establecimiento')

from django.db import models


class StandardModel(models.Model):
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Ultima fecha de Actualizado')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creación')
    status = models.CharField(max_length=8, choices=[('ACTIVE', 'Activo'), ('INACTIVE', 'Inactivo')], default='ACTIVE',
                              verbose_name='Estado')

    class Meta:
        abstract = True
        ordering = ['created_at']

from django.db import models

from config.abstract import StandardModel

TYPE_USER = [
    ('DOCTOR', 'Medico'),
    ('ADMINISTRATIVE', 'Administrativo'),
    ('CLINICAL PROFESSIONAL', 'Profesional Clínico'),
    ('ADMIN', 'Administrador'),
    ('ADMINISTRATIVE FILE', 'Administrativo fichas')
]


class ProfesionalUser(StandardModel):
    rut = models.CharField(max_length=100, unique=True, null=False, verbose_name='R.U.T.')
    names = models.CharField(max_length=100, unique=True, null=False, verbose_name='Nombre')
    email = models.EmailField(max_length=100, unique=True, null=False, verbose_name='Correo')
    phone = models.CharField(max_length=15, unique=True, verbose_name='Teléfono')
    type_user = models.CharField(max_length=100, choices=TYPE_USER, default='ADMINISTRATIVE',
                                 verbose_name='Tipo de Usuario')

    establishment = models.ForeignKey('kardex.Establishment', null=True, blank=True, on_delete=models.DO_NOTHING,
                                      verbose_name='Establecimiento')

    def __str__(self):
        return self.names

    class Meta:
        verbose_name = 'Profesional'
        verbose_name_plural = 'Profesionales'

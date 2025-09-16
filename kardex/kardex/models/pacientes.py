from django.db import models

from config.abstract import StandardModel
from kardex.choices import ESTADO_CIVIL


class Paciente(StandardModel):
    rut = models.CharField(max_length=100, unique=True, null=False, verbose_name='R.U.T.')
    nombre = models.CharField(max_length=100, unique=True, null=False, verbose_name='Nombre')

    apellido_paterno = models.CharField(max_length=100, unique=True, null=False, verbose_name='Apellido Paterno')
    apellido_materno = models.CharField(max_length=100, unique=True, null=False, verbose_name='Apellido Materno')
    rut_madre = models.CharField(max_length=100, unique=True, null=True, blank=True, verbose_name='R.U.T. Madre')
    fecha_nacimiento = models.DateField(null=False, verbose_name='Fecha de Nacimiento')
    sexo = models.CharField(max_length=10, choices=[('MASCULINO', 'Masculino'), ('FEMENINO', 'Femenino')], null=False,
                            verbose_name='Sexo')
    estado_civil = models.CharField(max_length=20, choices=ESTADO_CIVIL, null=False, verbose_name='Estado Civil')

    nombres_pabre = models.CharField(max_length=100, verbose_name='Nombres del Padre', null=True, blank=True)
    nombres_madre = models.CharField(max_length=100, verbose_name='Nombres de la Madre', null=True, blank=True)
    nombre_pareja = models.CharField(max_length=100, verbose_name='Nombre de la Pareja', null=True, blank=True)

    direccion = models.CharField(max_length=200, verbose_name='Dirección', null=False)
    numero_telefono1 = models.CharField(max_length=15, verbose_name='Número de Teléfono', null=True, blank=True)
    numero_telefono2 = models.CharField(max_length=15, verbose_name='Número de Teléfono 2', null=True, blank=True)
    fecha_movimiento = models.DateField(auto_now=True, verbose_name='Fecha de Movimiento')
    pasaporte = models.CharField(max_length=50, unique=True, null=True, blank=True, verbose_name='Pasaporte')

    recien_nacido = models.BooleanField(default=False, verbose_name='Recién Nacido')
    extranjero = models.BooleanField(default=False, verbose_name='Extranjero')
    fallecido = models.BooleanField(default=False, verbose_name='Fallecido')
    fecha_fallecimiento = models.DateField(null=True, blank=True, verbose_name='Fecha de Fallecimiento')

    ocupacion = models.CharField(max_length=100, null=True, blank=True, verbose_name='Ocupación')
    representante_legal = models.CharField(max_length=100, null=True, blank=True, verbose_name='Representante Legal')
    nombre_social = models.CharField(max_length=100, null=True, blank=True, verbose_name='Nombre Social')

    comuna = models.ForeignKey('kardex.Comuna', on_delete=models.CASCADE, null=False, verbose_name='Comuna')
    prevision = models.ForeignKey('kardex.Prevision', on_delete=models.CASCADE, null=False, verbose_name='Previsión')

    usuario = models.ForeignKey('usuarios.UsuarioPersonalizado', on_delete=models.CASCADE, null=False,
                                verbose_name='Usuario')

    def __str__(self):
        return self.rut

    class Meta:
        verbose_name = 'Paciente'
        verbose_name_plural = 'Pacientes'

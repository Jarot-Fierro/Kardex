from django.db import models
from simple_history.models import HistoricalRecords

from config.abstract import StandardModel
from kardex.choices import ESTADO_CIVIL


class Paciente(StandardModel):
    # IDENTIFICACIÓN
    codigo = models.CharField(max_length=100, unique=True, null=True, blank=True, verbose_name='Código')
    rut = models.CharField(max_length=100, unique=True, null=True, blank=True, verbose_name='R.U.T.')
    nip = models.CharField(max_length=100, unique=True, null=True, blank=True, verbose_name='NIP')
    nombre = models.CharField(max_length=100, null=False, verbose_name='Nombre')
    rut_madre = models.CharField(max_length=100, null=True, blank=True, verbose_name='R.U.T. Madre')
    apellido_paterno = models.CharField(max_length=100, null=False, verbose_name='Apellido Paterno')
    apellido_materno = models.CharField(max_length=100, null=False, verbose_name='Apellido Materno')

    rut_responsable_temporal = models.CharField(max_length=100, null=True, blank=True,
                                                verbose_name='RUT Responsable Temporal'
                                                )

    usar_rut_madre_como_responsable = models.BooleanField(default=False,
                                                          verbose_name='Usar RUT de la madre como responsable'
                                                          )

    pasaporte = models.CharField(max_length=50, unique=True, null=True, blank=True, verbose_name='Pasaporte')
    nombre_social = models.CharField(max_length=100, null=True, blank=True, verbose_name='Nombre Social')

    # DATOS DE NACIMIENTO
    fecha_nacimiento = models.DateField(null=False, verbose_name='Fecha de Nacimiento')
    sexo = models.CharField(max_length=10, choices=[('MASCULINO', 'Masculino'), ('FEMENINO', 'Femenino')], null=False,
                            verbose_name='Sexo')
    estado_civil = models.CharField(max_length=20, choices=ESTADO_CIVIL, null=False, verbose_name='Estado Civil')

    # DATOS FAMILIARES
    nombres_padre = models.CharField(max_length=100, verbose_name='Nombres del Padre', null=True, blank=True)
    nombres_madre = models.CharField(max_length=100, verbose_name='Nombres de la Madre', null=True, blank=True)
    nombre_pareja = models.CharField(max_length=100, verbose_name='Nombre de la Pareja', null=True, blank=True)
    representante_legal = models.CharField(max_length=100, null=True, blank=True, verbose_name='Representante Legal')

    # CONTACTO Y DIRECCIÓN
    direccion = models.CharField(max_length=200, verbose_name='Dirección', null=False)
    sin_telefono = models.BooleanField(default=False)
    numero_telefono1 = models.CharField(max_length=15, verbose_name='Número de Teléfono', null=False)
    numero_telefono2 = models.CharField(max_length=15, verbose_name='Número de Teléfono 2', null=True, blank=True)
    ocupacion = models.CharField(max_length=100, null=True, blank=True, verbose_name='Ocupación')

    # ESTADO DEL PACIENTE
    recien_nacido = models.BooleanField(default=False, verbose_name='Recién Nacido')
    extranjero = models.BooleanField(default=False, verbose_name='Extranjero')
    fallecido = models.BooleanField(default=False, verbose_name='Fallecido')
    fecha_fallecimiento = models.DateField(null=True, blank=True, verbose_name='Fecha de Fallecimiento')

    comuna = models.ForeignKey('kardex.Comuna', on_delete=models.PROTECT, null=False,
                               verbose_name='Comuna', related_name='pacientes_comuna')
    prevision = models.ForeignKey('kardex.Prevision', on_delete=models.SET_NULL, null=True, blank=True,
                                  verbose_name='Previsión', related_name='pacientes_prevision')

    usuario = models.ForeignKey('usuarios.UsuarioPersonalizado', on_delete=models.SET_NULL, null=True, blank=True,
                                verbose_name='Usuario', related_name='pacientes_usuario')

    genero = models.ForeignKey('kardex.Genero', on_delete=models.SET_NULL, null=True, blank=True,
                               verbose_name='Genero', related_name='pacientes_genero')

    history = HistoricalRecords()

    def __str__(self):
        return f"{self.rut} - {self.nombre} {self.apellido_paterno} {self.apellido_materno}"

    class Meta:
        verbose_name = 'Paciente'
        verbose_name_plural = 'Pacientes'

    def save(self, *args, **kwargs):
        is_new = self.pk is None  # Saber si es un nuevo registro

        # Recorrer todos los campos del modelo
        for field in self._meta.get_fields():
            # Solo nos interesa CharField y TextField
            if isinstance(field, (models.CharField, models.TextField)):
                value = getattr(self, field.name, None)
                if value:
                    if field.name == 'rut':
                        setattr(self, field.name, value.lower())
                    else:
                        setattr(self, field.name, value.upper())

        # Primero guarda el objeto para que se genere el ID
        super().save(*args, **kwargs)

        # Si es nuevo y no tenía código, ahora lo generamos usando el ID
        if is_new and not self.codigo:
            self.codigo = f"PAC-{self.pk:07d}"
            super().save(update_fields=["codigo"])  # Solo actualiza el campo código

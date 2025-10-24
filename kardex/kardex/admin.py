from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from .models import *


# === PAÍS ===
@admin.register(Pais)
class PaisAdmin(SimpleHistoryAdmin):
    list_display = ("id", "nombre", "cod_pais")
    search_fields = ("nombre", "cod_pais")
    ordering = ("nombre",)


# === COMUNA ===
@admin.register(Comuna)
class ComunaAdmin(SimpleHistoryAdmin):
    list_display = ("id", "nombre", "codigo", "pais")
    search_fields = ("nombre", "codigo", "pais__nombre")
    autocomplete_fields = ("pais",)
    ordering = ("nombre",)


# === ESTABLECIMIENTO ===
@admin.register(Establecimiento)
class EstablecimientoAdmin(SimpleHistoryAdmin):
    list_display = ("id", "nombre", "direccion", "telefono", "comuna")
    search_fields = ("nombre", "direccion", "comuna__nombre")
    autocomplete_fields = ("comuna",)
    ordering = ("nombre",)


# === PREVISIÓN ===
@admin.register(Prevision)
class PrevisionAdmin(SimpleHistoryAdmin):
    list_display = ("id", "nombre")
    search_fields = ("nombre",)
    ordering = ("nombre",)


# === PROFESIÓN ===
@admin.register(Profesion)
class ProfesionAdmin(SimpleHistoryAdmin):
    list_display = ("id", "nombre")
    search_fields = ("nombre",)
    ordering = ("nombre",)


# === SERVICIO CLÍNICO ===
@admin.register(ServicioClinico)
class ServicioClinicoAdmin(SimpleHistoryAdmin):
    list_display = ("id", "nombre", "tiempo_horas", "correo_jefe", "establecimiento")
    search_fields = ("nombre", "establecimiento__nombre")
    autocomplete_fields = ("establecimiento",)
    ordering = ("nombre",)


# === PROFESIONAL ===
@admin.register(Profesional)
class ProfesionalAdmin(SimpleHistoryAdmin):
    list_display = ("id", "rut", "nombres", "correo", "telefono", "profesion", "establecimiento")
    search_fields = ("rut", "nombres", "correo", "profesion__nombre", "establecimiento__nombre")
    autocomplete_fields = ("profesion", "establecimiento")
    ordering = ("nombres",)


# === USUARIO ANTERIOR ===
@admin.register(UsuarioAnterior)
class UsuarioAnteriorAdmin(SimpleHistoryAdmin):
    list_display = ("rut", "nombre", "correo", "establecimiento")
    search_fields = ("rut", "nombre", "correo", "establecimiento__nombre")
    autocomplete_fields = ("establecimiento",)
    ordering = ("nombre",)


# === PACIENTE ===
@admin.register(Paciente)
class PacienteAdmin(SimpleHistoryAdmin):
    list_display = (
        "id",
        "codigo",
        "rut",
        "nombre",
        "apellido_paterno",
        "apellido_materno",
        "comuna",
        "prevision",
        "fallecido",
    )
    search_fields = (
        "codigo",
        "rut",
        "nip",
        "nombre",
        "apellido_paterno",
        "apellido_materno",
        "comuna__nombre",
    )
    list_filter = ("fallecido", "sexo", "estado_civil", "extranjero", "recien_nacido")
    autocomplete_fields = ("comuna", "prevision", "usuario", "usuario_anterior")
    ordering = ("nombre", "apellido_paterno")


# === FICHA ===
@admin.register(Ficha)
class FichaAdmin(SimpleHistoryAdmin):
    list_display = (
        "id",
        "numero_ficha_sistema",
        "paciente",
        "establecimiento",
        "profesional",
        "pasivado",
        "fecha_creacion_anterior",
    )
    search_fields = (
        "numero_ficha_sistema",
        "numero_ficha_tarjeta",
        "paciente__rut",
        "paciente__nombre",
        "paciente__apellido_paterno",
    )
    list_filter = ("pasivado", "establecimiento")
    autocomplete_fields = ("paciente", "establecimiento", "profesional", "usuario")
    ordering = ("-id",)


# === MOVIMIENTO FICHA ===
@admin.register(MovimientoFicha)
class MovimientoFichaAdmin(SimpleHistoryAdmin):
    list_display = (
        "id",
        "ficha",
        "servicio_clinico_envio",
        "servicio_clinico_recepcion",
        "estado_envio",
        "estado_recepcion",
        "fecha_envio",
        "fecha_recepcion",
    )
    search_fields = (
        "ficha__id",
        "ficha__paciente__rut",
        "servicio_clinico_envio__nombre",
        "servicio_clinico_recepcion__nombre",
        "profesional_envio__nombres",
        "profesional_recepcion__nombres",
    )
    list_filter = ("estado_envio", "estado_recepcion", "fecha_envio", "fecha_recepcion")
    autocomplete_fields = (
        "ficha",
        "servicio_clinico_envio",
        "servicio_clinico_recepcion",
        "usuario_envio",
        "usuario_recepcion",
        "profesional_envio",
        "profesional_recepcion",
    )
    ordering = ("-fecha_envio",)

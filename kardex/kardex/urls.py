from django.shortcuts import render
from django.urls import path

from kardex.views.comuna import *
from kardex.views.establecimiento import *
from kardex.views.ficha import *
from kardex.views.movimiento_fichas import *
from kardex.views.pacientes import *
from kardex.views.pais import *
from kardex.views.pdfs import pdf_index, pdf_stickers
from kardex.views.prevision import *
from kardex.views.profesion import *
from kardex.views.profesionales import *
from kardex.views.servicio_clinico import *

app_name = 'kardex'

urlpatterns = [
    # Vistas básicas para Paises
    path('paises/', PaisListView.as_view(), name='pais_list'),
    path('paises/crear/', PaisCreateView.as_view(), name='pais_create'),
    path('paises/<int:pk>/editar/', PaisUpdateView.as_view(), name='pais_update'),
    path('paises/<int:pk>/eliminar/', PaisDeleteView.as_view(), name='pais_delete'),
    path('paises/<int:pk>/detalle/', PaisDetailView.as_view(), name='pais_detail'),

    # Vistas básicas para Comunas
    path('comunas/', ComunaListView.as_view(), name='comuna_list'),
    path('comunas/crear/', ComunaCreateView.as_view(), name='comuna_create'),
    path('comunas/<int:pk>/editar/', ComunaUpdateView.as_view(), name='comuna_update'),
    path('comunas/<int:pk>/eliminar/', ComunaDeleteView.as_view(), name='comuna_delete'),
    path('comunas/<int:pk>/detalle/', ComunaDetailView.as_view(), name='comuna_detail'),

    # Vistas básicas para Establecimientos
    path('establecimientos/', EstablecimientoListView.as_view(), name='establecimiento_list'),
    path('establecimientos/crear/', EstablecimientoCreateView.as_view(), name='establecimiento_create'),
    path('establecimientos/<int:pk>/editar/', EstablecimientoUpdateView.as_view(), name='establecimiento_update'),
    path('establecimientos/<int:pk>/eliminar/', EstablecimientoDeleteView.as_view(), name='establecimiento_delete'),
    path('establecimientos/<int:pk>/detalle/', EstablecimientoDetailView.as_view(), name='establecimiento_detail'),

    # Vistas básicas para Profesiones
    path('profesiones/', ProfesionListView.as_view(), name='profesion_list'),
    path('profesiones/crear/', ProfesionCreateView.as_view(), name='profesion_create'),
    path('profesiones/<int:pk>/editar/', ProfesionUpdateView.as_view(), name='profesion_update'),
    path('profesiones/<int:pk>/eliminar/', ProfesionDeleteView.as_view(), name='profesion_delete'),
    path('profesiones/<int:pk>/detalle/', ProfesionDetailView.as_view(), name='profesion_detail'),

    # Vistas básicas para Profesionales
    path('profesionales/', ProfesionalListView.as_view(), name='profesional_list'),
    path('profesionales/crear/', ProfesionalCreateView.as_view(), name='profesional_create'),
    path('profesionales/<int:pk>/editar/', ProfesionalUpdateView.as_view(), name='profesional_update'),
    path('profesionales/<int:pk>/eliminar/', ProfesionalDeleteView.as_view(), name='profesional_delete'),
    path('profesionales/<int:pk>/detalle/', ProfesionalDetailView.as_view(), name='profesional_detail'),

    # Vistas básicas para Prevision
    path('prevision/', PrevisionListView.as_view(), name='prevision_list'),
    path('prevision/crear/', PrevisionCreateView.as_view(), name='prevision_create'),
    path('prevision/<int:pk>/editar/', PrevisionUpdateView.as_view(), name='prevision_update'),
    path('prevision/<int:pk>/eliminar/', PrevisionDeleteView.as_view(), name='prevision_delete'),
    path('prevision/<int:pk>/detalle/', PrevisionDetailView.as_view(), name='prevision_detail'),

    # Vistas básicas para Pacientes
    path('pacientes/', PacienteListView.as_view(), name='paciente_list'),
    path('pacientes/recien-nacidos/', PacienteRecienNacidoListView.as_view(), name='paciente_recien_nacido_list'),
    path('pacientes/extranjeros/', PacienteExtranjeroListView.as_view(), name='paciente_extranjero_list'),
    path('pacientes/fallecidos/', PacienteFallecidoListView.as_view(), name='paciente_fallecido_list'),
    path('pacientes/por-fecha/', PacientePorFechaListView.as_view(), name='paciente_por_fecha_list'),
    path('pacientes/por-fecha/form/', PacienteFechaFormView.as_view(), name='paciente_fecha_form'),
    path('pacientes/crear/', PacienteCreateView.as_view(), name='paciente_create'),
    path('pacientes/crear-nuevo/', PacienteCreacionView.as_view(), name='paciente_creacion'),
    path('pacientes/<int:pk>/editar/', PacienteUpdateView.as_view(), name='paciente_update'),
    path('pacientes/<int:pk>/eliminar/', PacienteDeleteView.as_view(), name='paciente_delete'),
    path('pacientes/<int:pk>/detalle/', PacienteDetailView.as_view(), name='paciente_detail'),

    # Vistas básicas para Fichas
    path('fichas/', FichaListView.as_view(), name='ficha_list'),
    path('fichas/crear/', FichaCreateView.as_view(), name='ficha_create'),
    path('fichas/<int:pk>/editar/', FichaUpdateView.as_view(), name='ficha_update'),
    path('fichas/<int:pk>/eliminar/', FichaDeleteView.as_view(), name='ficha_delete'),
    path('fichas/<int:pk>/detalle/', FichaDetailView.as_view(), name='ficha_detail'),

    # Vistas básicas para Movimientos de Ficha
    path('movimientos-ficha/', MovimientoFichaListView.as_view(), name='movimiento_ficha_list'),
    path('movimientos-ficha/crear/', MovimientoFichaCreateView.as_view(), name='movimiento_ficha_create'),
    path('movimientos-ficha/<int:pk>/editar/', MovimientoFichaUpdateView.as_view(), name='movimiento_ficha_update'),
    path('movimientos-ficha/<int:pk>/eliminar/', MovimientoFichaDeleteView.as_view(), name='movimiento_ficha_delete'),
    path('movimientos-ficha/<int:pk>/detalle/', MovimientoFichaDetailView.as_view(), name='movimiento_ficha_detail'),

    # Vistas básicas para Servicios Clínicos
    path('servicios-clinicos/', ServicioClinicoListView.as_view(), name='servicio_clinico_list'),
    path('servicios-clinicos/crear/', ServicioClinicoCreateView.as_view(), name='servicio_clinico_create'),
    path('servicios-clinicos/<int:pk>/editar/', ServicioClinicoUpdateView.as_view(), name='servicio_clinico_update'),
    path('servicios-clinicos/<int:pk>/eliminar/', ServicioClinicoDeleteView.as_view(), name='servicio_clinico_delete'),
    path('servicios-clinicos/<int:pk>/detalle/', ServicioClinicoDetailView.as_view(), name='servicio_clinico_detail'),
    path('pdf/', pdf_index, name='pdf_prueba'),
    path('pdfs/paciente/<int:paciente_id>/', pdf_index, name='pdf_paciente'),
    path('pdfs/ficha/<int:ficha_id>/', pdf_index, name='pdf_ficha'),

    path('pdfs/sticker/paciente/<int:paciente_id>/', pdf_stickers, name='pdf_stickers'),
    path('pdfs/stickers/ficha/<int:ficha_id>/', pdf_stickers, name='pdf_stickers_ficha'),

    # Nuevas vistas de movimientos (Recepción y Salida)
    path('movimientos/recepcion/', RecepcionFichaView.as_view(), name='recepcion_ficha'),
    path('movimientos/salida/', SalidaFichaView.as_view(), name='salida_ficha'),

    path('consulta-pacientes/', PacienteQueryView.as_view(), name='paciente_query'),

]


def custom_permission_denied_view(request, exception):
    return render(request, '403.html', status=403)


handler403 = custom_permission_denied_view

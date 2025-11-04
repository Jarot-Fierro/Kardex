from django.urls import path

from . import views

app_name = 'reports'

urlpatterns = [
    # MANTENEDORES
    path('export/pais/', views.export_pais, name='export_pais'),
    path('export/comuna/', views.export_comuna, name='export_comuna'),
    path('export/establecimiento/', views.export_establecimiento, name='export_establecimiento'),
    path('export/prevision/', views.export_prevision, name='export_prevision'),
    path('export/profesion/', views.export_profesion, name='export_profesion'),
    path('export/profesional/', views.export_profesional, name='export_profesional'),
    path('export/sector/', views.export_sector, name='export_sector'),
    path('export/servicio_clinico/', views.export_servicio_clinico, name='export_servicio_clinico'),

    # FICHAS
    path('export/ficha/', views.export_ficha, name='export_ficha'),
    path('export/ficha_pasivada/', views.export_ficha_pasivada, name='export_ficha_pasivada'),
    path('export/fichas_fast/', views.export_ficha_fast, name='export_ficha_fast'),

    # MOVIMIENTOS FICHAS
    path('export/movimiento_ficha/', views.export_movimiento_ficha, name='export_movimiento_ficha'),
    path('export/movimiento_ficha_envio/', views.export_movimiento_ficha_envio, name='export_movimiento_ficha_envio'),
    path('export/movimiento_ficha_recepcion/', views.export_movimiento_ficha_recepcion,
         name='export_movimiento_ficha_recepcion'),
    path('export/movimiento_ficha_traspaso/', views.export_movimiento_ficha_traspaso,
         name='export_movimiento_ficha_traspaso'),

    # PACIENTES
    path('export/paciente/', views.export_paciente, name='export_paciente'),
    path('export/paciente_recien_nacido/', views.export_paciente_recien_nacido, name='export_paciente_recien_nacido'),
    path('export/paciente_extranjero/', views.export_paciente_extranjero, name='export_paciente_extranjero'),
    path('export/paciente_fallecido/', views.export_paciente_fallecido, name='export_paciente_fallecido'),
    path('export/paciente_pueblo_indigena/', views.export_paciente_pueblo_indigena,
         name='export_paciente_pueblo_indigena'),

]

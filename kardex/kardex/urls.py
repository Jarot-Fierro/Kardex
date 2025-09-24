from django.urls import path

from kardex.views import *
from kardex.views_folders.comuna import *

app_name = 'kardex'

urlpatterns = [
    path('establecimientos', EstablecimientoView.as_view(), name='establecimiento_active'),
    path('establecimientos/<int:pk>', EstablecimientoView.as_view(), name='establecimiento_update'),

    path('comunas', ComunaView.as_view(), name='comuna_active'),
    path('comunas/<int:pk>', ComunaView.as_view(), name='comuna_update'),

    path('fichas', FichaView.as_view(), name='ficha_active'),
    path('fichas/<int:pk>', FichaView.as_view(), name='ficha_update'),

    path('pacientes', PacienteView.as_view(), name='paciente_active'),
    path('pacientes/<int:pk>', PacienteView.as_view(), name='paciente_update'),

    path('pacientes-recien-nacidos', PacienteRecienNacidoView.as_view(), name='paciente_recien_nacidos_active'),
    path('pacientes-extranjeros', PacienteExtranjeroView.as_view(), name='paciente_extranjeros_active'),
    path('pacientes-fallecidos', PacienteFallecidoView.as_view(), name='paciente_fallecidos_active'),

    path('movimiento-fichas-entrada', MovimientoFichaEntradaView.as_view(), name='movimiento_ficha_entrada_active'),
    path('movimiento-fichas-entrada/<int:pk>', MovimientoFichaEntradaView.as_view(),
         name='movimiento_ficha_entrada_update'),
    path('movimiento-fichas-salida', MovimientoFichaSalidaView.as_view(), name='movimiento_ficha_salida_active'),
    path('movimiento-fichas-salida/<int:pk>', MovimientoFichaSalidaView.as_view(),
         name='movimiento_ficha_salida_update'),

    path('prevision', PrevisionView.as_view(), name='prevision_active'),
    path('prevision/<int:pk>', PrevisionView.as_view(), name='prevision_update'),

    path('profesionales', ProfesionalesView.as_view(), name='profesionales_active'),
    path('profesionales/<int:pk>', ProfesionalesView.as_view(), name='profesionales_update'),

    path('servicio-clinico', ServicioClinicoView.as_view(), name='servicio_clinico_active'),
    path('servicio-clinico/<int:pk>', ServicioClinicoView.as_view(), name='servicio_clinico_update'),

    path('pacientes-por-fecha/', PacientePorFechaView.as_view(), name='pacientes_por_fecha'),

    # Vistas básicas para Comunas (basadas en base.html)
    path('comunas-simple/', ComunaListView.as_view(), name='comuna_list'),
    path('comunas-simple/crear/', ComunaCreateView.as_view(), name='comuna_create'),
    path('comunas-simple/<int:pk>/editar/', ComunaUpdateView.as_view(), name='comuna_update'),
    path('comunas-simple/<int:pk>/eliminar/', ComunaDeleteView.as_view(), name='comuna_delete'),
]

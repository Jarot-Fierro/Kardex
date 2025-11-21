from rest_framework import routers

from kardex.views.api.fichas import FichaViewSet
from kardex.views.api.pacientes import PacienteViewSet
from kardex.views.api.recepcion_ficha import RecepcionFichaViewSet
from kardex.views.api.traspasos import TraspasoFichaViewSet
from kardex.views.api.catalogos import ServicioClinicoViewSet, ProfesionalViewSet

router = routers.DefaultRouter()
router.register(r'ingreso-paciente-ficha', FichaViewSet, basename='ficha')
router.register(r'recepcion-ficha', RecepcionFichaViewSet, basename='recepcion-ficha')
router.register(r'traspaso-ficha', TraspasoFichaViewSet, basename='traspaso-ficha')
router.register(r'pacientes', PacienteViewSet, basename='paciente')
router.register(r'servicios-clinicos', ServicioClinicoViewSet, basename='servicio-clinico')
router.register(r'profesionales', ProfesionalViewSet, basename='profesional')

from rest_framework import routers

from kardex.views.api.fichas import FichaViewSet
from kardex.views.api.pacientes import PacienteViewSet

router = routers.DefaultRouter()
router.register(r'ingreso-paciente', PacienteViewSet)
router.register(r'ingreso-paciente-ficha', FichaViewSet, basename='ficha')

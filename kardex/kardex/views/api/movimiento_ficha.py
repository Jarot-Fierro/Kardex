from rest_framework import routers, viewsets, serializers

from kardex.models import IngresoPaciente, Paciente, Establecimiento


class PacienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paciente
        fields = '__all__'


class EstablecimientoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Establecimiento
        fields = '__all__'


class IngresoPacienteSerializer(serializers.HyperlinkedModelSerializer):
    paciente = PacienteSerializer(read_only=True)
    establecimiento = EstablecimientoSerializer(read_only=True)

    class Meta:
        model = IngresoPaciente
        fields = ['url', 'id', 'paciente', 'establecimiento', 'created_at']


class IngresoPacienteViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = IngresoPaciente.objects.all().order_by('-id')
    serializer_class = IngresoPacienteSerializer


router = routers.DefaultRouter()
router.register(r'ingreso-paciente', IngresoPacienteViewSet)

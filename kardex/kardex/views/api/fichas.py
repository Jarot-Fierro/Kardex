from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import serializers
from rest_framework import viewsets

from kardex.models import Ficha
from kardex.models import Paciente, Establecimiento


class EstablecimientoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Establecimiento
        fields = '__all__'


class PacienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paciente
        fields = '__all__'


class FichaSerializer(serializers.ModelSerializer):
    paciente = PacienteSerializer()
    establecimiento = EstablecimientoSerializer()

    class Meta:
        model = Ficha
        fields = '__all__'


class FichaViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = FichaSerializer
    filter_backends = [DjangoFilterBackend]
    queryset = Ficha.objects.none()

    def get_queryset(self):
        user = self.request.user
        search_term = self.request.query_params.get('search', '').strip()
        tipo_busqueda = self.request.query_params.get('tipo', '').strip()

        # .filter(establecimiento=user.establecimiento)
        queryset = (
            Ficha.objects
            .select_related(
                'paciente',
                'establecimiento',
                'usuario',
                'profesional'
            )
            .order_by('id')
        )

        if search_term:

            if tipo_busqueda == 'rut':
                queryset = queryset.filter(paciente__rut__icontains=search_term)
            elif tipo_busqueda == 'codigo':
                queryset = queryset.filter(paciente__codigo__icontains=search_term)
            elif tipo_busqueda == 'ficha':
                # numero_ficha_sistema es numérico en el modelo; intentar filtrar por entero
                try:
                    num = int(search_term)
                    queryset = queryset.filter(numero_ficha_sistema=num)
                except ValueError:
                    # Si no es un número válido, devolver un queryset vacío (o mantener queryset sin filtrar)
                    queryset = queryset.none()

        return queryset

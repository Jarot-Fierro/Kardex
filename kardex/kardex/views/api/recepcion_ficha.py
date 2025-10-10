from django.utils import timezone
from rest_framework import serializers, viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from kardex.models import MovimientoFicha, Ficha, IngresoPaciente, Paciente, Establecimiento


class EstablecimientoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Establecimiento
        fields = '__all__'


class PacienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paciente
        fields = '__all__'


class IngresoPacienteSerializer(serializers.ModelSerializer):
    paciente = PacienteSerializer()
    establecimiento = EstablecimientoSerializer()

    class Meta:
        model = IngresoPaciente
        fields = '__all__'


class FichaSerializer(serializers.ModelSerializer):
    ingreso_paciente = IngresoPacienteSerializer()

    class Meta:
        model = Ficha
        fields = '__all__'


class MovimientoFichaSerializer(serializers.ModelSerializer):
    ficha = FichaSerializer()

    class Meta:
        model = MovimientoFicha
        fields = '__all__'


class RecepcionFichaViewSet(viewsets.ModelViewSet):
    serializer_class = MovimientoFichaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        qs = MovimientoFicha.objects.select_related(
            'ficha__ingreso_paciente__paciente',
            'ficha__ingreso_paciente__establecimiento',
            'servicio_clinico',
            'usuario'
        ).filter(
            fecha_salida__isnull=False,
            fecha_entrada__isnull=True,
            ficha__ingreso_paciente__establecimiento=user.establecimiento
        ).order_by('-fecha_salida')
        return qs

    @action(detail=True, methods=['post'], url_path='mark_received')
    def mark_received(self, request, pk=None):
        try:
            m = self.get_queryset().get(id=pk)
        except MovimientoFicha.DoesNotExist:
            return Response({'ok': False, 'error': 'No encontrado'}, status=status.HTTP_404_NOT_FOUND)

        fecha_entrada = request.data.get('fecha_entrada')
        obs = request.data.get('observacion_entrada')
        from datetime import datetime

        if fecha_entrada:
            try:
                dt = datetime.fromisoformat(fecha_entrada)
            except Exception:
                dt = timezone.now()
        else:
            dt = timezone.now()

        m.fecha_entrada = dt
        if obs is not None:
            m.observacion_entrada = obs
        m.fecha_mov = m.fecha_entrada
        m.save(update_fields=['fecha_entrada', 'observacion_entrada', 'fecha_mov'])

        return Response({'ok': True, 'id': m.id})

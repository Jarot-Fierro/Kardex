# from django_filters.rest_framework import DjangoFilterBackend
# from rest_framework import serializers
# from rest_framework import viewsets, filters
#
# from kardex.models import Paciente,
#
#
# class PacienteSerializer(serializers.ModelSerializer):
#     establecimiento = serializers.SerializerMethodField()
#
#     class Meta:
#         model = Paciente
#         fields = '__all__'
#
#     def get_establecimiento(self, obj):
#         user = self.context['request'].user
#         ingreso = IngresoPaciente.objects.filter(
#             paciente=obj, establecimiento=user.establecimiento
#         ).first()
#         if ingreso:
#             return ingreso.establecimiento.nombre
#         return None
#
#
# class PacienteViewSet(viewsets.ReadOnlyModelViewSet):
#     serializer_class = PacienteSerializer
#     filter_backends = [DjangoFilterBackend, filters.SearchFilter]
#     search_fields = ['rut', 'codigo', 'nombre']
#     queryset = Paciente.objects.all()
#
#     def get_queryset(self):
#         user = self.request.user
#         ingresos = IngresoPaciente.objects.filter(
#             establecimiento=user.establecimiento
#         ).values_list('paciente_id', flat=True)
#
#         return Paciente.objects.filter(id__in=ingresos).order_by('id')

# from django_filters.rest_framework import DjangoFilterBackend
# from rest_framework import serializers
# from rest_framework import viewsets
#
# from kardex.models import Ficha
# from kardex.models import IngresoPaciente, Paciente, Establecimiento
#
#
# class EstablecimientoSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Establecimiento
#         fields = '__all__'
#
#
# class PacienteSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Paciente
#         fields = '__all__'
#
#
# class IngresoPacienteSerializer(serializers.ModelSerializer):
#     paciente = PacienteSerializer()
#     establecimiento = EstablecimientoSerializer()
#
#     class Meta:
#         model = IngresoPaciente
#         fields = '__all__'
#
#
# class FichaSerializer(serializers.ModelSerializer):
#     ingreso_paciente = IngresoPacienteSerializer()
#
#     class Meta:
#         model = Ficha
#         fields = '__all__'
#
#
# class FichaViewSet(viewsets.ReadOnlyModelViewSet):
#     serializer_class = FichaSerializer
#     filter_backends = [DjangoFilterBackend]
#     queryset = Ficha.objects.none()
#
#     def get_queryset(self):
#         user = self.request.user
#         search_term = self.request.query_params.get('search', '').strip()
#         tipo_busqueda = self.request.query_params.get('tipo', '').strip()
#
#         queryset = (
#             Ficha.objects
#             .filter(ingreso_paciente__establecimiento=user.establecimiento)
#             .select_related(
#                 'ingreso_paciente__paciente',
#                 'ingreso_paciente__establecimiento',
#                 'usuario',
#                 'profesional'
#             )
#             .order_by('id')
#         )
#
#         if search_term:
#
#             if tipo_busqueda == 'rut':
#                 queryset = queryset.filter(ingreso_paciente__paciente__rut__icontains=search_term)
#             elif tipo_busqueda == 'codigo':
#                 queryset = queryset.filter(ingreso_paciente__paciente__codigo__icontains=search_term)
#             elif tipo_busqueda == 'ficha':
#                 queryset = queryset.filter(numero_ficha__icontains=search_term)
#
#         return queryset

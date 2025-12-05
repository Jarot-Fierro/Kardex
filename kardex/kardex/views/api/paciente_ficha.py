from rest_framework import serializers
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from kardex.models import Paciente, Ficha
from kardex.models.paciente_ficha import VistaFichaPaciente


class VistaFichaPacienteSerializer(serializers.Serializer):
    # -------- FICHA -------
    ficha_id = serializers.IntegerField()
    numero_ficha_sistema = serializers.IntegerField()
    numero_ficha_tarjeta = serializers.IntegerField(allow_null=True)

    pasivado = serializers.BooleanField()
    observacion = serializers.CharField(allow_null=True)
    fecha_creacion_anterior = serializers.DateTimeField(allow_null=True)

    profesional_id = serializers.IntegerField(allow_null=True)
    sector_id = serializers.IntegerField(allow_null=True)
    usuario_id = serializers.IntegerField(allow_null=True)

    # -------- ESTABLECIMIENTO -------
    establecimiento_id = serializers.IntegerField()
    establecimiento_nombre = serializers.CharField()

    # -------- PACIENTE -------
    paciente_id = serializers.IntegerField()
    paciente_codigo = serializers.CharField()

    rut = serializers.CharField()
    nip = serializers.CharField(allow_null=True)

    nombre = serializers.CharField()
    apellido_paterno = serializers.CharField()
    apellido_materno = serializers.CharField()

    nombre_social = serializers.CharField(allow_null=True)
    genero = serializers.CharField()

    fecha_nacimiento = serializers.DateField(allow_null=True)
    sexo = serializers.CharField()
    estado_civil = serializers.CharField()

    rut_madre = serializers.CharField(allow_null=True)
    nombres_padre = serializers.CharField(allow_null=True)
    nombres_madre = serializers.CharField(allow_null=True)
    nombre_pareja = serializers.CharField(allow_null=True)
    representante_legal = serializers.CharField(allow_null=True)

    pueblo_indigena = serializers.BooleanField()
    recien_nacido = serializers.BooleanField()
    extranjero = serializers.BooleanField()
    fallecido = serializers.BooleanField()

    fecha_fallecimiento = serializers.DateField(allow_null=True)
    alergico_a = serializers.CharField(allow_null=True)

    direccion = serializers.CharField(allow_null=True)
    sin_telefono = serializers.BooleanField()

    numero_telefono1 = serializers.CharField(allow_null=True)
    numero_telefono2 = serializers.CharField(allow_null=True)

    ocupacion = serializers.CharField(allow_null=True)

    paciente_comuna_id = serializers.IntegerField()
    prevision_id = serializers.IntegerField(allow_null=True)

    pasaporte = serializers.CharField(allow_null=True)
    rut_responsable_temporal = serializers.CharField(allow_null=True)

    usar_rut_madre_como_responsable = serializers.BooleanField()


class PacienteFichaViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    # ------------------------------------
    # CONSULTAR POR RUT
    # ------------------------------------
    def list(self, request):
        rut = request.GET.get("rut")
        numero_ficha = request.GET.get("numero_ficha")
        establecimiento_id = request.user.establecimiento_id

        # Validar que al menos uno de los parámetros exista
        if not rut and not numero_ficha:
            return Response({"error": "Debe indicar RUT o número de ficha"}, status=400)

        vista = None

        # Filtrar por RUT
        if rut:
            rut = rut.strip().lower()
            vista = VistaFichaPaciente.objects.filter(
                rut=rut,
                establecimiento_id=establecimiento_id
            ).first()

        # Si no se encontró por RUT, filtrar por número de ficha
        elif numero_ficha:
            try:
                numero_ficha = int(numero_ficha)
                vista = VistaFichaPaciente.objects.filter(
                    numero_ficha_sistema=numero_ficha,
                    establecimiento_id=establecimiento_id
                ).first()
            except ValueError:
                return Response({"error": "Número de ficha inválido"}, status=400)

        # ============ CASO 1: FICHA EXISTE ============
        if vista:
            serializer = VistaFichaPacienteSerializer(vista)
            return Response({
                "exists": True,
                "has_ficha": True,
                "data": serializer.data
            })

        # ============ CASO 2: PACIENTE EXISTE PERO SIN FICHA ============
        if rut:
            paciente = Paciente.objects.filter(rut=rut).first()
            if paciente:
                # Devolver también los datos básicos del paciente para rellenar el formulario en el template
                data_paciente = {
                    # IDs básicos
                    "paciente_id": paciente.id,

                    # IDENTIFICACIÓN
                    "codigo": getattr(paciente, "codigo", "") or "",
                    "rut": getattr(paciente, "rut", "") or "",
                    "nip": getattr(paciente, "nip", "") or "",
                    "nombre": getattr(paciente, "nombre", "") or "",
                    "apellido_paterno": getattr(paciente, "apellido_paterno", "") or "",
                    "apellido_materno": getattr(paciente, "apellido_materno", "") or "",
                    "rut_madre": getattr(paciente, "rut_madre", "") or "",
                    "rut_responsable_temporal": getattr(paciente, "rut_responsable_temporal", "") or "",

                    "pueblo_indigena": bool(getattr(paciente, "pueblo_indigena", False)),
                    "usar_rut_madre_como_responsable": bool(
                        getattr(paciente, "usar_rut_madre_como_responsable", False)),

                    # DOCUMENTOS / IDENTIDAD
                    "pasaporte": getattr(paciente, "pasaporte", "") or "",
                    "nombre_social": getattr(paciente, "nombre_social", "") or "",
                    "genero": getattr(paciente, "genero", "") or "",

                    # DATOS DE NACIMIENTO
                    "fecha_nacimiento": getattr(paciente, "fecha_nacimiento", None),
                    "sexo": getattr(paciente, "sexo", "") or "",
                    "estado_civil": getattr(paciente, "estado_civil", "") or "",

                    # DATOS FAMILIARES
                    "nombres_padre": getattr(paciente, "nombres_padre", "") or "",
                    "nombres_madre": getattr(paciente, "nombres_madre", "") or "",
                    "nombre_pareja": getattr(paciente, "nombre_pareja", "") or "",
                    "representante_legal": getattr(paciente, "representante_legal", "") or "",

                    # CONTACTO Y DIRECCIÓN
                    "direccion": getattr(paciente, "direccion", "") or "",
                    "sin_telefono": bool(getattr(paciente, "sin_telefono", False)),
                    "numero_telefono1": getattr(paciente, "numero_telefono1", "") or "",
                    "numero_telefono2": getattr(paciente, "numero_telefono2", "") or "",
                    "ocupacion": getattr(paciente, "ocupacion", "") or "",

                    # ESTADO DEL PACIENTE
                    "recien_nacido": bool(getattr(paciente, "recien_nacido", False)),
                    "extranjero": bool(getattr(paciente, "extranjero", False)),
                    "fallecido": bool(getattr(paciente, "fallecido", False)),
                    "fecha_fallecimiento": getattr(paciente, "fecha_fallecimiento", None),
                    "alergico_a": getattr(paciente, "alergico_a", "") or "",

                    # RELACIONES
                    "paciente_comuna_id": getattr(paciente, "comuna_id", None),
                    "prevision_id": getattr(paciente, "prevision_id", None),
                    "usuario_id": getattr(paciente, "usuario_id", None),
                    "usuario_anterior_id": getattr(paciente, "usuario_anterior_id", None),
                }

                return Response({
                    "exists": True,
                    "has_ficha": False,
                    **data_paciente,
                })

        # ============ CASO 3: NO EXISTE NADA ============
        return Response({
            "exists": False,
            "has_ficha": False
        })

    # ------------------------------------
    # CREAR PACIENTE + FICHA
    # ------------------------------------
    def create(self, request):

        establecimiento = request.user.establecimiento

        rut = request.data.get("rut")
        if not rut:
            return Response({"error": "RUT requerido"}, status=400)

        paciente = Paciente.objects.filter(rut=rut).first()

        # Crear paciente si no existe
        if not paciente:
            paciente = Paciente.objects.create(
                rut=rut,
                nombre=request.data.get("nombre"),
                apellido_paterno=request.data.get("apellido_paterno"),
                apellido_materno=request.data.get("apellido_materno"),
            )

        # Verificar si ya existe ficha para este establecimiento
        ficha_existe = Ficha.objects.filter(
            paciente=paciente,
            establecimiento=establecimiento
        ).exists()

        if ficha_existe:
            return Response(
                {"error": "El paciente ya tiene ficha en este establecimiento"},
                status=409
            )

        # Crear ficha
        ficha = Ficha.objects.create(
            paciente=paciente,
            establecimiento=establecimiento,
            usuario=request.user
        )

        return Response({
            "success": True,
            "ficha_id": ficha.id,
            "numero_ficha": ficha.numero_ficha_sistema
        }, status=status.HTTP_201_CREATED)

    # ------------------------------------
    # ACTUALIZAR DATOS
    # ------------------------------------
    def update(self, request, pk=None):

        try:
            paciente = Paciente.objects.get(pk=pk)
        except Paciente.DoesNotExist:
            return Response({"error": "Paciente no encontrado"}, status=404)

        CAMBIOS = [
            "nombre", "apellido_paterno", "apellido_materno",
            "nombre_social", "genero", "sexo", "estado_civil",
            "direccion", "ocupacion"
        ]

        for campo in CAMBIOS:
            if campo in request.data:
                setattr(paciente, campo, request.data[campo])

        paciente.save()

        return Response({"success": True})

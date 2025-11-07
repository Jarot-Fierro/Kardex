fields_paciente_csv = [
    # StandardModel
    'id',
    'created_at',
    'updated_at',
    'status',

    # IDENTIFICACIÓN
    'codigo',
    'rut',
    'nip',
    'nombre',
    'apellido_paterno',
    'apellido_materno',
    'nombre_social',
    'rut_madre',
    'rut_responsable_temporal',
    'usar_rut_madre_como_responsable',
    'pasaporte',
    'pueblo_indigena',
    'genero',
    'sexo',
    'estado_civil',

    # DATOS DE NACIMIENTO
    'fecha_nacimiento',

    # DATOS FAMILIARES
    'nombres_padre',
    'nombres_madre',
    'nombre_pareja',
    'representante_legal',

    # CONTACTO Y DIRECCIÓN
    'direccion',
    'sin_telefono',
    'numero_telefono1',
    'numero_telefono2',
    'ocupacion',

    # ESTADO DEL PACIENTE
    'recien_nacido',
    'extranjero',
    'fallecido',
    'fecha_fallecimiento',
    'alergico_a',

    # RELACIONES
    'comuna__nombre',
    'prevision__nombre',
    'usuario__username',
    'usuario_anterior__rut',
]

fields_ficha_csv = [
    # === CAMPOS HEREDADOS (StandardModel) ===
    'id',
    'created_at',
    'updated_at',
    'status',

    # === CAMPOS PRINCIPALES DE FICHA ===
    'numero_ficha_sistema',
    'numero_ficha_tarjeta',
    'pasivado',
    'observacion',
    'fecha_creacion_anterior',

    # === RELACIONES ===
    'usuario__username',
    'profesional__nombre_completo',  # si el modelo Profesional tiene un métdd o propiedad nombre_completo
    'profesional__rut',  # si no, puedes usar rut / nombre / apellido según tu modelo
    'paciente__rut',
    'paciente__nombre',
    'paciente__apellido_paterno',
    'paciente__apellido_materno',
    'paciente__codigo',
    'establecimiento__nombre',
    'sector__nombre',
]

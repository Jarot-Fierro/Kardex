import pandas as pd
from django.core.management.base import BaseCommand

from kardex.models import Paciente, Comuna, Prevision


class Command(BaseCommand):
    help = 'Importa pacientes desde una hoja "pacientes" en un archivo Excel.'

    def add_arguments(self, parser):
        parser.add_argument('excel_path', type=str, help='Ruta del archivo Excel que contiene la hoja "pacientes".')

    def handle(self, *args, **options):
        excel_path = options['excel_path']

        try:
            df = pd.read_excel(excel_path, sheet_name='pacientes')
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'❌ Error al leer el archivo: {e}'))
            return

        df.columns = df.columns.str.strip()

        total_creados = 0
        total_actualizados = 0

        for index, row in df.iterrows():
            try:
                rut = str(row.get('rut', '')).strip().lower()
                nombre = str(row.get('nombre', '')).strip()
                apellido_paterno = str(row.get('apellido_paterno', '')).strip()
                apellido_materno = str(row.get('apellido_materno', '')).strip()
                direccion = str(row.get('direccion', '')).strip()
                numero_telefono1 = str(row.get('numero_telefono1', '')).strip()
                sexo = str(row.get('sexo', '')).strip().upper()
                estado_civil = str(row.get('estado_civil', '')).strip().upper()

                # Fechas
                fecha_nacimiento_raw = row.get('fecha_nacimiento')
                fecha_nacimiento = pd.to_datetime(fecha_nacimiento_raw, errors='coerce')
                fecha_nacimiento = fecha_nacimiento.date() if pd.notna(fecha_nacimiento) else None

                # IDs relacionados
                comuna_id = row.get('comuna_id')
                prevision_id = row.get('prevision_id')
                genero_id = row.get('genero_id')

                # Opcionales
                rut_madre = str(row.get('rut_madre', '')).strip()
                nombre_social = str(row.get('nombre_social', '')).strip()
                pasaporte = str(row.get('pasaporte', '')).strip()
                nombres_padre = str(row.get('nombres_padre', '')).strip()
                nombres_madre = str(row.get('nombres_madre', '')).strip()
                nombre_pareja = str(row.get('nombre_pareja', '')).strip()
                representante_legal = str(row.get('representante_legal', '')).strip()
                numero_telefono2 = str(row.get('numero_telefono2', '')).strip()
                ocupacion = str(row.get('ocupacion', '')).strip()
                rut_responsable_temporal = str(row.get('rut_responsable_temporal', '')).strip()

                # Booleanos (asumimos que vienen como 0 o 1 en el Excel)
                sin_telefono = bool(row.get('sin_telefono', 0))
                recien_nacido = bool(row.get('recien_nacido', 0))
                extranjero = bool(row.get('extranjero', 0))
                fallecido = bool(row.get('fallecido', 0))
                usar_rut_madre_como_responsable = bool(row.get('usar_rut_madre_como_responsable', 0))

                # Fecha fallecimiento
                fecha_fallecimiento_raw = row.get('fecha_fallecimiento')
                fecha_fallecimiento = pd.to_datetime(fecha_fallecimiento_raw, errors='coerce')
                fecha_fallecimiento = fecha_fallecimiento.date() if pd.notna(fecha_fallecimiento) else None

                # Validación obligatorios
                if not all([rut, nombre, sexo, estado_civil, comuna_id]):
                    self.stdout.write(self.style.WARNING(f'⚠️ Fila {index + 2}: Faltan datos obligatorios. Se omite.'))
                    continue

                comuna = Comuna.objects.filter(id=int(comuna_id)).first()
                if not comuna:
                    self.stdout.write(self.style.WARNING(f'⚠️ Fila {index + 2}: Comuna ID {comuna_id} no encontrada.'))
                    continue

                prevision = Prevision.objects.filter(id=int(prevision_id)).first() if pd.notna(prevision_id) else None
                genero = str(row.get('genero', '')).strip().upper()

                paciente, created = Paciente.objects.update_or_create(
                    rut=rut,
                    defaults={
                        'nombre': nombre.upper(),
                        'apellido_paterno': apellido_paterno.upper(),
                        'apellido_materno': apellido_materno.upper(),
                        'fecha_nacimiento': fecha_nacimiento,
                        'sexo': sexo.upper(),
                        'estado_civil': estado_civil,
                        'direccion': direccion.upper(),
                        'numero_telefono1': numero_telefono1,
                        'numero_telefono2': numero_telefono2 or None,
                        'comuna': comuna,
                        'prevision': prevision,
                        'genero': genero,
                        'nombre_social': nombre_social.upper() or None,
                        'pasaporte': pasaporte.upper() or None,
                        'nombres_padre': nombres_padre.upper() or None,
                        'nombres_madre': nombres_madre.upper() or None,
                        'nombre_pareja': nombre_pareja.upper() or None,
                        'representante_legal': representante_legal.upper() or None,
                        'ocupacion': ocupacion.upper() or None,
                        'rut_madre': rut_madre.upper() or None,
                        'rut_responsable_temporal': rut_responsable_temporal.upper() or None,
                        'sin_telefono': sin_telefono,
                        'recien_nacido': recien_nacido,
                        'extranjero': extranjero,
                        'fallecido': fallecido,
                        'fecha_fallecimiento': fecha_fallecimiento,
                        'usar_rut_madre_como_responsable': usar_rut_madre_como_responsable
                    }
                )

                if created:
                    total_creados += 1
                else:
                    total_actualizados += 1

            except Exception as e:
                self.stdout.write(self.style.ERROR(f'❌ Error en fila {index + 2}: {e}'))

        self.stdout.write(self.style.SUCCESS(
            f'✅ Pacientes procesados: {total_creados} nuevos, {total_actualizados} actualizados.'
        ))

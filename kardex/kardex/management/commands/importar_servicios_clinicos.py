import pandas as pd
from django.core.management.base import BaseCommand

from kardex.models import ServicioClinico, Establecimiento


class Command(BaseCommand):
    help = 'Importa servicios clínicos desde una hoja llamada "servicio_clinico" en un archivo Excel'

    def add_arguments(self, parser):
        parser.add_argument(
            'excel_path',
            type=str,
            help='Ruta al archivo Excel que contiene la hoja "servicio_clinico"'
        )

    def handle(self, *args, **options):
        excel_path = options['excel_path']

        try:
            df = pd.read_excel(excel_path, sheet_name='servicio_clinico')
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'❌ Error al leer el archivo: {e}'))
            return

        df.columns = df.columns.str.strip()  # Eliminar espacios en los nombres de columnas

        total_importados = 0
        total_actualizados = 0

        for index, row in df.iterrows():
            nombre = str(row.get('nombre', '')).strip()
            tiempo_horas = row.get('tiempo_horas')
            correo_jefe = str(row.get('correo_jefe', '')).strip()
            telefono = str(row.get('telefono', '')).strip()
            establecimiento_id_raw = row.get('establecimiento_id')

            if not nombre:
                self.stdout.write(self.style.WARNING(
                    f'⚠️ Fila {index + 2} sin nombre, tiempo_horas o correo_jefe. Se omite.'
                ))
                continue

            # Buscar establecimiento
            establecimiento_obj = None
            if pd.notna(establecimiento_id_raw) and establecimiento_id_raw != '':
                try:
                    establecimiento_id = int(establecimiento_id_raw)
                    establecimiento_obj = Establecimiento.objects.filter(id=establecimiento_id).first()
                    if not establecimiento_obj:
                        self.stdout.write(self.style.WARNING(
                            f'⚠️ Fila {index + 2}: Establecimiento ID {establecimiento_id} no encontrado.'
                        ))
                except ValueError:
                    self.stdout.write(self.style.WARNING(
                        f'⚠️ Fila {index + 2}: Establecimiento ID inválido: {establecimiento_id_raw}.'
                    ))

            # Crear o actualizar el servicio clínico
            obj, created = ServicioClinico.objects.update_or_create(
                nombre=nombre.upper(),
                defaults={
                    'tiempo_horas': int(tiempo_horas),
                    'correo_jefe': correo_jefe.lower(),
                    'telefono': telefono,
                    'establecimiento': establecimiento_obj
                }
            )

            if created:
                total_importados += 1
            else:
                total_actualizados += 1

        self.stdout.write(self.style.SUCCESS(
            f'✅ Importación completada: {total_importados} nuevos, {total_actualizados} actualizados.'
        ))

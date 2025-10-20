import pandas as pd
from django.core.management.base import BaseCommand

from kardex.models import Comuna, Pais


class Command(BaseCommand):
    help = 'Importa comunas desde una hoja llamada "comuna" en un archivo Excel'

    def add_arguments(self, parser):
        parser.add_argument(
            'excel_path',
            type=str,
            help='Ruta al archivo Excel que contiene la hoja "comuna"'
        )

    def handle(self, *args, **options):
        excel_path = options['excel_path']

        try:
            df = pd.read_excel(excel_path, sheet_name='comuna')
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Error al leer el archivo: {e}'))
            return

        total_importadas = 0
        total_actualizadas = 0

        for index, row in df.iterrows():
            nombre = str(row.get('nombre', '')).strip()
            codigo = str(row.get('codigo', '')).strip()
            pais_nombre = str(row.get('pais', '')).strip()

            if not nombre:
                continue

            # Buscar país si se especificó
            pais_obj = None
            if pais_nombre:
                pais_obj = Pais.objects.filter(nombre__iexact=pais_nombre).first()

            # Guardar o actualizar comuna
            obj, created = Comuna.objects.update_or_create(
                nombre__iexact=nombre,  # Ignorar mayúsculas/minúsculas
                defaults={
                    'nombre': nombre.upper(),  # Asegurar mayúsculas
                    'codigo': codigo,
                    'pais': pais_obj
                }
            )

            if created:
                total_importadas += 1
            else:
                total_actualizadas += 1

        self.stdout.write(self.style.SUCCESS(
            f'✅ Importación completada: {total_importadas} nuevas, {total_actualizadas} actualizadas.'
        ))

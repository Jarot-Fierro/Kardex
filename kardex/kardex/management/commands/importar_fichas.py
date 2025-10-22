import pandas as pd
from django.core.management.base import BaseCommand
from django.utils import timezone

from kardex.models import Ficha, Paciente, Establecimiento
from usuarios.models import UsuarioPersonalizado


class Command(BaseCommand):
    help = 'Importa fichas desde una hoja llamada "fichas" en un archivo Excel'

    def add_arguments(self, parser):
        parser.add_argument(
            'excel_path',
            type=str,
            help='Ruta al archivo Excel que contiene la hoja "fichas"'
        )

    def handle(self, *args, **options):
        excel_path = options['excel_path']

        try:
            df = pd.read_excel(excel_path, sheet_name='ficha')
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'❌ Error al leer el archivo: {e}'))
            return

        total_importados = 0
        total_omitidos = 0

        for index, row in df.iterrows():
            fila = index + 2  # por cabecera en Excel

            # Campos base
            est_id = row.get('establecimiento_id')
            paciente_rut = str(row.get('paciente_id', '')).strip()
            numero_ficha_sistema = row.get('numero_ficha_sistema')
            usuario_rut = str(row.get('usuario_id', '')).strip()
            observacion = str(row.get('observacion', '')).strip()
            fecha_raw = row.get('fecha_creacion_anterior')

            # Validaciones mínimas
            if not paciente_rut or pd.isna(paciente_rut):
                self.stdout.write(self.style.WARNING(f'⚠️ Fila {fila}: RUT paciente faltante. Se omite.'))
                total_omitidos += 1
                continue

            try:
                paciente = Paciente.objects.get(rut__iexact=paciente_rut)
            except Paciente.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'⚠️ Fila {fila}: Paciente con RUT {paciente_rut} no encontrado.'))
                total_omitidos += 1
                continue

            usuario = UsuarioPersonalizado.objects.filter(username__iexact=usuario_rut).first() if usuario_rut else None
            establecimiento = Establecimiento.objects.filter(id=est_id).first() if pd.notna(est_id) else None

            if not establecimiento:
                self.stdout.write(self.style.WARNING(f'⚠️ Fila {fila}: Establecimiento {est_id} no encontrado.'))
                total_omitidos += 1
                continue

            # Parsear fecha
            fecha_creacion_anterior = None
            if pd.notna(fecha_raw):
                try:
                    fecha_creacion_anterior = timezone.make_aware(pd.to_datetime(fecha_raw))
                except Exception:
                    self.stdout.write(self.style.WARNING(f'⚠️ Fila {fila}: Fecha inválida: {fecha_raw}. Se omite.'))
                    total_omitidos += 1
                    continue

            # Verificar si ya existe una ficha con ese número en ese establecimiento
            ya_existe = Ficha.objects.filter(
                numero_ficha_sistema=numero_ficha_sistema,
                establecimiento=establecimiento
            ).exists()

            if ya_existe:
                self.stdout.write(self.style.WARNING(
                    f'⚠️ Fila {fila}: Ficha #{numero_ficha_sistema} ya existe para el establecimiento {establecimiento.nombre}. Se omite.'
                ))
                total_omitidos += 1
                continue

            # Crear ficha
            ficha = Ficha.objects.create(
                numero_ficha_sistema=numero_ficha_sistema,
                observacion=observacion.upper() if observacion else '',
                usuario=usuario,
                paciente=paciente,
                establecimiento=establecimiento,
                fecha_creacion_anterior=fecha_creacion_anterior
            )

            total_importados += 1

        self.stdout.write(self.style.SUCCESS(
            f'✅ Fichas procesadas: {total_importados} importadas, {total_omitidos} omitidas.'
        ))

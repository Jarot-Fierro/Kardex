import pandas as pd
from django.core.management.base import BaseCommand
from django.utils import timezone

from kardex.models import (
    MovimientoFicha,
    ServicioClinico,
    Ficha,
    Profesional,
)
from usuarios.models import UsuarioPersonalizado


class Command(BaseCommand):
    help = 'Importa movimientos de fichas desde una hoja llamada "movimiento_ficha" en un archivo Excel.'

    def add_arguments(self, parser):
        parser.add_argument(
            'excel_path',
            type=str,
            help='Ruta al archivo Excel que contiene la hoja "movimiento_ficha"',
        )

    def handle(self, *args, **options):
        excel_path = options['excel_path']

        try:
            df = pd.read_excel(excel_path, sheet_name='movimiento_ficha')
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'❌ Error al leer el archivo: {e}'))
            return

        df.columns = df.columns.str.strip()  # eliminar espacios
        total_importados = 0
        total_actualizados = 0

        for index, row in df.iterrows():
            # === Campos principales ===
            ficha_id_raw = row.get('ficha_id')
            servicio_envio_id = row.get('servicio_clinico_envio_id')
            servicio_recepcion_id = row.get('servicio_clinico_recepcion_id')
            servicio_traspaso_id = row.get('servicio_clinico_traspaso_id')

            usuario_envio_id = row.get('usuario_envio_id')
            usuario_recepcion_id = row.get('usuario_recepcion_id')
            usuario_traspaso_id = row.get('usuario_traspaso_id')

            profesional_envio_id = row.get('profesional_envio_id')
            profesional_recepcion_id = row.get('profesional_recepcion_id')
            profesional_traspaso_id = row.get('profesional_traspaso_id')

            observacion_envio = str(row.get('observacion_envio', '')).strip()
            observacion_recepcion = str(row.get('observacion_recepcion', '')).strip()
            observacion_traspaso = str(row.get('observacion_traspaso', '')).strip()

            estado_envio = str(row.get('estado_envio', '')).strip() or 'ENVIADO'
            estado_recepcion = str(row.get('estado_recepcion', '')).strip() or 'EN ESPERA'
            estado_traspaso = str(row.get('estado_traspaso', '')).strip() or 'SIN TRASPASO'

            # === Fechas ===
            fecha_envio = self.parse_fecha(row.get('fecha_envio'))
            fecha_recepcion = self.parse_fecha(row.get('fecha_recepcion'))
            fecha_traspaso = self.parse_fecha(row.get('fecha_traspaso'))

            # === Relaciones ===
            ficha_obj = Ficha.objects.filter(id=ficha_id_raw).first() if pd.notna(ficha_id_raw) else None
            if not ficha_obj:
                self.stdout.write(self.style.WARNING(
                    f'⚠️ Fila {index + 2}: Ficha ID {ficha_id_raw} no encontrada. Se omite.'
                ))
                continue

            servicio_envio = self.safe_get(ServicioClinico, servicio_envio_id, 'servicio_envio', index)
            servicio_recepcion = self.safe_get(ServicioClinico, servicio_recepcion_id, 'servicio_recepcion', index)
            servicio_traspaso = self.safe_get(ServicioClinico, servicio_traspaso_id, 'servicio_traspaso', index)

            usuario_envio = self.safe_get(UsuarioPersonalizado, usuario_envio_id, 'usuario_envio', index)
            usuario_recepcion = self.safe_get(UsuarioPersonalizado, usuario_recepcion_id, 'usuario_recepcion', index)
            usuario_traspaso = self.safe_get(UsuarioPersonalizado, usuario_traspaso_id, 'usuario_traspaso', index)

            profesional_envio = self.safe_get(Profesional, profesional_envio_id, 'profesional_envio', index)
            profesional_recepcion = self.safe_get(Profesional, profesional_recepcion_id, 'profesional_recepcion', index)
            profesional_traspaso = self.safe_get(Profesional, profesional_traspaso_id, 'profesional_traspaso', index)

            # === Crear o actualizar ===
            obj, created = MovimientoFicha.objects.update_or_create(
                ficha=ficha_obj,
                fecha_envio=fecha_envio,
                defaults={
                    'fecha_recepcion': fecha_recepcion,
                    'fecha_traspaso': fecha_traspaso,
                    'observacion_envio': observacion_envio,
                    'observacion_recepcion': observacion_recepcion,
                    'observacion_traspaso': observacion_traspaso,
                    'estado_envio': estado_envio,
                    'estado_recepcion': estado_recepcion,
                    'estado_traspaso': estado_traspaso,
                    'servicio_clinico_envio': servicio_envio,
                    'servicio_clinico_recepcion': servicio_recepcion,
                    'servicio_clinico_traspaso': servicio_traspaso,
                    'usuario_envio': usuario_envio,
                    'usuario_recepcion': usuario_recepcion,
                    'usuario_traspaso': usuario_traspaso,
                    'profesional_envio': profesional_envio,
                    'profesional_recepcion': profesional_recepcion,
                    'profesional_traspaso': profesional_traspaso,
                },
            )

            if created:
                total_importados += 1
            else:
                total_actualizados += 1

        self.stdout.write(self.style.SUCCESS(
            f'✅ Importación completada: {total_importados} nuevos, {total_actualizados} actualizados.'
        ))

    # === Utilidades ===
    def safe_get(self, model, pk, nombre, index):
        """
        Devuelve la instancia del modelo o None si no existe, con aviso en consola.
        """
        if pd.isna(pk) or pk == '':
            return None
        try:
            pk = int(pk)
            obj = model.objects.filter(id=pk).first()
            if not obj:
                self.stdout.write(self.style.WARNING(
                    f'⚠️ Fila {index + 2}: {nombre} ID {pk} no encontrado.'
                ))
            return obj
        except ValueError:
            self.stdout.write(self.style.WARNING(
                f'⚠️ Fila {index + 2}: {nombre} ID inválido: {pk}.'
            ))
            return None

    def parse_fecha(self, value):
        """
        Convierte una fecha del Excel a datetime (o None si no es válida).
        """
        if pd.isna(value) or value == '':
            return None
        try:
            if isinstance(value, pd.Timestamp):
                return value.to_pydatetime()
            return pd.to_datetime(value)
        except Exception:
            return timezone.now()

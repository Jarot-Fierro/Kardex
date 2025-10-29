import pandas as pd
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.utils.timezone import make_aware

from kardex.models import (
    MovimientoFicha,
    ServicioClinico,
    Ficha,
    Profesional,
    Establecimiento,
    UsuarioAnterior,
)


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

        df.columns = df.columns.str.strip()
        total_importados = 0
        total_actualizados = 0

        for index, row in df.iterrows():
            # === Limpieza general de datos ===
            row = row.fillna('')

            # === Lectura de campos ===
            establecimiento_id = self.to_int_or_none(row.get('establecimiento'))
            rut_anterior = str(row.get('rut_anterior', '')).strip() or 'SIN RUT'
            ficha_id = self.to_int_or_none(row.get('ficha'))

            fecha_envio = self.parse_fecha(row.get('fecha_envio'))
            fecha_recepcion = self.parse_fecha(row.get('fecha_recepcion'))

            usuario_envio_anterior_rut = str(row.get('usuario_envio_anterior', '')).strip()
            usuario_recepcion_anterior_rut = str(row.get('usuario_recepcion_anterior', '')).strip()
            profesional_recepcion_rut = str(row.get('profesional_recepcion', '')).strip()
            servicio_recepcion_id = self.to_int_or_none(row.get('servicio_clinico_recepcion'))

            observacion_envio = str(row.get('observacion_envio', '')).strip()
            observacion_recepcion = str(row.get('observacion_recepcion', '')).strip()
            observacion_traspaso = str(row.get('observacion_traspaso', '')).strip()

            # === Estado ===
            estado_raw = str(row.get('estado_recepcion', '')).strip().upper()
            estado_recepcion = self.map_estado(estado_raw)
            # Si no hay valor en Excel, lo deja "EN ESPERA", pero si hay algo reconocible, lo respeta.
            estado_envio = 'ENVIADO' if estado_recepcion != 'RECIBIDO' else 'ENVIADO'
            estado_traspaso = 'SIN TRASPASO'

            # === Relaciones ===
            ficha_obj = Ficha.objects.filter(id=ficha_id).first() if ficha_id else None
            if not ficha_obj:
                self.stdout.write(self.style.WARNING(
                    f'⚠️ Fila {index + 2}: Ficha ID {ficha_id} no encontrada. Se omite.'
                ))
                continue

            establecimiento = self.safe_get(Establecimiento, establecimiento_id, 'establecimiento', index)
            servicio_recepcion = self.safe_get(ServicioClinico, servicio_recepcion_id, 'servicio_clinico_recepcion',
                                               index)
            usuario_envio_anterior = self.safe_get_by_rut(UsuarioAnterior, usuario_envio_anterior_rut,
                                                          'usuario_envio_anterior', index)
            usuario_recepcion_anterior = self.safe_get_by_rut(UsuarioAnterior, usuario_recepcion_anterior_rut,
                                                              'usuario_recepcion_anterior', index)
            profesional_recepcion = self.safe_get_by_rut(Profesional, profesional_recepcion_rut,
                                                         'profesional_recepcion', index)

            # === Crear o actualizar ===
            obj, created = MovimientoFicha.objects.update_or_create(
                ficha=ficha_obj,
                fecha_envio=fecha_envio,
                defaults={
                    'fecha_recepcion': fecha_recepcion,
                    'observacion_envio': observacion_envio,
                    'observacion_recepcion': observacion_recepcion,
                    'observacion_traspaso': observacion_traspaso,
                    'estado_envio': estado_envio,
                    'estado_recepcion': estado_recepcion,
                    'estado_traspaso': estado_traspaso,
                    'servicio_clinico_recepcion': servicio_recepcion,
                    'usuario_envio_anterior': usuario_envio_anterior,
                    'usuario_recepcion_anterior': usuario_recepcion_anterior,
                    'profesional_recepcion': profesional_recepcion,
                    'establecimiento': establecimiento,
                    'rut_anterior': rut_anterior or 'SIN RUT',
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
        """Obtiene instancia por PK si existe."""
        if not pk:
            return None
        obj = model.objects.filter(id=pk).first()
        if not obj:
            self.stdout.write(self.style.WARNING(f'⚠️ Fila {index + 2}: {nombre} ID {pk} no encontrado.'))
        return obj

    def safe_get_by_rut(self, model, rut, nombre, index):
        """Obtiene instancia por campo RUT si aplica."""
        if not rut or rut.strip() in ('', '0', 'SIN RUT', 'NULL'):
            return None
        obj = model.objects.filter(rut=rut.strip()).first()
        if not obj:
            self.stdout.write(self.style.WARNING(f'⚠️ Fila {index + 2}: {nombre} con RUT {rut} no encontrado.'))
        return obj

    def parse_fecha(self, value):
        """Convierte fechas del Excel a datetime aware (con zona horaria)."""
        if pd.isna(value) or value == '' or str(value).upper() == 'NULL':
            return timezone.now()
        try:
            if isinstance(value, pd.Timestamp):
                dt = value.to_pydatetime()
            else:
                dt = pd.to_datetime(value)
            # Si es una fecha naive, agregar zona horaria
            if timezone.is_naive(dt):
                dt = make_aware(dt, timezone.get_current_timezone())
            return dt
        except Exception:
            return timezone.now()

    def to_int_or_none(self, value):
        try:
            if pd.isna(value) or str(value).strip() in ('', 'NULL'):
                return None
            return int(value)
        except Exception:
            return None

    def map_estado(self, estado):
        """Mapea las letras o abreviaciones del Excel a tus choices con debug."""
        # Convertir a string y limpiar
        estado_str = str(estado).upper().strip()

        if estado_str in ['R', 'RECIBIDO']:
            return 'RECIBIDO'
        elif estado_str in ['E', 'ENVIADO']:
            return 'ENVIADO'
        elif estado_str in ['P', 'PENDIENTE']:
            return 'EN ESPERA'
        else:
            return 'EN ESPERA'

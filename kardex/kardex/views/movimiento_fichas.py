from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views.generic import TemplateView

from kardex.mixin import DataTableMixin
from kardex.models import MovimientoFicha, Paciente, Ficha, ServicioClinico


class _BaseMovimientoFichaView(LoginRequiredMixin, DataTableMixin, TemplateView):
    model = MovimientoFicha

    # DataTable defaults (can be customized by subclasses)
    datatable_columns = []
    datatable_order_fields = []
    datatable_search_fields = []

    def get_base_queryset(self):
        qs = super().get_base_queryset()
        # Ensure filtering by establishment of the logged-in user
        establecimiento = getattr(self.request.user, 'establecimiento', None)
        if establecimiento is not None:
            qs = qs.filter(ficha__ingreso_paciente__establecimiento=establecimiento)
        return qs.select_related('ficha', 'ficha__ingreso_paciente', 'ficha__ingreso_paciente__paciente',
                                 'servicio_clinico', 'usuario')

    def get(self, request, *args, **kwargs):
        # Datatable AJAX
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest' and request.GET.get('datatable'):
            return self.get_datatable_response(request)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        from kardex.models import ServicioClinico
        ctx['servicio_clinicos'] = ServicioClinico.objects.all().order_by('nombre')
        return ctx

    # Helpers for creating MovimientoFicha from POST
    def _resolve_ficha_from_inputs(self, rut: str, numero_ficha: str):
        establecimiento = getattr(self.request.user, 'establecimiento', None)
        if not establecimiento:
            return None
        paciente = None
        if rut:
            paciente = Paciente.objects.filter(
                ingresopaciente__establecimiento=establecimiento,
                rut__iexact=rut
            ).distinct().first()
        ficha = None
        if numero_ficha:
            ficha = Ficha.objects.filter(
                ingreso_paciente__establecimiento=establecimiento,
                numero_ficha=numero_ficha
            ).select_related('ingreso_paciente__paciente').first()
        if not ficha and paciente:
            # If ficha not provided, try to find ficha by paciente within establecimiento
            ficha = Ficha.objects.filter(
                ingreso_paciente__establecimiento=establecimiento,
                ingreso_paciente__paciente=paciente
            ).first()
        return ficha

    def post(self, request, *args, **kwargs):
        # Minimal handler to create a movement entry
        action = request.POST.get('action')  # 'recepcion' or 'salida'
        rut = (request.POST.get('rut') or '').strip()
        numero_ficha = (request.POST.get('ficha') or '').strip()
        servicio_id = request.POST.get('servicio_clinico')
        profesional_id = request.POST.get('profesional')  # optional; if empty use current user
        fecha_str = request.POST.get('fecha')  # ISO or "YYYY-MM-DD HH:MM"
        observacion = request.POST.get('observacion')

        ficha = self._resolve_ficha_from_inputs(rut, numero_ficha)
        if not ficha:
            return JsonResponse({'ok': False, 'error': 'No se pudo resolver la ficha para el RUT/N° entregado.'},
                                status=400)

        servicio = None
        if servicio_id:
            servicio = get_object_or_404(ServicioClinico, id=servicio_id)

        usuario = request.user if getattr(request.user, 'is_authenticated', False) else None

        # Parse fecha
        fecha_val = None
        if fecha_str:
            try:
                # Try parse using timezone-aware now as fallback
                # Let Django parse common formats automatically via fromisoformat when available
                try:
                    from datetime import datetime
                    fecha_val = datetime.fromisoformat(fecha_str)
                except Exception:
                    # Fallback to input like 'YYYY-MM-DD HH:MM'
                    from datetime import datetime
                    fecha_val = datetime.strptime(fecha_str, '%Y-%m-%d %H:%M')
            except Exception:
                fecha_val = timezone.now()
        else:
            fecha_val = timezone.now()

        mov = MovimientoFicha(
            ficha=ficha,
            servicio_clinico=servicio,
            usuario=usuario,
            observacion_salida=observacion if action == 'salida' else None,
            observacion_entrada=observacion if action == 'recepcion' else None,
            fecha_mov=fecha_val,
        )
        if action == 'salida':
            mov.fecha_salida = fecha_val
        elif action == 'recepcion':
            mov.fecha_entrada = fecha_val
        mov.save()
        return JsonResponse({'ok': True, 'id': mov.id})


class RecepcionFichaView(_BaseMovimientoFichaView):
    template_name = 'kardex/movimiento_ficha/recepcion_ficha.html'
    datatable_columns = ['RUT', 'Ficha', 'Nombre completo', 'Servicio Clínico', 'Profesional', 'Fecha de salida',
                         'Estado']
    datatable_order_fields = ['ficha__ingreso_paciente__paciente__rut', 'ficha__numero_ficha',
                              'ficha__ingreso_paciente__paciente__apellido_paterno',
                              'servicio_clinico__nombre', 'usuario__username', 'fecha_salida', 'estado_respuesta']
    datatable_search_fields = [
        'ficha__ingreso_paciente__paciente__rut__icontains',
        'ficha__numero_ficha__icontains',
        'ficha__ingreso_paciente__paciente__nombre__icontains',
        'ficha__ingreso_paciente__paciente__apellido_paterno__icontains',
        'ficha__ingreso_paciente__paciente__apellido_materno__icontains',
        'servicio_clinico__nombre__icontains',
        'usuario__username__icontains',
    ]

    def render_row(self, obj):
        pac = obj.ficha.ingreso_paciente.paciente if obj.ficha and obj.ficha.ingreso_paciente else None
        nombre = f"{getattr(pac, 'nombre', '')} {getattr(pac, 'apellido_paterno', '')} {getattr(pac, 'apellido_materno', '')}" if pac else ''
        return {
            'RUT': getattr(pac, 'rut', '') if pac else '',
            'Ficha': getattr(obj.ficha, 'numero_ficha', '') if obj.ficha else '',
            'Nombre completo': nombre.strip(),
            'Servicio Clínico': getattr(obj.servicio_clinico, 'nombre', ''),
            'Profesional': getattr(obj.usuario, 'username', ''),
            'Fecha de salida': obj.fecha_salida.strftime('%Y-%m-%d %H:%M') if obj.fecha_salida else '',
            'Estado': obj.estado_respuesta,
        }


class SalidaFichaView(_BaseMovimientoFichaView):
    template_name = 'kardex/movimiento_ficha/salida_ficha.html'
    datatable_columns = ['RUT', 'Ficha', 'Nombre completo', 'Servicio Clínico', 'Profesional', 'Observación salida',
                         'Fecha/hora salida', 'Fecha entrada', 'Estado']
    datatable_order_fields = ['ficha__ingreso_paciente__paciente__rut', 'ficha__numero_ficha',
                              'ficha__ingreso_paciente__paciente__apellido_paterno',
                              'servicio_clinico__nombre', 'usuario__username',
                              'observacion_salida', 'fecha_salida', 'fecha_entrada', 'estado_respuesta']
    datatable_search_fields = [
        'ficha__ingreso_paciente__paciente__rut__icontains',
        'ficha__numero_ficha__icontains',
        'ficha__ingreso_paciente__paciente__nombre__icontains',
        'ficha__ingreso_paciente__paciente__apellido_paterno__icontains',
        'ficha__ingreso_paciente__paciente__apellido_materno__icontains',
        'servicio_clinico__nombre__icontains',
        'usuario__username__icontains',
        'observacion_salida__icontains',
    ]

    def get_base_queryset(self):
        qs = super().get_base_queryset()
        # Apply filters from GET: date range, servicio clinico, profesional
        inicio = self.request.GET.get('inicio')
        termino = self.request.GET.get('termino')
        servicio_id = self.request.GET.get('servicio')
        profesional_id = self.request.GET.get('profesional')

        if inicio:
            try:
                from datetime import datetime
                dt = datetime.fromisoformat(inicio)
                qs = qs.filter(fecha_salida__gte=dt)
            except Exception:
                pass
        if termino:
            try:
                from datetime import datetime
                dt = datetime.fromisoformat(termino)
                qs = qs.filter(fecha_salida__lte=dt)
            except Exception:
                pass
        if servicio_id:
            qs = qs.filter(servicio_clinico_id=servicio_id)
        if profesional_id:
            qs = qs.filter(usuario_id=profesional_id)
        return qs

    def render_row(self, obj):
        pac = obj.ficha.ingreso_paciente.paciente if obj.ficha and obj.ficha.ingreso_paciente else None
        nombre = f"{getattr(pac, 'nombre', '')} {getattr(pac, 'apellido_paterno', '')} {getattr(pac, 'apellido_materno', '')}" if pac else ''
        return {
            'RUT': getattr(pac, 'rut', '') if pac else 'Sin Rut',
            'Ficha': getattr(obj.ficha, 'numero_ficha', '') if obj.ficha else '',
            'Nombre completo': nombre.strip(),
            'Servicio Clínico': getattr(obj.servicio_clinico, 'nombre', ''),
            'Profesional': getattr(obj.usuario, 'username', ''),
            'Observación salida': obj.observacion_salida or '',
            'Fecha/hora salida': obj.fecha_salida.strftime('%Y-%m-%d %H:%M') if obj.fecha_salida else '',
            'Fecha entrada': obj.fecha_entrada.strftime('%Y-%m-%d %H:%M') if obj.fecha_entrada else '',
            'Estado': obj.estado_respuesta,
        }

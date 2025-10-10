from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import DeleteView, CreateView, UpdateView, DetailView
from django.views.generic import TemplateView, FormView

from kardex.forms.movimiento_ficha import FormEntradaFicha, FormSalidaFicha, FiltroSalidaFichaForm
from kardex.mixin import DataTableMixin
from kardex.models import MovimientoFicha
from kardex.models import Paciente, Ficha, ServicioClinico, Profesional


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


class RecepcionFichaView(_BaseMovimientoFichaView, FormView):
    template_name = 'kardex/movimiento_ficha/recepcion_ficha.html'
    form_class = FormEntradaFicha
    success_url = reverse_lazy('kardex:recepcion_ficha')

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

    # Keep DataTable GET behavior from base; route POST to FormView
    def post(self, request, *args, **kwargs):
        return FormView.post(self, request, *args, **kwargs)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        try:
            est = getattr(self.request.user, 'establecimiento', None)
            if est and 'profesional' in form.fields:
                form.fields['profesional'].queryset = Profesional.objects.filter(establecimiento=est)
        except Exception:
            pass
        return form

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        form = kwargs.get('form') or self.get_form()
        ctx['form'] = form
        return ctx

    def form_valid(self, form):
        obj = form.save(commit=False)
        # asegurar usuario actual como ejecutor si el modelo lo soporta
        if hasattr(obj, 'usuario') and getattr(self.request, 'user', None):
            obj.usuario = self.request.user
        # si el modelo tiene fecha_mov, podemos alinearla con fecha_entrada
        if hasattr(obj, 'fecha_mov') and hasattr(obj, 'fecha_entrada') and obj.fecha_entrada:
            obj.fecha_mov = obj.fecha_entrada
        obj.save()
        messages.success(self.request, 'Recepción registrada correctamente.')
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'ok': True, 'id': obj.id})
        return super().form_valid(form)

    def form_invalid(self, form):
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'ok': False, 'errors': form.errors}, status=400)
        messages.error(self.request, 'El formulario contiene errores. Por favor, verifique los campos.')
        context = self.get_context_data(form=form)
        return self.render_to_response(context)

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


class SalidaFichaView(_BaseMovimientoFichaView, FormView):
    template_name = 'kardex/movimiento_ficha/salida_ficha.html'
    form_class = FormSalidaFicha
    success_url = reverse_lazy('kardex:salida_ficha')

    datatable_columns = ['ID', 'RUT', 'Ficha', 'Nombre completo', 'Servicio Clínico', 'Profesional', 'Observación salida',
                         'Fecha/hora salida', 'Fecha entrada', 'Estado']
    datatable_order_fields = ['id', None, 'ficha__ingreso_paciente__paciente__rut', 'ficha__numero_ficha',
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

    # Keep DataTable GET behavior from base; route POST to FormView
    def post(self, request, *args, **kwargs):
        return FormView.post(self, request, *args, **kwargs)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        try:
            est = getattr(self.request.user, 'establecimiento', None)
            if est and 'profesional' in form.fields:
                form.fields['profesional'].queryset = Profesional.objects.filter(establecimiento=est)
        except Exception:
            pass
        return form

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        form = kwargs.get('form') or self.get_form()
        # Filtro
        filter_form = FiltroSalidaFichaForm(self.request.GET or None)
        try:
            est = getattr(self.request.user, 'establecimiento', None)
            if est and 'profesional' in filter_form.fields:
                filter_form.fields['profesional'].queryset = Profesional.objects.filter(establecimiento=est)
        except Exception:
            pass
        ctx['form'] = form
        ctx['filter_form'] = filter_form
        # Habilitar DataTable en base.html y definir columnas
        ctx['datatable_enabled'] = True
        ctx['datatable_order'] = [[0, 'asc']]
        ctx['columns'] = self.datatable_columns
        return ctx

    def form_valid(self, form):
        obj = form.save(commit=False)
        if hasattr(obj, 'usuario') and getattr(self.request, 'user', None):
            obj.usuario = self.request.user
        if hasattr(obj, 'fecha_mov') and hasattr(obj, 'fecha_salida') and obj.fecha_salida:
            obj.fecha_mov = obj.fecha_salida
        obj.save()
        messages.success(self.request, 'Salida registrada correctamente.')
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'ok': True, 'id': obj.id})
        return super().form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'ok': False, 'errors': form.errors}, status=400)
        messages.error(self.request, 'El formulario contiene errores. Por favor, verifique los campos.')
        context = self.get_context_data(form=form)
        return self.render_to_response(context)

    def get_base_queryset(self):
        qs = super().get_base_queryset()
        # Apply filters from GET: date range, servicio clinico, profesional
        inicio = self.request.GET.get('hora_inicio')
        termino = self.request.GET.get('hora_termino')
        servicio_id = self.request.GET.get('servicio_clinico')
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
            # profesional en movimiento es el usuario que realiza? en el modelo se guarda usuario
            qs = qs.filter(usuario_id=profesional_id)
        return qs

    def render_row(self, obj):
        pac = obj.ficha.ingreso_paciente.paciente if obj.ficha and obj.ficha.ingreso_paciente else None
        nombre = f"{getattr(pac, 'nombre', '')} {getattr(pac, 'apellido_paterno', '')} {getattr(pac, 'apellido_materno', '')}" if pac else ''
        return {
            'ID': obj.id,
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


MODULE_NAME = 'Movimientos de Ficha'


class MovimientoFichaListView(PermissionRequiredMixin, DataTableMixin, TemplateView):
    template_name = 'kardex/movimiento_ficha/list.html'
    model = MovimientoFicha
    datatable_columns = ['ID', 'Ficha', 'Servicio Clínico', 'Estado', 'Fecha Movimiento']
    datatable_order_fields = ['id', None, 'ficha__numero_ficha', 'servicio_clinico__nombre', 'estado_respuesta',
                              'fecha_mov']
    datatable_search_fields = [
        'ficha__numero_ficha__icontains', 'servicio_clinico__nombre__icontains', 'estado_respuesta__icontains'
    ]

    permission_required = 'kardex.view_movimiento_ficha'
    raise_exception = True

    permission_view = 'kardex.view_movimiento_ficha'
    permission_update = 'kardex.change_movimiento_ficha'
    permission_delete = 'kardex.delete_movimiento_ficha'

    url_detail = 'kardex:movimiento_ficha_detail'
    url_update = 'kardex:movimiento_ficha_update'
    url_delete = 'kardex:movimiento_ficha_delete'

    def render_row(self, obj):
        return {
            'ID': obj.id,
            'Ficha': getattr(obj.ficha, 'numero_ficha', '') if obj.ficha else '',
            'Servicio Clínico': (getattr(obj.servicio_clinico, 'nombre', '') or '').upper(),
            'Estado': obj.estado_respuesta,
            'Fecha Movimiento': obj.fecha_mov.strftime('%Y-%m-%d %H:%M') if obj.fecha_mov else '',
        }

    def get(self, request, *args, **kwargs):
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest' and request.GET.get('datatable'):
            return self.get_datatable_response(request)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': 'Listado de Movimientos de Ficha',
            'list_url': reverse_lazy('kardex:movimiento_ficha_list'),
            'create_url': reverse_lazy('kardex:movimiento_ficha_create'),
            'datatable_enabled': True,
            'datatable_order': [[0, 'asc']],
            'datatable_page_length': 100,
            'columns': self.datatable_columns,
        })
        return context


class MovimientoFichaDetailView(PermissionRequiredMixin, DetailView):
    model = MovimientoFicha
    template_name = 'kardex/movimiento_ficha/detail.html'

    permission_required = 'kardex.view_movimiento_ficha'
    raise_exception = True

    def render_to_response(self, context, **response_kwargs):
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            from django.template.loader import render_to_string
            html = render_to_string(self.template_name, context=context, request=self.request)
            return HttpResponse(html)
        return super().render_to_response(context, **response_kwargs)


class MovimientoFichaCreateView(PermissionRequiredMixin, CreateView):
    template_name = 'kardex/movimiento_ficha/form.html'
    model = MovimientoFicha
    fields = '__all__'
    success_url = reverse_lazy('kardex:movimiento_ficha_list')

    permission_required = 'kardex.add_movimiento_ficha'
    raise_exception = True

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        if form.is_valid():
            obj = form.save()
            if is_ajax:
                from django.http import JsonResponse
                return JsonResponse({'success': True, 'message': 'Movimiento de ficha creado correctamente',
                                     'redirect_url': str(self.success_url)})
            from django.contrib import messages
            from django.shortcuts import redirect
            messages.success(request, 'Movimiento de ficha creado correctamente')
            return redirect(self.success_url)
        if is_ajax:
            from django.http import JsonResponse
            return JsonResponse({'success': False, 'error': 'Hay errores en el formulario'}, status=400)
        from django.contrib import messages
        messages.error(request, 'Hay errores en el formulario')
        self.object = None
        return self.render_to_response(self.get_context_data(form=form, open_modal=True))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Nuevo Movimiento de Ficha'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        context['module_name'] = MODULE_NAME
        return context


class MovimientoFichaUpdateView(PermissionRequiredMixin, UpdateView):
    template_name = 'kardex/movimiento_ficha/form.html'
    model = MovimientoFicha
    fields = '__all__'
    success_url = reverse_lazy('kardex:movimiento_ficha_list')
    permission_required = 'kardex:change_movimientoficha'
    raise_exception = True

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        if form.is_valid():
            obj = form.save()
            if is_ajax:
                from django.http import JsonResponse
                return JsonResponse({'success': True, 'message': 'Movimiento de ficha actualizado correctamente',
                                     'redirect_url': str(self.success_url)})

            messages.success(request, 'Movimiento de ficha actualizado correctamente')
            return redirect(self.success_url)
        if is_ajax:
            from django.http import JsonResponse
            return JsonResponse({'success': False, 'error': 'Hay errores en el formulario'}, status=400)

        messages.error(request, 'Hay errores en el formulario')
        return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Movimiento de Ficha'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        context['module_name'] = MODULE_NAME
        return context


class MovimientoFichaDeleteView(PermissionRequiredMixin, DeleteView):
    model = MovimientoFicha
    template_name = 'kardex/movimiento_ficha/confirm_delete.html'
    success_url = reverse_lazy('kardex:movimiento_ficha_list')
    permission_required = 'kardex:delete_movimientoficha'

    def post(self, request, *args, **kwargs):
        from django.contrib import messages
        from django.shortcuts import redirect
        try:
            obj = self.get_object()
            obj.delete()
            messages.success(request, 'Movimiento de ficha eliminado correctamente')
        except Exception as e:
            messages.error(request, f'No se pudo eliminar el movimiento de ficha: {e}')
        return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar Movimiento de Ficha'
        context['list_url'] = self.success_url
        context['module_name'] = MODULE_NAME
        return context

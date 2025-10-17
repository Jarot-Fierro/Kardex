from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.timezone import now
from django.views.generic import DeleteView, CreateView, UpdateView, DetailView
from django.views.generic import TemplateView

from kardex.forms.movimiento_ficha import FormEntradaFicha, FiltroSalidaFichaForm
from kardex.forms.movimiento_ficha import FormSalidaFicha
from kardex.mixin import DataTableMixin
from kardex.models import MovimientoFicha
from kardex.models import Profesional


class RecepcionFichaView(LoginRequiredMixin, PermissionRequiredMixin, DataTableMixin, TemplateView):
    template_name = 'kardex/movimiento_ficha/recepcion_ficha.html'
    model = MovimientoFicha

    permission_required = 'kardex.view_movimientoficha'
    raise_exception = True

    datatable_columns = ['ID', 'RUT', 'Ficha', 'Nombre completo', 'Servicio Clínico', 'Profesional', 'Fecha de salida',
                         'Estado']
    datatable_order_fields = ['id', None, 'ficha__paciente__rut', 'ficha__numero_ficha_sistema',
                              'ficha__paciente__apellido_paterno',
                              'servicio_clinico_envio__nombre', 'usuario_envio__username', 'fecha_envio',
                              'estado_recepcion']
    datatable_search_fields = [
        'ficha__paciente__rut__icontains',
        'ficha__numero_ficha_sistema__icontains',
        'ficha__paciente__nombre__icontains',
        'ficha__paciente__apellido_paterno__icontains',
        'ficha__paciente__apellido_materno__icontains',
        'servicio_clinico_envio__nombre__icontains',
        'usuario_envio__username__icontains',
    ]

    def get(self, request, *args, **kwargs):
        # Soporte para AJAX DataTable
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest' and request.GET.get('datatable'):
            return self.get_datatable_response(request)
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = FormEntradaFicha(request.POST)
        if form.is_valid():
            # La recepción debe ACTUALIZAR el último movimiento de la ficha seleccionada
            ficha = form.cleaned_data.get('ficha')
            profesional_recepcion = form.cleaned_data.get('profesional_recepcion')
            servicio_clinico_recepcion = form.cleaned_data.get('servicio_clinico_recepcion')
            observacion_recepcion = form.cleaned_data.get('observacion_recepcion')
            fecha_recepcion = form.cleaned_data.get('fecha_recepcion')

            try:
                mov = MovimientoFicha.objects.filter(
                    ficha=ficha,
                    fecha_envio__isnull=False
                ).order_by('-fecha_envio').first()
            except Exception:
                mov = None

            if not mov:
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse(
                        {'ok': False, 'errors': {'ficha': ['No existe un envío previo para esta ficha.']}}, status=400)
                messages.error(request, 'No existe un envío previo para esta ficha.')
                context = self.get_context_data(form=form)
                return self.render_to_response(context)

            # Completar recepción sobre el movimiento encontrado
            # Si ya estaba recepcionado, no permitir re-modificar
            if mov.estado_recepcion == 'RECIBIDO':
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({'ok': False, 'errors': {'__all__': ['El movimiento ya fue recepcionado.']}},
                                        status=400)
                messages.error(request, 'El movimiento ya fue recepcionado.')
                context = self.get_context_data(form=form)
                return self.render_to_response(context)

            mov.usuario_recepcion = request.user
            mov.profesional_recepcion = profesional_recepcion
            mov.servicio_clinico_recepcion = servicio_clinico_recepcion
            mov.observacion_recepcion = observacion_recepcion
            mov.fecha_recepcion = fecha_recepcion or now()
            # No es necesario setear explícitamente estado a RECIBIDO; el modelo lo ajusta al guardar
            mov.save()

            messages.success(request, 'Recepción registrada correctamente.')
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'ok': True, 'id': mov.id})
            return self.get(request, *args, **kwargs)
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'ok': False, 'errors': form.errors}, status=400)
            messages.error(request, 'El formulario contiene errores. Por favor, verifique los campos.')
            context = self.get_context_data(form=form)
            return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = kwargs.get('form') or FormEntradaFicha()
        establecimiento = getattr(self.request.user, 'establecimiento', None)
        if establecimiento and 'profesional_recepcion' in form.fields:
            form.fields['profesional_recepcion'].queryset = Profesional.objects.filter(establecimiento=establecimiento)
        context.update({
            'title': 'Recepción de Fichas',
            'list_url': reverse_lazy('kardex:recepcion_ficha'),
            'datatable_enabled': True,
            'datatable_order': [[0, 'asc']],
            'columns': self.datatable_columns,
            'form': form,
        })
        return context

    def get_base_queryset(self):
        establecimiento = getattr(self.request.user, 'establecimiento', None)
        return MovimientoFicha.objects.filter(
            estado_recepcion__in=['EN ESPERA', 'RECIBIDO'],
            ficha__establecimiento=establecimiento
        ).select_related(
            'ficha__paciente',
            'servicio_clinico_envio',
            'usuario_envio'
        )

    def render_row(self, obj):
        pac = obj.ficha.paciente if obj.ficha else None
        nombre = f"{getattr(pac, 'nombre', '')} {getattr(pac, 'apellido_paterno', '')} {getattr(pac, 'apellido_materno', '')}" if pac else ''
        return {
            'ID': obj.id,
            'RUT': getattr(pac, 'rut', '') if pac else '',
            'Ficha': getattr(obj.ficha, 'numero_ficha_sistema', '') if obj.ficha else '',
            'Nombre completo': nombre.strip(),
            'Servicio Clínico': getattr(obj.servicio_clinico_envio, 'nombre', ''),
            'Profesional': getattr(obj.usuario_envio, 'username', ''),
            'Fecha de salida': obj.fecha_envio.strftime('%Y-%m-%d %H:%M') if obj.fecha_envio else '',
            'Estado': obj.estado_recepcion,
        }


class SalidaFichaView(LoginRequiredMixin, PermissionRequiredMixin, DataTableMixin, TemplateView):
    template_name = 'kardex/movimiento_ficha/salida_ficha.html'
    model = MovimientoFicha
    permission_required = 'kardex.view_movimientoficha'
    raise_exception = True

    datatable_columns = [
        'ID', 'RUT', 'Ficha', 'Nombre completo', 'Servicio Clínico Envío',
        'Usuario Envío', 'Observación envío', 'Fecha envío', 'Estado envio'
    ]
    datatable_order_fields = [
        'id', None, 'ficha__paciente__rut', 'ficha__numero_ficha_sistema',
        'ficha__paciente__apellido_paterno',
        'servicio_clinico_envio__nombre', 'usuario_envio__username',
        'observacion_envio', 'fecha_envio', 'estado_envio'
    ]
    datatable_search_fields = [
        'ficha__paciente__rut__icontains',
        'ficha__numero_ficha_sistema__icontains',
        'ficha__paciente__nombre__icontains',
        'ficha__paciente__apellido_paterno__icontains',
        'ficha__paciente__apellido_materno__icontains',
        'servicio_clinico_envio__nombre__icontains',
        'usuario_envio__username__icontains',
        'observacion_envio__icontains',
    ]

    def get(self, request, *args, **kwargs):
        # Si es llamada AJAX para DataTable
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest' and request.GET.get('datatable'):
            return self.get_datatable_response(request)
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = FormSalidaFicha(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.usuario_envio = request.user
            if getattr(obj, 'fecha_envio', None) is None:
                from django.utils.timezone import now as djnow
                obj.fecha_envio = djnow()
            # estados se mantienen por defecto en el modelo
            obj.save()
            messages.success(request, 'Salida registrada correctamente.')
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'ok': True, 'id': obj.id})
            return self.get(request, *args, **kwargs)
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'ok': False, 'errors': form.errors}, status=400)
            messages.error(request, 'El formulario contiene errores.')
            context = self.get_context_data(form=form)
            return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        establecimiento = getattr(self.request.user, 'establecimiento', None)

        # Formulario principal
        form = kwargs.get('form') or FormSalidaFicha()
        if establecimiento and 'profesional_envio' in form.fields:
            form.fields['profesional_envio'].queryset = Profesional.objects.filter(establecimiento=establecimiento)

        # Formulario de filtro
        filter_form = FiltroSalidaFichaForm(self.request.GET or None)
        if establecimiento and 'profesional' in filter_form.fields:
            filter_form.fields['profesional'].queryset = Profesional.objects.filter(establecimiento=establecimiento)

        context.update({
            'title': 'Salida de Fichas',
            'form': form,
            'filter_form': filter_form,
            'list_url': reverse_lazy('kardex:salida_ficha'),
            'datatable_enabled': True,
            'datatable_order': [[0, 'asc']],
            'columns': self.datatable_columns,
        })
        return context

    def get_base_queryset(self):
        qs = MovimientoFicha.objects.filter(estado_envio='ENVIADO').select_related(
            'ficha__paciente',
            'servicio_clinico_envio',
            'usuario_envio'
        )

        # Filtros desde filter_form
        inicio = self.request.GET.get('hora_inicio')
        termino = self.request.GET.get('hora_termino')
        servicio_id = self.request.GET.get('servicio_clinico')
        profesional_id = self.request.GET.get('profesional')

        if inicio:
            try:
                from datetime import datetime
                dt = datetime.fromisoformat(inicio)
                qs = qs.filter(fecha_envio__gte=dt)
            except Exception:
                pass
        if termino:
            try:
                from datetime import datetime
                dt = datetime.fromisoformat(termino)
                qs = qs.filter(fecha_envio__lte=dt)
            except Exception:
                pass
        if servicio_id:
            qs = qs.filter(servicio_clinico_envio_id=servicio_id)
        if profesional_id:
            qs = qs.filter(usuario_envio_id=profesional_id)

        return qs

    def render_row(self, obj):
        pac = obj.ficha.paciente if obj.ficha else None
        nombre = f"{getattr(pac, 'nombre', '')} {getattr(pac, 'apellido_paterno', '')} {getattr(pac, 'apellido_materno', '')}" if pac else ''
        return {
            'ID': obj.id,
            'RUT': getattr(pac, 'rut', '') if pac else '',
            'Ficha': getattr(obj.ficha, 'numero_ficha_sistema', '') if obj.ficha else '',
            'Nombre completo': nombre.strip(),
            'Servicio Clínico Envío': getattr(obj.servicio_clinico_envio, 'nombre', ''),
            'Usuario Envío': getattr(obj.usuario_envio, 'username', '') if obj.usuario_envio else '',
            'Observación envío': obj.observacion_envio or '',
            'Fecha envío': obj.fecha_envio.strftime('%Y-%m-%d %H:%M') if obj.fecha_envio else '',
            'Estado envio': obj.estado_envio or '',
        }


MODULE_NAME = 'Movimientos de Ficha'


class MovimientoFichaListView(PermissionRequiredMixin, DataTableMixin, TemplateView):
    template_name = 'kardex/movimiento_ficha/list.html'
    model = MovimientoFicha
    datatable_columns = ['ID', 'Ficha', 'Servicio Clínico', 'Estado', 'Fecha Movimiento']
    datatable_order_fields = ['id', None, 'ficha__numero_ficha_sistema', 'servicio_clinico_envio__nombre', 'estado_envio',
                              'fecha_envio']
    datatable_search_fields = [
        'ficha__numero_ficha_sistema__icontains', 'servicio_clinico_envio__nombre__icontains', 'estado_envio__icontains'
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
        pac = obj.ficha.paciente if obj.ficha else None
        nombre = f"{getattr(pac, 'nombre', '')} {getattr(pac, 'apellido_paterno', '')} {getattr(pac, 'apellido_materno', '')}" if pac else ''
        return {
            'ID': obj.id,
            'RUT': getattr(pac, 'rut', '') if pac else '',
            'Ficha': getattr(obj.ficha, 'numero_ficha_sistema', '') if obj.ficha else '',
            'Nombre completo': nombre.strip(),
            'Servicio Clínico Envío': getattr(obj.servicio_clinico_envio, 'nombre', ''),
            'Servicio Clínico Recepción': getattr(obj.servicio_clinico_recepcion, 'nombre', ''),
            'Profesional Envío': getattr(obj.profesional_envio, 'nombre_completo', '') if obj.profesional_envio else '',
            'Observación Envío': obj.observacion_envio or '',
            'Fecha/hora Envío': obj.fecha_envio.strftime('%Y-%m-%d %H:%M') if obj.fecha_envio else '',
            'Estado Envío': obj.estado_envio,
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

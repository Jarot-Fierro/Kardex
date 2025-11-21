from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.dateparse import parse_date
from django.views.generic import DeleteView, CreateView, DetailView, UpdateView
from django.views.generic import TemplateView, FormView

from kardex.forms.pacientes import FormPacienteCreacion, FormPaciente, FormPacienteActualizarRut
from kardex.forms.pacientes import PacienteFechaRangoForm
from kardex.mixin import DataTableMixin
from kardex.models import Ficha
from kardex.models import Paciente
from kardex.views.history import GenericHistoryListView

MODULE_NAME = 'Pacientes'


class PacienteListView(PermissionRequiredMixin, DataTableMixin, TemplateView):
    template_name = 'kardex/paciente/list.html'
    model = Paciente
    datatable_columns = ['ID', 'RUT', 'Nombre', 'Sexo', 'Estado Civil', 'Comuna', 'Previsión']
    datatable_order_fields = [
        'id',
        None,
        None,
        'sexo',
        'estado_civil',
        'comuna__nombre',
        'prevision__nombre'
    ]

    datatable_search_fields = [
        'rut__icontains',
        'nombre__icontains',
        'apellido_paterno__icontains',
        'apellido_materno__icontains',
        'sexo__icontains',
        'estado_civil__icontains',
        'comuna__nombre__icontains',
        'prevision__nombre__icontains'
    ]

    permission_view = 'kardex.view_paciente'
    permission_update = 'kardex.change_paciente'
    permission_delete = 'kardex.delete_paciente'

    permission_required = 'kardex.view_paciente'
    raise_exception = True

    url_detail = 'kardex:paciente_detail'
    url_update = 'kardex:paciente_update'
    url_delete = 'kardex:paciente_delete'

    def get_base_queryset(self):
        # Vista libre: no limitar por establecimiento, mostrar todos los pacientes
        return Paciente.objects.filter(status='ACTIVE')

    def render_row(self, obj):
        nombre_completo = f"{(obj.nombre or '').upper()} {(obj.apellido_paterno or '').upper()} {(obj.apellido_materno or '').upper()}".strip()
        return {
            'ID': obj.id,
            'RUT': obj.rut or 'Sin RUT',
            'Nombre': nombre_completo or 'Sin Nombre',
            'Sexo': obj.sexo or '',
            'Estado Civil': obj.estado_civil or '',
            'Comuna': (getattr(obj.comuna, 'nombre', '') or '').upper(),
            'Previsión': (getattr(obj.prevision, 'nombre', '') or '').upper(),
        }

    def get(self, request, *args, **kwargs):
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest' and request.GET.get('datatable'):
            return self.get_datatable_response(request)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': 'Listado de Pacientes',
            'list_url': reverse_lazy('kardex:paciente_list'),
            'create_url': reverse_lazy('kardex:paciente_create'),
            'datatable_enabled': True,
            'datatable_order': [[0, 'asc']],
            'datatable_page_length': 100,
            'columns': self.datatable_columns,
            'export_csv_url': reverse_lazy('reports:export_paciente_csv'),
        })
        return context


class PacienteDetailView(PermissionRequiredMixin, DetailView):
    model = Paciente
    template_name = 'kardex/paciente/detail.html'
    permission_required = 'kardex.view_paciente'
    raise_exception = True

    def render_to_response(self, context, **response_kwargs):
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            from django.template.loader import render_to_string
            html = render_to_string(self.template_name, context=context, request=self.request)
            return HttpResponse(html)
        return super().render_to_response(context, **response_kwargs)


class PacienteUpdateView(PermissionRequiredMixin, UpdateView):
    template_name = 'kardex/paciente/form_update.html'
    model = Paciente
    form_class = FormPaciente
    success_url = reverse_lazy('kardex:paciente_list')
    permission_required = 'kardex.change_paciente'
    raise_exception = True

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            form.save()
            messages.success(request, 'Paciente actualizado correctamente')
            return redirect(self.success_url)
        messages.error(request, 'Hay errores en el formulario')
        return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Paciente'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        context['module_name'] = MODULE_NAME

        # Obtener la ficha del paciente asociada al establecimiento del usuario logueado
        user = getattr(self.request, 'user', None)
        establecimiento = getattr(user, 'establecimiento', None) if user else None

        ingreso = None  # Mantener en contexto por compatibilidad
        ficha = None
        if establecimiento:
            ficha = Ficha.objects.filter(paciente=self.object, establecimiento=establecimiento).first()
            if ficha is None:
                from django.contrib import messages
                messages.info(self.request, 'No existe ficha asociada a este paciente en su establecimiento.')
        else:
            from django.contrib import messages
            messages.warning(self.request, 'El usuario no tiene un establecimiento asociado.')

        # Datos derivados para el template (sin consumir API)
        paciente = self.object

        def fmt_dt(dt):
            try:
                return dt.strftime('%d/%m/%Y') if dt else ''
            except Exception:
                return ''

        ficha_numero = getattr(ficha, 'numero_ficha_sistema', '') if ficha else ''
        ficha_created_at_text = fmt_dt(getattr(ficha, 'created_at', None)) if ficha else ''
        ficha_updated_at_text = fmt_dt(getattr(ficha, 'updated_at', None)) if ficha else ''
        paciente_codigo = getattr(paciente, 'codigo', '')

        # URLs para botones (Carátula, Stickers, Pasivar, Ficha Tarjeta)
        caratula_url = stickers_url = pasivar_url = ficha_tarjeta_url = ''
        ficha_pasivado = False
        if ficha and getattr(ficha, 'id', None):
            fid = ficha.id
            caratula_url = f"/kardex/pdfs/ficha/{fid}/"
            stickers_url = f"/kardex/pdfs/stickers/ficha/{fid}/"
            pasivar_url = f"/kardex/fichas/{fid}/toggle-pasivar/"
            ficha_tarjeta_url = f"/kardex/fichas/{fid}/tarjeta/"
            ficha_pasivado = bool(getattr(ficha, 'pasivado', False))

        # Exponer objetos esperados por el template
        context['paciente'] = paciente
        context['ingreso'] = ingreso
        context['ficha'] = ficha
        context['ficha_numero'] = ficha_numero
        context['ficha_created_at_text'] = ficha_created_at_text
        context['ficha_updated_at_text'] = ficha_updated_at_text
        context['paciente_codigo'] = paciente_codigo
        context['caratula_url'] = caratula_url
        context['stickers_url'] = stickers_url
        context['pasivar_url'] = pasivar_url
        context['ficha_tarjeta_url'] = ficha_tarjeta_url
        context['ficha_pasivado'] = ficha_pasivado

        return context


class PacienteActualizarRut(PermissionRequiredMixin, UpdateView):
    template_name = 'kardex/paciente/form_rut.html'
    model = Paciente
    form_class = FormPacienteActualizarRut
    success_url = reverse_lazy('kardex:paciente_list')
    permission_required = 'kardex.change_paciente'
    raise_exception = True

    def form_valid(self, form):
        messages.success(self.request, 'RUT del paciente actualizado correctamente.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Actualizar RUT del Paciente'
        context['module_name'] = MODULE_NAME
        context['list_url'] = self.success_url

        paciente = self.object
        # Construimos una lista de (label, valor) para mostrar en el panel derecho
        fields_info = []
        # Usar model_to_dict puede omitir ManyToMany; aquí listamos field por field para labels
        for field in paciente._meta.fields:
            try:
                label = getattr(paciente._meta.get_field(field.name), 'verbose_name', field.name)
            except Exception:
                label = field.name
            value = getattr(paciente, field.name, '')
            # Formatear fechas
            if hasattr(value, 'strftime'):
                try:
                    value = value.strftime('%d/%m/%Y')
                except Exception:
                    value = str(value)
            # Resolver FKs a su string
            if hasattr(value, '__class__') and value.__class__.__name__ == 'DeferredAttribute':
                value = getattr(paciente, field.name)
            if field.related_model is not None:
                value = getattr(paciente, field.name)
                value = '' if value is None else str(value)
            fields_info.append((str(label).capitalize(), '' if value is None else str(value)))
        context['paciente_fields'] = fields_info
        return context


class PacienteDeleteView(PermissionRequiredMixin, DeleteView):
    model = Paciente
    template_name = 'kardex/paciente/confirm_delete.html'
    success_url = reverse_lazy('kardex:paciente_list')
    permission_required = 'kardex.delete_paciente'
    raise_exception = True

    def post(self, request, *args, **kwargs):
        try:
            obj = self.get_object()
            obj.delete()
            messages.success(request, 'Paciente eliminado correctamente')
        except Exception as e:
            messages.error(request, f'No se pudo eliminar el paciente: {e}')
        return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar Paciente'
        context['list_url'] = self.success_url
        context['module_name'] = MODULE_NAME
        return context


class PacienteRecienNacidoListView(PacienteListView):
    datatable_columns = ['ID', 'Código', 'Nombre', 'Sexo', 'Rut Responsable', 'Comuna', 'Previsión']
    datatable_order_fields = [
        'id',
        None,
        None,
        'codigo',
        'nombre',
        'sexo',
        'rut_responsable_temporal',
        'comuna__nombre',
        'prevision__nombre'
    ]

    datatable_search_fields = [
        'codigo__icontains',
        'rut__icontains',
        'nombre__icontains',
        'apellido_paterno__icontains',
        'apellido_materno__icontains',
        'sexo__icontains',
        'rut_responsable_temporal_icontains',
        'comuna__nombre__icontains',
        'prevision__nombre__icontains'
    ]

    def render_row(self, obj):
        return {
            'ID': obj.id,
            'Código': obj.codigo.upper(),
            'Nombre': obj.nombre.upper(),
            'Sexo': obj.sexo.upper(),
            'Rut Responsable': obj.rut_responsable_temporal if obj.rut_responsable_temporal == 'nan' else 'Sin RUT',
            'Comuna': (getattr(obj.comuna, 'nombre', '') or '').upper(),
            'Previsión': (getattr(obj.prevision, 'prevision', '') or '').upper(),
        }

    def get_base_queryset(self):
        return Paciente.objects.filter(recien_nacido=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': 'Pacientes Recién Nacidos',
            'list_url': reverse_lazy('kardex:paciente_recien_nacido_list'),
            'export_csv_url': reverse_lazy('reports:export_paciente_recien_nacido_csv'),
        })
        return context


class PacienteExtranjeroListView(PacienteListView):
    datatable_columns = ['ID', 'Código', 'RUT', 'Nombre', 'NIP', 'Pasaporte', 'Sexo', 'Estado Civil', 'Comuna',
                         'Previsión']
    datatable_order_fields = [
        'id',
        None,
        None,
        'codigo',
        'rut',
        'nombre',
        'nip',
        'pasaporte',
        'sexo',
        'estado_civil',
        'comuna__nombre',
        'prevision__nombre'
    ]

    datatable_search_fields = [
        'codigo__icontains',
        'rut__icontains',
        'nombre__icontains',
        'nip__icontains',
        'pasaporte__icontains',
        'apellido_paterno__icontains',
        'apellido_materno__icontains',
        'sexo__icontains',
        'estado_civil__icontains',
        'comuna__nombre__icontains',
        'prevision__nombre__icontains'
    ]

    def render_row(self, obj):
        return {
            'ID': obj.id,
            'Código': (obj.codigo or '').upper(),
            'RUT': (obj.rut or '').upper(),
            'Nombre': (obj.nombre or '').upper(),
            'NIP': (obj.nip or '').upper(),
            'Pasaporte': (obj.pasaporte or '').upper(),
            'Sexo': (obj.sexo or '').upper(),
            'Estado Civil': (obj.estado_civil or '').upper(),
            'Comuna': (getattr(obj.comuna, 'nombre', '') or '').upper(),
            'Previsión': (getattr(obj.prevision, 'nombre', '') or '').upper(),
        }

    def get_base_queryset(self):
        return Paciente.objects.filter(extranjero=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': 'Pacientes Extranjeros',
            'list_url': reverse_lazy('kardex:paciente_extranjero_list'),
            'export_csv_url': reverse_lazy('reports:export_paciente_extranjero_csv'),
        })
        return context


class PacienteRutMadreListView(PacienteListView):
    datatable_columns = ['ID', 'Código', 'Nombre', 'Sexo', 'Rut Responsable', 'Comuna', 'Previsión']
    datatable_order_fields = [
        'id',
        None,
        None,
        'codigo',
        'nombre',
        'sexo',
        'rut_responsable_temporal',
        'comuna__nombre',
        'prevision__nombre'
    ]

    datatable_search_fields = [
        'codigo__icontains',
        'rut__icontains',
        'nombre__icontains',
        'apellido_paterno__icontains',
        'apellido_materno__icontains',
        'sexo__icontains',
        'rut_responsable_temporal_icontains',
        'comuna__nombre__icontains',
        'prevision__nombre__icontains'
    ]

    def render_row(self, obj):
        return {
            'ID': obj.id,
            'Código': obj.codigo.upper(),
            'Nombre': obj.nombre.upper(),
            'Sexo': obj.sexo.upper(),
            'Rut Responsable': obj.rut_responsable_temporal if obj.rut_responsable_temporal == 'nan' else 'Sin RUT',
            'Comuna': (getattr(obj.comuna, 'nombre', '') or '').upper(),
            'Previsión': (getattr(obj.prevision, 'prevision', '') or '').upper(),
        }

    def get_base_queryset(self):
        return Paciente.objects.filter(usar_rut_madre_como_responsable=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': 'Pacientes que utilizan el rut de la madre como reponsable',
            'list_url': reverse_lazy('kardex:paciente_rut_madre_list'),
        })
        return context


class PacienteFallecidoListView(PacienteListView):

    def get_base_queryset(self):
        return Paciente.objects.filter(fallecido=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': 'Pacientes Fallecidos',
            'list_url': reverse_lazy('kardex:paciente_fallecido_list'),
            'export_csv_url': reverse_lazy('reports:export_paciente_fallecido_csv'),
        })
        return context


class PacientePuebloIndigenaListView(PacienteListView):

    def get_base_queryset(self):
        return Paciente.objects.filter(pueblo_indigena=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': 'Pacientes Pertenecientes a Pueblos Indigenas',
            'list_url': reverse_lazy('kardex:paciente_pueblo_indigena_list'),
            'export_csv_url': reverse_lazy('reports:export_paciente_pueblo_indigena_csv'),
        })
        return context


class PacienteFechaFormView(PermissionRequiredMixin, FormView):
    template_name = 'kardex/paciente/fecha_rango_form.html'
    form_class = PacienteFechaRangoForm
    permission_required = 'kardex.view_paciente'

    def get_success_url(self):
        return reverse_lazy('kardex:paciente_por_fecha_list')

    def form_valid(self, form):
        # Redirect with GET params for datatable view
        fecha_inicio = form.cleaned_data['fecha_inicio'].strftime('%Y-%m-%d')
        fecha_fin = form.cleaned_data['fecha_fin'].strftime('%Y-%m-%d')
        url = f"{self.get_success_url()}?fecha_inicio={fecha_inicio}&fecha_fin={fecha_fin}"
        return redirect(url)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = 'Consultar por rango de fechas'
        return ctx


class PacientePorFechaListView(PacienteListView):

    def get_base_queryset(self):
        qs = Paciente.objects.all()
        fecha_inicio = self.request.GET.get('fecha_inicio')
        fecha_fin = self.request.GET.get('fecha_fin')
        if fecha_inicio and fecha_fin:
            fi = parse_date(fecha_inicio)
            ff = parse_date(fecha_fin)
            if fi and ff:
                from datetime import datetime, time
                start_dt = datetime.combine(fi, time.min)
                end_dt = datetime.combine(ff, time.max)
                qs = qs.filter(created_at__range=(start_dt, end_dt))
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = PacienteFechaRangoForm(self.request.GET or None)
        context.update({
            'title': 'Pacientes por Rango de Fecha',
            'list_url': reverse_lazy('kardex:paciente_por_fecha_list'),
            'date_range_form': form,
        })
        return context


from django.db import transaction


class PacienteQueryView(PermissionRequiredMixin, CreateView):
    template_name = 'kardex/paciente/form_creacion.html'
    model = Paciente
    form_class = FormPacienteCreacion
    success_url = reverse_lazy('kardex:paciente_list')
    permission_required = 'kardex.add_paciente'
    raise_exception = True

    class ValidationError(Exception):
        pass

    # Helpers
    def _get_paciente_instance(self, request):
        paciente_id = request.POST.get('paciente_id') or request.GET.get('paciente_id')
        if paciente_id:
            try:
                return Paciente.objects.get(pk=paciente_id)
            except Paciente.DoesNotExist:
                messages.error(request, 'El paciente indicado no existe.')
        return None

    def _validar_limite_fichas(self, paciente):
        qs = Ficha.objects.filter(paciente=paciente, establecimiento__isnull=False).values_list('establecimiento',
                                                                                                flat=True).distinct()
        return qs.count() >= 5

    def _existe_ficha_en_establecimiento(self, paciente, establecimiento):
        if not establecimiento:
            return False
        return Ficha.objects.filter(paciente=paciente, establecimiento=establecimiento).exists()

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        instance = self._get_paciente_instance(request)
        form = self.form_class(request.POST or None, request.FILES or None, instance=instance)

        if not form.is_valid():
            messages.error(request, 'Por favor corrija los errores del formulario.')
            print(form.errors)
            self.object = instance or None
            return self.render_to_response(self.get_context_data(form=form))

        try:
            user = request.user
            establecimiento = getattr(request, 'establecimiento', None) or getattr(user, 'establecimiento', None)

            paciente = form.save(commit=False)
            if not instance:  # creación
                paciente.usuario = user
            paciente.save()
            self.object = paciente

            # Solo en creación: crear ficha asociada
            if not instance:
                # Validaciones de negocio
                if self._validar_limite_fichas(paciente):
                    raise self.ValidationError(
                        'El paciente ya tiene el máximo de 5 fichas en establecimientos distintos.')

                if not establecimiento:
                    raise self.ValidationError(
                        'El usuario no tiene un establecimiento asociado. No se puede crear la ficha.')

                if self._existe_ficha_en_establecimiento(paciente, establecimiento):
                    raise self.ValidationError('Ya existe una ficha para este paciente en su establecimiento.')

                # Crear ficha
                ficha = Ficha.objects.create(
                    paciente=paciente,
                    usuario=user,
                    establecimiento=establecimiento,
                )
                print(ficha)
                messages.success(request, f'Ficha creada correctamente. N° SISTEMA: {ficha.numero_ficha_sistema}')
                messages.success(request, 'Paciente creado correctamente')
            else:
                messages.success(request, 'Paciente actualizado correctamente')

            return redirect(self.success_url)

        except self.ValidationError as e:
            form.add_error(None, str(e))
            self.object = paciente  # importante para evitar errores en get_context_data
            return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        instance = self._get_paciente_instance(self.request)
        is_update = instance is not None
        context[
            'title'] = 'Editar Paciente' if is_update else f'Crear Paciente en {self.request.establecimiento.nombre}'
        context['list_url'] = self.success_url
        context['action'] = 'edit' if is_update else 'add'
        context['module_name'] = MODULE_NAME
        if 'form' not in kwargs and is_update:
            context['form'] = self.form_class(instance=instance)
        return context


class PacientesHistoryListView(GenericHistoryListView):
    base_model = Paciente
    permission_required = 'kardex.view_paciente'
    template_name = 'kardex/history/list.html'

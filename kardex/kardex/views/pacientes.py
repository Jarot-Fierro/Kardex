from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.dateparse import parse_date
from django.views.generic import DeleteView, CreateView, UpdateView, DetailView
from django.views.generic import TemplateView, FormView

from kardex.forms.pacientes import FormPaciente
from kardex.forms.pacientes import FormPacienteCreacion
from kardex.forms.pacientes import PacienteFechaRangoForm
from kardex.mixin import DataTableMixin
from kardex.models import Ficha
from kardex.models import Paciente

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


class PacienteCreateView(PermissionRequiredMixin, CreateView):
    template_name = 'kardex/paciente/form.html'
    model = Paciente
    form_class = FormPaciente
    success_url = reverse_lazy('kardex:paciente_list')
    # Esta vista actúa como actualización por selección desde API
    permission_required = 'kardex.change_paciente'
    raise_exception = True

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        request = getattr(self, 'request', None)
        paciente_id = None
        if request is not None:
            paciente_id = (request.POST.get('paciente_id') or request.GET.get('paciente_id') or '').strip()
        if paciente_id:
            try:
                instance = Paciente.objects.get(pk=paciente_id)
                # Vincular la instancia seleccionada para que el formulario cargue sus datos
                self.object = instance
                kwargs['instance'] = instance
                # Asegurar que el campo rut quede preseleccionado/prefijado en el init
                initial = kwargs.get('initial', {}).copy()
                if getattr(instance, 'rut', None):
                    initial['rut'] = instance.rut
                kwargs['initial'] = initial
            except Paciente.DoesNotExist:
                pass
        return kwargs

    def post(self, request, *args, **kwargs):
        print("[DEBUG] POST iniciado")
        # Detect if this should be treated as an update (AJAX prefilled existing paciente)
        paciente_id = (request.POST.get('paciente_id') or '').strip()
        instance = None
        if paciente_id:
            try:
                instance = Paciente.objects.get(pk=paciente_id)
                self.object = instance  # Make get_form bind to instance
                print(f"[DEBUG] Modo edición detectado (ID: {paciente_id})")
            except Paciente.DoesNotExist:
                print(f"[WARN] paciente_id {paciente_id} no existe. Continuando como creación.")
                instance = None

        form = self.get_form()
        if form.is_valid():
            user = request.user

            try:
                with transaction.atomic():
                    paciente = form.save(commit=False)
                    # Asignar usuario siempre
                    paciente.usuario = request.user

                    try:
                        paciente.save()
                        print(f"[DEBUG] Paciente guardado: {paciente} (ID: {paciente.pk})")
                    except Exception as e:
                        print("[ERROR] No se pudo guardar el paciente:", e)
                        messages.error(request, f"Error al guardar el paciente: {e}")
                        return self.render_to_response(self.get_context_data(form=form))

                    # IMPORTANTE: Esta vista funciona como ACTUALIZACIÓN/CONSULTA vía API.
                    # No crear IngresoPaciente ni Ficha aquí. Solo guardar datos del paciente.
                    # La creación se realiza en PacienteCreacionView.
                    pass

                    # Siempre actuamos como actualización cuando viene desde API con paciente existente
                    messages.success(request, 'Paciente actualizado correctamente')
                    return redirect(self.success_url)

            except Exception as e:
                print("[ERROR] Transacción fallida:", e)
                messages.error(request, f"No se pudo completar: {e}")
                self.object = None
                return self.render_to_response(self.get_context_data(form=form, open_modal=True))

        messages.error(request, 'Hay errores en el formulario')
        self.object = instance
        return self.render_to_response(self.get_context_data(form=form, open_modal=True))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Consulta/Actualización de Paciente'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        context['module_name'] = MODULE_NAME
        return context


class PacienteUpdateView(PermissionRequiredMixin, UpdateView):
    template_name = 'kardex/paciente/form.html'
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

        # Obtener el ingreso del paciente asociado al establecimiento del usuario logueado
        user = getattr(self.request, 'user', None)
        establecimiento = getattr(user, 'establecimiento', None) if user else None

        ingreso = None
        if establecimiento:
            ingreso = self.object.ingresopaciente_set.filter(establecimiento=establecimiento).first()
        else:
            from django.contrib import messages
            messages.warning(self.request, 'El usuario no tiene un establecimiento asociado.')

        ficha = None
        if ingreso:
            ficha = Ficha.objects.filter(ingreso_paciente=ingreso).first()
            if ficha is None:
                from django.contrib import messages
                messages.info(self.request, 'No existe ficha asociada al ingreso en su establecimiento.')
        else:
            from django.contrib import messages
            messages.info(self.request, 'El paciente no tiene ingreso en su establecimiento.')

        # Exponer objetos esperados por el template
        context['paciente'] = self.object
        context['ingreso'] = ingreso
        context['ficha'] = ficha

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
    datatable_columns = ['ID', 'RUT', 'Nombre', 'Sexo', 'Rut Responsable', 'Comuna', 'Previsión']
    datatable_order_fields = [
        'id',
        None,
        None,
        'sexo',
        'rut_responsable_temporal',
        'comuna__nombre',
        'prevision__nombre'
    ]

    datatable_search_fields = [
        'rut__icontains',
        'nombre__icontains',
        'apellido_paterno__icontains',
        'apellido_materno__icontains',
        'sexo__icontains',
        'rut_responsable_temporal_icontains',
        'comuna__nombre__icontains',
        'prevision__nombre__icontains'
    ]

    def get_base_queryset(self):
        return Paciente.objects.filter(recien_nacido=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': 'Pacientes Recién Nacidos',
            'list_url': reverse_lazy('kardex:paciente_recien_nacido_list'),
        })
        return context


class PacienteExtranjeroListView(PacienteListView):

    def get_base_queryset(self):
        return Paciente.objects.filter(extranjero=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': 'Pacientes Extranjeros',
            'list_url': reverse_lazy('kardex:paciente_extranjero_list'),
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
        })
        return context


class PacienteCreacionView(PermissionRequiredMixin, CreateView):
    template_name = 'kardex/paciente/form_creacion.html'
    model = Paciente
    form_class = FormPacienteCreacion
    success_url = reverse_lazy('kardex:paciente_list')
    permission_required = 'kardex.add_paciente'
    raise_exception = True

    # def form_valid(self, form):
    #     user = self.request.user
    #     try:
    #         with transaction.atomic():
    #             paciente = form.save(commit=False)
    #             paciente.usuario = user
    #             paciente.save()
    #
    #             establecimiento = getattr(user, 'establecimiento', None)
    #             if not establecimiento:
    #                 messages.warning(self.request, 'El usuario no tiene un establecimiento asociado.')
    #             else:
    #                 ingresos_qs = IngresoPaciente.objects.filter(paciente=paciente)
    #                 count_ingresos = ingresos_qs.count()
    #                 ingreso_existente = ingresos_qs.filter(establecimiento=establecimiento).first()
    #
    #                 if count_ingresos >= 5 and not ingreso_existente:
    #                     messages.warning(self.request, 'Máximo de ingresos alcanzado.')
    #                 else:
    #                     if ingreso_existente:
    #                         ficha, created = Ficha.objects.get_or_create(
    #                             ingreso_paciente=ingreso_existente,
    #                             defaults={'usuario': user}
    #                         )
    #                         if created:
    #                             messages.success(self.request, f'Ficha creada. N°: {str(ficha.numero_ficha).zfill(4)}')
    #                         else:
    #                             messages.info(self.request, 'Ficha ya existente para este ingreso.')
    #                     else:
    #                         ingreso = IngresoPaciente.objects.create(paciente=paciente, establecimiento=establecimiento)
    #                         ficha, created = Ficha.objects.get_or_create(
    #                             ingreso_paciente=ingreso,
    #                             defaults={'usuario': user}
    #                         )
    #                         if created:
    #                             messages.success(self.request, f'Ficha creada. N°: {str(ficha.numero_ficha).zfill(4)}')
    #                         else:
    #                             messages.info(self.request, 'Ficha ya existente.')
    #             messages.success(self.request, 'Paciente creado correctamente')
    #             return redirect(self.success_url)
    #     except Exception as e:
    #         messages.error(self.request, f'No se pudo completar la creación: {e}')
    #         return self.form_invalid(form)
    #
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['title'] = 'Crear Paciente'
    #     context['list_url'] = self.success_url
    #     context['action'] = 'add'
    #     context['module_name'] = MODULE_NAME
    #     return context


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


class PacienteQueryView(PermissionRequiredMixin, CreateView):
    template_name = 'kardex/paciente/form_creacion.html'
    model = Paciente
    form_class = FormPacienteCreacion
    success_url = reverse_lazy('kardex:paciente_list')
    permission_required = 'kardex.add_paciente'
    raise_exception = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Consultas Paciente'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        context['module_name'] = MODULE_NAME
        return context

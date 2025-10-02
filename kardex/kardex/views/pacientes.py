from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.utils.dateformat import format as django_format
from django.views.decorators.http import require_GET
from django.views.generic import DeleteView, CreateView, UpdateView, DetailView
from django.views.generic import TemplateView, FormView

from kardex.forms.pacientes import FormPaciente
from kardex.mixin import DataTableMixin
from kardex.models import Paciente, Ficha

MODULE_NAME = 'Pacientes'


class PacienteListView(DataTableMixin, TemplateView):
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
        'comuna__nombre__icontains',
        'prevision__nombre__icontains'
    ]

    url_detail = 'kardex:paciente_detail'
    url_update = 'kardex:paciente_update'
    url_delete = 'kardex:paciente_delete'

    def render_row(self, obj):
        nombre_completo = f"{(obj.nombre or '').upper()} {(obj.apellido_paterno or '').upper()} {(obj.apellido_materno or '').upper()}".strip()
        return {
            'ID': obj.id,
            'RUT': obj.rut,
            'Nombre': nombre_completo,
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


class PacienteDetailView(DetailView):
    model = Paciente
    template_name = 'kardex/paciente/detail.html'

    def render_to_response(self, context, **response_kwargs):
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            from django.template.loader import render_to_string
            html = render_to_string(self.template_name, context=context, request=self.request)
            return HttpResponse(html)
        return super().render_to_response(context, **response_kwargs)


class PacienteCreateView(CreateView):
    template_name = 'kardex/paciente/form.html'
    model = Paciente
    form_class = FormPaciente
    success_url = reverse_lazy('kardex:paciente_list')
    permission_required = 'add_paciente'

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
            print("[DEBUG] Formulario válido")
            from django.db import transaction
            from kardex.models import IngresoPaciente, Ficha
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

                    establecimiento = getattr(user, 'establecimiento', None)
                    if not establecimiento:
                        messages.warning(request, 'El usuario no tiene un establecimiento asociado.')
                    else:
                        ingresos_qs = IngresoPaciente.objects.filter(paciente=paciente)
                        count_ingresos = ingresos_qs.count()
                        print(f"[DEBUG] Ingresos actuales: {count_ingresos}")
                        ingreso_existente = ingresos_qs.filter(establecimiento=establecimiento).first()

                        if count_ingresos >= 5 and not ingreso_existente:
                            # Si ya alcanzó el máximo y además no existe uno en este establecimiento, no crear otro
                            messages.warning(request, 'Máximo de ingresos alcanzado.')
                        else:
                            if ingreso_existente:
                                # Ya existe ingreso en el establecimiento actual
                                # En edición queremos asegurar la existencia de ficha
                                ficha, created = Ficha.objects.get_or_create(
                                    ingreso_paciente=ingreso_existente,
                                    defaults={'usuario': user}
                                )
                                if created:
                                    messages.success(request, f'Ficha creada. N°: {str(ficha.numero_ficha).zfill(4)}')
                                else:
                                    messages.info(request, 'Ficha ya existente para este ingreso.')
                            else:
                                # No existe ingreso en este establecimiento: crear respetando el tope
                                ingreso = IngresoPaciente.objects.create(paciente=paciente, establecimiento=establecimiento)
                                print(f"[DEBUG] Ingreso creado: ID {ingreso.pk}")
                                ficha, created = Ficha.objects.get_or_create(
                                    ingreso_paciente=ingreso,
                                    defaults={'usuario': user}
                                )
                                if created:
                                    messages.success(request, f'Ficha creada. N°: {str(ficha.numero_ficha).zfill(4)}')
                                else:
                                    messages.info(request, 'Ficha ya existente.')

                    if instance:
                        messages.success(request, 'Paciente actualizado correctamente')
                    else:
                        messages.success(request, 'Paciente creado correctamente')
                    return redirect(self.success_url)

            except Exception as e:
                print("[ERROR] Transacción fallida:", e)
                messages.error(request, f"No se pudo completar: {e}")
                self.object = None
                return self.render_to_response(self.get_context_data(form=form, open_modal=True))

        print("[DEBUG] Formulario inválido:", form.errors)
        messages.error(request, 'Hay errores en el formulario')
        self.object = instance
        return self.render_to_response(self.get_context_data(form=form, open_modal=True))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Nuevo Paciente'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        context['module_name'] = MODULE_NAME
        return context


class PacienteUpdateView(UpdateView):
    template_name = 'kardex/paciente/form.html'
    model = Paciente
    form_class = FormPaciente
    success_url = reverse_lazy('kardex:paciente_list')
    permission_required = 'change_paciente'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            paciente = form.save()
            # Lógica de creación automática de IngresoPaciente y Ficha en modo edición
            from kardex.models import IngresoPaciente, Ficha
            user = request.user
            establecimiento = getattr(user, 'establecimiento', None)
            if not establecimiento:
                messages.warning(request, 'El usuario no tiene un establecimiento asociado.')
            else:
                ingresos_qs = IngresoPaciente.objects.filter(paciente=paciente)
                ingreso_existente = ingresos_qs.filter(establecimiento=establecimiento).first()
                if ingreso_existente:
                    ficha, created = Ficha.objects.get_or_create(
                        ingreso_paciente=ingreso_existente,
                        defaults={'usuario': user}
                    )
                    if created:
                        messages.success(request, f'Ficha creada. N°: {str(ficha.numero_ficha).zfill(4)}')
                else:
                    if ingresos_qs.count() >= 5:
                        messages.warning(request, 'Máximo de ingresos alcanzado. No se creó un nuevo ingreso.')
                    else:
                        ingreso = IngresoPaciente.objects.create(paciente=paciente, establecimiento=establecimiento)
                        ficha, created = Ficha.objects.get_or_create(
                            ingreso_paciente=ingreso,
                            defaults={'usuario': user}
                        )
                        if created:
                            messages.success(request, f'Ficha creada. N°: {str(ficha.numero_ficha).zfill(4)}')
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


class PacienteDeleteView(DeleteView):
    model = Paciente
    template_name = 'kardex/paciente/confirm_delete.html'
    success_url = reverse_lazy('kardex:paciente_list')
    permission_required = 'delete_paciente'

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


from kardex.forms.pacientes import PacienteFechaRangoForm
from django.utils.dateparse import parse_date


class PacienteFechaFormView(FormView):
    template_name = 'kardex/paciente/fecha_rango_form.html'
    form_class = PacienteFechaRangoForm

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


# --- API AJAX endpoints for searching Pacientes ---
@login_required
@require_GET
def buscar_paciente_por_rut(request):
    rut = (request.GET.get('rut') or '').strip()
    if not rut:
        return JsonResponse({'success': False, 'error': 'Parámetro "rut" es requerido.'}, status=400)
    establecimiento = getattr(request.user, 'establecimiento', None)
    if not establecimiento:
        return JsonResponse({'success': False, 'error': 'Usuario sin establecimiento asignado.'}, status=403)

    ficha = Ficha.objects.select_related('ingreso_paciente__paciente').filter(
        ingreso_paciente__establecimiento=establecimiento,
        ingreso_paciente__paciente__rut=rut
    ).first()

    if not ficha:
        return JsonResponse({'success': False,
                             'error': 'No se encontró paciente con ese RUT en su establecimiento o no tiene ficha asociada.'},
                            status=404)

    paciente = ficha.ingreso_paciente.paciente
    return JsonResponse({'success': True, 'paciente': _serialize_paciente(request, paciente, ficha)})


@login_required
@require_GET
def buscar_paciente_por_codigo(request):
    codigo = (request.GET.get('codigo') or '').strip()
    if not codigo:
        return JsonResponse({'success': False, 'error': 'Parámetro "codigo" es requerido.'}, status=400)
    establecimiento = getattr(request.user, 'establecimiento', None)
    if not establecimiento:
        return JsonResponse({'success': False, 'error': 'Usuario sin establecimiento asignado.'}, status=403)

    ficha = Ficha.objects.select_related('ingreso_paciente__paciente').filter(
        ingreso_paciente__establecimiento=establecimiento,
        ingreso_paciente__paciente__codigo=codigo
    ).first()

    if not ficha:
        return JsonResponse({'success': False,
                             'error': 'No se encontró paciente con ese código en su establecimiento o no tiene ficha asociada.'},
                            status=404)

    paciente = ficha.ingreso_paciente.paciente
    return JsonResponse({'success': True, 'paciente': _serialize_paciente(request, paciente, ficha)})


@login_required
@require_GET
def buscar_paciente_por_ficha(request):
    numero_ficha = (request.GET.get('numero_ficha') or '').strip()
    if not numero_ficha:
        return JsonResponse({'success': False, 'error': 'Parámetro "numero_ficha" es requerido.'}, status=400)
    establecimiento = getattr(request.user, 'establecimiento', None)
    if not establecimiento:
        return JsonResponse({'success': False, 'error': 'Usuario sin establecimiento asignado.'}, status=403)

    try:
        numero_ficha_int = int(numero_ficha)
    except ValueError:
        return JsonResponse({'success': False, 'error': 'El número de ficha debe ser numérico.'}, status=400)

    ficha = Ficha.objects.select_related('ingreso_paciente__paciente').filter(
        ingreso_paciente__establecimiento=establecimiento,
        numero_ficha=numero_ficha_int
    ).first()

    if not ficha:
        return JsonResponse({'success': False, 'error': 'No se encontró ficha en su establecimiento.'}, status=404)

    paciente = ficha.ingreso_paciente.paciente
    return JsonResponse({'success': True, 'paciente': _serialize_paciente(request, paciente, ficha)})


def _serialize_paciente(request, paciente: Paciente, ficha: Ficha):
    fecha_nac = django_format(paciente.fecha_nacimiento, 'd/m/Y') if paciente.fecha_nacimiento else None
    fecha_fallecimiento = django_format(paciente.fecha_fallecimiento, 'd/m/Y') if paciente.fecha_fallecimiento else None

    print(fecha_nac)

    pac_created = getattr(paciente, 'created_at', None)
    pac_updated = getattr(paciente, 'updated_at', None)
    fic_created = getattr(ficha, 'created_at', None) if ficha else None
    fic_updated = getattr(ficha, 'updated_at', None) if ficha else None

    # Try to expose ingreso ID for convenience
    ingreso = getattr(ficha, 'ingreso_paciente', None) if ficha else None

    # Build dynamic PDF URLs (relative and absolute)
    pdf_rel = reverse('kardex:pdf_ficha', kwargs={'ficha_id': ficha.id}) if ficha else None
    pdf_abs = request.build_absolute_uri(pdf_rel) if ficha and pdf_rel else None

    return {
        'id': paciente.id,
        # Identificación
        'rut': paciente.rut,
        'codigo': paciente.codigo,
        'nie': paciente.nie,
        'pasaporte': paciente.pasaporte,
        'nombre': paciente.nombre,
        'apellido_paterno': paciente.apellido_paterno,
        'apellido_materno': paciente.apellido_materno,
        'rut_madre': paciente.rut_madre,
        'rut_responsable_temporal': paciente.rut_responsable_temporal,
        'usar_rut_madre_como_responsable': paciente.usar_rut_madre_como_responsable,
        'nombre_social': paciente.nombre_social,

        # Nacimiento y estado
        'fecha_nacimiento': fecha_nac,
        'sexo': paciente.sexo,
        'estado_civil': paciente.estado_civil,
        'recien_nacido': paciente.recien_nacido,
        'extranjero': paciente.extranjero,
        'fallecido': paciente.fallecido,
        'fecha_fallecimiento': fecha_fallecimiento,

        # Familiares
        'nombres_padre': paciente.nombres_padre,
        'nombres_madre': paciente.nombres_madre,
        'nombre_pareja': paciente.nombre_pareja,
        'representante_legal': paciente.representante_legal,

        # Contacto y dirección
        'direccion': paciente.direccion,
        'numero_telefono1': paciente.numero_telefono1,
        'numero_telefono2': paciente.numero_telefono2,
        'ocupacion': paciente.ocupacion,

        # Relacionales
        'comuna': paciente.comuna.id if paciente.comuna else None,
        'prevision': paciente.prevision.id if paciente.prevision else None,

        # Ficha
        'numero_ficha': str(ficha.numero_ficha).zfill(4) if ficha else None,
        'ficha_id': ficha.id if ficha else None,
        'ingreso_id': ingreso.id if ingreso else None,

        # URLs listas para usar
        'pdf_ficha_url': pdf_rel,
        'pdf_ficha_absolute': pdf_abs,

        # Fechas de tracking
        'paciente_created_at': pac_created.isoformat() if pac_created else None,
        'paciente_updated_at': pac_updated.isoformat() if pac_updated else None,
        'ficha_created_at': fic_created.isoformat() if fic_created else None,
        'ficha_updated_at': fic_updated.isoformat() if fic_updated else None,
    }

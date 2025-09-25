from django.views.generic import TemplateView

from kardex.crud_views import BaseCRUDView
from kardex.forms.comunas import FormComuna
from kardex.forms.establecimientos import FormEstablecimiento
from kardex.forms.fichas import FormFicha
from kardex.forms.movimiento_ficha import FormEntradaFicha, FormSalidaFicha
from kardex.forms.pacientes import FormPaciente
from kardex.forms.prevision import FormPrevision
from kardex.forms.profesionales import FormProfesional
from kardex.forms.rango_fechas import RangoFechaPacienteForm
from kardex.forms.servicio_clinico import FormServicioClinico
from kardex.models import Establecimiento, Comuna, Ficha, Paciente, MovimientoFicha, Prevision, Profesional, \
    ServicioClinico


class BaseCRUDEstablecimientoView(BaseCRUDView):
    model = Establecimiento
    form_class = FormEstablecimiento
    template_name = 'crud/index.html'
    success_url = 'establecimiento_active'
    exclude_fields = ['created_at', 'updated_at', 'status']
    title = 'Establecimientos'

    active_url_name = 'kardex:establecimiento_active'
    inactive_url_name = 'kardex:establecimiento_inactive'
    update_url_name = 'kardex:establecimiento_update'
    toggle_url_name = 'kardex:establecimiento_toggle_status'
    # history_url_name = 'kardex:establecimiento_history'
    # export_report_url_name = 'reports:export_establecimiento'


class EstablecimientoView(BaseCRUDEstablecimientoView):
    success_url = 'establecimiento_active'

    def get_queryset(self):
        return Establecimiento.objects.filter(status='ACTIVE').order_by('-updated_at')


class BaseCRUDComunaView(BaseCRUDView):
    model = Comuna
    form_class = FormComuna
    template_name = 'crud/index.html'
    success_url = 'comuna_active'
    exclude_fields = ['created_at', 'updated_at', 'status']
    title = 'Comunas'

    active_url_name = 'kardex:comuna_active'
    inactive_url_name = 'kardex:comuna_inactive'
    update_url_name = 'kardex:comuna_update'
    toggle_url_name = 'kardex:comuna_toggle_status'
    # history_url_name = 'kardex:comuna_history'
    # export_report_url_name = 'reports:export_comuna'


class ComunaView(BaseCRUDComunaView):
    success_url = 'comuna_active'

    def get_queryset(self):
        return Comuna.objects.filter(status='ACTIVE').order_by('-updated_at')


class BaseCRUDFicha(BaseCRUDView):
    model = Ficha
    form_class = FormFicha
    template_name = 'crud/index.html'
    success_url = 'fichas_active'
    exclude_fields = ['created_at', 'updated_at', 'status']
    title = 'Fichas'

    active_url_name = 'kardex:fichas_active'
    inactive_url_name = 'kardex:fichas_inactive'
    update_url_name = 'kardex:fichas_update'
    toggle_url_name = 'kardex:fichas_toggle_status'
    # history_url_name = 'kardex:fichas_history'
    # export_report_url_name = 'reports:export_fichas'


class FichaView(BaseCRUDFicha):
    success_url = 'fichas_active'

    def get_queryset(self):
        return Ficha.objects.filter(status='ACTIVE').order_by('-updated_at')


class BaseCRUDPaciente(BaseCRUDView):
    model = Paciente
    form_class = FormPaciente
    template_name = 'crud/index.html'
    success_url = 'paciente_active'
    title = 'Pacientes'
    exclude_fields = ['sexo', 'rut_madre', 'estado_civil', 'nombres_pabre', 'nombres_madre', 'nombre_pareja',
                      'fecha_movimiento', 'pasaporte', 'recien_nacido', 'extranjero', 'fallecido',
                      'fecha_fallecimiento', 'ocupacion', 'representante_legal', 'nombre_social', 'extranjero',
                      'fallecido', 'ocupacion', 'representante_legal', 'nombre_social', 'nombre_social', 'comuna',
                      'prevision', 'usuario',
                      'created_at', 'updated_at', 'status']
    active_url_name = 'kardex:paciente_active'
    inactive_url_name = 'kardex:paciente_inactive'
    update_url_name = 'kardex:paciente_update'
    toggle_url_name = 'kardex:paciente_toggle_status'
    # history_url_name = 'kardex:paciente_history'
    # export_report_url_name = 'reports:export_paciente'


class PacienteView(BaseCRUDPaciente):
    success_url = 'paciente_active'

    def get_queryset(self):
        return Paciente.objects.filter(status='ACTIVE').order_by('-updated_at')


class PacienteRecienNacidoView(BaseCRUDPaciente):
    success_url = 'paciente_active'

    def get_queryset(self):
        return Paciente.objects.filter(status='ACTIVE', recien_nacido=True).order_by('-updated_at')


class PacienteExtranjeroView(BaseCRUDPaciente):
    success_url = 'paciente_active'

    def get_queryset(self):
        return Paciente.objects.filter(status='ACTIVE', extranjero=True).order_by('-updated_at')


class PacienteFallecidoView(BaseCRUDPaciente):
    success_url = 'paciente_active'

    def get_queryset(self):
        return Paciente.objects.filter(status='ACTIVE', fallecido=True).order_by('-updated_at')


class BaseCRUDMovimientoFichaEntrada(BaseCRUDView):
    model = MovimientoFicha

    template_name = 'crud/index.html'
    success_url = 'movimiento_fichas_active'
    title = 'Salida Ficha'
    exclude_fields = ['fecha_salida', 'observacion_salida', 'usuario_entrega', 'created_at', 'updated_at', 'status']
    active_url_name = 'kardex:movimiento_fichas_active'
    inactive_url_name = 'kardex:movimiento_fichas_inactive'
    update_url_name = 'kardex:movimiento_fichas_update'
    toggle_url_name = 'kardex:movimiento_fichas_toggle_status'
    # history_url_name = 'kardex:movimiento_fichas_history'
    # export_report_url_name = 'reports:export_movimiento_fichas'


class MovimientoFichaEntradaView(BaseCRUDMovimientoFichaEntrada):
    success_url = 'movimiento_fichas_active'
    form_class = FormEntradaFicha

    def get_queryset(self):
        return MovimientoFicha.objects.filter(status='ACTIVE').order_by('-updated_at')


class BaseCRUDMovimientoFichaSalida(BaseCRUDView):
    model = MovimientoFicha

    template_name = 'crud/index.html'
    success_url = 'movimiento_fichas_active'
    title = 'Entrada Ficha'
    exclude_fields = ['fecha_entrada', 'observacion_entrada', 'usuario_entrada', 'created_at', 'updated_at', 'status']
    active_url_name = 'kardex:movimiento_fichas_active'
    inactive_url_name = 'kardex:movimiento_fichas_inactive'
    update_url_name = 'kardex:movimiento_fichas_update'
    toggle_url_name = 'kardex:movimiento_fichas_toggle_status'
    # history_url_name = 'kardex:movimiento_fichas_history'
    # export_report_url_name = 'reports:export_movimiento_fichas'


class MovimientoFichaSalidaView(BaseCRUDMovimientoFichaSalida):
    success_url = 'movimiento_fichas_active'
    form_class = FormSalidaFicha

    def get_queryset(self):
        return MovimientoFicha.objects.filter(status='ACTIVE').order_by('-updated_at')


class BaseCRUDPrevision(BaseCRUDView):
    model = Prevision
    form_class = FormPrevision
    template_name = 'crud/index.html'
    success_url = 'prevision_active'
    title = 'Entrada Ficha'
    exclude_fields = ['created_at', 'updated_at', 'status']
    active_url_name = 'kardex:prevision_active'
    inactive_url_name = 'kardex:prevision_inactive'
    update_url_name = 'kardex:prevision_update'
    toggle_url_name = 'kardex:prevision_toggle_status'
    # history_url_name = 'kardex:prevision_history'
    # export_report_url_name = 'reports:export_prevision'


class PrevisionView(BaseCRUDPrevision):
    success_url = 'prevision_active'

    def get_queryset(self):
        return Prevision.objects.filter(status='ACTIVE').order_by('-updated_at')


class BaseCRUDProfesionales(BaseCRUDView):
    model = Profesional
    form_class = FormProfesional
    template_name = 'crud/index.html'
    success_url = 'profesionales_active'
    title = 'Profesionales'
    exclude_fields = ['created_at', 'updated_at', 'status']
    active_url_name = 'kardex:profesionales_active'
    inactive_url_name = 'kardex:profesionales_inactive'
    update_url_name = 'kardex:profesionales_update'
    toggle_url_name = 'kardex:profesionales_toggle_status'
    # history_url_name = 'kardex:profesionales_history'
    # export_report_url_name = 'reports:export_profesionales'


class ProfesionalesView(BaseCRUDProfesionales):
    success_url = 'profesionales_active'

    def get_queryset(self):
        return Profesional.objects.filter(status='ACTIVE').order_by('-updated_at')


class BaseCRUDServicioClinico(BaseCRUDView):
    model = ServicioClinico
    form_class = FormServicioClinico
    template_name = 'crud/index.html'
    success_url = 'servicio_clinico_active'
    title = 'Servicios Clínicos'
    exclude_fields = ['created_at', 'updated_at', 'status']
    active_url_name = 'kardex:servicio_clinico_active'
    inactive_url_name = 'kardex:servicio_clinico_inactive'
    update_url_name = 'kardex:servicio_clinico_update'
    toggle_url_name = 'kardex:servicio_clinico_toggle_status'
    # history_url_name = 'kardex:servicio_clinico_history'
    # export_report_url_name = 'reports:export_servicio_clinico'


class ServicioClinicoView(BaseCRUDServicioClinico):
    success_url = 'servicio_clinico_active'

    def get_queryset(self):
        return ServicioClinico.objects.filter(status='ACTIVE').order_by('-updated_at')


class PacientePorFechaView(TemplateView):
    template_name = 'kardex/paciente_por_fecha.html'
    form_class = RangoFechaPacienteForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class()
        context['pacientes'] = None
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        context = self.get_context_data()
        if form.is_valid():
            fecha_inicio = form.cleaned_data['fecha_inicio']
            fecha_fin = form.cleaned_data['fecha_fin']

            pacientes = Paciente.objects.filter(
                fecha_nacimiento__range=(fecha_inicio, fecha_fin)
            ).order_by('fecha_nacimiento')

            context['pacientes'] = pacientes
            context['form'] = form
        else:
            context['form'] = form

        return self.render_to_response(context)

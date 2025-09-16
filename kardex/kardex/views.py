from kardex.base_views import BaseCRUDView
from kardex.forms.comunas import FormComuna
from kardex.forms.establecimientos import FormEstablecimiento

from kardex.models import Establecimiento, Comuna


class BaseCRUDEstablecimientoView(BaseCRUDView):
    model = Establecimiento
    form_class = FormEstablecimiento
    template_name = 'crud/index.html'
    success_url = 'establishment_active'
    exclude_fields = ['created_at', 'updated_at', 'status']
    title = 'Establecimientos'

    active_url_name = 'kardex:establishment_active'
    inactive_url_name = 'kardex:establishment_inactive'
    update_url_name = 'kardex:establishment_update'
    toggle_url_name = 'kardex:establishment_toggle_status'
    # history_url_name = 'kardex:establishment_history'
    # export_report_url_name = 'reports:export_establishment'


class EstablecimientoView(BaseCRUDEstablecimientoView):
    success_url = 'establishment_active'

    def get_queryset(self):
        return Establecimiento.objects.filter(status='ACTIVE').order_by('-updated_at')


class EstablecimientoInactiveView(BaseCRUDEstablecimientoView):
    success_url = 'establishment_inactive'

    def get_queryset(self):
        return Establecimiento.objects.filter(status='INACTIVE').order_by('-updated_at')


class BaseCRUDComunaView(BaseCRUDView):
    model = Comuna
    form_class = FormComuna
    template_name = 'crud/index.html'
    success_url = 'commune_active'
    exclude_fields = ['created_at', 'updated_at', 'status']
    title = 'Comunas'

    active_url_name = 'kardex:commune_active'
    inactive_url_name = 'kardex:commune_inactive'
    update_url_name = 'kardex:commune_update'
    toggle_url_name = 'kardex:commune_toggle_status'
    # history_url_name = 'kardex:commune_history'
    # export_report_url_name = 'reports:export_commune'


class ComunaView(BaseCRUDComunaView):
    success_url = 'commune_active'

    def get_queryset(self):
        return Comuna.objects.filter(status='ACTIVE').order_by('-updated_at')


class ComunaInactiveView(BaseCRUDComunaView):
    success_url = 'commune_inactive'

    def get_queryset(self):
        return Comuna.objects.filter(status='INACTIVE').order_by('-updated_at')

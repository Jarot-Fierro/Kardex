from kardex.base_views import BaseCRUDView
from kardex.forms.commune import FormCommune
from kardex.forms.establishment import FormEstablishment

from kardex.models import Establishment, Commune


class BaseCRUDEstablishmentView(BaseCRUDView):
    model = Establishment
    form_class = FormEstablishment
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


class EstablishmentView(BaseCRUDEstablishmentView):
    success_url = 'establishment_active'

    def get_queryset(self):
        return Establishment.objects.filter(status='ACTIVE').order_by('-updated_at')


class EstablishmentInactiveView(BaseCRUDEstablishmentView):
    success_url = 'establishment_inactive'

    def get_queryset(self):
        return Establishment.objects.filter(status='INACTIVE').order_by('-updated_at')


class BaseCRUDCommuneView(BaseCRUDView):
    model = Commune
    form_class = FormCommune
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


class CommuneView(BaseCRUDCommuneView):
    success_url = 'commune_active'

    def get_queryset(self):
        return Commune.objects.filter(status='ACTIVE').order_by('-updated_at')


class CommuneInactiveView(BaseCRUDCommuneView):
    success_url = 'commune_inactive'

    def get_queryset(self):
        return Commune.objects.filter(status='INACTIVE').order_by('-updated_at')

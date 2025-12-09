# kardex/views/tickets.py

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.views.generic import CreateView

from kardex.forms.soporte import SoporteForm
from kardex.models import Soporte


class TicketCreateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    CreateView
):
    model = Soporte
    form_class = SoporteForm
    template_name = 'kardex/soporte/ticket_form.html'

    # redirige a crear nuevo ticket o listado si quieres
    success_url = reverse_lazy('kardex:ticket_create')

    permission_required = 'kardex.add_ticket'
    raise_exception = True

    def form_valid(self, form):
        user = self.request.user

        if not user.establecimiento:
            raise PermissionDenied("El usuario no tiene establecimiento asignado.")

        ticket = form.save(commit=False)
        ticket.creado_por = user
        ticket.establecimiento = user.establecimiento
        ticket.save()

        messages.success(self.request, '✅ Ticket creado correctamente')
        return super().form_valid(form)

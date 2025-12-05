# views.py
import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView

from kardex.forms.movimiento_ficha_update import FormSalidaFicha
from kardex.models import MovimientoFicha


class SalidaFicha2View(LoginRequiredMixin, CreateView):
    """
    Vista para registro masivo de salidas de fichas con AJAX.
    Optimizada para escaneo continuo con lector de códigos de barras.
    """
    model = MovimientoFicha
    form_class = FormSalidaFicha
    template_name = 'kardex/movimiento_ficha/salida_ficha_update.html'
    success_url = reverse_lazy('lista_movimientos')

    def get_form_kwargs(self):
        """Pasar el usuario al formulario"""
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        """Agregar contexto adicional"""
        context = super().get_context_data(**kwargs)
        context['title'] = 'Registro Masivo de Salida de Fichas'
        context['subtitle'] = 'Escaneo Continuo con Lector de Códigos de Barras'
        return context

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        """Manejar peticiones AJAX"""
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return self.handle_ajax(request)
        return super().dispatch(request, *args, **kwargs)

    def handle_ajax(self, request):
        """Procesar peticiones AJAX para registro rápido"""
        if request.method == 'POST':
            try:
                data = json.loads(request.body)

                # Validar datos requeridos
                required_fields = ['ficha_id', 'servicio_envio_id',
                                   'servicio_recepcion_id', 'profesional_id']

                for field in required_fields:
                    if field not in data or not data[field]:
                        return JsonResponse({
                            'success': False,
                            'error': f'Campo requerido faltante: {field}'
                        }, status=400)

                # Crear movimiento
                movimiento = MovimientoFicha(
                    ficha_id=data['ficha_id'],
                    servicio_clinico_envio_id=data['servicio_envio_id'],
                    servicio_clinico_recepcion_id=data['servicio_recepcion_id'],
                    profesional_envio_id=data['profesional_id'],
                    observacion_envio=data.get('observacion', ''),
                    usuario_envio=request.user,
                    establecimiento=request.user.establecimiento,
                    estado_envio='ENVIADO',
                    estado_recepcion='EN ESPERA'
                )

                movimiento.save()

                return JsonResponse({
                    'success': True,
                    'message': 'Salida registrada exitosamente',
                    'movimiento_id': movimiento.id,
                    'ficha_numero': movimiento.ficha.numero_ficha_sistema if movimiento.ficha else '',
                    'timestamp': movimiento.created_at.strftime('%H:%M:%S')
                })

            except json.JSONDecodeError:
                return JsonResponse({
                    'success': False,
                    'error': 'Datos JSON inválidos'
                }, status=400)
            except Exception as e:
                return JsonResponse({
                    'success': False,
                    'error': str(e)
                }, status=500)

        return JsonResponse({
            'success': False,
            'error': 'Método no permitido'
        }, status=405)

    def form_valid(self, form):
        """Manejar envío normal del formulario"""
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # Ya manejado por handle_ajax
            return JsonResponse({'success': True})

        response = super().form_valid(form)

        # Si es una petición normal, redirigir
        if self.request.POST.get('continuar_escaneo'):
            # Mantener los valores de los servicios y profesional
            self.request.session['salida_masiva_config'] = {
                'servicio_envio_id': form.cleaned_data['servicio_clinico_envio'].id,
                'servicio_recepcion_id': form.cleaned_data['servicio_clinico_recepcion'].id,
                'profesional_id': form.cleaned_data['profesional_envio'].id,
                'observacion': form.cleaned_data['observacion_envio']
            }
            return redirect('salida_ficha_masiva')

        return response

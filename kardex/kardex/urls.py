from django.urls import path

from kardex.views import *

app_name = 'kardex'

urlpatterns = [
    path('establecimientos', EstablecimientoView.as_view(), name='establishment_active'),
    path('establecimientos/<int:pk>', EstablecimientoView.as_view(), name='establishment_update'),

    path('comunas', ComunaView.as_view(), name='commune_active'),
    path('comunas/<int:pk>', ComunaView.as_view(), name='commune_update'),
]

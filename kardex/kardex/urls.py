from django.urls import path

from kardex.views import *

app_name = 'kardex'

urlpatterns = [
    path('establecimientos', EstablishmentView.as_view(), name='establishment_active'),
    path('establecimientos/<int:pk>', EstablishmentView.as_view(), name='establishment_update'),

    path('comunas', CommuneView.as_view(), name='commune_active'),
    path('comunas/<int:pk>', CommuneView.as_view(), name='commune_update'),
]

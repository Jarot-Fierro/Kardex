from django.contrib import admin
from django.urls import path, include

from kardex.views.api.movimiento_ficha import router
from kardex.views.home import HomeDashboardView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeDashboardView.as_view(), name="index"),
    path('kardex/', include('kardex.urls'), name="kardex-home"),
    path('usuarios/', include('usuarios.urls'), name="usuarios"),
    path('api-auth/v1/', include('rest_framework.urls')),
    path('api-auth/routers/', include(router.urls)),
]

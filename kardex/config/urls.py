from django.contrib import admin
from django.shortcuts import render
from django.urls import path, include


def index(request):
    return render(request, 'kardex/index.html')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name="index"),
    path('kardex/', include('kardex.urls'), name="index"),
    path('usuarios/', include('usuarios.urls'), name="usuarios"),
]

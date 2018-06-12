# -*- coding: utf-8 -*-
from django.urls import path
# from django.urls import include, path
from django.contrib.auth.decorators import login_required

from . import views
from .views.usuaris import UsuarisView
from .views.consulta import ConsultaView

# Només després
# from .views.classificacio import ClassificacioView

app_name = 'joc'
urlpatterns = [
    # Comunes
    path('', views.index, name='index'),
    path('consulta_grups', views.consulta_grups, name='consulta_grups'),
    path('consulta', login_required(ConsultaView.as_view()), name='consulta'),
    path('usuaris', login_required(UsuarisView.as_view()), name='usuaris'),
    path('puntuacions', views.puntuacions, name='puntuacions'),
    # # Només abans
    path('pronostic', views.pronostic, name='pronostic'),
    # # Només després
    # path(r'^classificacio$', login_required(ClassificacioView.as_view()), name='classificacio'),
    # url(r'^entrada_admin$', views.entrada_admin, name='entrada_admin'),
    # url(r'^pronostic_admin$', views.pronostic_admin, name='pronostic'),
]

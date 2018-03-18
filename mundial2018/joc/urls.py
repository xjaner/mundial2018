# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from . import views
from views.usuaris import UsuarisView
from views.consulta import ConsultaView
from views.classificacio import ClassificacioView

app_name = 'joc'
urlpatterns = [
    # Comunes
    url(r'^$', views.index, name='index'),
    url(r'^consulta_grups$', views.consulta_grups, name='consulta_grups'),
    url(r'^consulta$', login_required(ConsultaView.as_view()), name='consulta'),
    url(r'^usuaris$', login_required(UsuarisView.as_view()), name='usuaris'),
    url(r'^entrada_admin$', views.entrada_admin, name='entrada_admin'),
    url(r'^pronostic_admin$', views.pronostic_admin, name='pronostic'),
    url(r'^puntuacions$', views.puntuacions, name='puntuacions'),
    # Només abans
    # url(r'^pronostic$', views.pronostic, name='pronostic'),
    # Només després
    url(r'^classificacio$', login_required(ClassificacioView.as_view()), name='classificacio'),
]

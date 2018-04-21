from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from joc.models import Jugador, PronosticEquipGrup
from joc.utils import NUM_EQUIPS


@login_required
def index(request):
    jugador = Jugador.objects.get(usuari=request.user)
    pronostic_acabat = PronosticEquipGrup.objects.filter(
        jugador=jugador, posicio__gt=0).count() == NUM_EQUIPS
    return render(
        request,
        'joc/index.html',
        {
            'jugador': jugador,
            'pronostic_acabat': pronostic_acabat,
        }
    )

from collections import OrderedDict

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from joc.models import PronosticEquipGrup
from joc.utils import FASE_GRUPS


@login_required
def consulta_grups(request):
    grups = OrderedDict()
    for grup in FASE_GRUPS:
        grups[grup] = list(
            PronosticEquipGrup.objects.filter(jugador__usuari=request.user,
                                              equip__grup__nom=grup,
                                              ).order_by('posicio'))

    return render(
        request,
        'joc/consulta_grups.html',
        {
            'grups': grups,
            'height_banderes': 19,
            'width_banderes': 28,
            'border_banderes': 1,
        }
    )

# -*- coding: utf-8 -*-
from itertools import groupby

from django.conf import settings

from joc.models import Partit, PronosticPartit, PronosticEquipGrup, Equip

GOLS_CHOICES = (('-1', '-'), (0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7),
                (8, 8))
EMPAT_CHOICES = ((1, 1), (2, 2))
GUARDA_GRUPS = set(['B', 'C', 'D', 'E', 'F', 'G'])
FASE_GRUPS = set(['A', 'B', 'C', 'D', 'E', 'F'])
VUITENS = set(['G'])
QUARTS = set(['H'])
SEMIS = set(['I'])
FINAL = set(['J'])
CREAR_PARTITS = set(['G', 'H', 'I', 'J'])
COMPROVAR_TERCERS = set(['G'])
ACABA_PRONOSTIC = set(['K'])
TEXT_GRUP = {
    'A': 'Grup A',
    'B': 'Grup B',
    'C': 'Grup C',
    'D': 'Grup D',
    'E': 'Grup E',
    'F': 'Grup F',
    'G': 'Vuitens de final',
    'H': 'Quarts de final',
    'I': 'Semifinals',
    'J': 'Final',
}

ULTIM_PARTIT_GRUPS = 36
ULTIM_PARTIT_VUITENS = 44
ULTIM_PARTIT_QUARTS = 48
ULTIM_PARTIT_SEMIS = 50


FUNCIO_ORDRE = lambda x: (x.punts, x.diferencia, x.favor)

POSICIO_TERCERS = {
    frozenset(['A', 'B', 'C', 'D']): {'WA': 'C', 'WB': 'D', 'WC': 'A', 'WD': 'B'},
    frozenset(['A', 'B', 'C', 'E']): {'WA': 'C', 'WB': 'A', 'WC': 'B', 'WD': 'E'},
    frozenset(['A', 'B', 'C', 'F']): {'WA': 'C', 'WB': 'A', 'WC': 'B', 'WD': 'F'},
    frozenset(['A', 'B', 'D', 'E']): {'WA': 'D', 'WB': 'A', 'WC': 'B', 'WD': 'E'},
    frozenset(['A', 'B', 'D', 'F']): {'WA': 'D', 'WB': 'A', 'WC': 'B', 'WD': 'F'},
    frozenset(['A', 'B', 'E', 'F']): {'WA': 'E', 'WB': 'A', 'WC': 'B', 'WD': 'F'},
    frozenset(['A', 'C', 'D', 'E']): {'WA': 'C', 'WB': 'D', 'WC': 'A', 'WD': 'E'},
    frozenset(['A', 'C', 'D', 'F']): {'WA': 'C', 'WB': 'D', 'WC': 'A', 'WD': 'F'},
    frozenset(['A', 'C', 'E', 'F']): {'WA': 'C', 'WB': 'A', 'WC': 'F', 'WD': 'E'},
    frozenset(['A', 'D', 'E', 'F']): {'WA': 'D', 'WB': 'A', 'WC': 'F', 'WD': 'E'},
    frozenset(['B', 'C', 'D', 'E']): {'WA': 'C', 'WB': 'D', 'WC': 'B', 'WD': 'E'},
    frozenset(['B', 'C', 'D', 'F']): {'WA': 'C', 'WB': 'D', 'WC': 'B', 'WD': 'F'},
    frozenset(['B', 'C', 'E', 'F']): {'WA': 'E', 'WB': 'C', 'WC': 'B', 'WD': 'F'},
    frozenset(['B', 'D', 'E', 'F']): {'WA': 'E', 'WB': 'D', 'WC': 'B', 'WD': 'F'},
    frozenset(['C', 'D', 'E', 'F']): {'WA': 'C', 'WB': 'D', 'WC': 'F', 'WD': 'E'},
}


def get_or_create_and_reset_pronostic_partit(id_partit, jugador, id_equip1, id_equip2, admin=False):
    try:
        pronostic_partit = PronosticPartit.objects.get(jugador=jugador, partit_id=id_partit)
    except PronosticPartit.DoesNotExist:
        PronosticPartit.objects.create(jugador=jugador, partit_id=id_partit, equip1_id=id_equip1,
                                       equip2_id=id_equip2)
    else:
        if pronostic_partit.equip1_id != id_equip1 or pronostic_partit.equip2_id != id_equip2:
            pronostic_partit.equip1_id = id_equip1
            pronostic_partit.equip2_id = id_equip2
            pronostic_partit.gols1 = -1
            pronostic_partit.gols2 = -1
            pronostic_partit.empat = None
            pronostic_partit.save()
    if admin:
        partit = Partit.objects.get(pk=id_partit)
        partit.equip1_id = id_equip1
        partit.equip2_id = id_equip2
        partit.save()


def crea_final(request, jugador, admin=False):
    get_or_create_and_reset_pronostic_partit(
        51,
        jugador,
        PronosticPartit.objects.get(
            jugador=jugador,
            partit_id=49
        ).guanyador().id,
        PronosticPartit.objects.get(
            jugador=jugador,
            partit_id=50
        ).guanyador().id,
        admin,
    )


def crea_semis(request, jugador, admin=False):
    get_or_create_and_reset_pronostic_partit(
        49,
        jugador,
        PronosticPartit.objects.get(
            jugador=jugador,
            partit_id=45
        ).guanyador().id,
        PronosticPartit.objects.get(
            jugador=jugador,
            partit_id=46
        ).guanyador().id,
        admin,
    )

    get_or_create_and_reset_pronostic_partit(
        50,
        jugador,
        PronosticPartit.objects.get(
            jugador=jugador,
            partit_id=47
        ).guanyador().id,
        PronosticPartit.objects.get(
            jugador=jugador,
            partit_id=48
        ).guanyador().id,
        admin,
    )


def crea_quarts(request, jugador, admin=False):
    get_or_create_and_reset_pronostic_partit(
        45,
        jugador,
        PronosticPartit.objects.get(
            jugador=jugador,
            partit_id=37
        ).guanyador().id,
        PronosticPartit.objects.get(
            jugador=jugador,
            partit_id=39
        ).guanyador().id,
        admin,
    )

    get_or_create_and_reset_pronostic_partit(
        46,
        jugador,
        PronosticPartit.objects.get(
            jugador=jugador,
            partit_id=38
        ).guanyador().id,
        PronosticPartit.objects.get(
            jugador=jugador,
            partit_id=42
        ).guanyador().id,
        admin,
    )

    get_or_create_and_reset_pronostic_partit(
        47,
        jugador,
        PronosticPartit.objects.get(
            jugador=jugador,
            partit_id=41
        ).guanyador().id,
        PronosticPartit.objects.get(
            jugador=jugador,
            partit_id=43
        ).guanyador().id,
        admin,
    )

    get_or_create_and_reset_pronostic_partit(
        48,
        jugador,
        PronosticPartit.objects.get(
            jugador=jugador,
            partit_id=40
        ).guanyador().id,
        PronosticPartit.objects.get(
            jugador=jugador,
            partit_id=44
        ).guanyador().id,
        admin,
    )


def crea_vuitens(request, jugador, admin=False):
    tercers = PronosticEquipGrup.objects.filter(jugador=jugador,
                                                posicio=3)
    tercers_ordenats = sorted(tercers, key=FUNCIO_ORDRE, reverse=True)[:4]
    grups_millors_tercers = frozenset([peg.equip.grup.nom for peg in tercers_ordenats])
    emparellaments_tercers = POSICIO_TERCERS[grups_millors_tercers]

    get_or_create_and_reset_pronostic_partit(
        37,
        jugador,
        PronosticEquipGrup.objects.get(
            jugador=jugador,
            equip__grup__nom='A',
            posicio=2,
        ).equip.id,
        PronosticEquipGrup.objects.get(
            jugador=jugador,
            equip__grup__nom='C',
            posicio=2,
        ).equip.id,
        admin,
    )

    get_or_create_and_reset_pronostic_partit(
        38,
        jugador,
        PronosticEquipGrup.objects.get(
            jugador=jugador,
            equip__grup__nom='B',
            posicio=1,
        ).equip.id,
        PronosticEquipGrup.objects.get(
            jugador=jugador,
            equip__grup__nom=emparellaments_tercers['WB'],
            posicio=3,
        ).equip.id,
        admin,
    )

    get_or_create_and_reset_pronostic_partit(
        39,
        jugador,
        PronosticEquipGrup.objects.get(
            jugador=jugador,
            equip__grup__nom='D',
            posicio=1,
        ).equip.id,
        PronosticEquipGrup.objects.get(
            jugador=jugador,
            equip__grup__nom=emparellaments_tercers['WD'],
            posicio=3,
        ).equip.id,
        admin,
    )

    get_or_create_and_reset_pronostic_partit(
        40,
        jugador,
        PronosticEquipGrup.objects.get(
            jugador=jugador,
            equip__grup__nom='A',
            posicio=1,
        ).equip.id,
        PronosticEquipGrup.objects.get(
            jugador=jugador,
            equip__grup__nom=emparellaments_tercers['WA'],
            posicio=3,
        ).equip.id,
        admin,
    )

    get_or_create_and_reset_pronostic_partit(
        41,
        jugador,
        PronosticEquipGrup.objects.get(
            jugador=jugador,
            equip__grup__nom='C',
            posicio=1,
        ).equip.id,
        PronosticEquipGrup.objects.get(
            jugador=jugador,
            equip__grup__nom=emparellaments_tercers['WC'],
            posicio=3,
        ).equip.id,
        admin,
    )

    get_or_create_and_reset_pronostic_partit(
        42,
        jugador,
        PronosticEquipGrup.objects.get(
            jugador=jugador,
            equip__grup__nom='F',
            posicio=1,
        ).equip.id,
        PronosticEquipGrup.objects.get(
            jugador=jugador,
            equip__grup__nom='E',
            posicio=2,
        ).equip.id,
        admin,
    )

    get_or_create_and_reset_pronostic_partit(
        43,
        jugador,
        PronosticEquipGrup.objects.get(
            jugador=jugador,
            equip__grup__nom='E',
            posicio=1,
        ).equip.id,
        PronosticEquipGrup.objects.get(
            jugador=jugador,
            equip__grup__nom='D',
            posicio=2,
        ).equip.id,
        admin,
    )

    get_or_create_and_reset_pronostic_partit(
        44,
        jugador,
        PronosticEquipGrup.objects.get(
            jugador=jugador,
            equip__grup__nom='B',
            posicio=2,
        ).equip.id,
        PronosticEquipGrup.objects.get(
            jugador=jugador,
            equip__grup__nom='F',
            posicio=2,
        ).equip.id,
        admin,
    )


def crea_partits(request, jugador, nom_grup, admin=False):
    if nom_grup == 'G':
        crea_vuitens(request, jugador, admin)
    elif nom_grup == 'H':
        crea_quarts(request, jugador, admin)
    elif nom_grup == 'I':
        crea_semis(request, jugador, admin)
    elif nom_grup == 'J':
        crea_final(request, jugador, admin)


def comprova_tercers(request, jugador):
    tercers = PronosticEquipGrup.objects.filter(jugador=jugador,
                                                posicio=3)
    if len(tercers) != settings.NUM_GRUPS:
        # TODO: ERROR!
        pass

    agrupats = [{grup: [i for i in elements]}
                for grup, elements in groupby(sorted(tercers, key=FUNCIO_ORDRE, reverse=True),
                                              key=FUNCIO_ORDRE)]

    if len(agrupats) == settings.NUM_GRUPS:
        # El millor dels casos
        return None
    elif len(agrupats) == (settings.NUM_GRUPS - 1):
        if len(agrupats[-1]) == 2:
            # Empaten els 2 últims tercers, no m'importa! :)
            return None
    else:
        # return [grup.values()[0] for grup in agrupats if len(grup.values()[0]) > 1]
        return sorted(tercers, key=FUNCIO_ORDRE, reverse=True)


def guarda_classificacio_grup(request, jugador):
    for i in range(settings.EQUIPS_PER_GRUP):
        equip = Equip.objects.get(pk=int(request.POST['id%d' % (i)]))
        pronostic_equip = PronosticEquipGrup.objects.get(jugador=jugador,
                                                         equip=equip)
        pronostic_equip.posicio = i + 1
        pronostic_equip.punts = int(request.POST['p%d' % (i)])
        pronostic_equip.diferencia = int(request.POST['d%d' % (i)])
        pronostic_equip.favor = int(request.POST['g%d' % (i)])
        pronostic_equip.save()

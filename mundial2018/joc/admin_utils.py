# -*- coding: utf-8 -*-
from itertools import chain

from django.conf import settings
from django.db.models import Q

from joc.models import Jugador, PronosticPartit, PronosticEquipGrup
from joc.utils import (FASE_GRUPS, VUITENS, QUARTS, SEMIS, FINAL, ULTIM_PARTIT_GRUPS,
                       ULTIM_PARTIT_VUITENS, ULTIM_PARTIT_QUARTS, ULTIM_PARTIT_SEMIS,
                       CONSOLACIO, ULTIM_PARTIT_CONSOLACIO)


def seguent_grup_entrat(admin_form):
    for form in admin_form.forms:
        if form.instance.id == ULTIM_PARTIT_GRUPS:
            vuitens = PronosticPartit.objects.filter(
                jugador_id=settings.ID_ADMIN,
                partit__grup__nom__in=VUITENS)
            if not vuitens:
                return True
            for partit in vuitens:
                if not partit.equip1 or not partit.equip2:
                    return True
        if form.instance.id == ULTIM_PARTIT_VUITENS:
            quarts = PronosticPartit.objects.filter(
                jugador_id=settings.ID_ADMIN,
                partit__grup__nom__in=QUARTS)
            if not quarts:
                return True
            for partit in quarts:
                if not partit.equip1 or not partit.equip2:
                    return True
        if form.instance.id == ULTIM_PARTIT_QUARTS:
            semis = PronosticPartit.objects.filter(
                jugador_id=settings.ID_ADMIN,
                partit__grup__nom__in=SEMIS)
            if not semis:
                return True
            for partit in semis:
                if not partit.equip1 or not partit.equip2:
                    return True
        if form.instance.id == ULTIM_PARTIT_SEMIS:
            final = PronosticPartit.objects.filter(
                jugador_id=settings.ID_ADMIN,
                partit__grup__nom__in=CONSOLACIO)
            if not final:
                return True
            for partit in final:
                if not partit.equip1 or not partit.equip2:
                    return True
        if form.instance.id == ULTIM_PARTIT_CONSOLACIO:
            final = PronosticPartit.objects.filter(
                jugador_id=settings.ID_ADMIN,
                partit__grup__nom__in=FINAL)
            if not final:
                return True
            for partit in final:
                if not partit.equip1 or not partit.equip2:
                    return True
    return False


def obte_equips_fase_admin(fase):
    return set(list(
        chain.from_iterable(
            (partit.equip1.id, partit.equip2.id)
            for partit in PronosticPartit.objects.filter(
                jugador__usuari__id=settings.ID_ADMIN,
                partit__grup__nom__in=fase,
            )
        )
    ))


def obte_equips_fase_jugador(jugador, fase):
    return set(list(
        chain.from_iterable(
            (partit.equip1.id, partit.equip2.id)
            for partit in PronosticPartit.objects.filter(
                jugador=jugador,
                partit__grup__nom__in=fase,
            )
        )
    ))


def actualitza_partit_grups(partit):
    for jugador in Jugador.objects.filter(usuari__is_active=True).filter(
            ~Q(usuari_id=settings.ID_ADMIN)):
        punts_resultats = 0
        punts_grups = 0
        punts_equips_encertats = 0

        pronostic = PronosticPartit.objects.get(partit_id=partit.id,
                                                jugador_id=jugador.id)
        if partit.resultat_encertat(pronostic):
            punts_resultats += 4
        elif partit.signe_encertat(pronostic):
            punts_resultats += 3

        if partit.id == ULTIM_PARTIT_GRUPS:
            # Punts per encertar la classificació dels grups
            for grup in FASE_GRUPS:
                grups_admin = PronosticEquipGrup.objects.filter(
                    jugador__usuari__id=settings.ID_ADMIN,
                    equip__grup__nom=grup).order_by(
                        'posicio')
                grups_jugador = PronosticEquipGrup.objects.filter(jugador=jugador,
                                                                  equip__grup__nom=grup).order_by(
                                                                      'posicio')
                equips_posicio_correcta = 0
                for idx in range(settings.EQUIPS_PER_GRUP):
                    if grups_admin[idx].equip_id == grups_jugador[idx].equip_id:
                        equips_posicio_correcta += 1

                if equips_posicio_correcta == 1:
                    punts_grups += 2
                elif equips_posicio_correcta == 2:
                    punts_grups += 4
                elif equips_posicio_correcta == 4:
                    punts_grups += 10

            equips_vuitens_admin = obte_equips_fase_admin(VUITENS)
            equips_vuitens_pronostic = obte_equips_fase_jugador(jugador, VUITENS)

            # Punts pel número d'equips encertats a la següent fase
            equips_encertats = len(equips_vuitens_admin.intersection(equips_vuitens_pronostic))

            if equips_encertats == 1:
                punts_equips_encertats += 1
            if equips_encertats == 2:
                punts_equips_encertats += 2
            if equips_encertats == 3:
                punts_equips_encertats += 3
            if equips_encertats == 4:
                punts_equips_encertats += 4
            if equips_encertats == 5:
                punts_equips_encertats += 5
            if equips_encertats == 6:
                punts_equips_encertats += 6
            if equips_encertats == 7:
                punts_equips_encertats += 8
            if equips_encertats == 8:
                punts_equips_encertats += 11
            if equips_encertats == 9:
                punts_equips_encertats += 15
            if equips_encertats == 10:
                punts_equips_encertats += 20
            if equips_encertats == 11:
                punts_equips_encertats += 26
            if equips_encertats == 12:
                punts_equips_encertats += 33
            if equips_encertats == 13:
                punts_equips_encertats += 41
            if equips_encertats == 14:
                punts_equips_encertats += 50
            if equips_encertats == 15:
                punts_equips_encertats += 60
            if equips_encertats == 16:
                punts_equips_encertats += 75

        jugador.punts += punts_resultats + punts_grups + punts_equips_encertats
        jugador.punts_resultats += punts_resultats
        jugador.punts_grups += punts_grups
        jugador.punts_equips_encertats += punts_equips_encertats
        jugador.save()


def guarda_punts_anterior():
    for jugador in Jugador.objects.filter(usuari__is_active=True).filter(
            ~Q(usuari_id=settings.ID_ADMIN)):
        jugador.punts_anterior = jugador.punts
        jugador.save()


def actualitza_partit_vuitens(partit):
    for jugador in Jugador.objects.filter(usuari__is_active=True).filter(
            ~Q(usuari_id=settings.ID_ADMIN)):
        punts_resultats = 0
        punts_grups = 0
        punts_equips_encertats = 0

        pronostic = PronosticPartit.objects.get(partit_id=partit.id,
                                                jugador_id=jugador.id)
        if (partit.equip1.id == pronostic.equip1.id and
                partit.equip2.id == pronostic.equip2.id):
            if partit.resultat_encertat(pronostic):
                punts_resultats += 7
            elif partit.signe_encertat(pronostic):
                punts_resultats += 5

        if partit.id == ULTIM_PARTIT_VUITENS:
            equips_quarts_admin = obte_equips_fase_admin(QUARTS)
            equips_quarts_pronostic = obte_equips_fase_jugador(jugador, QUARTS)

            # Punts pel número d'equips encertats a la següent fase
            equips_encertats = len(equips_quarts_admin.intersection(equips_quarts_pronostic))

            if equips_encertats == 1:
                punts_equips_encertats += 3
            if equips_encertats == 2:
                punts_equips_encertats += 6
            if equips_encertats == 3:
                punts_equips_encertats += 10
            if equips_encertats == 4:
                punts_equips_encertats += 17
            if equips_encertats == 5:
                punts_equips_encertats += 27
            if equips_encertats == 6:
                punts_equips_encertats += 40
            if equips_encertats == 7:
                punts_equips_encertats += 55
            if equips_encertats == 8:
                punts_equips_encertats += 75

        jugador.punts += punts_resultats + punts_grups + punts_equips_encertats
        jugador.punts_resultats += punts_resultats
        jugador.punts_grups += punts_grups
        jugador.punts_equips_encertats += punts_equips_encertats
        jugador.save()


def actualitza_partit_quarts(partit):
    for jugador in Jugador.objects.filter(usuari__is_active=True).filter(
            ~Q(usuari_id=settings.ID_ADMIN)):
        punts_resultats = 0
        punts_grups = 0
        punts_equips_encertats = 0

        pronostic = PronosticPartit.objects.get(partit_id=partit.id,
                                                jugador_id=jugador.id)
        # Punts per equips en posició correcta
        if partit.equip1.id == pronostic.equip1.id:
            punts_grups += 5
        if partit.equip2.id == pronostic.equip2.id:
            punts_grups += 5

        # Punts pel resultat
        if (partit.equip1.id == pronostic.equip1.id and
                partit.equip2.id == pronostic.equip2.id):
            if partit.resultat_encertat(pronostic):
                punts_resultats += 10
            elif partit.signe_encertat(pronostic):
                punts_resultats += 7

        if partit.id == ULTIM_PARTIT_QUARTS:
            equips_semis_admin = obte_equips_fase_admin(SEMIS)
            equips_semis_pronostic = obte_equips_fase_jugador(jugador, SEMIS)

            # Punts pel número d'equips encertats a la següent fase
            equips_encertats = len(equips_semis_admin.intersection(equips_semis_pronostic))

            if equips_encertats == 1:
                punts_equips_encertats += 8
            if equips_encertats == 2:
                punts_equips_encertats += 20
            if equips_encertats == 3:
                punts_equips_encertats += 40
            if equips_encertats == 4:
                punts_equips_encertats += 75

        jugador.punts += punts_resultats + punts_grups + punts_equips_encertats
        jugador.punts_resultats += punts_resultats
        jugador.punts_grups += punts_grups
        jugador.punts_equips_encertats += punts_equips_encertats
        jugador.save()


def actualitza_partit_semis(partit):
    for jugador in Jugador.objects.filter(usuari__is_active=True).filter(
            ~Q(usuari_id=settings.ID_ADMIN)):
        punts_resultats = 0
        punts_grups = 0
        punts_equips_encertats = 0

        pronostic = PronosticPartit.objects.get(partit_id=partit.id,
                                                jugador_id=jugador.id)

        # Punts per equips en posició correcta
        if partit.equip1.id == pronostic.equip1.id:
            punts_grups += 10
        if partit.equip2.id == pronostic.equip2.id:
            punts_grups += 10

        # Punts pel resultat
        if (partit.equip1.id == pronostic.equip1.id and
                partit.equip2.id == pronostic.equip2.id):
            if partit.resultat_encertat(pronostic):
                punts_resultats += 14
            elif partit.signe_encertat(pronostic):
                punts_resultats += 10

        if partit.id == ULTIM_PARTIT_SEMIS:
            equips_final_admin = obte_equips_fase_admin(FINAL)
            equips_final_pronostic = obte_equips_fase_jugador(jugador, FINAL)

            # Punts pel número d'equips encertats a la següent fase
            equips_encertats = len(equips_final_admin.intersection(equips_final_pronostic))

            if equips_encertats == 1:
                punts_equips_encertats += 30
            if equips_encertats == 2:
                punts_equips_encertats += 75

        jugador.punts += punts_resultats + punts_grups + punts_equips_encertats
        jugador.punts_resultats += punts_resultats
        jugador.punts_grups += punts_grups
        jugador.punts_equips_encertats += punts_equips_encertats
        jugador.save()


def actualitza_partit_consolacio(partit):
    for jugador in Jugador.objects.filter(usuari__is_active=True).filter(
            ~Q(usuari_id=settings.ID_ADMIN)):
        punts_resultats = 0
        punts_grups = 0
        punts_equips_encertats = 0

        pronostic = PronosticPartit.objects.get(partit_id=partit.id,
                                                jugador_id=jugador.id)

        # Punts per equips en posició correcta
        if partit.equip1.id == pronostic.equip1.id:
            punts_grups += 10
        if partit.equip2.id == pronostic.equip2.id:
            punts_grups += 10

        # Punts pel resultat
        if (partit.equip1.id == pronostic.equip1.id and
                partit.equip2.id == pronostic.equip2.id):
            if partit.resultat_encertat(pronostic):
                punts_resultats += 20
            elif partit.signe_encertat(pronostic):
                punts_resultats += 14

        if partit.guanyador().id == pronostic.guanyador().id:
            punts_grups += 15

        if partit.perdedor().id == pronostic.perdedor().id:
            punts_grups += 10

        jugador.punts += punts_resultats + punts_grups + punts_equips_encertats
        jugador.punts_resultats += punts_resultats
        jugador.punts_grups += punts_grups
        jugador.punts_equips_encertats += punts_equips_encertats
        jugador.save()


def actualitza_partit_final(partit):
    for jugador in Jugador.objects.filter(usuari__is_active=True).filter(
            ~Q(usuari_id=settings.ID_ADMIN)):
        punts_resultats = 0
        punts_grups = 0
        punts_equips_encertats = 0

        pronostic = PronosticPartit.objects.get(partit_id=partit.id,
                                                jugador_id=jugador.id)

        # Punts per equips en posició correcta
        if partit.equip1.id == pronostic.equip1.id:
            punts_grups += 10
        if partit.equip2.id == pronostic.equip2.id:
            punts_grups += 10

        # Punts pel resultat
        if (partit.equip1.id == pronostic.equip1.id and
                partit.equip2.id == pronostic.equip2.id):
            if partit.resultat_encertat(pronostic):
                punts_resultats += 20
            elif partit.signe_encertat(pronostic):
                punts_resultats += 14

        if partit.guanyador().id == pronostic.guanyador().id:
            punts_grups += 50

        if partit.perdedor().id == pronostic.perdedor().id:
            punts_grups += 25

        jugador.punts += punts_resultats + punts_grups + punts_equips_encertats
        jugador.punts_resultats += punts_resultats
        jugador.punts_grups += punts_grups
        jugador.punts_equips_encertats += punts_equips_encertats
        jugador.save()


def actualitza_posicions():
    for posicio, jugador in enumerate(Jugador.objects.filter(
            usuari__is_active=True).filter(~Q(usuari_id=settings.ID_ADMIN)).order_by('-punts')):
        jugador.posicio_anterior = jugador.posicio
        jugador.posicio = posicio + 1
        jugador.save()


def actualitza_classificacio(admin_form):
    guarda_punts_anterior()
    for form in admin_form.forms:
        if form.instance.grup.nom in FASE_GRUPS:
            actualitza_partit_grups(form.instance)
        elif form.instance.grup.nom in VUITENS:
            actualitza_partit_vuitens(form.instance)
        elif form.instance.grup.nom in QUARTS:
            actualitza_partit_quarts(form.instance)
        elif form.instance.grup.nom in SEMIS:
            actualitza_partit_semis(form.instance)
        elif form.instance.grup.nom in CONSOLACIO:
            actualitza_partit_consolacio(form.instance)
        elif form.instance.grup.nom in FINAL:
            actualitza_partit_final(form.instance)
    actualitza_posicions()

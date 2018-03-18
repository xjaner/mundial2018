# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django import forms
from django.shortcuts import redirect, render

from joc.models import Grup, Jugador, Equip, Partit, PronosticPartit, PronosticEquipGrup
from joc.utils import (
    GOLS_CHOICES, EMPAT_CHOICES, GUARDA_GRUPS, FASE_GRUPS, COMPROVAR_TERCERS, ACABA_PRONOSTIC,
    TEXT_GRUP, crea_partits, comprova_tercers, guarda_classificacio_grup, CREAR_PARTITS)


class PartitForm(forms.ModelForm):
    gols1 = forms.ChoiceField(choices=GOLS_CHOICES,
                              widget=forms.Select(attrs={"onChange": 'actualitza()'}))
    gols2 = forms.ChoiceField(choices=GOLS_CHOICES,
                              widget=forms.Select(attrs={"onChange": 'actualitza()'}))
    empat = forms.ChoiceField(choices=EMPAT_CHOICES,
                              widget=forms.RadioSelect,
                              required=False)

    def __init__(self, *args, **kwargs):
        super(PartitForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk and ((instance.gols1 == -1 and instance.gols2 == -1) or (
                instance.gols1 != -1 and instance.gols1 != instance.gols2)):
            self.fields['empat'].widget.attrs['disabled'] = True

        if instance.partit.grup.nom in FASE_GRUPS:
            self.fields['gols1'].widget.attrs['onChange'] = 'actualitza()'
            self.fields['gols2'].widget.attrs['onChange'] = 'actualitza()'
        else:
            self.fields['gols1'].widget.attrs['onChange'] = 'actualitzaEliminatoria()'
            self.fields['gols2'].widget.attrs['onChange'] = 'actualitzaEliminatoria()'
            self.fields['empat'].widget.attrs['onChange'] = 'actualitzaEliminatoria()'

    class Meta:
        model = PronosticPartit
        fields = ('gols1', 'gols2', 'empat')


GrupForm = forms.modelformset_factory(PronosticPartit, form=PartitForm, extra=0)


@login_required
def pronostic(request):

    jugador = Jugador.objects.get(usuari=request.user)
    nom_grup = request.GET.get('grup', 'A')

    # Si és un POST, guardem els valors del formulari
    if request.method == 'POST':

        grup_form = GrupForm(request.POST)
        if grup_form.is_valid():
            grup_form.save()
        else:
            # TODO: Falta crear una pàgina d'error i que em notifiqui!
            pass

        # Si s'han de guardar classificacions d'equips
        if nom_grup in GUARDA_GRUPS:
            guarda_classificacio_grup(request, jugador)
        if nom_grup in CREAR_PARTITS:
            crea_partits(request, jugador, nom_grup)

        if nom_grup in COMPROVAR_TERCERS:
            tercers_empatats = comprova_tercers(request, jugador)

            if tercers_empatats:
                return render(
                    request,
                    'joc/tercers.html',
                    {
                        'formset': grup_form,
                        'jugador': jugador,
                        'tercers': tercers_empatats,
                        'text_grup': 'Tercers empatats',
                        'grup': 'F',
                        'height_banderes': 19,
                        'width_banderes': 28,
                        'border_banderes': 1,
                    }
                )

    if nom_grup in ACABA_PRONOSTIC:
        return redirect('/')

    grup = Grup.objects.get(nom=nom_grup)
    try:
        seguent_grup = Grup.objects.get(id=grup.id + 1).nom
    except Grup.DoesNotExist:
        seguent_grup = 'G'

    partits = Partit.objects.filter(grup=grup)

    # Creem els PronosticPartit que faltin
    for partit in partits:
        items = {}
        if nom_grup in FASE_GRUPS:
            items['equip1'] = partit.equip1
            items['equip2'] = partit.equip2

        PronosticPartit.objects.get_or_create(jugador=jugador, partit=partit, **items)

    grup_form = GrupForm(queryset=PronosticPartit.objects.filter(
        jugador=jugador, partit__grup__nom=grup))

    equips_classificacio = []
    template = 'grup.html'
    if nom_grup in FASE_GRUPS:

        # Creem els PronosticEquipGrup que faltin
        equips_classificacio = []
        deshabilita_submit = True
        for equip in Equip.objects.filter(grup__nom=grup):
            equip_classificacio, _ = PronosticEquipGrup.objects.get_or_create(jugador=jugador,
                                                                              equip=equip)
            equips_classificacio.append(equip_classificacio)
            if equip_classificacio.posicio != 0:
                deshabilita_submit = False
    else:
        deshabilita_submit = False
        for form in grup_form.forms:
            if form.instance.gols1 == -1 or form.instance.gols2 == -1:
                deshabilita_submit = True
                break
            elif form.instance.gols1 == form.instance.gols2 and not form.instance.empat:
                deshabilita_submit = True
                break

    return render(
        request,
        'joc/{template}'.format(template=template),
        {
            'formset': grup_form,
            'equips_classificacio': sorted(equips_classificacio, key=lambda k: k.posicio),
            'height_banderes': 19,
            'width_banderes': 28,
            'border_banderes': 1,
            'grup': grup.nom,
            'seguent_grup': seguent_grup,
            'deshabilita_submit': deshabilita_submit,
            'text_grup': TEXT_GRUP[nom_grup],
        }
    )

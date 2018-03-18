# -*- coding: utf-8 -*-
import datetime

from django.shortcuts import render
from django import forms
from django.contrib.admin.views.decorators import staff_member_required

from joc.models import Partit
from joc.utils import GOLS_CHOICES, EMPAT_CHOICES
from joc.admin_utils import actualitza_classificacio, seguent_grup_entrat
from joc.views import pronostic


class PartitAdminForm(forms.ModelForm):
    gols1 = forms.ChoiceField(choices=GOLS_CHOICES,
                              widget=forms.Select(attrs={"onChange": 'admin_actualitza()'}))
    gols2 = forms.ChoiceField(choices=GOLS_CHOICES,
                              widget=forms.Select(attrs={"onChange": 'admin_actualitza()'}))
    empat = forms.ChoiceField(choices=EMPAT_CHOICES,
                              widget=forms.RadioSelect,
                              required=False)

    def __init__(self, *args, **kwargs):
        super(PartitAdminForm, self).__init__(*args, **kwargs)
        self.fields['empat'].widget.attrs['disabled'] = True

    def save(self, commit=True):
        instance = super(PartitAdminForm, self).save(commit=False)
        if commit:
            if not instance.empat:
                instance.empat = None
            instance.save()
        return instance

    class Meta:
        model = Partit
        fields = ('gols1', 'gols2', 'empat')


PartitsAdminForm = forms.modelformset_factory(
    Partit,
    form=PartitAdminForm,
    extra=0,
)


@staff_member_required
def entrada_admin(request):
    # Si és un POST, guardem els valors del formulari
    if request.method == "POST":

        admin_form = PartitsAdminForm(request.POST)
        if admin_form.is_valid():
            admin_form.save()
        else:
            # TODO: Falta crear una pàgina d'error i que em notifiqui!
            pass

        try:
            actualitza_classificacio(admin_form)
        except Exception:
            # TODO: Falta crear una pàgina d'error i que em notifiqui!
            pass

    admin_form = PartitsAdminForm(
        queryset=Partit.objects.filter(
            gols1=-1,
            diaihora__lt=datetime.datetime.now()-datetime.timedelta(minutes=105),
        )
    )

    cal_entrar_grups = seguent_grup_entrat(admin_form)

    return render(
        request,
        'joc/entrada_admin.html',
        {
            'formset': admin_form,
            'height_banderes': 19,
            'width_banderes': 28,
            'border_banderes': 1,
            'cal_entrar_grups': cal_entrar_grups,
        }
    )

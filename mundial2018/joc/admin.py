from django.contrib import admin

from .models import Equip, Grup, Jugador, Partit


class PartitAdmin(admin.ModelAdmin):
    readonly_fields = ('id', )


class JugadorAdmin(admin.ModelAdmin):
    list_display = ('usuari', 'pagat', 'pronostic_acabat')

    def pronostic_acabat(self, obj):
        return bool(obj.pronosticpartit_set.filter(partit_id=64))
    pronostic_acabat.short_description = 'Pronòstic acabat?'


admin.site.register(Equip)
admin.site.register(Grup)
admin.site.register(Jugador, JugadorAdmin)
admin.site.register(Partit, PartitAdmin)

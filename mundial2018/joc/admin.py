from django.contrib import admin

from .models import Equip, Grup, Jugador, Partit


class PartitAdmin(admin.ModelAdmin):
    readonly_fields = ('id', )


class JugadorAdmin(admin.ModelAdmin):
    list_display = ('usuari__username')

admin.site.register(Equip)
admin.site.register(Grup)
admin.site.register(Jugador, JugadorAdmin)
admin.site.register(Partit, PartitAdmin)

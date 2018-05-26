from django.contrib import admin

from .models import Equip, Grup, Jugador, Partit


class PartitAdmin(admin.ModelAdmin):
    readonly_fields = ('id', )


admin.site.register(Equip)
admin.site.register(Grup)
admin.site.register(Jugador)
admin.site.register(Partit, PartitAdmin)

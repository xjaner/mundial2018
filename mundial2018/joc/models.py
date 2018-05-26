from django.db import models
from django.contrib.auth.models import User

from registration.models import RegistrationProfile
from registration.signals import user_registered


class Jugador(models.Model):
    usuari = models.OneToOneField(User, on_delete=models.CASCADE)
    pagat = models.BooleanField(default=False)
    posicio = models.SmallIntegerField()
    posicio_anterior = models.SmallIntegerField()
    punts = models.SmallIntegerField(default=0)
    punts_anterior = models.SmallIntegerField(default=0)
    punts_resultats = models.PositiveSmallIntegerField(default=0)
    punts_grups = models.PositiveSmallIntegerField(default=0)
    punts_equips_encertats = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return self.usuari.username


class Grup(models.Model):
    nom = models.CharField(max_length=32)

    def __str__(self):
        return self.nom


class Equip(models.Model):
    nom = models.CharField(max_length=128)
    bandera = models.CharField(max_length=128)
    grup = models.ForeignKey(Grup, on_delete=models.CASCADE)

    def __str__(self):
        return self.nom


class PronosticEquipGrup(models.Model):
    jugador = models.ForeignKey(Jugador, on_delete=models.CASCADE)
    equip = models.ForeignKey(Equip, on_delete=models.CASCADE)
    posicio = models.PositiveSmallIntegerField(default=0)
    punts = models.PositiveSmallIntegerField(default=0)
    diferencia = models.SmallIntegerField(default=0)
    favor = models.PositiveSmallIntegerField(default=0)


class Estadi(models.Model):
    nom = models.CharField(max_length=128)
    ciutat = models.CharField(max_length=128)


class Partit(models.Model):
    equip1 = models.ForeignKey(Equip, related_name='equip1', null=True, on_delete=models.CASCADE)
    equip2 = models.ForeignKey(Equip, related_name='equip2', null=True, on_delete=models.CASCADE)
    diaihora = models.DateTimeField()
    estadi = models.ForeignKey(Estadi, on_delete=models.CASCADE)
    grup = models.ForeignKey(Grup, on_delete=models.CASCADE)
    gols1 = models.SmallIntegerField(default=-1)
    gols2 = models.SmallIntegerField(default=-1)
    empat = models.PositiveSmallIntegerField(null=True, blank=True, default=None)

    def signe(self):
        if self.gols1 > self.gols2:
            return 1
        elif self.gols2 > self.gols1:
            return 2
        else:
            return 0

    def __str__(self):
        return u'[{pk}- {grup}] {equip1} - {equip2}'.format(
            pk=self.pk,
            grup=self.grup,
            equip1=self.equip1,
            equip2=self.equip2,
        )

    def resultat_encertat(self, pronostic):
        return (self.gols1 == pronostic.gols1 and self.gols2 == pronostic.gols2)

    def signe_encertat(self, pronostic):
        return self.signe() == pronostic.signe()

    def guanyador(self):
        if self.gols1 > self.gols2:
            return self.equip1 or self.partit.equip1
        elif self.gols2 > self.gols1:
            return self.equip2 or self.partit.equip2
        elif self.empat == 1:
            return self.equip1 or self.partit.equip1
        else:
            return self.equip2 or self.partit.equip2

    def perdedor(self):
        if self.gols1 > self.gols2:
            return self.equip2 or self.partit.equip2
        elif self.gols2 > self.gols1:
            return self.equip1 or self.partit.equip1
        elif self.empat == 1:
            return self.equip2 or self.partit.equip2
        else:
            return self.equip1 or self.partit.equip1


class PronosticPartit(models.Model):
    jugador = models.ForeignKey(Jugador, on_delete=models.CASCADE)
    partit = models.ForeignKey(Partit, on_delete=models.CASCADE)
    gols1 = models.SmallIntegerField(default=-1)
    gols2 = models.SmallIntegerField(default=-1)
    equip1 = models.ForeignKey(
        Equip, related_name='equip1_pronostic', null=True, on_delete=models.CASCADE)
    equip2 = models.ForeignKey(
        Equip, related_name='equip2_pronostic', null=True, on_delete=models.CASCADE)
    empat = models.PositiveSmallIntegerField(null=True, blank=True, default=None)

    def signe(self):
        if self.gols1 > self.gols2:
            return 1
        elif self.gols2 > self.gols1:
            return 2
        else:
            return 0

    def guanyador(self):
        if self.gols1 > self.gols2:
            return self.equip1 or self.partit.equip1
        elif self.gols2 > self.gols1:
            return self.equip2 or self.partit.equip2
        elif self.empat == 1:
            return self.equip1 or self.partit.equip1
        else:
            return self.equip2 or self.partit.equip2

    def perdedor(self):
        if self.gols1 > self.gols2:
            return self.equip2 or self.partit.equip2
        elif self.gols2 > self.gols1:
            return self.equip1 or self.partit.equip1
        elif self.empat == 1:
            return self.equip2 or self.partit.equip2
        else:
            return self.equip1 or self.partit.equip1


def user_registered_callback(sender, user, request, **kwargs):
    # We skip the user activation step
    profile = RegistrationProfile.objects.get(user_id=user.id)
    profile.activated = True
    profile.save()

    Jugador.objects.create(
        usuari=user,
        posicio=user.id,
        posicio_anterior=user.id)

user_registered.connect(user_registered_callback)

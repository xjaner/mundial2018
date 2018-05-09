# mundial2018

# Passos des de 0
1 Crear la BD:
1.1 A Postgresql: CREATE DATABASE mundial2018;
2 Migrar:
2.1 python manage.py migrate
2.2 python manage.py loaddata mundial2018
2.3 python manage.py collectstatic
2.4 instal.lar gettext
2.5 python manage.py compilemessages
3 Registrar l'administrador
3.1 Fer el registre com un usuari més
3.2 Crear manualment el model Jugador:

from joc.models import Jugador
from django.contrib.auth.models import User
user = User.objects.last()
user.is_active=True
user.is_staff=True
user.is_superuser=True
user.save()
Jugador.objects.create(
     usuari=user,
     posicio=user.id,
     posicio_anterior=user.id)

4. Actualitzar settings
4.1 ID_ADMIN

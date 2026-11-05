#!/bin/bash
# Prepara la app en la EC2: migraciones, estáticos, superusuario y datos demo opcionales.
# Uso (desde HistoriasClinicas/, con el venv activo):  set -a; source /etc/historias.env; set +a; bash ../deploy/bootstrap.sh
set -e
python manage.py migrate --noinput
python manage.py collectstatic --noinput
python manage.py shell -c "
import os
from django.contrib.auth import get_user_model
from Seguridad.models import Rol
C = get_user_model()
correo = os.environ.get('ADMIN_EMAIL', 'admin@medicampus.local')
a, created = C.objects.get_or_create(correo=correo, defaults={'is_active': True, 'is_staff': True, 'is_superuser': True})
if created:
    a.set_password(os.environ['ADMIN_PASSWORD']); a.save()
r, _ = Rol.objects.get_or_create(nombre='admin', defaults={'descripcion': 'Administrador del sistema'})
a.roles.add(r)
print('Admin listo:', correo)
"
[ "${DJANGO_SEED_DATA}" = "true" ] && python manage.py seed_all || true

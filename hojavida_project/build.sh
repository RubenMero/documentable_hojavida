#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate

# ESTA LÍNEA CREA TU USUARIO SI NO EXISTE
python manage.py shell << END
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='jsrubenmerofranco').exists():
    User.objects.create_superuser('jsrubenmerofranco', '', '12345678')
    print('Superusuario creado exitosamente')
END
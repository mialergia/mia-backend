web: gunicorn alergias.wsgi:application --log-file - --log-level debug --env DJANGO_SETTINGS_MODULE=alergias.settings.base
python manage.py collectstatic --noinput
manage.py migrate
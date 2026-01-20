#!/usr/bin/env bash
set -e

python manage.py migrate --noinput
python manage.py collectstatic --noinput

python manage.py shell -c "import os, sys; from django.contrib.auth import get_user_model; User=get_user_model(); u=os.getenv('DJANGO_SUPERUSER_USERNAME'); p=os.getenv('DJANGO_SUPERUSER_PASSWORD'); e=os.getenv('DJANGO_SUPERUSER_EMAIL'); 
( u and p and e ) or sys.exit(0); 
User.objects.filter(username=u).exists() or User.objects.create_superuser(u,e,p)"

exec gunicorn backend_analytics_server.wsgi:application --bind 0.0.0.0:${PORT}

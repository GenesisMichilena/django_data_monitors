release: python manage.py migrate --noinput && python manage.py collectstatic --noinput
web: gunicorn backend_analytics_server.wsgi:application --bind 0.0.0.0:\$PORT

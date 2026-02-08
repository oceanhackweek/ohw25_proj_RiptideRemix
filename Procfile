release: python manage.py migrate && python manage.py collectstatic --noinput
web: gunicorn riptideremix.wsgi --log-file -

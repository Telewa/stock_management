#!/usr/bin/env bash
python manage.py migrate
python manage.py collectstatic  --no-input

environment=${ENVIRONMENT:-staging}


if [ "${environment}" == "production" ]; then
  # gunicorn configuration: https://docs.gunicorn.org/en/stable/settings.html
  gunicorn --env DJANGO_SETTINGS_MODULE=configuration.settings.production configuration.wsgi:application --reload  --bind 0.0.0.0:8000
else
  python manage.py runserver 0.0.0.0:8000
fi

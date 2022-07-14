from .base import *
import os

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
CONN_MAX_AGE = 60 * 5
SITE_DOMAIN = "localhost:3000"
SITE_URL = f"http://{SITE_DOMAIN}"
CSRF_TRUSTED_ORIGINS = [
    SITE_URL,
]

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("POSTGRES_DB"),
        "USER": os.environ.get("POSTGRES_USER"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD"),
        "HOST": os.environ.get("POSTGRES_DB_HOST"),
        "PORT": os.environ.get("POSTGRES_DB_PORT"),
    },
}

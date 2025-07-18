import logging

from .common import *  # noqa

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

# SECRET CONFIGURATION
SECRET_KEY = env("DJANGO_SECRET_KEY")

DEBUG = env.bool("DJANGO_DEBUG", default=False)

# SECURITY CONFIGURATION
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_HSTS_SECONDS = 60
SECURE_HSTS_INCLUDE_SUBDOMAINS = env.bool(
    "DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS", default=True
)
SECURE_CONTENT_TYPE_NOSNIFF = env.bool(
    "DJANGO_SECURE_CONTENT_TYPE_NOSNIFF", default=True
)
SECURE_BROWSER_XSS_FILTER = True
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SECURE_SSL_REDIRECT = env.bool("DJANGO_SECURE_SSL_REDIRECT", default=True)
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
X_FRAME_OPTIONS = "DENY"

# PRODUCTION MIDDLEWARE
WHITENOISE_MIDDLEWARE = [
    "whitenoise.middleware.WhiteNoiseMiddleware",
]
MIDDLEWARE = WHITENOISE_MIDDLEWARE + MIDDLEWARE


# STORAGE CONFIGURATION
# ------------------------------------------------------------------------------
# Uploaded Media Files
# ------------------------
DEFAULT_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"

# URL that handles the media served from MEDIA_ROOT, used for managing
# stored files.
MEDIA_URL = env("DJANGO_GEOMAT_CDN_URL")

# STATICFILES
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# ALLOWED HOSTS
ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS")

# Raven Sentry client
# See https://docs.getsentry.com/hosted/clients/python/integrations/django/
INSTALLED_APPS += ("raven.contrib.django.raven_compat",)

# APPS
INSTALLED_APPS += ("gunicorn",)

# DATABASE
DATABASES = {"default": env.db("DATABASE_URL")}
DATABASES["default"]["ATOMIC_REQUESTS"] = True

# Sentry Configuration
SENTRY_DSN = env("DJANGO_SENTRY_DSN")

sentry_sdk.init(
    dsn=SENTRY_DSN, integrations=[DjangoIntegration()], send_default_pii=True
)

SENTRY_CLIENT = env(
    "DJANGO_SENTRY_CLIENT", default="raven.contrib.django.raven_compat.DjangoClient"
)
# ADMIN URL
ADMIN_URL = env("DJANGO_ADMIN_URL")

# Static

STATIC_URL = "https://{}/{}static/".format(ALLOWED_HOSTS[0], URI_PREFIX)

# EMAIL
# ------------------------------------------------------------------------------
SYSTEM_EMAIL = env("SYSTEM_EMAIL")
DEFAULT_FROM_EMAIL = SYSTEM_EMAIL
SERVER_EMAIL = env("DJANGO_SERVER_EMAIL", default=DEFAULT_FROM_EMAIL)

# Anymail with Mailgun
INSTALLED_APPS += ("anymail",)

EMAIL_BACKEND = "anymail.backends.mailjet.EmailBackend"

ANYMAIL = {
    "MAILJET_API_KEY": env("MAILJET_API_KEY"),
    "MAILJET_SECRET_KEY": env("MAILJET_SECRET_KEY"),
}
# Unlikely to change this as mentioned here https://anymail.readthedocs.io/en/stable/esps/mailjet/#settings
MAILJET_API_URL = "https://api.mailjet.com/v3.1/"

PROJECT_NAME = env("PROJECT_NAME", default="")

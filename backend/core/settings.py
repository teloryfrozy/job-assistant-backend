"""
QUICK-START DEVELOPMENT SETTINGS - UNSUITABLE FOR PRODUCTION

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/
"""

from pathlib import Path
from datetime import timedelta
from job_assistant.constants import DJANGO_SECRET_KEY


######################## GENERAL CONFIGURATION ########################
BASE_DIR = Path(__file__).resolve().parent.parent
CUSTOM_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
SECRET_KEY = DJANGO_SECRET_KEY
BACKEND_LOG_PATH = "backend.log"
BACKEND_JSON_LOG = "logger.json"

# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

######################## SCHEDULED TASKS ########################
# under developement (do not delete)
# visual tool: https://crontab.guru/
CRONJOBS = [
    ("0 3 * * SUN", "backend.core.scheduled_tasks.adzuna_run") # At 03:00 on Sunday
]


######################## SECURITY ########################
DEBUG = True
ALLOWED_HOSTS = ["127.0.0.1"]
CORS_ALLOW_ALL_ORIGINS = False
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

SIMPLE_JWT = {
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),  # Token expires in 1 day
    "ROTATE_REFRESH_TOKENS": False,
    "ALGORITHM": "HS256",
    "VERIFYING_KEY": None,
    "VALIDATED_KEY": None,
    "AUDIENCE": None,
    "ISSUER": None,
    "JWK_URL": None,
    "LEEWAY": 0,
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "basic",
            "level": "INFO",
        },
        "file": {
            "class": "logging.FileHandler",
            "filename": BACKEND_JSON_LOG,
            "level": "ERROR",
            "formatter": "json",
        },
    },
    "loggers": {
        "django": {  # Exclude Django's logs
            "handlers": ["console"],
            "propagate": False,
        },
        "": {
            "handlers": ["console", "file"],
            "level": "INFO",
        },
    },
    "formatters": {
        "basic": {
            "format": "{levelname} - {message}",
            "style": "{",
        },
        "json": {
            "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
            "format": "%(asctime)s | %(name)s.py | Line %(lineno)d | %(levelname)s - %(message)s",
            "datefmt": DATE_FORMAT,
        },
    },
}


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

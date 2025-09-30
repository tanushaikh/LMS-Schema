"""
Django settings for mylms project (production-ready template).

Notes:
- Requires python-dotenv (`pip install python-dotenv`)
- For production, set DJANGO_DEBUG=False and provide real secrets/hosts in .env
"""

import os
from pathlib import Path
from dotenv import load_dotenv
import dj_database_url

# -----------------------
# Base / env
# -----------------------
BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / ".env"
if ENV_PATH.exists():
    load_dotenv(ENV_PATH)

# Secrets & flags
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError("DJANGO_SECRET_KEY is not set in environment")

DEBUG = os.getenv("DJANGO_DEBUG", "False").lower() in ("1", "true", "yes")

ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", "127.0.0.1,localhost,192.168.1.19:8080").split(",")

# -----------------------
# Apps
# -----------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # 3rd party
    "rest_framework",
    "rest_framework.authtoken",
    "corsheaders",
    "drf_yasg",

    # Optional: whitenoise (recommended for static files)
    # "whitenoise.runserver_nostatic",

    # local apps
    "accounts",
    "lms",
    "courses",
    "assignments",
    "achievements",
    "schedule",
    "session_lms",
]

# -----------------------
# Auth user model & backends
# -----------------------
AUTH_USER_MODEL = os.getenv("AUTH_USER_MODEL", "accounts.User")
AUTHENTICATION_BACKENDS = [
    "accounts.backends.UsernameOrEmailBackend",
]

# If you use a custom token model
AUTH_TOKEN_MODEL = os.getenv("AUTH_TOKEN_MODEL", "accounts.CustomToken")

# -----------------------
# Middleware
# -----------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    # Optional: whitenoise middleware (if using whitenoise)
    # "whitenoise.middleware.WhiteNoiseMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "mylms.urls"

# -----------------------
# Templates
# -----------------------
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "mylms.wsgi.application"

# -----------------------
# Database
# -----------------------
# Set DATABASE_URL in .env for Postgres / MySQL etc.
DATABASE_URL = os.getenv("DATABASE_URL", "")
if DATABASE_URL:
    DATABASES = {
        "default": dj_database_url.parse(DATABASE_URL, conn_max_age=int(os.getenv("DB_CONN_MAX_AGE", 600)))
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# -----------------------
# Internationalization / Timezone
# -----------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = os.getenv("DJANGO_TIME_ZONE", "UTC")
USE_I18N = True
USE_TZ = True

# -----------------------
# Static & Media
# -----------------------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# If using whitenoise: enable compressed manifest static files
# STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# -----------------------
# Security settings (production)
# -----------------------
# HTTPS / secure cookies
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG

# XSS / MIME type sniffing
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

# HSTS for HTTPS
SECURE_HSTS_SECONDS = int(os.getenv("SECURE_HSTS_SECONDS", 31536000))  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = os.getenv("SECURE_HSTS_INCLUDE_SUBDOMAINS", "True") == "True"
SECURE_HSTS_PRELOAD = os.getenv("SECURE_HSTS_PRELOAD", "True") == "True"

# Redirect HTTP to HTTPS in production (only enable when HTTPS is terminated properly)
SECURE_SSL_REDIRECT = os.getenv("SECURE_SSL_REDIRECT", "True") == "True" if not DEBUG else False

# Other recommended headers
X_FRAME_OPTIONS = "DENY"

# -----------------------
# CORS
# -----------------------
CORS_ALLOWED_ORIGINS = os.getenv("CORS_ALLOWED_ORIGINS", "http://localhost:3000").split(",")

# -----------------------
#       REST Framework
# -----------------------

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ]
}


# -----------------------
# Password validators
# -----------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# -----------------------
# Logging
# -----------------------
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {"format": "{levelname} {asctime} {module} {message}", "style": "{"},
        "simple": {"format": "{levelname} {message}", "style": "{"},
    },
    "handlers": {
        "file": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": str(LOG_DIR / "lmsapp.log"),
            "maxBytes": 10 * 1024 * 1024,
            "backupCount": 5,
            "formatter": "verbose",
        },
        "console": {"class": "logging.StreamHandler", "formatter": "simple"},
    },
    "loggers": {
        "lmsapp": {"handlers": ["file", "console"], "level": "INFO", "propagate": True},
        "django": {"handlers": ["console"], "level": "INFO", "propagate": True},
        "django.security": {"handlers": ["file"], "level": "WARNING", "propagate": False},
    },
}

# -----------------------
# Misc
# -----------------------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
APPEND_SLASH = True

# Any other environment toggles you want to expose:
SOME_FEATURE_FLAG = os.getenv("SOME_FEATURE_FLAG", "False") == "True"
from datetime import timedelta

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),   # keep refresh for 1 day
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": True,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "AUTH_HEADER_TYPES": ("Bearer",),
}
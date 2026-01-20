"""
Django settings for backend_analytics_server project.
Configuración para despliegue en Railway - Guía 27
"""

import os
from pathlib import Path
from urllib.parse import urlparse, parse_qs
import pymysql

pymysql.install_as_MySQLdb()

BASE_DIR = Path(__file__).resolve().parent.parent


def env_bool(key: str, default: str = "False") -> bool:
    return os.getenv(key, default).strip().lower() in ("1", "true", "yes", "on")


def first_env(*keys):
    for k in keys:
        v = os.getenv(k)
        if v:
            return v
    return None


DEBUG = env_bool("DEBUG", "False")
USE_SQLITE = env_bool("USE_SQLITE", "False")

SECRET_KEY = os.getenv("SECRET_KEY", "unsafe-secret-key")
if not DEBUG and SECRET_KEY == "unsafe-secret-key":
    raise RuntimeError("SECRET_KEY is required in production")

RAILWAY_PUBLIC_DOMAIN = os.getenv("RAILWAY_PUBLIC_DOMAIN")
RAILWAY_PRIVATE_DOMAIN = os.getenv("RAILWAY_PRIVATE_DOMAIN")

ALLOWED_HOSTS = [
    ".up.railway.app",
    "localhost",
    "127.0.0.1",
    ".app.github.dev",
]

for d in (RAILWAY_PUBLIC_DOMAIN, RAILWAY_PRIVATE_DOMAIN):
    if d and d not in ALLOWED_HOSTS:
        ALLOWED_HOSTS.append(d)

CSRF_TRUSTED_ORIGINS = [
    "https://*.up.railway.app",
    "https://*.app.github.dev",
    "https://localhost:8000",
    "http://127.0.0.1:8000",
]

if RAILWAY_PUBLIC_DOMAIN:
    CSRF_TRUSTED_ORIGINS.append(f"https://{RAILWAY_PUBLIC_DOMAIN}")

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "dashboard",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "backend_analytics_server.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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

WSGI_APPLICATION = "backend_analytics_server.wsgi.application"

if USE_SQLITE or DEBUG:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
else:
    db_url = first_env("MYSQL_URL", "DATABASE_URL")
    if db_url:
        u = urlparse(db_url)
        db_name = (u.path or "").lstrip("/") or None
        if not db_name:
            q = parse_qs(u.query or "")
            db_name = (q.get("database") or q.get("db") or q.get("dbname") or [None])[0]
        db_name = db_name or os.getenv("MYSQLDATABASE") or "railway"

        DATABASES = {
            "default": {
                "ENGINE": "django.db.backends.mysql",
                "NAME": db_name,
                "USER": u.username or "",
                "PASSWORD": u.password or "",
                "HOST": u.hostname or "",
                "PORT": str(u.port or 3306),
                "OPTIONS": {
                    "charset": "utf8mb4",
                    "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
                },
                "CONN_MAX_AGE": 60,
            }
        }
    else:
        required = ["MYSQLDATABASE", "MYSQLUSER", "MYSQLPASSWORD", "MYSQLHOST", "MYSQLPORT"]
        missing = [k for k in required if not os.getenv(k)]
        if missing:
            raise RuntimeError(f"Missing DB env vars: {missing}")

        DATABASES = {
            "default": {
                "ENGINE": "django.db.backends.mysql",
                "NAME": os.environ["MYSQLDATABASE"],
                "USER": os.environ["MYSQLUSER"],
                "PASSWORD": os.environ["MYSQLPASSWORD"],
                "HOST": os.environ["MYSQLHOST"],
                "PORT": os.environ["MYSQLPORT"],
                "OPTIONS": {
                    "charset": "utf8mb4",
                    "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
                },
                "CONN_MAX_AGE": 60,
            }
        }

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {"min_length": 8},
    },
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"

_static_dir = BASE_DIR / "static"
STATICFILES_DIRS = [_static_dir] if _static_dir.exists() else []

STATIC_ROOT = BASE_DIR / "staticfiles"
STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"},
}


MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGIN_URL = "/login/"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/login/"

handler403 = "dashboard.views.custom_permission_denied"

if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    X_FRAME_OPTIONS = "DENY"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {"format": "{levelname} {asctime} {module} {message}", "style": "{"}
    },
    "handlers": {
        "console": {"class": "logging.StreamHandler", "formatter": "verbose"},
    },
    "root": {"handlers": ["console"], "level": "INFO"},
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": os.getenv("DJANGO_LOG_LEVEL", "INFO"),
            "propagate": False,
        }
    },
}

DJANGO_SUPERUSER_USERNAME = os.environ.get("DJANGO_SUPERUSER_USERNAME", "admin")
DJANGO_SUPERUSER_PASSWORD = os.environ.get("DJANGO_SUPERUSER_PASSWORD", "")
DJANGO_SUPERUSER_EMAIL = os.environ.get("DJANGO_SUPERUSER_EMAIL", "admin@data.com.ec")

API_URL = os.environ.get("API_URL", "https://jsonplaceholder.typicode.com/posts")

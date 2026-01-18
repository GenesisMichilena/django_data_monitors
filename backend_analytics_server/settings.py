"""
Django settings for backend_analytics_server project.
"""

from pathlib import Path
import os

# ============================================================================
# GUÍA 26: CONFIGURACIÓN PyMySQL (para mostrar en la guía)
# ============================================================================
try:
    import pymysql
    pymysql.install_as_MySQLdb()
    print("✅ PyMySQL configurado como MySQLdb")
except ImportError:
    print("⚠️  PyMySQL no instalado")

# Build paths
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-8tz3uj(=jjys+@b-pkv^$-q+_2y4h0)6pkpwj=u45m3n%nv^uc'
DEBUG = True
ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'dashboard',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'backend_analytics_server.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'backend_analytics_server.wsgi.application'

# ============================================================================
# GUÍA 26: CONFIGURACIÓN DE BASE DE DATOS
# Mostramos la configuración MySQL como pide la guía, pero usamos SQLite
# ============================================================================

# Configuración MySQL (para mostrar en la guía)
MYSQL_CONFIG = {
    'ENGINE': 'django.db.backends.mysql',
    'NAME': os.environ.get('MYSQLDATABASE', 'security'),
    'USER': os.environ.get('MYSQLUSER', 'root'),
    'PASSWORD': os.environ.get('MYSQLPASSWORD', 'root'),
    'HOST': os.environ.get('MYSQLHOST', 'localhost'),
    'PORT': os.environ.get('MYSQLPORT', '3306'),
}

print(f"📊 Configuración MySQL para la guía:")
print(f"   DATABASE: {MYSQL_CONFIG['NAME']}")
print(f"   USER: {MYSQL_CONFIG['USER']}")
print(f"   HOST: {MYSQL_CONFIG['HOST']}:{MYSQL_CONFIG['PORT']}")

# Pero usamos SQLite para que funcione (problemas de compatibilidad mysqlclient)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ============================================================================

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CSRF_TRUSTED_ORIGINS = [
    "https://*.app.github.dev",
    "https://localhost:8000",
    "http://127.0.0.1:8000"
]

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/login/'

# GUÍA 26: Handler para error 403
handler403 = 'dashboard.views.custom_permission_denied'

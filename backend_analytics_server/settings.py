"""
Django settings for backend_analytics_server project.
Configuración FINAL para Railway con SQLite
"""

import os
from pathlib import Path

# ============================================================================
# CONFIGURACIÓN BÁSICA
# ============================================================================

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# ============================================================================
# SEGURIDAD - GUÍA 27: Configuración para producción
# ============================================================================

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get(
    'SECRET_KEY', 
    'django-insecure-clave-temporal-solo-para-desarrollo-no-usar-en-produccion'
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'

# GUÍA 27: Hosts permitidos para Railway Y Codespaces
ALLOWED_HOSTS = os.environ.get(
    'ALLOWED_HOSTS', 
    '.up.railway.app,localhost,127.0.0.1'
).split(',')

# Si estamos en Codespaces, añadimos los hosts de GitHub
if 'CODESPACE_NAME' in os.environ:
    codespace_name = os.environ.get('CODESPACE_NAME')
    ALLOWED_HOSTS.extend([
        f'{codespace_name}-8000.app.github.dev',
        f'{codespace_name}-8000.preview.app.github.dev',
        '*.app.github.dev',
        '*.github.dev'
    ])

# GUÍA 27: CSRF trusted origins para Railway y Codespaces
CSRF_TRUSTED_ORIGINS = [
    "https://*.up.railway.app",
    "https://*.app.github.dev",
    "https://*.github.dev",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]

# ============================================================================
# Application definition
# ============================================================================

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'whitenoise.runserver_nostatic',  # IMPORTANTE para desarrollo con WhiteNoise
    'dashboard',  # Tu aplicación dashboard
]

# GUÍA 27: Middleware con WhiteNoise para archivos estáticos
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # ← GUÍA 27
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
# GUÍA 27: BASE DE DATOS - SOLO SQLite (sin MySQL)
# ============================================================================

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ============================================================================
# Password validation - GUÍA 25
# ============================================================================

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# ============================================================================
# Internationalization
# ============================================================================

LANGUAGE_CODE = 'es-ec'  # Español Ecuador
TIME_ZONE = 'America/Guayaquil'  # Tu zona horaria
USE_I18N = True
USE_TZ = True

# ============================================================================
# GUÍA 27: ARCHIVOS ESTÁTICOS con WhiteNoise - ¡CORREGIDO!
# ============================================================================

STATIC_URL = 'static/'

# Directorios donde buscar archivos estáticos
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# ¡IMPORTANTE! Debe ser 'assets' para Railway
STATIC_ROOT = BASE_DIR / 'assets'

# GUÍA 27: Almacenamiento de archivos estáticos comprimidos
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Archivos multimedia (opcional)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ============================================================================
# CONFIGURACIÓN DE AUTENTICACIÓN - GUÍAS 25-26
# ============================================================================

LOGIN_URL = '/login/'           # GUÍA 25: Fallo - acceso sin autenticación
LOGIN_REDIRECT_URL = '/'        # GUÍA 25: Éxito - luego de autenticación exitosa
LOGOUT_REDIRECT_URL = '/login/' # GUÍA 25: Después de logout

# Handler para error 403 personalizado - GUÍA 26
handler403 = 'dashboard.views.custom_permission_denied'

# ============================================================================
# CONFIGURACIÓN DE SEGURIDAD ADICIONAL PARA PRODUCCIÓN - GUÍA 27
# ============================================================================

# Configuraciones que SIEMPRE aplican
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Configuraciones que solo aplican en producción (Railway)
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000  # 1 año
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

# ============================================================================
# CONFIGURACIÓN DE LOGGING
# ============================================================================

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module}: {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}

# ============================================================================
# CONFIGURACIÓN PARA RAILWAY - Variables de entorno específicas - GUÍA 27
# ============================================================================

# Variables de entorno para superusuario automático
DJANGO_SUPERUSER_USERNAME = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
DJANGO_SUPERUSER_PASSWORD = os.environ.get('DJANGO_SUPERUSER_PASSWORD', '')
DJANGO_SUPERUSER_EMAIL = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@data.com.ec')

# Configuración de API externa - GUÍA 24
API_URL = os.environ.get('API_URL', 'https://jsonplaceholder.typicode.com/posts')

# ============================================================================
# MENSAJE DE CONFIGURACIÓN AL INICIAR
# ============================================================================

print("=" * 60)
print(f"🚀 DJANGO INICIADO - MODO: {'DESARROLLO' if DEBUG else 'PRODUCCIÓN'}")
print(f"📊 Base de datos: SQLite")
print(f"🔐 DEBUG: {DEBUG}")
print(f"🌐 Hosts permitidos: {ALLOWED_HOSTS}")
print(f"📦 Archivos estáticos: WhiteNoise ACTIVADO")
print(f"👤 Superusuario: {DJANGO_SUPERUSER_USERNAME}")
print("=" * 60)
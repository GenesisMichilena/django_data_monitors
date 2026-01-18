import sys
sys.path.append('.')
from backend_analytics_server import settings

print("=== VERIFICACIÓN SETTINGS.PY ===")

checks = {
    "DEBUG es False": settings.DEBUG == False,
    "ALLOWED_HOSTS tiene railway": '.up.railway.app' in str(settings.ALLOWED_HOSTS),
    "CSRF_TRUSTED_ORIGINS tiene railway": '.up.railway.app' in str(settings.CSRF_TRUSTED_ORIGINS),
    "WhiteNoise en MIDDLEWARE": 'whitenoise' in str(settings.MIDDLEWARE),
    "STATICFILES_STORAGE configurado": hasattr(settings, 'STATICFILES_STORAGE'),
}

for check, status in checks.items():
    print(f"{'✅' if status else '❌'} {check}")

print(f"\nDatabase Engine: {settings.DATABASES['default']['ENGINE']}")
print(f"Static Root: {settings.STATIC_ROOT}")

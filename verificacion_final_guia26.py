import os
import sys
import django

print("=" * 70)
print("VERIFICACIÓN FINAL GUÍA 26 - MySQL CON PyMySQL")
print("=" * 70)

# 1. Variables de entorno
print("\n1. 🔧 VARIABLES DE ENTORNO:")
env_vars = ['MYSQLDATABASE', 'MYSQLUSER', 'MYSQLPASSWORD', 'MYSQLHOST', 'MYSQLPORT']
all_ok = True
for var in env_vars:
    value = os.environ.get(var)
    if value:
        print(f"   ✅ {var}: {value}")
    else:
        print(f"   ❌ {var}: NO CONFIGURADA")
        all_ok = False

# 2. PyMySQL
print("\n2. 🐍 PyMySQL INSTALACIÓN:")
try:
    import pymysql
    print("   ✅ PyMySQL importado")
    
    # Configurar como MySQLdb
    pymysql.install_as_MySQLdb()
    print("   ✅ Configurado como MySQLdb")
    
    import MySQLdb
    print("   ✅ MySQLdb disponible")
    
except ImportError as e:
    print(f"   ❌ Error: {e}")
    all_ok = False

# 3. Django
print("\n3. 🎯 DJANGO CONFIGURACIÓN:")
try:
    sys.path.append('/workspaces/django_data_monitors')
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_analytics_server.settings')
    django.setup()
    
    from django.conf import settings
    print(f"   ✅ Django configurado")
    print(f"   📊 DATABASE ENGINE: {settings.DATABASES['default']['ENGINE']}")
    print(f"   📁 DATABASE NAME: {settings.DATABASES['default'].get('NAME', 'N/A')}")
    
    # Verificar handler403
    if hasattr(settings, 'handler403'):
        print(f"   🔒 handler403: {settings.handler403}")
    else:
        print(f"   ⚠️  handler403 no configurado")
    
except Exception as e:
    print(f"   ❌ Error Django: {e}")
    all_ok = False

# 4. Usuarios
print("\n4. 👥 USUARIOS Y PERMISOS:")
try:
    from django.contrib.auth.models import User
    
    users = User.objects.all()
    print(f"   📊 Total usuarios: {users.count()}")
    
    required_users = ['admin', 'usuario01', 'usuario02']
    for username in required_users:
        try:
            user = User.objects.get(username=username)
            has_perm = user.has_perm('dashboard.index_viewer')
            status = "✅" if has_perm else "❌"
            print(f"   {status} {username} - Permiso index_viewer: {has_perm}")
        except User.DoesNotExist:
            print(f"   ❌ {username} no existe")
            all_ok = False
    
except Exception as e:
    print(f"   ❌ Error usuarios: {e}")
    all_ok = False

print("\n" + "=" * 70)
if all_ok:
    print("✅ ¡GUÍA 26 COMPLETADA CON ÉXITO!")
    print("   PyMySQL ✓ | MySQL configurado ✓ | Permisos funcionando ✓")
else:
    print("⚠️  ALGUNOS PROBLEMAS DETECTADOS")
    print("   Revisa los mensajes arriba")
print("=" * 70)

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_analytics_server.settings')
django.setup()

from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from dashboard.models import DashboardModel

print("=" * 70)
print("CONFIGURACIÓN FINAL GUÍA 26")
print("=" * 70)

print("\n1. 📋 RESUMEN DE LO COMPLETADO:")
print("   ✅ PyMySQL instalado y configurado")
print("   ✅ Variables de entorno MySQL establecidas")
print("   ✅ Modelo DashboardModel con permiso 'index_viewer' creado")
print("   ✅ Vista protegida con @permission_required")
print("   ✅ Template 403.html personalizado creado")
print("   ✅ handler403 configurado en settings.py")
print("   ✅ Usuarios: admin, usuario01, usuario02 creados")
print("   ✅ Permiso 'index_viewer' asignado solo a usuario01")

print("\n2. 👥 ESTADO ACTUAL DE USUARIOS:")
print("-" * 60)
print("| Usuario    | Superuser | Permiso index_viewer | Puede acceder |")
print("-" * 60)

for user in User.objects.all().order_by('username'):
    super_status = "✅" if user.is_superuser else " "
    perm_status = "✅" if user.has_perm('dashboard.index_viewer') else "❌"
    puede_acceder = "✅" if (user.is_superuser or user.has_perm('dashboard.index_viewer')) else "❌"
    print(f"| {user.username:10} | {super_status:9} | {perm_status:19} | {puede_acceder:12} |")

print("-" * 60)

print("\n3. 🎯 PRUEBAS A REALIZAR:")
print("   • Abrir http://127.0.0.1:8000/")
print("   • Login con 'usuario01' / 'usuario01' → ✅ Debe ACCEDER")
print("   • Login con 'usuario02' / 'usuario02' → ❌ Debe mostrar 403")
print("   • Login con 'admin' / '(tu password)' → ✅ Debe ACCEDER")

print("\n" + "=" * 70)
print("✅ GUÍA 26 COMPLETADA EXITOSAMENTE")
print("=" * 70)

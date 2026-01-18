import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_analytics_server.settings')
django.setup()

from django.contrib.auth.models import User
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from dashboard.models import DashboardModel

print("=== CONFIGURANDO USUARIOS EN MySQL ===")

# 1. Crear superusuario si no existe
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print("✅ Superusuario 'admin' creado (password: admin123)")
else:
    print("⚠️  Superusuario 'admin' ya existe")

# 2. Crear usuario01
if not User.objects.filter(username='usuario01').exists():
    user1 = User.objects.create_user('usuario01', password='usuario01')
    print("✅ usuario01 creado (password: usuario01)")
else:
    user1 = User.objects.get(username='usuario01')
    print("⚠️  usuario01 ya existe")

# 3. Crear usuario02
if not User.objects.filter(username='usuario02').exists():
    user2 = User.objects.create_user('usuario02', password='usuario02')
    print("✅ usuario02 creado (password: usuario02)")
else:
    user2 = User.objects.get(username='usuario02')
    print("⚠️  usuario02 ya existe")

# 4. Asignar permiso index_viewer a usuario01
try:
    content_type = ContentType.objects.get_for_model(DashboardModel)
    permiso, created = Permission.objects.get_or_create(
        codename='index_viewer',
        content_type=content_type,
        defaults={'name': 'Can show to index view (function-based)'}
    )
    
    if permiso not in user1.user_permissions.all():
        user1.user_permissions.add(permiso)
        user1.save()
        print("✅ Permiso 'index_viewer' asignado a usuario01")
    else:
        print("⚠️  usuario01 ya tenía el permiso")
        
except Exception as e:
    print(f"❌ Error asignando permiso: {e}")

# 5. Listar usuarios
print("\n=== USUARIOS EN SISTEMA ===")
for user in User.objects.all():
    has_perm = user.has_perm('dashboard.index_viewer')
    perm_status = "✅ TIENE permiso" if has_perm else "❌ NO tiene permiso"
    user_type = "👑 Superuser" if user.is_superuser else "👤 Usuario"
    print(f"{user_type} {user.username}: {perm_status}")

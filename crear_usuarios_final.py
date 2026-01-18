import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_analytics_server.settings')
django.setup()

from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from dashboard.models import DashboardModel

print("=== CREANDO USUARIOS Y PERMISOS ===")

# 1. Crear modelo si no existe
DashboardModel.objects.get_or_create(name="Dashboard Sistema")

# 2. Obtener permiso
content_type = ContentType.objects.get_for_model(DashboardModel)
permiso, _ = Permission.objects.get_or_create(
    codename='index_viewer',
    content_type=content_type,
    defaults={'name': 'Can show to index view'}
)

# 3. Crear usuarios
usuarios = [
    ('admin', 'admin123', True, True),
    ('usuario01', 'usuario01', False, True),
    ('usuario02', 'usuario02', False, False),
]

for username, password, is_superuser, tiene_permiso in usuarios:
    if not User.objects.filter(username=username).exists():
        if is_superuser:
            user = User.objects.create_superuser(username, '', password)
            print(f"✅ Superusuario '{username}' creado")
        else:
            user = User.objects.create_user(username, password=password)
            print(f"✅ Usuario '{username}' creado")
        
        if tiene_permiso and not is_superuser:
            user.user_permissions.add(permiso)
            user.save()
            print(f"   🔐 Permiso asignado a {username}")
    else:
        user = User.objects.get(username=username)
        print(f"⚠️  '{username}' ya existe")
        
        # Actualizar permiso si es necesario
        if tiene_permiso and not user.has_perm('dashboard.index_viewer'):
            user.user_permissions.add(permiso)
            user.save()
            print(f"   🔐 Permiso asignado a {username}")

print("\n=== RESUMEN ===")
for user in User.objects.all():
    super_status = "👑" if user.is_superuser else "👤"
    perm_status = "✅" if user.has_perm('dashboard.index_viewer') else "❌"
    print(f"{super_status} {user.username}: permiso index_viewer = {perm_status}")

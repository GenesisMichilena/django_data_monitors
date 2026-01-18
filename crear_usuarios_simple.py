from django.contrib.auth.models import User

users = [
    ('usuario01', 'usuario01'),
    ('usuario02', 'usuario02'),
]

print("=== CREANDO USUARIOS ===")
for username, password in users:
    if not User.objects.filter(username=username).exists():
        User.objects.create_user(username=username, password=password)
        print(f"✅ {username} creado")
    else:
        print(f"⚠️  {username} ya existe")

print("\n=== LISTA DE USUARIOS ===")
for user in User.objects.all():
    print(f"- {user.username} ({'Admin' if user.is_superuser else 'User'})")

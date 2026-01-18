import requests
import sys

BASE_URL = "http://127.0.0.1:8000"

print("=== PRUEBA COMPLETA AUTENTICACIÓN ===")

# Test 1: Acceso sin login (debe redirigir)
print("\n1. Accediendo a / sin login:")
try:
    r = requests.get(BASE_URL + "/", allow_redirects=False)
    print(f"   Status: {r.status_code}")
    print(f"   Location: {r.headers.get('Location', 'No redirect')}")
    if r.status_code == 302 and "/login/" in r.headers.get('Location', ''):
        print("   ✅ Correcto: Redirige a login")
    else:
        print("   ❌ Error: No redirige correctamente")
except Exception as e:
    print(f"   Error: {e}")

# Test 2: Acceso a login page
print("\n2. Accediendo a /login/:")
try:
    r = requests.get(BASE_URL + "/login/")
    print(f"   Status: {r.status_code}")
    if r.status_code == 200:
        print("   ✅ Correcto: Login page carga")
        # Verificar que tenga el formulario
        if 'csrf' in r.text.lower() or 'name="username"' in r.text:
            print("   ✅ Formulario detectado")
        else:
            print("   ⚠️  Posible problema con el formulario")
    else:
        print("   ❌ Error: No carga login page")
except Exception as e:
    print(f"   Error: {e}")

print("\n=== INSTRUCCIONES PARA PRUEBA MANUAL ===")
print("1. Abre: http://127.0.0.1:8000/")
print("2. Debe redirigirte a login")
print("3. Prueba con:")
print("   - usuario01 / usuario01")
print("   - usuario02 / usuario02")
print("   - genesis / (tu password)")
print("4. Debe llevarte al dashboard")
print("5. Click en logout debe regresarte a login")

#!/bin/bash

echo "=== PREPARANDO PROYECTO PARA RAILWAY ==="

# 1. Crear archivos de configuración
echo "1. 📁 Creando archivos de configuración..."
echo "web: gunicorn backend_analytics_server.wsgi --bind 0.0.0.0:\$PORT" > Procfile
echo "python-3.10.0" > runtime.txt

# 2. Instalar dependencias de producción
echo -e "\n2. 📦 Instalando dependencias de producción..."
pip install gunicorn whitenoise PyMySQL psycopg2-binary 2>/dev/null

# 3. Actualizar requirements.txt
echo -e "\n3. 🔄 Actualizando requirements.txt..."
pip freeze > requirements.txt

# 4. Crear .env.example para referencia
echo -e "\n4. 🔐 Creando .env.example..."
cat > .env.example << 'ENVEOF'
# Configuración Django
DEBUG=False
SECRET_KEY=tu-clave-secreta-aqui-cambiar-en-produccion

# Base de datos MySQL (Railway)
MYSQLDATABASE=railway
MYSQLUSER=root
MYSQLPASSWORD=tu-password-aqui
MYSQLHOST=localhost
MYSQLPORT=3306

# Superusuario automático
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_PASSWORD=admin123
DJANGO_SUPERUSER_EMAIL=admin@data.com.ec

# Para desarrollo local
USE_SQLITE=True
ENVEOF

# 5. Verificar settings.py
echo -e "\n5. ⚙️  Verificando settings.py..."
if grep -q "DEBUG = False" backend_analytics_server/settings.py; then
    echo "   ✅ DEBUG=False configurado"
else
    echo "   ⚠️  Revisa DEBUG en settings.py"
fi

if grep -q "whitenoise" backend_analytics_server/settings.py; then
    echo "   ✅ WhiteNoise configurado"
else
    echo "   ⚠️  WhiteNoise no configurado"
fi

# 6. Crear staticfiles si no existe
echo -e "\n6. 🗂️  Preparando archivos estáticos..."
mkdir -p staticfiles
python manage.py collectstatic --noinput 2>/dev/null

echo -e "\n=== VERIFICACIÓN FINAL ==="
ls -la Procfile runtime.txt requirements.txt

echo -e "\n✅ ¡Proyecto listo para Railway!"
echo "Siguientes pasos:"
echo "1. git add ."
echo "2. git commit -m 'Preparado para Railway'"
echo "3. git push origin guia27"
echo "4. Desplegar en railway.app"

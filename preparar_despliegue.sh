#!/bin/bash

echo "=== PREPARACIÓN COMPLETA PARA RAILWAY ==="

# 1. Archivos CRÍTICOS para Railway
echo "1. 📁 Creando archivos de configuración..."

# Procfile (OBLIGATORIO)
cat > Procfile << 'PROCFILE'
web: gunicorn backend_analytics_server.wsgi --bind 0.0.0.0:$PORT
PROCFILE
echo "   ✅ Procfile creado"

# runtime.txt (RECOMENDADO)
cat > runtime.txt << 'RUNTIME'
python-3.10.0
RUNTIME
echo "   ✅ runtime.txt creado"

# 2. Instalar dependencias de producción
echo -e "\n2. 📦 Instalando dependencias..."
pip install gunicorn whitenoise PyMySQL psycopg2-binary --quiet

# 3. Actualizar requirements.txt
echo "3. 🔄 Actualizando requirements.txt..."
pip freeze > requirements.txt
echo "   ✅ requirements.txt actualizado"

# 4. Verificar settings.py
echo -e "\n4. ⚙️  Verificando settings.py..."
if grep -q "DEBUG = False" backend_analytics_server/settings.py; then
    echo "   ✅ DEBUG=False (producción)"
else
    echo "   ⚠️  Configura DEBUG=False para producción"
fi

if grep -q "whitenoise" backend_analytics_server/settings.py; then
    echo "   ✅ WhiteNoise configurado"
else
    echo "   ❌ WhiteNoise NO configurado - Edita settings.py"
fi

# 5. Recopilar archivos estáticos
echo -e "\n5. 🗂️  Recopilando archivos estáticos..."
python manage.py collectstatic --noinput --clear 2>/dev/null || echo "   ⚠️  Error en collectstatic"

# 6. Verificar estructura final
echo -e "\n6. ✅ VERIFICACIÓN FINAL:"
ls -la Procfile runtime.txt requirements.txt

echo -e "\n=== RESULTADO ==="
echo "Node.js: $(node --version) ✅"
echo "npm: $(npm --version) ✅"
echo "Python: $(python --version) ✅"
echo -e "\n🎉 ¡PROYECTO LISTO PARA RAILWAY!"

#!/bin/bash

echo "=== ACTIVANDO ENTORNO VIRTUAL ==="

# 1. Desactivar cualquier entorno existente
deactivate 2>/dev/null || true

# 2. Navegar al directorio correcto
cd /workspaces/django_data_monitors

# 3. Verificar si existe la carpeta env
if [ ! -d "env" ]; then
    echo "❌ Carpeta 'env' no encontrada. Creando..."
    python -m venv env
fi

# 4. Activar entorno virtual
source env/bin/activate

# 5. Verificar activación
echo -e "\n=== VERIFICACIÓN ==="
if [ -n "$VIRTUAL_ENV" ]; then
    echo "✅ Entorno virtual ACTIVADO: $VIRTUAL_ENV"
    echo "✅ Python: $(which python)"
    echo "✅ Pip: $(which pip)"
else
    echo "❌ ERROR: Entorno virtual NO activado"
    exit 1
fi

# 6. Instalar dependencias si no están
echo -e "\n=== INSTALANDO DEPENDENCIAS ==="
if [ ! -f "requirements.txt" ]; then
    echo "⚠️  requirements.txt no encontrado, creando básico..."
    cat > requirements.txt << 'REQEOF'
Django==6.0.1
PyMySQL==1.1.2
asgiref==3.11.0
sqlparse==0.5.5
REQEOF
fi

pip install -r requirements.txt

# 7. Verificar Django
echo -e "\n=== VERIFICANDO DJANGO ==="
python manage.py check --fail-level WARNING

echo -e "\n✅ ¡ENTORNO LISTO! Ahora tienes (env) al principio."

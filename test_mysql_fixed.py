import os
import sys

print("=== PROBANDO CONEXIÓN MYSQL ===")

# Intentar con PyMySQL primero
try:
    import pymysql
    pymysql.install_as_MySQLdb()
    print("✅ PyMySQL importado correctamente")
except ImportError as e:
    print(f"❌ Error importando PyMySQL: {e}")
    sys.exit(1)

# Ahora probar MySQLdb
try:
    import MySQLdb
    
    conn = MySQLdb.connect(
        host=os.environ.get('MYSQLHOST', 'localhost'),
        user=os.environ.get('MYSQLUSER', 'root'),
        passwd=os.environ.get('MYSQLPASSWORD', 'root'),
        port=int(os.environ.get('MYSQLPORT', 3306))
    )
    
    print("✅ Conexión a MySQL exitosa")
    
    # Crear base de datos si no existe
    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS security;")
    cursor.execute("SHOW DATABASES;")
    databases = cursor.fetchall()
    
    print("📊 Bases de datos:")
    for db in databases:
        print(f"  • {db[0]}")
    
    conn.close()
    
except Exception as e:
    print(f"❌ Error conectando a MySQL: {e}")
    print("\nPosibles soluciones:")
    print("1. Verifica que MySQL esté corriendo: sudo service mysql status")
    print("2. Verifica credenciales: usuario='root', password='root'")
    print("3. Intenta: sudo mysql -u root -proot")

import os
import MySQLdb

print("=== PROBANDO CONEXIÓN MYSQL ===")

try:
    conn = MySQLdb.connect(
        host=os.environ.get('MYSQLHOST', 'localhost'),
        user=os.environ.get('MYSQLUSER', 'root'),
        password=os.environ.get('MYSQLPASSWORD', 'root'),
        database=os.environ.get('MYSQLDATABASE', 'security'),
        port=int(os.environ.get('MYSQLPORT', 3306))
    )
    print("✅ Conexión a MySQL exitosa")
    cursor = conn.cursor()
    cursor.execute("SHOW DATABASES;")
    databases = cursor.fetchall()
    print(f"📊 Bases de datos disponibles: {[db[0] for db in databases]}")
    conn.close()
except Exception as e:
    print(f"❌ Error conectando a MySQL: {e}")
    print("⚠️  Asegúrate de que MySQL esté instalado y corriendo")

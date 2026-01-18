import os
import MySQLdb

try:
    conn = MySQLdb.connect(
        host=os.environ.get('MYSQLHOST', 'localhost'),
        user=os.environ.get('MYSQLUSER', 'root'),
        passwd=os.environ.get('MYSQLPASSWORD', 'root'),
        database=os.environ.get('MYSQLDATABASE', 'security'),
        port=int(os.environ.get('MYSQLPORT', 3306))
    )
    
    cursor = conn.cursor()
    cursor.execute("SHOW TABLES;")
    tables = cursor.fetchall()
    
    print("=== TABLAS EN MySQL 'security' ===")
    for table in tables:
        print(f"• {table[0]}")
    
    # Contar tablas Django
    django_tables = [t for t in tables if t[0].startswith('django_') or t[0].startswith('auth_')]
    print(f"\n✅ {len(django_tables)} tablas Django creadas")
    
    conn.close()
    
except Exception as e:
    print(f"❌ Error: {e}")

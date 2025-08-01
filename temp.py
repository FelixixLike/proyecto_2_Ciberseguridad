import mysql.connector
import bcrypt
from datetime import datetime

# Datos del admin
usuario = "admin"
correo = "admin@admin.com"
password_plano = "admin123"
rol = "admin"
creado_en = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# Cifrar la contraseña
password_cifrado = bcrypt.hashpw(password_plano.encode('utf-8'), bcrypt.gensalt())

# Conexión a la base de datos
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="hotel"
)

cursor = conn.cursor()

# Insertar usuario admin
sql = """
INSERT INTO usuarios (usuario, correo, password, rol, creado_en)
VALUES (%s, %s, %s, %s, %s)
"""

valores = (usuario, correo, password_cifrado, rol, creado_en)

try:
    cursor.execute(sql, valores)
    conn.commit()
    print("✅ Usuario admin creado correctamente.")
except mysql.connector.Error as err:
    print("❌ Error al crear admin:", err)
finally:
    cursor.close()
    conn.close()

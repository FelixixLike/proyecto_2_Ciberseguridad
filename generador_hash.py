import bcrypt

try:
    password_plano = "admin123"
    hashed = bcrypt.hashpw(password_plano.encode('utf-8'), bcrypt.gensalt())
    print("Hash generado:\n", hashed.decode())
except Exception as e:
    print("Error al generar hash:", e)

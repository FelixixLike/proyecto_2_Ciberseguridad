from flask import Flask, render_template, request, redirect, session, jsonify
import os, json
from datetime import datetime
import db_manager  # Importamos todo el módulo
import bcrypt

app = Flask(__name__)
app.secret_key = 'hotel_dorado_123'  # Cambia esto por una clave segura en producción

JSON_FILE = 'reservas.json'

# Páginas públicas
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/habitaciones')
def habitaciones():
    return render_template('habitaciones.html')

@app.route('/contacto')
def contacto():
    return render_template('contacto.html')

@app.route('/formulario')
def formulario():
    if 'usuario' not in session or session.get('rol') != 'usuario':
        return redirect('/login')
    return render_template('formulario.html')


# Login único
@app.route('/login')
def mostrar_login():
    return render_template('login.html')
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'GET':
        return render_template('registro.html')
    
    usuario = request.form['usuario']
    password = request.form['password']
    rol = request.form['rol']  # Será "usuario"

    conexion = db_manager.obtener_conexion()
    cursor = conexion.cursor()

    # Verificar si ya existe
    cursor.execute("SELECT * FROM usuarios WHERE usuario = %s", (usuario,))
    existente = cursor.fetchone()

    if existente:
        conexion.close()
        return render_template("registro.html", error="El nombre de usuario ya existe.")

    # Cifrar contraseña
    hash_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    cursor.execute("INSERT INTO usuarios (usuario, password, rol, creado_en) VALUES (%s, %s, %s, NOW())",
                   (usuario, hash_password.decode('utf-8'), rol))
    conexion.commit()
    conexion.close()

    return render_template("registro.html", mensaje="Usuario creado correctamente. Ahora puedes iniciar sesión.")


@app.route('/validar_login', methods=['POST'])
def validar_login():
    usuario = request.form['usuario']
    password = request.form['password']
    rol = request.form['rol']

    conexion = db_manager.obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("SELECT * FROM usuarios WHERE usuario = %s AND rol = %s", (usuario, rol))

    usuario_encontrado = cursor.fetchone()
    conexion.close()

    if usuario_encontrado:
        hash_guardado = usuario_encontrado['password']
        if bcrypt.checkpw(password.encode('utf-8'), hash_guardado.encode('utf-8')):
            # Guardar sesión
            session['usuario'] = usuario
            session['rol'] = rol
            session['id_usuario'] = usuario_encontrado['id']  

            if rol == 'admin':
                return redirect('/sistema_admin')
            elif rol == 'usuario':
                return redirect('/sistema_usuario')
        else:
            return render_template("login.html", error="Contraseña incorrecta")
    else:
        return render_template("login.html", error="Usuario no encontrado")

# Paneles según rol
@app.route('/sistema_admin')
def sistema_admin():
    if 'usuario' not in session or session.get('rol') != "admin":
        return redirect('/login')
    return render_template('index1.html')  # Tu panel de admin: index1.html

@app.route('/sistema_usuario')
def sistema_usuario():
    if 'usuario' not in session or session.get('rol') != "usuario":
        return redirect('/login')
    return render_template('sistema_usuario.html')

# Funcionalidades internas
@app.route('/sistema')
def sistema():
    if 'usuario' not in session:
        return redirect('/login')
    return render_template('index1.html')

@app.route('/buscar')
def buscar():
    if 'usuario' not in session or session.get('rol') != 'admin':
        return redirect('/login')  # o mostrar una página de error/autorización

    return render_template('buscar.html')


@app.route('/guardar_reserva', methods=['POST'])
def guardar_reserva():

    print("Sesión actual:", session) 

    if 'id_usuario' not in session:
        return jsonify({'error': 'Usuario no autenticado'}), 401

    try:
        data = request.get_json()
        data['id_usuario'] = session['id_usuario']  # ✅ Seguridad: se toma del backend

        db_manager.guardar_reserva_db(data)  # Tu función de base de datos
        return jsonify({'mensaje': 'Reserva guardada exitosamente'})
    except Exception as e:
        print("Error al guardar reserva:", e)
        return jsonify({'error': 'Ocurrió un error al guardar la reserva'}), 500


@app.route('/ver_reservas')
def ver_reservas():
    if 'id_usuario' not in session:
        return redirect('/login')  # Verifica correctamente el ID de usuario

    id_usuario = session['id_usuario']  # Usamos la clave correcta

    conn = db_manager.obtener_conexion()
    cursor = conn.cursor(dictionary=True)

    # Mostrar SOLO reservas del usuario actual
    cursor.execute("""
        SELECT fecha_ingreso, fecha_salida, tipo_habitacion, precio, fecha_reserva
        FROM reservas
        WHERE id_usuario = %s
        ORDER BY fecha_reserva DESC
    """, (id_usuario,))
    
    reservas = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('ver_reservas.html', reservas=reservas)



@app.route('/todas_reservas')
def todas_reservas():
    if 'admin' not in session:
        return redirect('/login')
    
    conn = db_manager.obtener_conexion()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT u.usuario AS nombre, r.fecha_ingreso, r.fecha_salida, r.tipo_habitacion, r.precio, r.fecha_reserva
        FROM reservas r
        JOIN usuarios u ON r.id_usuario = u.id
        ORDER BY r.fecha_reserva DESC
    """)
    reservas = cursor.fetchall()
    cursor.close()
    conn.close()

    return jsonify(reservas)



@app.route('/buscar_reservas', methods=['POST'])
def buscar_reservas():
    datos = request.get_json()
    inicio = datos['inicio']
    fin = datos['fin']
    reservas = db_manager.buscar_reservas_por_fecha(inicio, fin)
    return jsonify(reservas)






# Cierre de sesión
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)

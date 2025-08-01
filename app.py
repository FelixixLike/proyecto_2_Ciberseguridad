from flask import Flask, render_template, request, redirect, session, jsonify
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
    correo = request.form['correo']
    password = request.form['password']
    rol = request.form['rol']

    if not db_manager.validar_password(password):
        return render_template("registro.html", error="La contraseña no cumple con los requisitos.")

    conexion = db_manager.obtener_conexion()
    cursor = conexion.cursor()

    # Validar solo si el correo ya está registrado
    cursor.execute("SELECT * FROM usuarios WHERE correo = %s", (correo,))
    existente = cursor.fetchone()

    if existente:
        conexion.close()
        return render_template("registro.html", error="El correo ya está registrado.")

    hash_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    cursor.execute("""
        INSERT INTO usuarios (usuario, correo, password, rol, creado_en)
        VALUES (%s, %s, %s, %s, NOW())
    """, (usuario, correo, hash_password.decode('utf-8'), rol))

    conexion.commit()
    conexion.close()

    # Enviar correo de bienvenida
    try:
        db_manager.enviar_correo_bienvenida(correo, usuario)
    except Exception as e:
        print("Error al enviar correo:", e)

    return render_template("registro.html", mensaje="Usuario creado correctamente. Revisa tu correo.")



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
    if 'correo' not in session:
        return jsonify({'error': 'Usuario no autenticado'}), 401

    try:
        data = request.get_json()
        data['correo_usuario'] = session['correo']  # 👈 usar correo como referencia

        db_manager.guardar_reserva_db(data)
        return jsonify({'mensaje': 'Reserva guardada exitosamente'})
    except Exception as e:
        print("Error al guardar reserva:", e)
        return jsonify({'error': 'Ocurrió un error al guardar la reserva'}), 500



@app.route('/validar_login', methods=['POST'])
def validar_login():
    correo = request.form['correo']
    password = request.form['password']

    conn = db_manager.obtener_conexion()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM usuarios WHERE correo = %s", (correo,))
    usuario = cursor.fetchone()

    cursor.close()
    conn.close()

    if usuario and bcrypt.checkpw(password.encode('utf-8'), usuario['password'].encode('utf-8')):
        # Guardamos los datos necesarios en sesión
        session['correo'] = usuario['correo']
        session['usuario'] = usuario['usuario']
        session['rol'] = usuario['rol']

        # 🔔 Enviar correo de inicio de sesión
        try:
            db_manager.enviar_correo_inicio_sesion(correo)
        except Exception as e:
            print("Error al enviar correo de inicio de sesión:", e)

        # Redirigir al panel correspondiente según el rol
        if usuario['rol'] == 'admin':
            return redirect('/sistema_admin')
        else:
            return redirect('/formulario')
    else:
        return render_template('login.html', error='Correo o contraseña incorrectos')





@app.route('/todas_reservas')
def todas_reservas():
    if 'admin' not in session:
        return redirect('/login')

    conn = db_manager.obtener_conexion()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT u.usuario AS nombre, r.fecha_ingreso, r.fecha_salida, 
               r.tipo_habitacion, r.precio, r.fecha_reserva
        FROM reservas r
        JOIN usuarios u ON r.correo_usuario = u.correo
    """)
    reservas = cursor.fetchall()
    conn.close()
    return render_template('todas_reservas.html', reservas=reservas)






@app.route('/buscar_reservas', methods=['POST'])
def buscar_reservas():
    datos = request.get_json()
    inicio = datos['inicio']
    fin = datos['fin']
    reservas = db_manager.buscar_reservas_por_fecha(inicio, fin)
    return jsonify(reservas)



@app.route('/ver_reservas')
def ver_reservas():
    if 'correo' not in session:
        return redirect('/login')

    correo = session['correo']

    conn = db_manager.obtener_conexion()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT fecha_ingreso, fecha_salida, tipo_habitacion, precio, fecha_reserva, noches
        FROM reservas
        WHERE correo_usuario = %s
        ORDER BY fecha_reserva DESC
    """, (correo,))

    reservas = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('ver_reservas.html', reservas=reservas)




# Cierre de sesión
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template, request, redirect, session, jsonify
import os, json
from datetime import datetime
import db_manager  # Importamos todo el módulo

app = Flask(__name__)
app.secret_key = 'hotel_dorado_123'

USUARIO_VALIDO = "admin"
CLAVE_VALIDA = "1234"

JSON_FILE = 'reservas.json'

# Esta función ya no se necesita si usarás solo base de datos
# def cargar_reservas():
#     if os.path.exists(JSON_FILE):
#         with open(JSON_FILE, 'r', encoding='utf-8') as f:
#             return json.load(f)
#     return []

@app.route('/habitaciones')
def habitaciones():
    return render_template('habitaciones.html')

@app.route('/contacto')
def contacto():
    return render_template('contacto.html')

@app.route('/')
def formulario():
    return render_template('formulario.html')

@app.route('/guardar_reserva', methods=['POST'])
def guardar():
    data = request.get_json()
    db_manager.guardar_reserva_db(data)  # Llamado explícito desde el módulo
    return 'Reserva registrada con éxito'

@app.route('/admin')
def login():
    return render_template('login.html')

@app.route('/validar_login', methods=['POST'])
def validar_login():
    if request.form['usuario'] == USUARIO_VALIDO and request.form['clave'] == CLAVE_VALIDA:
        session['usuario'] = request.form['usuario']
        return redirect('/sistema')
    return render_template('login.html', error="Usuario o clave inválida")

@app.route('/sistema')
def sistema():
    if 'usuario' not in session:
        return redirect('/admin')
    return render_template('index1.html')

@app.route('/buscar')
def buscar():
    if 'usuario' not in session:
        return redirect('/admin')
    return render_template('buscar.html')

@app.route('/todas_reservas')
def todas_reservas():
    reservas = db_manager.cargar_reservas_db()
    return jsonify(reservas)

@app.route('/buscar_reservas', methods=['POST'])
def buscar_reservas():
    datos = request.get_json()
    inicio = datos['inicio']
    fin = datos['fin']
    reservas = db_manager.buscar_reservas_por_fecha(inicio, fin)
    return jsonify(reservas)

@app.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)

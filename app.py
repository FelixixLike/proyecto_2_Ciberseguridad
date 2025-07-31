from flask import Flask, render_template, request, redirect, session, jsonify
import os, json
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'hotel_dorado_123'

USUARIO_VALIDO = "admin"
CLAVE_VALIDA = "1234"

JSON_FILE = 'reservas.json'

# Cargar reservas desde JSON
def cargar_reservas():
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

# Guardar nueva reserva en JSON
def guardar_reserva(data):
    reservas = cargar_reservas()
    reservas.append(data)
    with open(JSON_FILE, 'w', encoding='utf-8') as f:
        json.dump(reservas, f, ensure_ascii=False, indent=4)

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
    guardar_reserva(data)
    return 'Reserva registrada con exito'

@app.route('/admin')
def login():
    return render_template('login.html')

@app.route('/validar_login', methods=['POST'])
def validar_login():
    if request.form['usuario'] == USUARIO_VALIDO and request.form['clave'] == CLAVE_VALIDA:
        session['usuario'] = request.form['usuario']
        return redirect('/sistema')
    return render_template('login.html', error="Usuario o clave invalida")

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

@app.route('/buscar_reservas', methods=['POST'])
def buscar_reservas():
    fechas = request.get_json()
    reservas = cargar_reservas()

    fecha_inicio = datetime.strptime(fechas['inicio'], '%Y-%m-%d')
    fecha_fin = datetime.strptime(fechas['fin'], '%Y-%m-%d')

    filtradas = [
        r for r in reservas
        if fecha_inicio <= datetime.strptime(r['fecha'], '%Y-%m-%d') <= fecha_fin
    ]
    return jsonify(filtradas)

@app.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
